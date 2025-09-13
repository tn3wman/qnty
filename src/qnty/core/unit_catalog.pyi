from typing import Final

from .unit import Unit, UnitNamespace

class Units:
    # =======================
    # BASE UNITS
    # =======================
    dimensionless: Final[Unit]
    dless: Final[Unit]  # alias for dimensionless
    scalar: Final[Unit]  # alias for dimensionless

    # Time
    kilo_second: Final[Unit]  # alias for second
    hecto_second: Final[Unit]  # alias for second
    deca_second: Final[Unit]  # alias for second
    das: Final[Unit]  # alias for second

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

    # =======================
    # DERIVED UNITS
    # =======================

    # Force
    N: Final[Unit]  # alias for newton
    newton : Final[Unit]
    newtons : Final[Unit]  # alias for newton

    # Pressure
    Pa: Final[Unit]  # alias for pascal
    pascal : Final[Unit]
    pascals : Final[Unit]  # alias for pascal

class DimensionlessUnits(UnitNamespace):
    dimensionless: Final[Unit]
    dless: Final[Unit]
    scalar: Final[Unit]

class LengthUnits(UnitNamespace):
    # Core SI
    meter: Final[Unit]
    millimeter: Final[Unit]
    inch: Final[Unit]

class PressureUnits(UnitNamespace):
    pascal: Final[Unit]
    pascals: Final[Unit]
    Pa: Final[Unit]

class AccelerationUnits(UnitNamespace):
    meter_per_square_second: Final[Unit]
    foot_per_square_second: Final[Unit]

u: Units
