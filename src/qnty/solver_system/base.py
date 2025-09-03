from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Set, Any, Optional
from qnty.variable_system import TypeSafeVariable as Variable
from qnty.equation_system.equation import Equation
from qnty.problem_system.dependency_graph import DependencyGraph


class SolveError(Exception):
    """Exception raised when solving fails."""
    pass


@dataclass
class SolveResult:
    """Result of a solve operation."""
    variables: Dict[str, Variable]
    steps: List[Dict[str, Any]] = field(default_factory=list)
    success: bool = True
    message: str = ""
    method: str = ""
    iterations: int = 0


class BaseSolver(ABC):
    """Base class for all equation solvers."""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.steps = []
    
    @abstractmethod
    def can_handle(self, equations: List[Equation], unknowns: Set[str], 
                   dependency_graph: Optional[DependencyGraph] = None, 
                   analysis: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if this solver can handle the given problem.
        
        Args:
            equations: List of equations to solve
            unknowns: Set of unknown variable symbols
            dependency_graph: Optional dependency graph for analysis
            analysis: Optional system analysis results
            
        Returns:
            True if this solver can handle the problem
        """
        pass
    
    @abstractmethod
    def solve(self, equations: List[Equation], variables: Dict[str, Variable],
              dependency_graph: Optional[DependencyGraph] = None,
              max_iterations: int = 100, tolerance: float = 1e-10) -> SolveResult:
        """
        Solve the system of equations.
        
        Args:
            equations: List of equations to solve
            variables: Dictionary of all variables (known and unknown)
            dependency_graph: Optional dependency graph
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance
            
        Returns:
            SolveResult containing the solution
        """
        pass
    
    def _log_step(self, iteration: int, variable: str, equation: str, 
                  result: str, method: Optional[str] = None):
        """Log a solving step."""
        step = {
            'iteration': iteration,
            'variable': variable,
            'equation': equation,
            'result': result,
            'method': method or self.__class__.__name__
        }
        self.steps.append(step)
        if self.logger:
            self.logger.debug(f"Solved {variable} = {result}")
    
    def _get_known_variables(self, variables: Dict[str, Variable]) -> Set[str]:
        """Get symbols of known variables."""
        return {s for s, v in variables.items() if v.is_known}
    
    def _get_unknown_variables(self, variables: Dict[str, Variable]) -> Set[str]:
        """Get symbols of unknown variables."""
        return {s for s, v in variables.items() if not v.is_known}