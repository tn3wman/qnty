# Qnty

**High-performance unit system library for Python with dimensional safety and fast unit conversions for engineering calculations.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Development Status](https://img.shields.io/badge/status-beta-orange.svg)](https://pypi.org/project/qnty/)

## ⚠️ Important Disclaimer

**🚧 Work in Progress**: Qnty is currently in active development and has not been thoroughly vetted for production engineering calculations. While we strive for accuracy, this library should not be used for critical engineering applications without independent verification.

**📐 Accuracy Notice**: The authors are not responsible or liable for incorrect results, calculation errors, or any consequences arising from the use of this library. Always validate calculations independently using established engineering tools and practices.

**🚀 Learn from History**: Remember, even NASA's Mars Climate Orbiter had a $327 million oops moment due to unit conversion errors between metric and imperial systems. Don't let your project become the next cautionary tale - double-check everything!

*Use Qnty to help prevent unit errors, but always verify critical calculations through multiple methods.*

---

Qnty is designed around **type safety** and **performance optimization** using compile-time dimensional analysis. It provides ultra-fast unit conversions and dimensional checking for engineering applications where performance matters.

## ✨ Key Features

- **🚀 Ultra-Fast Performance**: Prime number encoding and pre-computed conversion tables
- **🛡️ Type Safety**: Compile-time dimensional analysis prevents unit errors
- **⚡ Zero-Cost Abstractions**: Optimized operations with `__slots__` and caching
- **🔗 Fluent API**: Intuitive method chaining for readable code
- **🧮 Engineering-Focused**: Built for real-world engineering calculations
- **🧬 Mathematical System**: Built-in equation solving and expression trees
- **📊 Comprehensive Testing**: 457 tests with performance benchmarks
- **🏗️ Clean Architecture**: Circular import-free design with strict dependency hierarchy

## 🚀 Quick Start

### Installation

```bash
pip install qnty
# or with Poetry
poetry add qnty
```

### Basic Usage

```python
from qnty import Length, Pressure, Dimensionless
from qnty.variable import FastQuantity
from qnty.units import LengthUnits, PressureUnits

# Type-safe variables with fluent API
beam_length = Length("beam_length")
beam_length.set(100.0).millimeters
print(beam_length)  # beam_length: 100.0 mm

# Convert units effortlessly
length_in_meters = beam_length.quantity.to(LengthUnits.meter)
print(length_in_meters)  # 0.1 m

# High-performance calculations
pressure = FastQuantity(150.0, PressureUnits.psi)
area = FastQuantity(0.5, LengthUnits.meter) * FastQuantity(2.0, LengthUnits.meter)
force = pressure * area  # Automatic dimensional analysis
```

### Engineering Example

```python
from qnty import Length, Pressure

# ASME pressure vessel calculation with mixed units
pressure = Pressure("internal_pressure")
diameter = Length("outer_diameter") 
stress = Pressure("allowable_stress")

# Set values with different units - no manual conversion needed!
pressure.set(2900.75).psi        # Imperial
diameter.set(168.275).millimeters  # Metric
stress.set(137.895).MPa          # SI

# Qnty handles all unit conversions automatically
thickness = (pressure.quantity * diameter.quantity) / (2 * stress.quantity)
print(f"Required thickness: {thickness}")  # Automatically in correct units
```

### Mathematical Equations & Solving

```python
from qnty import Length, Pressure, Dimensionless

# Define engineering variables
T = Length("Wall Thickness", is_known=False)  # Unknown to solve for
T_bar = Length(0.147, "inches", "Nominal Wall Thickness")
U_m = Dimensionless(0.125, "Mill Undertolerance")

# Create equation using fluent API: T = T_bar * (1 - U_m)
equation = T.equals(T_bar * (1 - U_m))

# Solve automatically
known_vars = {"T_bar": T_bar, "U_m": U_m}
result = equation.solve_for("T", known_vars)
print(f"Solved thickness: {result.quantity}")  # 0.128625 inches

# Verify equation is satisfied
assert equation.check_residual(known_vars) is True
```

## 🏗️ Architecture

### Clean Dependency Design

Qnty features a carefully designed architecture that eliminates circular imports through a strict dependency hierarchy:

```python
variable → variables → expression → equation
```

This ensures clean type checking, maintainable code, and optimal performance throughout the system.

### Core Components

### 🔢 Dimensional System

- Prime number encoding for ultra-fast dimensional compatibility checks
- Zero-cost dimensional analysis at compile time
- Immutable dimension signatures for thread safety

### ⚙️ High-Performance Quantities

- `FastQuantity`: Optimized for engineering calculations with `__slots__`
- Cached SI factors and dimension signatures
- Fast-path optimizations for same-unit operations

### 🎯 Type-Safe Variables

- `Length`, `Pressure`, `Dimensionless`: Domain-specific variables with compile-time safety
- Fluent API with specialized setters
- Prevents dimensional errors at the type level

### 🔄 Smart Unit System

- Pre-computed conversion tables
- Automatic unit resolution for calculations
- Support for mixed-unit operations

### 🧬 Mathematical System

- Built-in equation solving with symbolic manipulation
- Expression trees for complex mathematical operations
- Automatic residual checking and validation
- Engineering equation support (ASME, pressure vessels, etc.)

## 📊 Performance

Qnty significantly outperforms other unit libraries with **18.9x average speedup** over Pint:

### Real Benchmark Results (μs per operation)

| Operation | Qnty | Pint | **Speedup** |
|-----------|------|------|-------------|
| Unit Conversion (m → mm) | 0.50 | 9.72 | **19.5x** |
| Mixed Unit Addition (mm + in) | 0.76 | 17.52 | **23.1x** |
| Multiplication (m × m) | 0.82 | 10.64 | **12.9x** |
| Division (psi ÷ mm) | 0.87 | 11.23 | **12.9x** |
| Complex ASME Equation | 4.07 | 106.17 | **26.1x** 🚀 |
| Type-Safe Variables | 0.98 | 9.65 | **9.8x** |
| Chained Operations | 1.83 | 42.22 | **23.1x** |
| Loop (10 additions) | 5.32 | 79.48 | **14.9x** |
| **AVERAGE** | **1.89** | **35.83** | **18.9x** 🏆 |

*Benchmarks performed on typical engineering calculations. Run `pytest tests/test_benchmark.py -v -s` to verify on your system.*

## 🧪 Advanced Features

### Fluent API Design

```python
# Method chaining for readable code
pipe_system = {
    'inlet': Pressure("inlet").set(150.0).psi,
    'outlet': Pressure("outlet").set(120.0).psi,
    'diameter': Length("diameter").set(6.0).inches,
    'length': Length("length").set(100.0).feet
}

pressure_drop = pipe_system['inlet'].quantity - pipe_system['outlet'].quantity
```

### Dimensional Safety

```python
# This will raise a TypeError at assignment time
length = Length("distance")
try:
    length.set(100.0).psi  # Wrong! Pressure unit for length variable
except TypeError as e:
    print(f"Caught error: {e}")  # Unit psi incompatible with expected dimension

# Type checker catches this at development time
```

### Mixed Unit Calculations

```python
# Automatically handles unit conversions in calculations
width = Length("width").set(100.0).millimeters
height = Length("height").set(4.0).inches  # Different unit!

# Qnty automatically converts to compatible units
area = width.quantity * height.quantity
perimeter = 2 * (width.quantity + height.quantity)
```

### Equation Solving System

```python
from qnty import Length, Pressure, Dimensionless

# Multi-variable engineering equations
P = Pressure(90, "psi", "P")  # Known
D = Length(0.84, "inches", "D")  # Known
t = Length("t", is_known=False)  # Unknown - solve for this
S = Pressure(20000, "psi", "S")  # Known

# ASME pressure vessel equation: P = (S * t) / ((D/2) + 0.6*t)
# Rearranged to solve for t
equation = t.equals((P * D) / (2 * S - 1.2 * P))

# Solve automatically
known_variables = {"P": P, "D": D, "S": S}
thickness_result = equation.solve_for("t", known_variables)
print(f"Required thickness: {thickness_result.quantity}")

# Verify solution
assert equation.check_residual(known_variables) is True
```

### Import Strategy

Qnty provides a clean, minimal public API:

```python
# Preferred import style - clean public API
from qnty import Length, Pressure, Dimensionless

# Internal imports when needed for advanced usage
from qnty.variable import FastQuantity, TypeSafeVariable
from qnty.expression import Expression
from qnty.equation import Equation, EquationSystem
```

## 🔧 Development

### Setup Development Environment

```bash
git clone https://github.com/your-username/qnty.git
cd qnty
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test file
pytest tests/test_dimension.py -v

# Run benchmarks
python tests/test_benchmark.py
```

### Code Quality

```bash
# Linting with ruff (200 character line length)
ruff check src/ tests/
ruff format src/ tests/

# Type checking
mypy src/qnty/
```

## 📚 Documentation

### Core Classes

- **`FastQuantity`**: High-performance quantity with value and unit
- **`TypeSafeVariable`**: Base class for dimension-specific variables
- **`Length`**, **`Pressure`**, **`Dimensionless`**: Specialized variables with fluent setters
- **`Equation`**: Mathematical equations with solving capabilities
- **`Expression`**: Abstract base for mathematical expression trees
- **`DimensionSignature`**: Immutable dimension encoding system
- **`UnitConstant`**: Type-safe unit definitions

### Unit Categories

- **Length**: meter, millimeter, inch, foot, etc.
- **Pressure**: pascal, psi, bar, kilopascal, megapascal, etc.
- **Dimensionless**: ratios, efficiency factors, etc.
- *More dimensions coming soon*

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the [Pint](https://pint.readthedocs.io/) library
- Built for the engineering community
- Designed with performance-critical applications in mind

---

**Ready to supercharge your engineering calculations?** Install Qnty today and experience the power of type-safe, high-performance unit handling! 🚀
