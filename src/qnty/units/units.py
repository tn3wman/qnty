from ..dimensions import dim
from .core import UnitNamespace, add_unit, write_units_stub

dimensionless = add_unit(
    dim.D, symbol="", si_factor=1.0,
    aliases=("dless", "scalar",),
)

# (L,M,T,I,Θ,N,J)

meter = add_unit(
    dim.L, symbol="m", si_factor=1.0,
    aliases=("meters","metre","metres",),
    allow_prefix=True, expose_prefixed_to_u=True
)

gram = add_unit(
    dim.M, symbol="g", si_factor=1e-3,
    aliases=("grams",),
    allow_prefix=True, expose_prefixed_to_u=True
)

second = add_unit(
    dim.T, symbol="s", si_factor=1.0,
    aliases=("seconds",),
    allow_prefix=True, expose_prefixed_to_u=True
)


class DimensionlessUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = ""

    dimensionless = dimensionless

class LengthUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = "meter"

    meter = meter

if __name__ == "__main__":
    write_units_stub("units.pyi")

