from math import e
from typing import TYPE_CHECKING, Final

from .dimension_catalog import dim
from .unit import Unit, UnitNamespace, add_unit, attach_composed, u

if TYPE_CHECKING:
    from . import u

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

###############################################
# SECONDARY UNITS
###############################################

# =======================
# VELOCITY
# =======================
meter_per_second = attach_composed(
    u.meter / u.second, name="meter_per_second", symbol="m/s",
    aliases=("meters_per_second","m/s",),
)

# =======================
# ACCELERATION
# =======================
meter_per_square_second = attach_composed(
    u.meter / (u.second**2), name="meter_per_square_second", symbol="m/s²",
    aliases=("meter_per_square_second","meters_per_square_second","m/s2",),
)

foot_per_square_second = attach_composed(
    u.foot / (u.second**2), name="foot_per_square_second", symbol="ft/s²",
    aliases=("foot_per_square_second","feet_per_square_second","foot_per_second_squared","feet_per_second_squared","ft/s2",),
)

class AccelerationUnits(UnitNamespace):
    __slots__ = ()
    # Preferred must reference the attribute name, not the symbol
    __preferred__ = "meter_per_square_second"

    meter_per_square_second: Final[Unit] = meter_per_square_second
    foot_per_square_second: Final[Unit] = foot_per_square_second

# =======================
# AREA
# =======================
square_meter = attach_composed(
    u.meter**2, name="square_meter", symbol="m²",
    aliases=("square_meter","square_meters","m2",),
)

# =======================
# VOLUME
# =======================
cubic_meter = attach_composed(
    u.meter**3, name="cubic_meter", symbol="m³",
    aliases=("cubic_meter","cubic_meters","m3",),
)

# =======================
# SOLID ANGLE
# =======================



# =======================
# PLANE ANGLE
# =======================



###############################################
# DERIVED UNITS
###############################################

# =======================
# FORCE
# =======================
newton = attach_composed(
    u.kg * u.meter / (u.second**2), name="newton", symbol="N",
    aliases=("newtons","N",),
)


# =======================
# PRESSURE
# =======================
pascal = attach_composed(
    u.newton / (u.meter**2), name="pascal", symbol="Pa",
    aliases=("pascals","Pa",),
)

class PressureUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = "Pa"

    Pa: Final[Unit] = pascal
    pascal: Final[Unit] = pascal
    pascals: Final[Unit] = pascal


# =======================
# STRESS
# =======================


# =======================
# ENERGY
# =======================


# =======================
# WORK
# =======================


# =======================
# POWER
# =======================

# =======================
# ENERGY FLOW
# =======================


# =======================
# HEAT FLOW
# =======================




