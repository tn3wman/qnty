# dimensions_core.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, Iterable, Final, Protocol
from types import MappingProxyType
import inspect, re

# =======================
# Configuration
# =======================
N_BASE: Final[int] = 7  # number of base axes (e.g., L,M,T,I,Θ,N,J)

# =======================
# Prime-int backend (num/den)
# =======================
DimVec = tuple[int, ...]
PRIMES: Final[tuple[int, ...]] = (2,3,5,7,11,13,17)  # extend if >10 bases

def vadd(a: DimVec, b: DimVec) -> DimVec: return tuple(x+y for x,y in zip(a,b))  # type: ignore
def vsub(a: DimVec, b: DimVec) -> DimVec: return tuple(x-y for x,y in zip(a,b))  # type: ignore
def vpow(a: DimVec, k: int)    -> DimVec: return tuple(x*k for x in a)          # type: ignore
def zeros(n: int = N_BASE) -> DimVec: return (0,) * n

class DimBackend(Protocol):
    def encode(self, v: DimVec) -> object: ...
    def mul(self, c1: object, c2: object) -> object: ...
    def div(self, c1: object, c2: object) -> object: ...
    def pow(self, c: object, k: int) -> object: ...

class PrimeIntBackend:
    """Compact prime code: (num:int, den:int) with GCD reduction."""
    __slots__ = ()
    
    def encode(self, v: DimVec) -> tuple[int,int]:
        # all zeros → (1,1) i.e., truly dimensionless
        num = den = 1
        for p, e in zip(PRIMES, v):
            if e >= 0:
                if e: num *= p**e
            else:
                de = -e
                if de: den *= p**de
        return self._reduce(num, den)
    def mul(self, a, b): return self._reduce(a[0]*b[0], a[1]*b[1])
    def div(self, a, b): return self._reduce(a[0]*b[1], a[1]*b[0])
    def pow(self, a, k):
        if k == 0: return (1,1)
        if k > 0:  return self._reduce(pow(a[0], k), pow(a[1], k))
        k = -k;    return self._reduce(pow(a[1], k), pow(a[0], k))
    @staticmethod
    def _reduce(num: int, den: int) -> Tuple[int,int]:
        if den < 0: num, den = -num, -den
        if den == 1 or num == 0: return (num, 1 if den != 0 else 0)
        from math import gcd
        g = gcd(abs(num), den)
        if g > 1: num //= g; den //= g
        return (num, den)

BACKEND: DimBackend = PrimeIntBackend()

# =======================
# Dimension (frozen)
# =======================
@dataclass(frozen=True, slots=True)
class Dimension:
    exps: DimVec                 # canonical tuple (immutable)
    code: Tuple[int,int]         # compact prime code (immutable ints)
    def __mul__(self, o: "Dimension") -> "Dimension": return Dimension(vadd(self.exps, o.exps), BACKEND.mul(self.code, o.code))
    def __truediv__(self, o: "Dimension") -> "Dimension": return Dimension(vsub(self.exps, o.exps), BACKEND.div(self.code, o.code))
    def __pow__(self, k: int) -> "Dimension": return Dimension(vpow(self.exps, k), BACKEND.pow(self.code, k))
    def __eq__(self, o: object) -> bool: return isinstance(o, Dimension) and self.code == o.code
    def __hash__(self) -> int: return hash(self.code)
    def __repr__(self) -> str:
        num, den = self.code
        return f"Dim{self.exps} [{num}/{den}]"

# =======================
# Global namespace (sealed) + registry + helpers
# =======================
class Dimensions:
    __slots__ = ("__sealed",)
    def __init__(self): object.__setattr__(self, "_Dimensions__sealed", False)
    def __setattr__(self, k, v):
        if self.__sealed: raise AttributeError("dim is sealed; cannot modify.")
        object.__setattr__(self, k, v)

dim = Dimensions()

# registries
_dim_registry: Dict[str, Dimension] = {}   # canonical names -> Dimension
_dim_aliases: Dict[str, str] = {}          # alias -> canonical name

def _caller_var_name(fn: str) -> str:
    """Best-effort LHS variable name from the calling source line."""
    frame = inspect.currentframe().f_back.f_back
    line = inspect.getframeinfo(frame).code_context[0]
    m = re.match(rf"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*{fn}\b", line)
    if not m:
        raise RuntimeError("Could not auto-detect variable name for registration")
    return m.group(1)

def add_dimension(exps: DimVec, *, name: str|None=None, aliases: Iterable[str] = ()) -> Dimension:
    """Create a base Dimension from raw exponents, register on `dim`, support aliases."""
    if name is None: name = _caller_var_name("add_dimension")
    if name in _dim_registry or name in _dim_aliases:
        raise KeyError(f"Dimension name '{name}' already defined.")
    v = tuple(exps)
    d = Dimension(v, BACKEND.encode(v))
    setattr(dim, name, d)
    _dim_registry[name] = d
    for a in aliases:
        if a in _dim_registry or a in _dim_aliases:
            raise KeyError(f"Dimension alias '{a}' already in use.")
        setattr(dim, a, d)
        _dim_aliases[a] = name
    return d

def add_derived(d: Dimension, *, name: str|None=None, aliases: Iterable[str] = ()) -> Dimension:
    """Register an already-composed Dimension (using *, /, **)."""
    if name is None: name = _caller_var_name("add_derived")
    if name in _dim_registry or name in _dim_aliases:
        raise KeyError(f"Dimension name '{name}' already defined.")
    setattr(dim, name, d)
    _dim_registry[name] = d
    for a in aliases:
        if a in _dim_registry or a in _dim_aliases:
            raise KeyError(f"Dimension alias '{a}' already in use.")
        setattr(dim, a, d)
        _dim_aliases[a] = name
    return d

def seal_dimensions() -> None:
    """Freeze the dim namespace to prevent accidental modification."""
    object.__setattr__(dim, "_Dimensions__sealed", True)

def dimensions_map() -> MappingProxyType[str, Dimension]:
    """Immutable view of canonical dimension registry (excludes aliases)."""
    return MappingProxyType(_dim_registry)

def write_dimensions_stub(path: str = "dimensions.pyi") -> None:
    """Generate a .pyi stub so tools know all dim.<name> and alias attributes."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("from typing import Final\n")
        f.write("from .dimensions_core import Dimension\n\n")
        f.write("class Dimensions:\n")
        for name in sorted(_dim_registry):
            f.write(f"    {name}: Final[Dimension]\n")
        for alias, canonical in sorted(_dim_aliases.items()):
            f.write(f"    {alias}: Final[Dimension]  # alias for {canonical}\n")
        f.write("\n")
        f.write("dim: Final[Dimensions]\n")

# =======================
# Optional: declarative catalog metaclass (frozen)
# =======================
class DimensionNamespaceMeta(type):
    """
    Declarative catalogs:
      - Any class attr that is a tuple[int,...] becomes a Dimension (base)
      - Any class attr that is a callable(cls)->Dimension is evaluated as derived
      - All Dimensions are auto-registered on global `dim` (frozen)
    """
    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        # 1) base tuples -> Dimension
        for k, v in list(ns.items()):
            if isinstance(v, tuple) and all(isinstance(x, int) for x in v):
                d = Dimension(v, BACKEND.encode(v))
                setattr(cls, k, d)
        # 2) callables(cls) -> derived Dimensions
        for k, v in list(ns.items()):
            if callable(v):
                d = v(cls)
                if not isinstance(d, Dimension):
                    raise TypeError(f"{name}.{k} did not return a Dimension")
                setattr(cls, k, d)
        # 3) register to global dim
        for k, v in cls.__dict__.items():
            if isinstance(v, Dimension):
                if k in _dim_registry or k in _dim_aliases:
                    raise KeyError(f"Dimension '{k}' already defined.")
                setattr(dim, k, v)
                _dim_registry[k] = v
        # freeze class
        def _blocked_setattr(self, *_a, **_k):  # type: ignore[unused-argument]
            raise AttributeError(f"{name} is frozen; define dimensions in the class body.")
        cls.__setattr__ = _blocked_setattr  # type: ignore[attr-defined]
        return cls

class DimensionNamespace(metaclass=DimensionNamespaceMeta):
    __slots__ = ()

# =======================
# Example setup (includes Dimensionless)
# =======================
# Canonical dimensionless (all zeros) — prime code becomes (1, 1)
Dimensionless = add_dimension(zeros(), aliases=("Dimless", "Scalar"))

# Common bases (name and aliases are up to you)
L = add_dimension((1,0,0,0,0,0,0), aliases=("Length",))
M = add_dimension((0,1,0,0,0,0,0), aliases=("Mass",))
T = add_dimension((0,0,1,0,0,0,0), aliases=("Time",))

# Derived via normal arithmetic
Area         = add_derived(dim.L * dim.L)
Volume       = add_derived(dim.L ** 3)
Velocity     = add_derived(dim.L / dim.T)
Acceleration = add_derived(dim.L / (dim.T ** 2))
Force        = add_derived(dim.M * dim.L / (dim.T ** 2))
Pressure     = add_derived(dim.Force / dim.Area)
AbsorbedDose = add_derived(dim.L * dim.L / (dim.T ** 2),
                           aliases=("HeadOfCombustion", "HeatOfCombustion"))

# =======================
# Example declarative catalog (optional)
# =======================
class MechanicsDims(DimensionNamespace):
    # You can re-declare for namespacing or add field-specific ones.
    # Base (tuples):
    L = (1,0,0,0,0,0,0)
    M = (0,1,0,0,0,0,0)
    T = (0,0,1,0,0,0,0)
    # Explicit dimensionless in the catalog too (optional):
    Dimensionless = zeros()

    # Derived (callables receive the class with bound Dimensions):
    Area     = lambda cls: cls.L * cls.L
    Volume   = lambda cls: cls.L ** 3
    Velocity = lambda cls: cls.L / cls.T
    Accel    = lambda cls: cls.L / (cls.T ** 2)
    Force    = lambda cls: cls.M * cls.L / (cls.T ** 2)
    Pressure = lambda cls: cls.Force / cls.Area

# Seal once finished defining everything in this module
def seal_dimensions_now() -> None:
    # Call this from your package __init__ after all catalogs/defs are loaded.
    seal_dimensions()

if __name__ == "__main__":
    # Quick sanity checks
    print("dim.Dimensionless:", dim.Dimensionless)   # Dim(0,…,0) [1/1]
    print("dim.Area:", dim.Area)
    print("dim.Pressure:", dim.Pressure)
    print("dim.HeatOfCombustion is dim.AbsorbedDose:", dim.HeatOfCombustion is dim.AbsorbedDose)
    # write_dimensions_stub("dimensions.pyi")
