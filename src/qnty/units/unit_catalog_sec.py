from . import u
from .core import Final, Unit, UnitNamespace, attach_composed

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



