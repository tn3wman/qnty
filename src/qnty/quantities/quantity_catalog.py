from typing import cast, overload

from ..units import AccelerationUnits  # example namespace for Acceleration
from ..units.core import Unit
from .core import FieldQuantity, FieldSetter, UnitApplier, UnitChanger, _get_namespace_dim, bind_quantity_namespace


class AccelerationSetter(FieldSetter["Acceleration"]):
    __slots__ = ()


class Acceleration(FieldQuantity["Acceleration"]):
    __slots__ = ()
    # Bind to its unit namespace for generic helpers
    UNIT_NS = AccelerationUnits
    SETTER_CLS = AccelerationSetter

    # typed unit applier: expose known units as properties
    class ToUnit(UnitApplier["Acceleration"]):
        __slots__ = ()

    class AsUnit(UnitChanger["Acceleration"]):
        __slots__ = ()

    @property
    def to_unit(self) -> "Acceleration.ToUnit":
        accel_dim = _get_namespace_dim(self.UNIT_NS)
        return Acceleration.ToUnit(self, accel_dim)

    @property
    def as_unit(self) -> "Acceleration.AsUnit":
        accel_dim = _get_namespace_dim(self.UNIT_NS)
        return Acceleration.AsUnit(self, accel_dim)
    @overload
    def set(self, value: float) -> AccelerationSetter: ...
    @overload
    def set(self, value: float, unit: Unit["Acceleration"]) -> "Acceleration": ...
    @overload
    def set(self, value: float, unit: str) -> "Acceleration": ...

    def set(
        self,
    value: float,
    unit: Unit["Acceleration"] | str | None = None,
    ) -> "Acceleration | AccelerationSetter":
        # Match the correct overload: if unit is None, call the 1-arg overload; otherwise forward to base
        if unit is None:
            # dimension-aware setter using namespace dim
            return cast("Acceleration | AccelerationSetter", AccelerationSetter(self, value, _get_namespace_dim(self.UNIT_NS)))
        return cast("Acceleration | AccelerationSetter", super().set(value, unit))

bind_quantity_namespace(Acceleration, AccelerationSetter, Acceleration.UNIT_NS)
