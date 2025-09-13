
from . import unit_catalog as uc
from .quantity_meta import quantity


@quantity(uc.AccelerationUnits)
class Acceleration:
    """Acceleration quantity with automatic boilerplate."""
    pass

@quantity(uc.LengthUnits)
class Length:
    """Length quantity with automatic boilerplate."""
    pass

@quantity(uc.DimensionlessUnits)
class Dimensionless:
    """Dimensionless quantity with automatic boilerplate."""
    pass
