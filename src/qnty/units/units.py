from ..dimensions import dim
from .core import add_unit, write_units_stub, UnitNamespace

#     meter    = add_unit(dim.L, symbol="m",  si_factor=1.0, aliases=("meters","metre","metres"), allow_prefix=True, expose_prefixed_to_u=True)

# (L,M,T,I,Θ,N,J)

meter = add_unit(
    dim.L, symbol="m", si_factor=1.0,
    aliases=("meters","metre","metres",),
    allow_prefix=True, expose_prefixed_to_u=True
)

gram = add_unit(
    dim.M, symbol="g", si_factor=1e-3,
    aliases=("kilogram","kilograms",),
    allow_prefix=True, expose_prefixed_to_u=True
)

second = add_unit(
    dim.T, symbol="s", si_factor=1.0,
    aliases=("seconds",),
    allow_prefix=True, expose_prefixed_to_u=True
)

dimensionless = add_unit(
    dim.D, symbol="", si_factor=1.0,
    aliases=("dless", "scalar",),
)

class DimensionlessUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = ""

    dimensionless = dimensionless



if __name__ == "__main__":
    write_units_stub("namespace.pyi")

