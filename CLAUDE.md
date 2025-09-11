# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Testing
- `pytest` - Run all tests
- `pytest tests/test_dimension.py -v` - Run specific test file with verbose output
- `pytest tests/test_benchmark.py -v -s` - Run performance benchmarks

### Linting and Code Quality
- `ruff check src/ tests/` - Check for linting issues
- `ruff format src/ tests/` - Format code according to project standards
- Line length is set to 200 characters

### Package Management
- `pip install -e .` - Install package in development mode
- `pip install -e .[dev]` - Install with development dependencies
- `pip install -e .[benchmark]` - Install with benchmark dependencies (includes Pint for comparisons)

## Architecture Overview

Qnty is a high-performance unit system library built around several core architectural concepts:

### Core Components

1. **Dimension System** (`src/qnty/dimensions/`)
   - `signature.py`: Prime number-encoded dimension signatures for ultra-fast dimensional analysis
   - `base.py`: Base dimension definitions using prime number encoding
   - `field_dims.py`: Pre-defined dimension signatures for common engineering quantities

2. **Quantity System** (`src/qnty/quantities/`)
   - `base_qnty.py`: Core FastQuantity class with `__slots__` optimization
   - `field_qnty.py`: Quantity field descriptors for Problem classes
   - `field_vars.py`: Auto-generated type-safe quantity classes (100+ engineering quantities)

3. **Units System** (`src/qnty/units/`)
   - `registry.py`: Unit conversion registry with pre-computed conversion factors
   - `field_units.py`: Unit class definitions for each quantity type
   - `prefixes.py`: SI and engineering unit prefixes

4. **Problem Solving** (`src/qnty/problems/`)
   - `problem.py`: Main Problem class for engineering calculations
   - `solving.py`: Equation reconstruction and solving pipeline
   - `composition.py`: Proxy system for composed problems

5. **Mathematical Expression System** (`src/qnty/expressions/`)
   - `nodes.py`: Expression tree nodes (BinaryOperation, VariableReference, etc.)
   - `functions.py`: Mathematical functions (sin, cos, sqrt, etc.)
   - `types.py`: Type definitions for expression system

6. **Equation Solving** (`src/qnty/solving/`)
   - `manager.py`: Solver management and orchestration
   - `solvers/`: Different solving strategies (iterative, simultaneous)
   - `order.py`: Dependency ordering for equation solving

### Key Design Patterns

1. **Prime Number Encoding**: Dimensions use prime number encoding for O(1) compatibility checking
2. **Type Safety**: Extensive use of type hints and dimensional analysis at compile time
3. **Performance Optimization**: `__slots__`, caching, pre-computed conversions
4. **Fluent API**: Method chaining for readable engineering calculations
5. **Problem-Oriented Design**: Engineering problems as classes with declarative syntax

### Important Implementation Details

- All quantities use `__slots__` for memory efficiency
- Dimension compatibility is checked using prime number multiplication/division
- Unit conversions use pre-computed factors stored in registries
- Mathematical expressions build AST trees for symbolic manipulation
- The Problem class uses metaclass magic for automatic variable discovery
- Equation solving supports both iterative and simultaneous methods

### Auto-Generated Code
- `field_vars.py` contains 100+ auto-generated quantity classes
- Each quantity class is dimensionally typed and includes appropriate unit classes
- Unit conversion factors are pre-computed and cached for performance

### Testing Strategy
- Comprehensive test suite with 187+ tests
- Performance benchmarks comparing against Pint library
- Dimensional analysis correctness tests
- Mathematical function accuracy tests