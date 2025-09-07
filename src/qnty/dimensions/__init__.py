"""
Core Dimensions Module
======================

Core dimensional analysis components providing compile-time type safety.

This module provides the fundamental building blocks for qnty's dimensional analysis system:
- BaseDimension: Prime-number-encoded base dimensions
- DimensionSignature: Ultra-fast dimensional compatibility checking
"""

from .field_dims import *
from .base import BASE_DIMENSIONS, DIMENSION_SYMBOLS, PRIME_MAP, BaseDimension
from .signature import DimensionSignature

__all__ = ["BaseDimension", "DimensionSignature", "BASE_DIMENSIONS", "DIMENSION_SYMBOLS", "PRIME_MAP"]
