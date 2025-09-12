from typing import Final

from . import u
from .core import Unit, UnitNamespace, attach_composed

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
