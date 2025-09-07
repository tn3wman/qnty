"""
Base Dimensions
===============

Core base dimensions using prime number encoding for efficient dimensional analysis.

This file contains the fundamental dimensional primitives for the qnty system.
"""

from enum import IntEnum
from types import MappingProxyType
from typing import Any


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


# Immutable dimension symbols for display
DIMENSION_SYMBOLS: dict[str, str] = MappingProxyType(
    {
        "length": "L",
        "mass": "M",
        "time": "T",
        "current": "A",
        "temp": "Θ",
        "amount": "N",
        "luminosity": "J",
    }
)

# Immutable base dimensions configuration for generators
BASE_DIMENSIONS: dict[str, dict[str, Any]] = MappingProxyType(
    {
        "LENGTH": {"prime": BaseDimension.LENGTH, "params": {"length": 1}},
        "MASS": {"prime": BaseDimension.MASS, "params": {"mass": 1}},
        "TIME": {"prime": BaseDimension.TIME, "params": {"time": 1}},
        "CURRENT": {"prime": BaseDimension.CURRENT, "params": {"current": 1}},
        "TEMPERATURE": {"prime": BaseDimension.TEMPERATURE, "params": {"temp": 1}},
        "AMOUNT": {"prime": BaseDimension.AMOUNT, "params": {"amount": 1}},
        "LUMINOSITY": {"prime": BaseDimension.LUMINOSITY, "params": {"luminosity": 1}},
        "DIMENSIONLESS": {"prime": BaseDimension.DIMENSIONLESS, "params": {}},
    }
)

# Immutable prime mapping for signature calculations
PRIME_MAP: dict[str, BaseDimension] = MappingProxyType(
    {
        "length": BaseDimension.LENGTH,
        "mass": BaseDimension.MASS,
        "time": BaseDimension.TIME,
        "current": BaseDimension.CURRENT,
        "temp": BaseDimension.TEMPERATURE,
        "amount": BaseDimension.AMOUNT,
        "luminosity": BaseDimension.LUMINOSITY,
    }
)
