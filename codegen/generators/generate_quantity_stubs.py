# isort: skip_file
"""
Generate typed .pyi stubs for Quantity classes created with @quantity decorator.
- Scans qnty.core.quantity_catalog for classes with UNIT_NS
- Reads their UNIT_NS to enumerate unit attribute names
- Emits properties for Setter, ToUnit, and AsUnit classes for IDE autocompletion

This complements the runtime dynamic binding in quantity_meta.py.
"""
from __future__ import annotations

import inspect
from pathlib import Path

import qnty.core.quantity_catalog as qcat
from qnty.core.unit import Unit, UnitNamespace


OUT_PATH = Path(qcat.__file__).with_suffix(".pyi")


def unit_names_from_namespace(ns: type) -> list[str]:
    names: list[str] = []
    for name, val in vars(ns).items():
        if isinstance(val, Unit):
            names.append(name)
    return sorted(names)


def get_unit_names_and_aliases(unit_ns: type[UnitNamespace]) -> list[str]:
    """Get all unit names and their valid-identifier aliases from a unit namespace."""
    names = set()

    # Get canonical names from the namespace
    for attr_name in dir(unit_ns):
        if not attr_name.startswith("_"):
            attr_val = getattr(unit_ns, attr_name)
            if isinstance(attr_val, Unit):
                names.add(attr_name)

                # Add aliases that are valid identifiers
                for alias in attr_val.aliases:
                    if alias.isidentifier():
                        names.add(alias)

    return sorted(names)


def find_quantities() -> list[type]:
    """Find all quantity classes in the catalog that have UNIT_NS."""
    qty_types: list[type] = []
    for _name, obj in vars(qcat).items():
        if inspect.isclass(obj) and hasattr(obj, "UNIT_NS"):
            qty_types.append(obj)
    return qty_types


def write_stub():
    lines: list[str] = []
    lines.append("# isort: skip_file\n")
    lines.append("from __future__ import annotations\n\n")
    lines.append("from typing import overload\n\n")
    lines.append("from .unit import Unit\n")
    lines.append("from .quantity import Quantity, QuantitySetter, UnitApplier, UnitChanger\n")

    # For each quantity, emit typed properties from UNIT_NS
    for qty in find_quantities():
        unit_ns = qty.UNIT_NS  # type: ignore[attr-defined]
        unit_names = get_unit_names_and_aliases(unit_ns)
        setter_name = f"{qty.__name__}Setter"

        lines.append("\n")

        # Setter class with unit properties
        lines.append(f"class {setter_name}(QuantitySetter[{qty.__name__}]):\n")
        for name in unit_names:
            lines.append("    @property\n")
            lines.append(f"    def {name}(self) -> {qty.__name__}: ...\n")
        lines.append("\n")

        # Main Quantity class
        lines.append(f"class {qty.__name__}(Quantity[{qty.__name__}]):\n")
        lines.append(f"    def __init__(self, name: str, value: float | None = None, preferred: Unit[{qty.__name__}] | None = None) -> None: ...\n")

        # ToUnit nested class
        lines.append(f"    class ToUnit(UnitApplier[{qty.__name__}]):\n")
        for name in unit_names:
            lines.append("        @property\n")
            lines.append(f"        def {name}(self) -> {qty.__name__}: ...\n")
        lines.append(f"\n        def __call__(self, unit: Unit[{qty.__name__}] | str) -> {qty.__name__}: ...\n\n")

        # AsUnit nested class
        lines.append(f"    class AsUnit(UnitChanger[{qty.__name__}]):\n")
        for name in unit_names:
            lines.append("        @property\n")
            lines.append(f"        def {name}(self) -> {qty.__name__}: ...\n")
        lines.append(f"\n        def __call__(self, unit: Unit[{qty.__name__}] | str) -> {qty.__name__}: ...\n\n")

        # Properties
        lines.append("    @property\n")
        lines.append(f"    def to_unit(self) -> {qty.__name__}.ToUnit: ...\n\n")
        lines.append("    @property\n")
        lines.append(f"    def as_unit(self) -> {qty.__name__}.AsUnit: ...\n\n")

        # Set method overloads
        lines.append("    @overload\n")
        lines.append(f"    def set(self, value: float) -> {setter_name}: ...\n")
        lines.append("    @overload\n")
        lines.append(f"    def set(self, value: float, unit: Unit[{qty.__name__}]) -> {qty.__name__}: ...\n")
        lines.append("    @overload\n")
        lines.append(f"    def set(self, value: float, unit: str) -> {qty.__name__}: ...\n")

    OUT_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    write_stub()
