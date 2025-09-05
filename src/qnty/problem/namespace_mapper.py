"""
Namespace Mapper for Equation Reconstruction System.

Handles mapping of variable names to their proper namespaces during
equation reconstruction and composite expression resolution.
"""

import re
from typing import Set
from logging import Logger

from qnty.quantities.unified_variable import UnifiedVariable as Variable

# Type aliases
VariableDict = dict[str, Variable]
NamespaceMapping = dict[str, str]

# Compiled regex patterns for performance
VARIABLE_PATTERN = re.compile(r"\b[A-Za-z][A-Za-z0-9_]*\b")

# Constants for better maintainability
EXCLUDED_FUNCTION_NAMES: Set[str] = {"sin", "cos", "max", "min", "exp", "log", "sqrt", "tan"}


class NamespaceMapper:
    """
    Focused class for handling variable namespace mapping operations.
    
    Provides efficient mapping of base variable names to their namespaced
    counterparts with caching for performance optimization.
    """
    
    def __init__(self, variables: VariableDict, logger: Logger):
        """
        Initialize the namespace mapper.
        
        Args:
            variables: Dictionary of available variables
            logger: Logger for debugging
        """
        self.variables = variables
        self.logger = logger
        
        # Performance optimization caches
        self._namespace_cache: dict[str, Set[str]] = {}
        self._variable_mapping_cache: dict[frozenset, NamespaceMapping] = {}
        self._all_variable_names: Set[str] | None = None
    
    def extract_base_variables_from_composites(self, missing_vars: list[str]) -> Set[str]:
        """
        Extract base variable symbols from composite expressions.

        Args:
            missing_vars: List of missing variable names from composite expressions

        Returns:
            Set of base variable symbols found in the expressions

        Example:
            '(D - (T - c) * 2.0)' -> {'D', 'T', 'c'}
        """
        if not missing_vars:
            return set()

        base_vars: Set[str] = set()

        for missing_var in missing_vars:
            # Use compiled regex for better performance
            matches = VARIABLE_PATTERN.findall(missing_var)

            for match in matches:
                # Filter out obvious non-variable terms using constant set
                if match not in EXCLUDED_FUNCTION_NAMES:
                    base_vars.add(match)

        return base_vars
    
    def find_namespace_mappings(self, base_vars: Set[str]) -> NamespaceMapping:
        """
        Find which namespace each base variable should map to.

        Args:
            base_vars: Set of base variable symbols to map

        Returns:
            Mapping from base variable names to namespaced variable names

        Example:
            {'D': 'branch_D', 'T': 'header_T', 'c': 'branch_c'}
        """
        if not base_vars:
            return {}

        # Use cache key for performance optimization
        cache_key = frozenset(base_vars)
        if cache_key in self._variable_mapping_cache:
            return self._variable_mapping_cache[cache_key]

        mappings: NamespaceMapping = {}

        # For each base variable, find the best namespace match
        for base_var in base_vars:
            candidates = self._find_namespace_candidates(base_var)

            # Use heuristics to pick the best candidate
            if len(candidates) == 1:
                mappings[base_var] = candidates[0]
            elif len(candidates) > 1:
                # If multiple candidates, use context clues or pick first namespace alphabetically
                best_candidate = sorted(candidates)[0]
                mappings[base_var] = best_candidate
                self.logger.debug(f"Multiple candidates for '{base_var}': {candidates}, chose '{best_candidate}'")
            else:
                self.logger.debug(f"No candidates found for base variable: {base_var}")

        # Cache the result for performance
        self._variable_mapping_cache[cache_key] = mappings
        return mappings
    
    def _find_namespace_candidates(self, base_var: str) -> list[str]:
        """
        Find all possible namespace candidates for a base variable.

        Args:
            base_var: Base variable name to find candidates for

        Returns:
            List of candidate namespaced variable names
        """
        candidates = []

        # Cache variable names for performance
        if self._all_variable_names is None:
            self._all_variable_names = set(self.variables.keys())

        # Look for exact matches in namespaced variables
        for var_name in self._all_variable_names:
            if "_" in var_name:
                _, var_part = var_name.split("_", 1)  # namespace not needed here
                if var_part == base_var:
                    candidates.append(var_name)

        return candidates
    
    def clear_caches(self) -> None:
        """
        Clear all internal caches. Should be called when variables change.

        This method provides a way to reset cached data when the problem
        state changes, ensuring cache consistency.
        """
        self._namespace_cache.clear()
        self._variable_mapping_cache.clear()
        self._all_variable_names = None