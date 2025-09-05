# Qnty

**High-performance unit system library for Python with dimensional safety and fast unit conversions for engineering calculations.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Development Status](https://img.shields.io/badge/status-beta-orange.svg)](https://pypi.org/project/qnty/)

## ⚠️ Important Disclaimer

**🚧 Work in Progress**: Qnty is currently in active development and has not been thoroughly vetted for production engineering calculations. While we strive for accuracy, this library should not be used for critical engineering applications without independent verification.

**📐 Accuracy Notice**: The authors are not responsible or liable for incorrect results, calculation errors, or any consequences arising from the use of this library. Always validate calculations independently using established engineering tools and practices.

*Use Qnty to help prevent unit errors, but always verify critical calculations through multiple methods.*

---

## ✨ Key Features

- **🚀 Ultra-Fast Performance**: Prime number encoding and pre-computed conversion tables
- **🛡️ Type Safety**: Compile-time dimensional analysis prevents unit errors
- **⚡ Zero-Cost Abstractions**: Optimized operations with `__slots__` and caching
- **🔗 Fluent API**: Intuitive method chaining for readable code
- **🧮 Engineering-Focused**: Built for real-world engineering calculations
- **🧬 Mathematical System**: Built-in equation solving and expression trees
- **📊 Comprehensive Testing**: 187 tests with performance benchmarks

## 🚀 Quick Start

### Installation

```bash
pip install qnty
```

### Basic Usage

```python
from qnty import Length, Pressure, Area

# Create quantities with dimensional safety
width = Length(3, "meter", "Width")
height = Length(2, "meter", "Height")

# Solve mathematical expressions
area = Area("area", is_known=False)
area.solve_from(width * height)
print(f"Area: {area}")  # Area: 6.0 m²
```

### Engineering Example

```python
from qnty import Problem, Length, Pressure

class PipeThickness(Problem):
    """Calculate pipe wall thickness"""
    
    # Known parameters
    pressure = Pressure(150, "pound_force_per_square_inch", "Internal Pressure")
    diameter = Length(6, "inch", "Pipe Diameter")
    allowable_stress = Pressure(20000, "pound_force_per_square_inch", "Allowable Stress")
    
    # Unknown to solve for
    thickness = Length("thickness", is_known=False)
    
    # Engineering equation: t = (P × D) / (2 × S)
    equation = thickness.equals((pressure * diameter) / (2 * allowable_stress))

# Solve the problem
problem = PipeThickness()
problem.solve()
print(f"Required thickness: {problem.thickness}")
```

### Mathematical Operations

```python
from qnty import Length, sqrt, Area

# Dimensional analysis with mathematical functions
area = Area(25, "square_meter", "Square Area")
side = Length("side", is_known=False)
side.solve_from(sqrt(area))  # Returns Length, not Area!
print(f"Side length: {side}")  # Side length: 5.0 m
```

## 📚 Documentation

- **[📖 Tutorial](docs/TUTORIAL.md)** - Step-by-step learning guide
- **[📋 API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[🏗️ Examples](examples/)** - Real-world engineering examples
- **[📁 Full Documentation](docs/)** - Complete documentation index

## 🚀 Performance

Qnty significantly outperforms other unit libraries with **18.9x average speedup** over Pint:

| Operation | Qnty | Pint | **Speedup** |
|-----------|------|------|-------------|
| Mixed Unit Addition | 0.76 μs | 17.52 μs | **23.1x** |
| Complex ASME Equation | 4.07 μs | 106.17 μs | **26.1x** 🚀 |
| Type-Safe Variables | 0.98 μs | 9.65 μs | **9.8x** |
| **AVERAGE** | **1.89 μs** | **35.83 μs** | **18.9x** 🏆 |

*Run `pytest tests/test_benchmark.py -v -s` to verify on your system.*

## 🧮 100+ Engineering Quantities

Qnty provides comprehensive coverage of engineering domains:

```python
from qnty import (
    # Mechanical
    Length, Area, Volume, Mass, Force, Pressure, Temperature,
    # Electrical  
    ElectricPotential, ElectricCurrentIntensity, ElectricResistance,
    # Thermal
    ThermalConductivity, HeatTransferCoefficient,
    # Fluid Dynamics
    ViscosityDynamic, MassFlowRate, VolumetricFlowRate,
    # And 80+ more...
)
```

## 🔧 Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run specific test
pytest tests/test_dimension.py -v

# Run benchmarks
python tests/test_benchmark.py

# Lint code
ruff check src/ tests/
ruff format src/ tests/
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see [CLAUDE.md](CLAUDE.md) for development guidelines and:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass: `pytest`
5. Submit a pull request

---

**Ready to supercharge your engineering calculations?** 🚀

- Start with the **[Tutorial](docs/TUTORIAL.md)**
- Browse the **[API Reference](docs/API_REFERENCE.md)**
- Try the **[Examples](examples/)**
