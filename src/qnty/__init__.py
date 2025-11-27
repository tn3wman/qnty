"""
Qnty - High-Performance Unit System for Engineering
====================================================

A fast, type-safe unit system library for Python with dimensional safety and optimized unit conversions for engineering calculations.
"""

# from . import (quantity, expressions)

from .algebra import (
    abs_expr,
    cond_expr,
    cos,
    exp,
    ln,
    log10,
    max_expr,
    min_expr,
    range_expr,
    sin,
    sqrt,
    sum_expr,
    summation,
    tan,
    When,
)
from .core.quantity_catalog import *
from .problems import Problem

# Integration module for frontend frameworks (Reflex, FastAPI, etc.)
from . import integration
