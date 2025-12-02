"""
Vector class for 2D vectors using Quantity objects for magnitude and angle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import EllipsisType

from ..coordinates import Cartesian, CoordinateSystem
from ..core.quantity import Quantity


@dataclass
class VectorDTO:
    """
    JSON-serializable Vector data transfer object.

    A simple dataclass containing the essential vector data for frontend
    consumption. All values are primitives (float, str) for easy serialization.

    Attributes:
        name: Vector name (e.g., "F_1", "F_R")
        magnitude: Magnitude value in the requested unit
        angle: Angle value in the requested unit
        reference: Reference axis the angle is measured from (e.g., "+x", "-y")
    """

    name: str | None
    magnitude: float
    angle: float
    reference: str


@dataclass
class Vector:
    """
    A 2D vector represented by magnitude and angle.

    Both magnitude and angle are stored as Quantity objects, providing
    dimensional safety and unit conversion capabilities.

    Attributes:
        magnitude: The magnitude of the vector as a Quantity (e.g., Force, Length)
        angle: The angle of the vector as a Quantity (must be angle dimension)
        wrt: The axis the angle is measured from (e.g., "+x", "-y")
        coordinate_system: The coordinate system the vector is defined in
        name: Optional name for the vector
    """

    magnitude: Quantity
    angle: Quantity
    wrt: str = "+x"
    coordinate_system: CoordinateSystem = field(default_factory=Cartesian)
    name: str | None = None

    def __repr__(self) -> str:
        name_str = f"'{self.name}' " if self.name else ""
        return f"Vector({name_str}magnitude={self.magnitude}, angle={self.angle}, wrt='{self.wrt}')"

    def to_dto(
        self,
        magnitude_unit: str = "N",
        angle_unit: str = "degree",
    ) -> VectorDTO:
        """
        Convert this Vector to a JSON-serializable VectorDTO.

        Args:
            magnitude_unit: Target unit for magnitude (e.g., "N", "lbf", "kN")
            angle_unit: Target unit for angle (e.g., "degree", "radian")

        Returns:
            VectorDTO with converted values

        Example:
            >>> vec = Vector(magnitude=Q(100, "N"), angle=Q(60, "degree"), name="F_1")
            >>> dto = vec.to_dto(magnitude_unit="lbf", angle_unit="degree")
            >>> print(dto.magnitude)  # ~22.48 lbf
        """
        # Convert magnitude to requested unit
        mag_converted = self.magnitude.to_unit(magnitude_unit)
        mag_value = mag_converted.magnitude()

        # Convert angle to requested unit
        angle_converted = self.angle.to_unit(angle_unit)
        angle_value = angle_converted.magnitude()

        return VectorDTO(
            name=self.name,
            magnitude=mag_value,
            angle=angle_value,
            reference=self.wrt,
        )


@dataclass
class VectorUnknown:
    """
    A 2D vector with potentially unknown magnitude and/or angle.

    This class is used to represent vectors where one or both of the
    magnitude and angle are unknown (represented by ellipsis ...).
    Used in problem definitions where unknowns need to be solved.

    Attributes:
        magnitude: The magnitude as a Quantity, or ... if unknown
        angle: The angle as a Quantity, or ... if unknown
        wrt: The axis the angle is measured from (e.g., "+x", "-y")
        coordinate_system: The coordinate system the vector is defined in
        name: Optional name for the vector
    """

    magnitude: Quantity | EllipsisType
    angle: Quantity | EllipsisType
    wrt: str = "+x"
    coordinate_system: CoordinateSystem = field(default_factory=Cartesian)
    name: str | None = None

    @property
    def has_unknown_magnitude(self) -> bool:
        """Check if magnitude is unknown."""
        return self.magnitude is ...

    @property
    def has_unknown_angle(self) -> bool:
        """Check if angle is unknown."""
        return self.angle is ...

    @property
    def has_unknowns(self) -> bool:
        """Check if this vector has any unknown values."""
        return self.has_unknown_magnitude or self.has_unknown_angle

    def __repr__(self) -> str:
        name_str = f"'{self.name}' " if self.name else ""
        mag_str = "..." if self.magnitude is ... else str(self.magnitude)
        angle_str = "..." if self.angle is ... else str(self.angle)
        return f"VectorUnknown({name_str}magnitude={mag_str}, angle={angle_str}, wrt='{self.wrt}')"
