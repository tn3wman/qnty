# units_core.py
from __future__ import annotations

import inspect
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Final

from ..dimensions import Dimension


# =======================
# Utilities
# =======================
def _norm(s: str) -> str:
    return s.strip().casefold().replace(" ", "").replace("_", "").replace("-", "").replace("^", "").replace("·", "")


_SUP: Final[dict[int, str]] = {2: "²", 3: "³"}


def _caller_var_name(fn: str) -> str:
    frame = inspect.currentframe()
    if frame is None or frame.f_back is None or frame.f_back.f_back is None:
        raise RuntimeError("Could not access call stack for variable name detection")
    frame = frame.f_back.f_back
    frame_info = inspect.getframeinfo(frame)
    if frame_info.code_context is None or not frame_info.code_context:
        raise RuntimeError("Could not get source code context for variable name detection")
    line = frame_info.code_context[0]
    m = re.match(rf"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*{fn}\b", line)
    if not m:
        raise RuntimeError("Could not auto-detect variable name")
    return m.group(1)


# =======================
# Prefix catalog (SI core)
# =======================
# name, symbol, factor
PREFIXES: Final[tuple[tuple[str, str, float], ...]] = (
    ("kilo", "k", 1e3),
    ("hecto", "h", 1e2),
    ("deca", "da", 1e1),
    ("deci", "d", 1e-1),
    ("centi", "c", 1e-2),
    ("milli", "m", 1e-3),
    ("micro", "μ", 1e-6),  # use 'μ' (mu); add 'u' as alias on registration
    ("nano", "n", 1e-9),
)


# =======================
# Unit (frozen) + Registry + sealed 'u' namespace
# =======================
@dataclass(frozen=True, slots=True)
class Unit:
    name: str
    symbol: str
    dim: Dimension
    si_factor: float
    si_offset: float = 0.0  # reserved for affine scales


class UnitRegistry:
    __slots__ = ("by_key", "preferred", "_intern_by_symbol", "_UnitRegistry__sealed")

    def __init__(self):
        self.by_key = {}
        self.preferred = {}
        self._intern_by_symbol = {}
        self._UnitRegistry__sealed = False

    def register(self, u: Unit, *aliases: str) -> Unit:
        if self._UnitRegistry__sealed:
            raise AttributeError("Unit registry is sealed; cannot register.")
        for k in set(aliases) | {u.name, u.symbol}:
            self.by_key[_norm(k)] = u
        self._intern_by_symbol.setdefault(u.symbol, u)
        return u

    def get(self, alias: str) -> Unit:
        k = _norm(alias)
        if k not in self.by_key:
            raise KeyError(f"Unknown unit alias: {alias!r}")
        return self.by_key[k]

    def set_preferred(self, u: Unit) -> None:
        self.preferred[u.dim] = u

    def preferred_for(self, d: Dimension) -> Unit | None:
        return self.preferred.get(d)

    def seal(self) -> None:
        self._UnitRegistry__sealed = True


ureg = UnitRegistry()


class Units:
    def __init__(self):
        self.__sealed = False

    def __setattr__(self, k, v):
        if hasattr(self, "_Units__sealed") and self.__sealed:
            raise AttributeError("u is sealed; cannot modify.")
        object.__setattr__(self, k, v)


u = Units()
_unit_registry: dict[str, Unit] = {}
_unit_aliases: dict[str, str] = {}


# =======================
# Prefix generation
# =======================
def _generate_prefixed_units(base: Unit, *, expose_to_u: bool = False) -> None:
    """
    Create prefixed variants for a base unit, e.g., N -> kN, mN, ...
    Registers each variant with:
      - symbol = <prefix-symbol> + base.symbol  (e.g., "kN")
      - name   = <prefix-name> + "_" + base.name (e.g., "kilo_newton")
      - aliases include "u" micro variant if symbol had μ
    Optionally attaches them as attributes on `u` (if expose_to_u=True).
    """
    for pname, psym, pfactor in PREFIXES:
        sym = f"{psym}{base.symbol}"
        name = f"{pname}_{base.name}"
        if sym in ureg._intern_by_symbol:
            continue  # already generated
        unit = Unit(name=name, symbol=sym, dim=base.dim, si_factor=base.si_factor * pfactor)
        aliases = {name, sym}
        # Include ASCII 'u' alias for micro (μ)
        if psym == "μ":
            aliases.add(f"u{base.symbol}")
            aliases.add(f"micro_{base.name}")
        ureg.register(unit, *aliases)
        if expose_to_u:
            setattr(u, name, unit)
            _unit_aliases[name] = base.name
            setattr(u, sym, unit)  # allow u.kN, u.mN, etc.
            _unit_aliases[sym] = base.name
            if psym == "μ":
                setattr(u, f"u{base.symbol}", unit)
                _unit_aliases[f"u{base.symbol}"] = base.name


# =======================
# Add/base units with allow_prefix
# =======================
def add_unit(
    dim_obj: Dimension,
    *,
    symbol: str,
    si_factor: float,
    si_offset: float = 0.0,
    name: str | None = None,
    aliases: Iterable[str] = (),
    allow_prefix: bool = False,
    expose_prefixed_to_u: bool = False,
) -> Unit:
    if name is None:
        name = _caller_var_name("add_unit")
    if name in _unit_registry or name in _unit_aliases:
        raise KeyError(f"Unit name '{name}' already defined.")
    unit = Unit(name=name, symbol=symbol, dim=dim_obj, si_factor=si_factor, si_offset=si_offset)
    ureg.register(unit, name, symbol, *aliases)
    setattr(u, name, unit)
    _unit_registry[name] = unit
    for a in aliases:
        if a in _unit_registry or a in _unit_aliases:
            raise KeyError(f"Unit alias '{a}' already in use.")
        setattr(u, a, unit)
        _unit_aliases[a] = name

    if allow_prefix:
        _generate_prefixed_units(unit, expose_to_u=expose_prefixed_to_u)
    return unit


# =======================
# Add/composed units
# =======================
def attach_composed(unit: Unit, *, name: str, symbol: str | None = None, aliases: Iterable[str] = (), set_preferred: bool = False) -> Unit:
    """
    Take an already composed unit (e.g., u.lbf / (u.inch**2)),
    give it a canonical name/symbol, register it, and expose it on `u`.

    - Keeps the original dimension & si_factor of `unit`.
    - Registers both your new symbol AND the original composed symbol as aliases,
      so lookups by "psi" and "lbf/in²" both work.
    """
    if name in _unit_registry or name in _unit_aliases:
        raise KeyError(f"Unit name '{name}' already defined.")

    # Use given symbol or reuse the composed unit's symbol
    sym = symbol or unit.symbol

    # Create a "named view" of the composed unit
    named = Unit(name=name, symbol=sym, dim=unit.dim, si_factor=unit.si_factor, si_offset=unit.si_offset)

    # Register with aliases: new name, new symbol, original composed symbol, plus any extras
    all_aliases = set(aliases) | {name, sym, unit.symbol}
    ureg.register(named, *all_aliases)

    # Expose on the dot-namespace
    setattr(u, name, named)
    _unit_registry[name] = named

    # Also expose any alias strings as dot attributes if you want (optional; comment out if too noisy)
    for a in aliases:
        if a in _unit_registry or a in _unit_aliases:
            continue
        setattr(u, a, named)
        _unit_aliases[a] = name

    if set_preferred:
        ureg.set_preferred(named)

    return named


# =======================
# Composition (operator overloading) with interning
# =======================
def _compose(a: Unit, b: Unit, *, div: bool) -> Unit:
    sym = f"{a.symbol}/{b.symbol}" if div else f"{a.symbol}·{b.symbol}"
    if sym in ureg._intern_by_symbol:
        return ureg._intern_by_symbol[sym]
    name = f"{a.name}_per_{b.name}" if div else f"{a.name}_{b.name}"
    dimn = a.dim / b.dim if div else a.dim * b.dim
    fact = (a.si_factor / b.si_factor) if div else (a.si_factor * b.si_factor)
    return ureg.register(Unit(name=name, symbol=sym, dim=dimn, si_factor=fact))


def _pow_unit(a: Unit, k: int) -> Unit:
    if k == 1:
        return a
    sym = f"{a.symbol}{_SUP.get(k, '^' + str(k))}"
    if sym in ureg._intern_by_symbol:
        return ureg._intern_by_symbol[sym]
    name = f"{a.name}_{k}"
    return ureg.register(Unit(name=name, symbol=sym, dim=(a.dim**k), si_factor=(a.si_factor**k)))


Unit.__mul__ = lambda self, other: _compose(self, other, div=False)  # type: ignore[attr-defined]
Unit.__truediv__ = lambda self, other: _compose(self, other, div=True)  # type: ignore[attr-defined]
Unit.__pow__ = lambda self, k: _pow_unit(self, k)  # type: ignore[attr-defined]


# =======================
# Stubs & sealing
# =======================
def write_units_stub(path: str = "units.pyi") -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("from typing import Final\n")
        f.write("from .core import Unit\n\n")
        f.write("class Units:\n")
        for name in sorted(_unit_registry):
            f.write(f"    {name}: Final[Unit]\n")
        for alias, canonical in sorted(_unit_aliases.items()):
            f.write(f"    {alias}: Final[Unit]  # alias for {canonical}\n")
        f.write("\n")
        f.write("u: Final[Units]\n")


def seal_units() -> None:
    ureg.seal()
    u.__sealed = True


# =======================
# UnitNamespace (declarative catalogs)
# =======================
@dataclass(frozen=True, slots=True)
class UnitDef:
    symbol: str
    dim: Dimension
    si_factor: float
    si_offset: float = 0.0
    aliases: tuple[str, ...] = ()
    allow_prefix: bool = False


class UnitNamespaceMeta(type):
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        expose_pref = bool(ns.get("__expose_prefixed__", False))
        preferred_name = ns.get("__preferred__", None)

        created: dict[str, Unit] = {}
        for attr, val in list(ns.items()):
            if isinstance(val, UnitDef):
                unit = add_unit(
                    val.dim,
                    symbol=val.symbol,
                    si_factor=val.si_factor,
                    si_offset=val.si_offset,
                    name=attr,
                    aliases=val.aliases,
                    allow_prefix=val.allow_prefix,
                    expose_prefixed_to_u=expose_pref,
                )
                setattr(cls, attr, unit)
                created[attr] = unit

        # Handle preferred by canonical name, if provided
        if preferred_name:
            if preferred_name not in created:
                raise KeyError(f"__preferred__='{preferred_name}' not found in {name}")
            ureg.set_preferred(created[preferred_name])

        # Freeze class (catalogs are constant after creation)
        def _blocked_setattr(self, *_a, **_k):
            raise AttributeError(f"{name} is frozen; define units in the class body.")

        cls.__setattr__ = _blocked_setattr  # type: ignore[attr-defined]
        return cls


class UnitNamespace(metaclass=UnitNamespaceMeta):
    __slots__ = ()


# =======================
# Example: ForceUnits catalog (real units)
# =======================
# NOTE: You can change __expose_prefixed__ to False if you don't want u.kN, u.mN, ...

# You can define additional catalogs similarly:
# class PressureUnits(UnitNamespace): ...
# class MassDensityUnits(UnitNamespace): ...

# =======================
# Small demo / defaults (optional)
# =======================
# if __name__ == "__main__":
#     newton = UnitDef("N",    dim.Force, si_factor=1.0,     aliases=("N","newtons"), allow_prefix=True)

#     class ForceUnits(UnitNamespace):
#         """Unit constants for Force."""
#         __slots__ = ()
#         __preferred__ = "newton"
#         __expose_prefixed__ = True  # expose kN, mN, μN, etc. on `u`

#         newton = newton
#         dyne   = UnitDef("dyn",  dim.Force, si_factor=1e-5,    aliases=("dyne","dynes"), allow_prefix=True)
#         lbf    = UnitDef("lbf",  dim.Force, si_factor=4.4482216152605, aliases=("pound_force","poundforce"))
#     # A couple of base units to make the demo nicer (define yours elsewhere if you prefer)
#     meter    = add_unit(dim.L, symbol="m",  si_factor=1.0, aliases=("meters","metre","metres"), allow_prefix=True, expose_prefixed_to_u=True)
#     second   = add_unit(dim.T, symbol="s",  si_factor=1.0, aliases=("sec","secs","seconds"),   allow_prefix=True, expose_prefixed_to_u=True)
#     kilogram = add_unit(dim.M, symbol="kg", si_factor=1.0, aliases=("kilograms","kg"))

#     # Composition still works:
#     mps = u.m / u.s  # "m/s" (composed; not auto-attached unless you do it yourself)

#     # Preferred: Force set to N by ForceUnits; set more if desired:
#     # ureg.set_preferred(u.Pa)  # once you define PressureUnits

#     # Seal when your catalogs are loaded:
#     seal_units()

#     # Quick print:
#     F = Q(1.5, u.kN)  # thanks to prefixes on newton
#     print("Force:", F)  # prints in preferred (N) by default; convert if you like: F.to(u.kN)
