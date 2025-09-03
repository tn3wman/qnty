"""
Solver package for the Optinova engineering problem library.

This package contains different solver implementations for solving systems
of engineering equations.
"""

from .base import BaseSolver, SolveResult, SolveError
from .iterative import IterativeSolver
from .simultaneous import SimultaneousEquationSolver
from .manager import SolverManager

__all__ = [
    'BaseSolver',
    'SolveResult', 
    'SolveError',
    'IterativeSolver',
    'SimultaneousEquationSolver',
    'SolverManager'
]