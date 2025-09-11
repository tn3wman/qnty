from dataclasses import dataclass

# =========================================================
# Dimensions (7 base: L, M, T, I, Θ, N, J)
# =========================================================

DimVec = tuple[int,int,int,int,int,int,int]


@dataclass(frozen=True)
class Dimension:
    exps: DimVec
    def __mul__(self, other):
        return Dimension(tuple(a+b for a,b in zip(self.exps, other.exps, strict=False)))
    def __truediv__(self, other):
        return Dimension(tuple(a-b for a,b in zip(self.exps, other.exps, strict=False)))
    def __pow__(self, p:int):
        result = tuple(a*p for a in self.exps)
        if len(result) != 7:
            raise ValueError("Dimension exponent vector must have length 7")
        return Dimension(result)
    def __hash__(self): return hash(self.exps)

def dim_add(a: DimVec, b: DimVec) -> DimVec:
    return tuple(x+y for x,y in zip(a,b, strict=False))  # type: ignore

def dim_sub(a: DimVec, b: DimVec) -> DimVec:
    return tuple(x-y for x,y in zip(a,b, strict=False))  # type: ignore

def dim_pow(a: DimVec, p: int) -> DimVec:
    return tuple(x*p for x in a)  # type: ignore


