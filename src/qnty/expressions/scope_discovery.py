"""
Scope Discovery Service
=======================

Centralized service for automatically discovering variables from the calling scope.
Consolidates all scope inspection logic used across expressions, equations, and variable solving.
"""

import inspect
import logging
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from ..quantities.quantity import TypeSafeVariable
    from .nodes import Expression

# Setup logging for better debugging
_logger = logging.getLogger(__name__)


class ScopeDiscoveryService:
    """
    Centralized service for scope discovery operations.
    
    Provides optimized variable discovery from calling scopes with caching,
    depth limits, and consistent error handling.
    """
    
    # Class-level optimization settings
    _scope_cache = {}
    _variable_type_cache = {}
    _max_scope_cache_size = 100
    _max_search_depth = 8
    
    @classmethod
    def discover_variables(cls, required_vars: set[str], enable_caching: bool = True) -> dict[str, "TypeSafeVariable"]:
        """
        Discover variables from the calling scope.
        
        Args:
            required_vars: Set of variable names to find
            enable_caching: Whether to use caching for performance
            
        Returns:
            Dictionary mapping variable names to TypeSafeVariable instances
        """
        if not required_vars:
            return {}
            
        # Check cache first if enabled
        if enable_caching:
            cache_key = frozenset(required_vars)
            if cache_key in cls._scope_cache:
                _logger.debug(f"Cache hit for variables: {required_vars}")
                return cls._scope_cache[cache_key]
            
            # Clean cache if it gets too large
            if len(cls._scope_cache) >= cls._max_scope_cache_size:
                cls._scope_cache.clear()
                _logger.debug("Cleared scope cache due to size limit")
        
        # Get the calling frame (skip through internal calls)
        frame = inspect.currentframe()
        if frame is None:
            _logger.warning("Unable to access current frame")
            return {}
            
        try:
            # Skip frames until we find one outside the internal system
            frame = cls._find_user_frame(frame)
            if frame is None:
                _logger.debug("No user frame found within search depth")
                return {}
                
            discovered = cls._search_frame_for_variables(frame, required_vars)
            
            # Cache the result if caching is enabled
            if enable_caching and required_vars:
                cache_key = frozenset(required_vars)
                cls._scope_cache[cache_key] = discovered
                _logger.debug(f"Cached discovery result for variables: {required_vars}")
                
            return discovered
            
        finally:
            del frame
    
    @classmethod 
    def can_auto_evaluate(cls, expression: "Expression") -> tuple[bool, dict[str, "TypeSafeVariable"]]:
        """
        Check if expression can be auto-evaluated from scope.
        
        Args:
            expression: Expression to check for auto-evaluation
            
        Returns:
            Tuple of (can_evaluate, discovered_variables)
        """
        try:
            required_vars = expression.get_variables()
            if not required_vars:
                return True, {}  # No variables needed, can evaluate
                
            discovered = cls.discover_variables(required_vars, enable_caching=True)
            
            # Check if all required variables are available and have values
            for var_name in required_vars:
                if var_name not in discovered:
                    _logger.debug(f"Variable '{var_name}' not found in scope")
                    return False, {}
                    
                var = discovered[var_name]
                if not hasattr(var, "quantity") or var.quantity is None:
                    _logger.debug(f"Variable '{var_name}' has no quantity")
                    return False, {}
                    
            _logger.debug(f"Expression can be auto-evaluated with variables: {list(discovered.keys())}")
            return True, discovered
            
        except Exception as e:
            _logger.warning(f"Error during auto-evaluation check: {e}")
            return False, {}
    
    @classmethod
    def find_variables_in_scope(cls, filter_func=None) -> dict[str, "TypeSafeVariable"]:
        """
        Find all TypeSafeVariable instances in the calling scope.
        
        Args:
            filter_func: Optional function to filter variables (var) -> bool
            
        Returns:
            Dictionary mapping variable names/symbols to TypeSafeVariable instances
        """
        frame = inspect.currentframe()
        if frame is None:
            _logger.warning("Unable to access current frame")
            return {}
            
        try:
            frame = cls._find_user_frame(frame)
            if frame is None:
                return {}
                
            discovered = {}
            
            # Search locals first
            for obj in frame.f_locals.values():
                if cls._is_typesafe_variable(obj):
                    if filter_func is None or filter_func(obj):
                        var_name = cls._get_variable_name(obj)
                        if var_name:
                            discovered[var_name] = obj
                            
            # Search globals for remaining variables
            for obj in frame.f_globals.values():
                if cls._is_typesafe_variable(obj):
                    if filter_func is None or filter_func(obj):
                        var_name = cls._get_variable_name(obj)
                        if var_name and var_name not in discovered:
                            discovered[var_name] = obj
                            
            return discovered
            
        finally:
            del frame
    
    @classmethod
    def _find_user_frame(cls, current_frame: Any) -> Optional[Any]:
        """
        Find the first frame outside the internal system (expressions, equations, etc.).
        
        Args:
            current_frame: Starting frame
            
        Returns:
            User frame or None if not found within depth limit
        """
        frame = current_frame
        depth = 0
        
        # Files and function names to skip
        internal_files = ("expression.py", "equation.py", "nodes.py", "scope_discovery.py", "expression_quantity.py")
        internal_functions = ("__str__", "__repr__", "_can_auto_evaluate", "_discover_variables_from_scope")
        
        while frame and depth < cls._max_search_depth:
            filename = frame.f_code.co_filename
            function_name = frame.f_code.co_name
            
            # Check if this frame is from internal code
            is_internal = (
                any(filename.endswith(internal_file) for internal_file in internal_files) or
                function_name in internal_functions
            )
            
            if not is_internal:
                _logger.debug(f"Found user frame at depth {depth}: {filename}:{function_name}")
                return frame
                
            frame = frame.f_back
            depth += 1
            
        _logger.debug(f"No user frame found within {cls._max_search_depth} levels")
        return None
    
    @classmethod
    def _search_frame_for_variables(cls, frame: Any, required_vars: set[str]) -> dict[str, "TypeSafeVariable"]:
        """
        Search a specific frame for required variables.
        
        Args:
            frame: Frame to search
            required_vars: Set of variable names to find
            
        Returns:
            Dictionary of found variables
        """
        discovered = {}
        
        # Search locals first (most common case)
        local_vars = frame.f_locals
        for var_name in required_vars:
            # Direct lookup first (fastest)
            if var_name in local_vars:
                obj = local_vars[var_name]
                if cls._is_typesafe_variable(obj):
                    discovered[var_name] = obj
                    continue
                    
        # Get globals once for reuse
        global_vars = frame.f_globals
        
        # Search globals only for remaining variables
        if len(discovered) < len(required_vars):
            remaining_vars = required_vars - discovered.keys()
            for var_name in remaining_vars:
                if var_name in global_vars:
                    obj = global_vars[var_name]
                    if cls._is_typesafe_variable(obj):
                        discovered[var_name] = obj
                        
        # Additional search for variables by symbol/name if direct lookup failed
        if len(discovered) < len(required_vars):
            remaining_vars = required_vars - discovered.keys()
            
            # Search locals by symbol/name
            for obj in local_vars.values():
                if cls._is_typesafe_variable(obj):
                    obj_name = cls._get_variable_name(obj)
                    if obj_name in remaining_vars:
                        discovered[obj_name] = obj
                        remaining_vars.remove(obj_name)
                        if not remaining_vars:
                            break
                            
            # Search globals by symbol/name if still needed
            if remaining_vars:
                for obj in global_vars.values():
                    if cls._is_typesafe_variable(obj):
                        obj_name = cls._get_variable_name(obj)
                        if obj_name in remaining_vars:
                            discovered[obj_name] = obj
                            remaining_vars.remove(obj_name)
                            if not remaining_vars:
                                break
        
        _logger.debug(f"Found {len(discovered)} of {len(required_vars)} required variables")
        return discovered
    
    @classmethod
    def _is_typesafe_variable(cls, obj) -> bool:
        """
        Check if object is a TypeSafeVariable with caching for performance.
        
        Args:
            obj: Object to check
            
        Returns:
            True if object is a TypeSafeVariable
        """
        obj_type = type(obj)
        if obj_type not in cls._variable_type_cache:
            # Import here to avoid circular imports
            from ..quantities.quantity import TypeSafeVariable
            
            is_variable = (
                isinstance(obj, TypeSafeVariable) and
                hasattr(obj, "symbol") and 
                hasattr(obj, "name") and 
                hasattr(obj, "quantity")
            )
            cls._variable_type_cache[obj_type] = is_variable
            
        return cls._variable_type_cache[obj_type]
    
    @classmethod
    def _get_variable_name(cls, var) -> Optional[str]:
        """
        Get the name/symbol to use for a variable.
        
        Args:
            var: TypeSafeVariable instance
            
        Returns:
            Variable name/symbol or None if not available
        """
        try:
            # Prefer symbol over name for equation solving
            return var.symbol if var.symbol else var.name
        except (AttributeError, TypeError):
            return None
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear all caches for testing or memory management."""
        cls._scope_cache.clear()
        cls._variable_type_cache.clear()
        _logger.debug("Cleared all scope discovery caches")
        
    @classmethod
    def set_max_depth(cls, depth: int) -> None:
        """Set maximum search depth for scope discovery."""
        if depth > 0:
            cls._max_search_depth = depth
            _logger.debug(f"Set max search depth to {depth}")
        else:
            raise ValueError("Depth must be positive")
            
    @classmethod
    def enable_debug_logging(cls) -> None:
        """Enable debug logging for scope discovery operations."""
        logging.getLogger(__name__).setLevel(logging.DEBUG)
        
    @classmethod
    def disable_debug_logging(cls) -> None:
        """Disable debug logging for scope discovery operations."""
        logging.getLogger(__name__).setLevel(logging.WARNING)


# Convenience function for backward compatibility
def discover_variables_from_scope(required_vars: set[str]) -> dict[str, "TypeSafeVariable"]:
    """
    Convenience function to discover variables from scope.
    
    Args:
        required_vars: Set of variable names to find
        
    Returns:
        Dictionary mapping variable names to TypeSafeVariable instances
    """
    return ScopeDiscoveryService.discover_variables(required_vars)