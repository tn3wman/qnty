from typing import Final

from ..dimensions import dim
from . import u
from .core import Unit, UnitNamespace, add_unit

__all__ = ['DimensionlessUnits', 'LengthUnits']

dimensionless = add_unit(
    dim.D, symbol="", si_factor=1.0,
    aliases=("dless", "scalar",),
)

# ==============
# TIME
# ==============
second = add_unit(
    dim.T, symbol="s", si_factor=1.0,
    aliases=("seconds",),
    allow_prefix=True, expose_prefixed_to_u=True
)

# ==============
# LENGTH
# ==============
meter = add_unit(
    dim.L, symbol="m", si_factor=1.0,
    aliases=("meters","metre","metres",),
    allow_prefix=True, expose_prefixed_to_u=True
)

inch = add_unit(
    dim.L, symbol="in", si_factor=0.0254,
    aliases=("inches",),
)

foot = add_unit(
    dim.L, symbol="ft", si_factor=0.3048,
    aliases=("feet","ft",),
)

class LengthUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = "meter"

    meter: Final[Unit] = meter
    millimeter: Final[Unit] = u.milli_meter
    inch: Final[Unit] = inch
    foot: Final[Unit] = foot

# ==============
# MASS
# ==============
gram = add_unit(
    dim.M, symbol="g", si_factor=1e-3,
    aliases=("grams",),
    allow_prefix=True, expose_prefixed_to_u=True
)

# ==============
# TEMPERATURE
# ==============
kelvin = add_unit(
    dim.Θ, symbol="K", si_factor=1.0,
)

# ==============
# LUMINOUS INTENSITY
# ==============
candela = add_unit(
    dim.J, symbol="cd", si_factor=1.0,
)

# ==============
# ELECTRIC CURRENT
# ==============
ampere = add_unit(
    dim.A, symbol="A", si_factor=1.0,
    aliases=("amperes","amps","amp",),
    allow_prefix=True, expose_prefixed_to_u=True
)

# ==============
# AMOUNT OF SUBSTANCE
# ==============
mole = add_unit(
    dim.N, symbol="mol", si_factor=1.0,
    aliases=("moles",),
    allow_prefix=True, expose_prefixed_to_u=True
)

class DimensionlessUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = ""

    dimensionless: Final[Unit] = dimensionless



# if __name__ == "__main__":
#     write_units_stub("units.pyi")

