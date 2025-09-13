
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


@quantity(uc.MassDensityUnits)
class MassDensity:
    """Mass density quantity with automatic boilerplate."""
    pass

@quantity(uc.ViscosityDynamicUnits)
class ViscosityDynamic:
    """Dynamic viscosity quantity with automatic boilerplate."""
    pass

@quantity(uc.ViscosityKinematicUnits)
class ViscosityKinematic:
    """Kinematic viscosity quantity with automatic boilerplate."""
    pass

