"""
Core Dimensions Module
======================

"""

from .core import Dimension
from .namespace import *


def __getattr__(name: str):
    if name == "dim":
        # Import and return the actual dim object from core
        from .core import dim

        return dim
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = (
    "Dimension",
    "dim",
)
