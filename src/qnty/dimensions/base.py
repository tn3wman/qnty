"""
Base Dimensions
===============

Core base dimensions using prime number encoding for efficient dimensional analysis.

This file contains the fundamental dimensional primitives for the qnty system.
"""

from enum import IntEnum


# TODO: This should be frozen and immutable
class BaseDimension(IntEnum):
    """Base dimensions as prime numbers for efficient bit operations."""

    DIMENSIONLESS = 1  # Must be 1 to act as multiplicative identity
    LENGTH = 2
    MASS = 3
    TIME = 5
    CURRENT = 7
    TEMPERATURE = 11
    AMOUNT = 13
    LUMINOSITY = 17


# TODO: This should be frozen and immutable
# Dimension symbols for display
DIMENSION_SYMBOLS = {
    "length": "L",
    "mass": "M",
    "time": "T",
    "current": "A",
    "temp": "Θ",
    "amount": "N",
    "luminosity": "J",
}

# TODO: This should be frozen and immutable
# Base dimensions configuration for generators
BASE_DIMENSIONS = {
    "LENGTH": {"prime": BaseDimension.LENGTH, "params": {"length": 1}},
    "MASS": {"prime": BaseDimension.MASS, "params": {"mass": 1}},
    "TIME": {"prime": BaseDimension.TIME, "params": {"time": 1}},
    "CURRENT": {"prime": BaseDimension.CURRENT, "params": {"current": 1}},
    "TEMPERATURE": {"prime": BaseDimension.TEMPERATURE, "params": {"temp": 1}},
    "AMOUNT": {"prime": BaseDimension.AMOUNT, "params": {"amount": 1}},
    "LUMINOSITY": {"prime": BaseDimension.LUMINOSITY, "params": {"luminosity": 1}},
    "DIMENSIONLESS": {"prime": BaseDimension.DIMENSIONLESS, "params": {}},
}

# TODO: This should be frozen and immutable
# Prime mapping for signature calculations
PRIME_MAP = {
    "length": BaseDimension.LENGTH,
    "mass": BaseDimension.MASS,
    "time": BaseDimension.TIME,
    "current": BaseDimension.CURRENT,
    "temp": BaseDimension.TEMPERATURE,
    "amount": BaseDimension.AMOUNT,
    "luminosity": BaseDimension.LUMINOSITY,
}
