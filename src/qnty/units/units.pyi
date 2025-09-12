from typing import Final

from .core import Unit

class Units:
    dimensionless: Final[Unit]
    gram: Final[Unit]
    meter: Final[Unit]
    second: Final[Unit]
    centi_gram: Final[Unit]  # alias for gram
    centi_meter: Final[Unit]  # alias for meter
    centi_second: Final[Unit]  # alias for second
    cg: Final[Unit]  # alias for gram
    cm: Final[Unit]  # alias for meter
    cs: Final[Unit]  # alias for second
    dag: Final[Unit]  # alias for gram
    dam: Final[Unit]  # alias for meter
    das: Final[Unit]  # alias for second
    deca_gram: Final[Unit]  # alias for gram
    deca_meter: Final[Unit]  # alias for meter
    deca_second: Final[Unit]  # alias for second
    deci_gram: Final[Unit]  # alias for gram
    deci_meter: Final[Unit]  # alias for meter
    deci_second: Final[Unit]  # alias for second
    dg: Final[Unit]  # alias for gram
    dless: Final[Unit]  # alias for dimensionless
    dm: Final[Unit]  # alias for meter
    ds: Final[Unit]  # alias for second
    grams: Final[Unit]  # alias for gram
    hecto_gram: Final[Unit]  # alias for gram
    hecto_meter: Final[Unit]  # alias for meter
    hecto_second: Final[Unit]  # alias for second
    hg: Final[Unit]  # alias for gram
    hm: Final[Unit]  # alias for meter
    hs: Final[Unit]  # alias for second
    kg: Final[Unit]  # alias for gram
    kilo_gram: Final[Unit]  # alias for gram
    kilo_meter: Final[Unit]  # alias for meter
    kilo_second: Final[Unit]  # alias for second
    km: Final[Unit]  # alias for meter
    ks: Final[Unit]  # alias for second
    meters: Final[Unit]  # alias for meter
    metre: Final[Unit]  # alias for meter
    metres: Final[Unit]  # alias for meter
    mg: Final[Unit]  # alias for gram
    micro_gram: Final[Unit]  # alias for gram
    micro_meter: Final[Unit]  # alias for meter
    micro_second: Final[Unit]  # alias for second
    milli_gram: Final[Unit]  # alias for gram
    milli_meter: Final[Unit]  # alias for meter
    milli_second: Final[Unit]  # alias for second
    mm: Final[Unit]  # alias for meter
    ms: Final[Unit]  # alias for second
    nano_gram: Final[Unit]  # alias for gram
    nano_meter: Final[Unit]  # alias for meter
    nano_second: Final[Unit]  # alias for second
    ng: Final[Unit]  # alias for gram
    nm: Final[Unit]  # alias for meter
    ns: Final[Unit]  # alias for second
    scalar: Final[Unit]  # alias for dimensionless
    seconds: Final[Unit]  # alias for second
    ug: Final[Unit]  # alias for gram
    um: Final[Unit]  # alias for meter
    us: Final[Unit]  # alias for second
    μg: Final[Unit]  # alias for gram
    μm: Final[Unit]  # alias for meter
    μs: Final[Unit]  # alias for second

u: Final[Units]
