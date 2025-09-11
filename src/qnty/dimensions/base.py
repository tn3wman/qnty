from dataclasses import dataclass

# =========================================================
# Dimensions (7 base: L, M, T, I, Θ, N, J)
# =========================================================

DimVec = tuple[int,int,int,int,int,int,int]


@dataclass(frozen=True)
class Dimension:
    exps: DimVec
    def __mul__(self, other): 
        # Optimized version avoiding generator expressions for better performance
        a_exps, b_exps = self.exps, other.exps
        return Dimension((a_exps[0]+b_exps[0], a_exps[1]+b_exps[1], a_exps[2]+b_exps[2], 
                         a_exps[3]+b_exps[3], a_exps[4]+b_exps[4], a_exps[5]+b_exps[5], a_exps[6]+b_exps[6]))
    def __truediv__(self, other): 
        # Optimized version avoiding generator expressions for better performance
        a_exps, b_exps = self.exps, other.exps
        return Dimension((a_exps[0]-b_exps[0], a_exps[1]-b_exps[1], a_exps[2]-b_exps[2], 
                         a_exps[3]-b_exps[3], a_exps[4]-b_exps[4], a_exps[5]-b_exps[5], a_exps[6]-b_exps[6]))
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


