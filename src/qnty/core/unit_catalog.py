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

# US customary mass units
# Canonical mass unit: pound (lb). Include common aliases and legacy "pound_mass" name.
pound = add_unit(
    dim.M, symbol="lb", si_factor=0.45359237,
    aliases=("lb", "lbm", "lbs", "pounds", "pound_mass"),
)

# Backward-compatible name
pound_mass = pound

slug = add_unit(
    dim.M, symbol="slug", si_factor=14.59390293720636,
    aliases=("slugs",),
)

ounce = add_unit(
    dim.M, symbol="oz", si_factor=0.028349523125,
    aliases=("ounces",),
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

# TODO: Add option to add prefixes to composed units
liter = attach_composed(
    u.deci_meter**3, name="liter", symbol="L",
    aliases=("liters","litre","litres",),
)

milli_liter = attach_composed(
    u.centi_meter**3, name="milli_liter", symbol="mL",
    aliases=("milliliters", "millilitre","millilitres"),
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

# US customary force unit
pound_force = add_unit(
    dim.Force, symbol="lbf", si_factor=4.4482216152605,
    aliases=("poundforce", "lbf"),
)


# =======================
# PRESSURE
# =======================
pascal = attach_composed(
    u.newton / (u.meter**2), name="pascal", symbol="Pa",
    aliases=("pascals","Pa",),
)

pound_force_per_square_inch = attach_composed(
    u.pound_force / (u.inch**2), name="pound_force_per_square_inch", symbol="psi",
    aliases=("psi", "lbf/in2", "lbf/in²",),
)

class PressureUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = "Pa"

    Pa: Final[Unit] = pascal
    pascal: Final[Unit] = pascal
    pascals: Final[Unit] = pascal
    pound_force_per_square_inch: Final[Unit] = pound_force_per_square_inch


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


# =======================
# MASS DENSITY
# =======================
kilogram_per_cubic_meter = attach_composed(
    u.kg / (u.meter**3), name="kilogram_per_cubic_meter", symbol="kg/m³",
    aliases=("kg_per_m3", "kg/m3",),
)

pound_mass_per_cubic_foot = attach_composed(
    u.pound_mass / (u.foot**3), name="pound_mass_per_cubic_foot", symbol="lbm/ft³",
    aliases=("lbm_per_ft3", "lbm/ft3",),
)

ounce_per_milliliter = attach_composed(
    u.ounce / u.milli_liter, name="ounce_per_milliliter", symbol="oz/mL",
    aliases=("oz_per_mL", "oz/mL",),
)

class MassDensityUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = "kilogram_per_cubic_meter"

    kilogram_per_cubic_meter: Final[Unit] = kilogram_per_cubic_meter
    pound_mass_per_cubic_foot: Final[Unit] = pound_mass_per_cubic_foot
    ounce_per_milliliter: Final[Unit] = ounce_per_milliliter



pascal_second = attach_composed(
    u.pascal * u.second, name="pascal_second", symbol="Pa·s",
    aliases=("pascal_second","pascal_seconds","Pa·s","Pa.s",),
)

poise = attach_composed(
    u.gram / (u.centi_meter * u.second), name="poise", symbol="P",
    aliases=("poise","P",),
)

pound_force_second_per_square_foot = attach_composed(
    u.pound_force * u.second / (u.foot**2), name="pound_force_second_per_square_foot", symbol="lbf·s/ft²",
    aliases=("lbf·s/ft²","lbf*s/ft2",),
)


class ViscosityDynamicUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = "pascal_second"

    pascal_second: Final[Unit] = pascal_second
    poise: Final[Unit] = poise
    pound_force_second_per_square_foot: Final[Unit] = pound_force_second_per_square_foot



square_meter_per_second = attach_composed(
    u.meter**2 / u.second, name="square_meter_per_second", symbol="m²/s",
    aliases=("square_meter_per_second","square_meters_per_second","m2/s",),
)
foot_squared_per_second = attach_composed(
    u.foot**2 / u.second, name="foot_squared_per_second", symbol="ft²/s",
    aliases=("foot_squared_per_second","feet_squared_per_second","ft2/s",),
)


class ViscosityKinematicUnits(UnitNamespace):
    __slots__ = ()
    __preferred__ = "square_meter_per_second"

    square_meter_per_second: Final[Unit] = square_meter_per_second
    foot_squared_per_second: Final[Unit] = foot_squared_per_second


