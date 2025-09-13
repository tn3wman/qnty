from typing import Final

from .dimension import Dimension

class Dimensions:
    ABSORBED_RADIATION_DOSE: Final[Dimension]
    ACCELERATION: Final[Dimension]
    MASS_DENSITY: Final[Dimension]
    VISCOSITY_DYNAMIC: Final[Dimension]
    VISCOSITY_KINEMATIC: Final[Dimension]
    
    Area: Final[Dimension]
    D: Final[Dimension]
    Energy: Final[Dimension]
    Force: Final[Dimension]
    A: Final[Dimension]
    J: Final[Dimension]
    L: Final[Dimension]
    M: Final[Dimension]
    N: Final[Dimension]
    Power: Final[Dimension]
    Pressure: Final[Dimension]
    T: Final[Dimension]
    Volume: Final[Dimension]
    Θ: Final[Dimension]
    AMOUNT: Final[Dimension]  # alias for N
    AREA: Final[Dimension]  # alias for Area
    AbsorbedRadiationDose: Final[Dimension]  # alias for ABSORBED_RADIATION_DOSE
    Acceleration: Final[Dimension]  # alias for ACCELERATION
    CURRENT: Final[Dimension]  # alias for I
    DIMENSIONLESS: Final[Dimension]  # alias for D
    DLESS: Final[Dimension]  # alias for D
    ENERGY: Final[Dimension]  # alias for Energy
    FORCE: Final[Dimension]  # alias for Force
    LENGTH: Final[Dimension]  # alias for L
    LUMINOUS_INTENSITY: Final[Dimension]  # alias for J
    MASS: Final[Dimension]  # alias for M
    POWER: Final[Dimension]  # alias for Power
    PRESSURE: Final[Dimension]  # alias for Pressure
    SCALAR: Final[Dimension]  # alias for D
    TEMPERATURE: Final[Dimension]  # alias for Θ
    TIME: Final[Dimension]  # alias for T
    VOLUME: Final[Dimension]  # alias for Volume

dim: Final[Dimensions]
