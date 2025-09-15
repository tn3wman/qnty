from typing import Final

from numpy import square
from sympy import deg

from .unit import Unit, UnitNamespace

class Units:
    # =======================
    # BASE UNITS
    # =======================
    dimensionless: Final[Unit]
    dless: Final[Unit]  # alias for dimensionless
    scalar: Final[Unit]  # alias for dimensionless

    radian : Final[Unit]
    radians : Final[Unit]  # alias for radian
    degree : Final[Unit]
    degrees : Final[Unit]  # alias for degree
    deg : Final[Unit]  # alias for degree


    # Time
    kilo_second: Final[Unit]  # alias for second
    hecto_second: Final[Unit]  # alias for second
    deca_second: Final[Unit]  # alias for second
    das: Final[Unit]  # alias for second
    minute: Final[Unit]  # alias for second


    second: Final[Unit]
    seconds: Final[Unit]  # alias for second
    deci_second: Final[Unit]  # alias for second
    ds: Final[Unit]  # alias for second

    centi_second: Final[Unit]  # alias for second
    cs: Final[Unit]  # alias for second

    milli_second: Final[Unit]  # alias for second
    micro_second: Final[Unit]  # alias for second
    nano_second: Final[Unit]  # alias for second


    # Length
    kilo_meter: Final[Unit]  # alias for meter
    hecto_meter: Final[Unit]  # alias for meter
    deca_meter: Final[Unit]  # alias for meter
    dam: Final[Unit]  # alias for meter

    meter: Final[Unit]
    meters: Final[Unit]  # alias for meter
    metre: Final[Unit]  # alias for meter
    metres: Final[Unit]  # alias for meter
    deci_meter: Final[Unit]  # alias for meter
    dm: Final[Unit]  # alias for meter

    centi_meter: Final[Unit]  # alias for meter
    cm: Final[Unit]  # alias for meter

    milli_meter: Final[Unit]  # alias for meter
    micro_meter: Final[Unit]  # alias for meter
    nano_meter: Final[Unit]  # alias for meter

    foot: Final[Unit]
    feet: Final[Unit]  # alias for foot
    ft: Final[Unit]  # alias for foot
    inch: Final[Unit]


    # Mass
    kilo_gram: Final[Unit]  # alias for gram
    hecto_gram: Final[Unit]  # alias for gram
    deca_gram: Final[Unit]  # alias for gram
    dag: Final[Unit]  # alias for gram
    gram: Final[Unit]
    grams: Final[Unit]  # alias for gram
    deci_gram: Final[Unit]  # alias for gram
    dg: Final[Unit]  # alias for gram
    centi_gram: Final[Unit]  # alias for gram
    cg: Final[Unit]  # alias for gram
    milli_gram: Final[Unit]  # alias for gram
    micro_gram: Final[Unit]  # alias for gram
    nano_gram: Final[Unit]  # alias for gram

    ounce : Final[Unit]
    ounces : Final[Unit]  # alias for ounce
    oz: Final[Unit]  # alias for ounce
    pound_mass: Final[Unit]
    lbm: Final[Unit]  # alias for pound_mass
    slug: Final[Unit]
    slugs: Final[Unit]  # alias for slug


    hg: Final[Unit]  # alias for gram
    hm: Final[Unit]  # alias for meter
    hs: Final[Unit]  # alias for second
    kg: Final[Unit]  # alias for gram
    km: Final[Unit]  # alias for meter
    ks: Final[Unit]  # alias for second
    mg: Final[Unit]  # alias for gram
    mm: Final[Unit]  # alias for meter
    ms: Final[Unit]  # alias for second
    ng: Final[Unit]  # alias for gram
    nm: Final[Unit]  # alias for meter
    ns: Final[Unit]  # alias for second
    ug: Final[Unit]  # alias for gram
    um: Final[Unit]  # alias for meter
    us: Final[Unit]  # alias for second
    μg: Final[Unit]  # alias for gram
    μm: Final[Unit]  # alias for meter
    μs: Final[Unit]  # alias for second

    # =======================
    # SECONDARY UNITS
    # =======================
    # Acceleration
    meter_per_square_second: Final[Unit]
    foot_per_square_second: Final[Unit]
    foot_per_second_squared: Final[Unit]  # alias for foot_per_square_second

    square_meter: Final[Unit]
    square_foot: Final[Unit]
    square_millimeter: Final[Unit]

    # Velocity
    meter_per_second: Final[Unit]
    foot_per_second: Final[Unit]

    # Volume
    liter: Final[Unit]
    liters: Final[Unit]  # alias for liter
    litre: Final[Unit]  # alias for liter
    litres: Final[Unit]  # alias for liter
    cubic_meter: Final[Unit]
    cubic_meters: Final[Unit]  # alias for cubic_meter
    m3: Final[Unit]  # alias for cubic_meter
    milli_liter: Final[Unit]
    gallon: Final[Unit]
    cubic_foot: Final[Unit]

    # =======================
    # DERIVED UNITS
    # =======================

    # Force
    N: Final[Unit]  # alias for newton
    newton : Final[Unit]
    newtons : Final[Unit]  # alias for newton
    lbf: Final[Unit]  # alias for pound_force
    pound_force : Final[Unit]

    # Pressure
    Pa: Final[Unit]  # alias for pascal
    pascal : Final[Unit]
    pascals : Final[Unit]  # alias for pascal

class DimensionlessUnits(UnitNamespace):
    dimensionless: Final[Unit]
    dless: Final[Unit]
    scalar: Final[Unit]

class AnglePlaneUnits(UnitNamespace):
    radian: Final[Unit]
    radians: Final[Unit]
    degree: Final[Unit]
    degrees: Final[Unit]
    deg: Final[Unit]

class LengthUnits(UnitNamespace):
    # Core SI
    meter: Final[Unit]
    millimeter: Final[Unit]
    inch: Final[Unit]

class AreaUnits(UnitNamespace):
    square_meter: Final[Unit]
    square_foot: Final[Unit]
    square_millimeter: Final[Unit]

class VelocityLinearUnits(UnitNamespace):
    meter_per_second: Final[Unit]
    foot_per_second: Final[Unit]

class PressureUnits(UnitNamespace):
    pascal: Final[Unit]
    pascals: Final[Unit]
    Pa: Final[Unit]

class AccelerationUnits(UnitNamespace):
    meter_per_square_second: Final[Unit]
    foot_per_square_second: Final[Unit]

class MassDensityUnits(UnitNamespace):
    kilogram_per_cubic_meter: Final[Unit]
    pound_mass_per_cubic_foot: Final[Unit]
    ounce_per_milliliter: Final[Unit]

class VolumetricFlowRateUnits(UnitNamespace):
    cubic_meter_per_second: Final[Unit]
    gallon_per_minute: Final[Unit]
    cubic_foot_per_minute: Final[Unit]

class ViscosityDynamicUnits(UnitNamespace):
    pascal_second: Final[Unit]
    poise: Final[Unit]
    pound_force_second_per_square_foot: Final[Unit]

class ViscosityKinematicUnits(UnitNamespace):
    square_meter_per_second: Final[Unit]
    foot_squared_per_second: Final[Unit]

u: Units
