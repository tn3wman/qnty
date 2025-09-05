"""
Base Dimensions
===============

Core base dimensions using prime number encoding for efficient dimensional analysis.

This file contains the fundamental dimensional primitives for the qnty system.
"""

from enum import IntEnum


class BaseDimension(IntEnum):
    """Base dimensions as prime numbers for efficient bit operations."""
    LENGTH = 2
    MASS = 3
    TIME = 5
    CURRENT = 7
    TEMPERATURE = 11
    AMOUNT = 13
    LUMINOSITY = 17
    DIMENSIONLESS = 1  # Must be 1 to act as multiplicative identity