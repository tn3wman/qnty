# tuple_encoding_demo_7d.py
"""
Minimal tuple-encoded dimensional analysis (7 bases: L, M, T, I, Θ, N, J).

- Dimension is a fixed 7-tuple of ints (exponents).
- Unit has a scale to SI and a Dimension.
- Quantity stores SI values + Dimension, supports + - * / ** and to(unit).

This is intentionally small to compare structure + perf vs prime encoding.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict
import random, time

Dim7 = Tuple[int,int,int,int,int,int,int]  # (L,M,T,I,Θ,N,J)

def add(a: Dim7, b: Dim7) -> Dim7:
    return tuple(x+y for x,y in zip(a,b))  # type: ignore

def sub(a: Dim7, b: Dim7) -> Dim7:
    return tuple(x-y for x,y in zip(a,b))  # type: ignore

def pw(a: Dim7, k: int) -> Dim7:
    return tuple(x*k for x in a)  # type: ignore

@dataclass(frozen=True, slots=True)
class Dimension:
    exps: Dim7
    def __mul__(self, other: "Dimension") -> "Dimension":
        return Dimension(add(self.exps, other.exps))
    def __truediv__(self, other: "Dimension") -> "Dimension":
        return Dimension(sub(self.exps, other.exps))
    def __pow__(self, k: int) -> "Dimension":
        return Dimension(pw(self.exps, k))
    def __hash__(self) -> int:
        return hash(self.exps)
    def __repr__(self) -> str:
        return f"Dim{self.exps}"

# Base dimensions
L  = Dimension((1,0,0,0,0,0,0))
M  = Dimension((0,1,0,0,0,0,0))
T  = Dimension((0,0,1,0,0,0,0))
I_ = Dimension((0,0,0,1,0,0,0))
TH = Dimension((0,0,0,0,1,0,0))
N_ = Dimension((0,0,0,0,0,1,0))
J_ = Dimension((0,0,0,0,0,0,1))
DIMLESS = Dimension((0,0,0,0,0,0,0))

# Derived (only L,M,T used in examples)
Area      = L**2
Volume    = L**3
Velocity  = L / T
Acceleration = L / (T**2)
Force     = M * Acceleration            # M L T^-2
Pressure  = Force / (L**2)              # M L^-1 T^-2

@dataclass(frozen=True, slots=True)
class Unit:
    name: str
    factor_to_si: float
    dim: Dimension

@dataclass(frozen=True, slots=True)
class Quantity:
    value: float  # stored in SI
    dim: Dimension
    def __mul__(self, other: "Quantity|float") -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.value*other.value, self.dim*other.dim)
        return Quantity(self.value*float(other), self.dim)
    def __truediv__(self, other: "Quantity|float") -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.value/other.value, self.dim/other.dim)
        return Quantity(self.value/float(other), self.dim)
    def __pow__(self, k: int) -> "Quantity":
        return Quantity(self.value**k, self.dim**k)
    def __add__(self, other: "Quantity") -> "Quantity":
        if self.dim != other.dim: raise TypeError("dim mismatch")
        return Quantity(self.value+other.value, self.dim)
    def __sub__(self, other: "Quantity") -> "Quantity":
        if self.dim != other.dim: raise TypeError("dim mismatch")
        return Quantity(self.value-other.value, self.dim)
    def to(self, unit: Unit) -> float:
        if unit.dim != self.dim: raise TypeError("conversion dim mismatch")
        return self.value / unit.factor_to_si
    def __repr__(self) -> str:
        return f"{self.value:.6g} [ {self.dim} ]"

def Q(val: float, unit: Unit) -> Quantity:
    return Quantity(val*unit.factor_to_si, unit.dim)

# Basic units (SI + a couple convenience ones)
meter    = Unit("m", 1.0, L)
kilogram = Unit("kg", 1.0, M)
second   = Unit("s", 1.0, T)
ampere   = Unit("A", 1.0, I_)
kelvin   = Unit("K", 1.0, TH)
mole     = Unit("mol",1.0, N_)
candela  = Unit("cd",1.0, J_)

newton = Unit("N", 1.0, Force)
pascal = Unit("Pa", 1.0, Pressure)
foot   = Unit("ft", 0.3048, L)
psi    = Unit("psi", 6894.757293168, Pressure)

def tiny_demo():
    a = Q(8, foot) * Q(12, foot)     # area
    f = Q(75, kilogram) * (Q(9.80665, meter) / (Q(1, second)**2))
    p = f / a
    return {
        "area_m2": a.to(Unit("m^2", 1.0, L**2)),
        "force_N": f.to(newton),
        "pressure_Pa": p.to(pascal),
        "pressure_psi": p.to(psi),
    }

def tiny_perf(n=50_000, seed=0) -> Dict[str,float]:
    random.seed(seed)
    vecs = [ tuple(random.randint(-6,6) for _ in range(7)) for _ in range(n) ]
    dims = [ Dimension(v) for v in vecs ]
    # compose (mul -> add exponents)
    t0=time.perf_counter(); acc=DIMLESS
    for d in dims:
        acc = acc * d
    t1=time.perf_counter(); mul_s = t1-t0
    # divide (sub exponents)
    t0=time.perf_counter(); acc=DIMLESS
    for d in dims:
        acc = acc / d
    t1=time.perf_counter(); div_s = t1-t0
    # equality
    t0=time.perf_counter(); cnt=0
    for i in range(0, n-1, 2):
        cnt += 1 if dims[i]==dims[i+1] else 0
    t1=time.perf_counter(); eq_s = t1-t0
    return {"mul_s": mul_s, "div_s": div_s, "eq_s": eq_s}

if __name__ == "__main__":
    print("DEMO:", tiny_demo())
    print("PERF:", tiny_perf())
