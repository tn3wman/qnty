# isort: skip_file
"""
Generate typed .pyi stubs for FieldQuantity subclasses that declare UNIT_NS.
- Scans qnty.quantities.quantity_catalog for subclasses (e.g., Acceleration)
- Reads their UNIT_NS to enumerate canonical unit attribute names
- Emits properties (including identifier-safe aliases) for Setter, ToUnit, and AsUnit so IDEs get autocompletion

This complements the runtime dynamic binding in core.py without duplicating logic.
"""
from __future__ import annotations

import inspect
from pathlib import Path

import qnty.quantities.core as core
import qnty.quantities.quantity_catalog as qcat
from qnty.units.core import Unit, _unit_aliases


OUT_PATH = Path(qcat.__file__).with_suffix(".pyi")


def unit_names_from_namespace(ns: type) -> list[str]:
    names: list[str] = []
    for name, val in vars(ns).items():
        if isinstance(val, Unit):
            names.append(name)
    return sorted(names)


def alias_names_for(canonical: str) -> list[str]:
    """Return all valid-identifier alias names for a canonical unit name."""
    aliases: list[str] = []
    for alias, base in _unit_aliases.items():
        if base == canonical and alias != canonical and alias.isidentifier():
            aliases.append(alias)
    return sorted(set(aliases))


def find_quantities() -> list[type]:
    qty_types: list[type] = []
    for _name, obj in vars(qcat).items():
        if inspect.isclass(obj) and issubclass(obj, core.FieldQuantity):
            if obj is core.FieldQuantity:
                continue
            # We only support quantities that declare UNIT_NS and SETTER_CLS
            if hasattr(obj, "UNIT_NS") and hasattr(obj, "SETTER_CLS"):
                qty_types.append(obj)
    return qty_types


def write_stub():
    lines: list[str] = []
    lines.append("# isort: skip_file\n")
    lines.append("from __future__ import annotations\n\n")
    lines.append("from typing import overload\n\n")
    lines.append("from ..units.core import Unit\n")
    lines.append("from .core import FieldQuantity, FieldSetter, UnitApplier, UnitChanger\n\n\n")

    # For each quantity, emit typed properties from UNIT_NS
    for qty in find_quantities():
        setter = getattr(qcat, qty.__name__ + "Setter")
        unit_ns = qty.UNIT_NS  # type: ignore[attr-defined]
        names = unit_names_from_namespace(unit_ns)  # type: ignore[arg-type]

        # Setter with canonical names and aliases
        lines.append(f"class {setter.__name__}(FieldSetter[{qty.__name__}]):\n")
        for n in names:
            lines.append("    @property\n")
            lines.append(f"    def {n}(self) -> {qty.__name__}: ...\n")
            for alias in alias_names_for(n):
                lines.append("    @property\n")
                lines.append(f"    def {alias}(self) -> {qty.__name__}: ...\n")
        lines.append("\n\n")

        # Quantity with nested ToUnit/AsUnit and __call__
        lines.append(f"class {qty.__name__}(FieldQuantity[{qty.__name__}]):\n")
        lines.append(f"    class ToUnit(UnitApplier[{qty.__name__}]):\n")
        for n in names:
            lines.append("        @property\n")
            lines.append(f"        def {n}(self) -> {qty.__name__}: ...\n")
            for alias in alias_names_for(n):
                lines.append("        @property\n")
                lines.append(f"        def {alias}(self) -> {qty.__name__}: ...\n")
        lines.append(f"\n        def __call__(self, unit: Unit[{qty.__name__}] | str) -> {qty.__name__}: ...\n\n")

        lines.append(f"    class AsUnit(UnitChanger[{qty.__name__}]):\n")
        for n in names:
            lines.append("        @property\n")
            lines.append(f"        def {n}(self) -> {qty.__name__}: ...\n")
            for alias in alias_names_for(n):
                lines.append("        @property\n")
                lines.append(f"        def {alias}(self) -> {qty.__name__}: ...\n")
        lines.append(f"\n        def __call__(self, unit: Unit[{qty.__name__}] | str) -> {qty.__name__}: ...\n\n")

        lines.append(f"    @property\n    def to_unit(self) -> {qty.__name__}.ToUnit: ...\n\n")
        lines.append(f"    @property\n    def as_unit(self) -> {qty.__name__}.AsUnit: ...\n\n")

        lines.append("    @overload\n")
        lines.append(f"    def set(self, value: float) -> {setter.__name__}: ...\n")
        lines.append("    @overload\n")
        lines.append(f"    def set(self, value: float, unit: Unit[{qty.__name__}]) -> {qty.__name__}: ...\n")
        lines.append("    @overload\n")
        lines.append(f"    def set(self, value: float, unit: str) -> {qty.__name__}: ...\n\n\n")

    OUT_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    write_stub()
