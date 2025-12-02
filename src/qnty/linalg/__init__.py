"""
Linear algebra module for qnty.
"""

from .vector2 import Vector, VectorUnknown
from .vectors2 import create_vector_resultant, create_vectors_polar

__all__ = [
    "Vector",
    "VectorUnknown",
    "create_vector_resultant",
    "create_vectors_polar",
]
