"""
Core Dimensions Module
======================

Core dimensional analysis components providing compile-time type safety.

This module provides the fundamental building blocks for qnty's dimensional analysis system:
- BaseDimension: Prime-number-encoded base dimensions
- DimensionSignature: Ultra-fast dimensional compatibility checking
"""

from .base import BaseDimension
from .signature import DimensionSignature

__all__ = ["BaseDimension", "DimensionSignature"]