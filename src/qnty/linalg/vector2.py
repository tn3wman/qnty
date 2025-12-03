"""
Vector class for 2D vectors using Quantity objects for magnitude and angle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import EllipsisType

from ..coordinates import Cartesian, CoordinateSystem
from ..core.quantity import Quantity
from ..equations.angle_finder import angles_are_equivalent, get_absolute_angle


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
        _is_resultant: Internal flag indicating if this is a resultant vector
    """

    magnitude: Quantity
    angle: Quantity
    wrt: str = "+x"
    coordinate_system: CoordinateSystem = field(default_factory=Cartesian)
    name: str | None = None
    _is_resultant: bool = field(default=False, repr=False)

    @property
    def is_resultant(self) -> bool:
        """Check if this vector is a resultant of other vectors."""
        return self._is_resultant

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

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on magnitude and absolute angle.

        Two vectors are equal if they have the same magnitude and point
        in the same direction, regardless of how the angle is represented.
        """
        if not isinstance(other, Vector):
            return NotImplemented

        return self.magnitude == other.magnitude and get_absolute_angle(self) == get_absolute_angle(other)

    def is_close(self, other: Vector, rtol: float = 0.01) -> bool:
        """
        Check if this vector is close to another within tolerance.

        Handles angle equivalence properly - angles that differ by 360° are
        considered equal (e.g., 352.9° and -7.1° are equivalent).

        Args:
            other: Vector to compare against
            rtol: Relative tolerance (default 1%)

        Returns:
            True if vectors are close within tolerances
        """
        if not isinstance(other, Vector):
            return False

        return (
            self.magnitude.is_close(other.magnitude, rtol=rtol)
            and angles_are_equivalent(get_absolute_angle(self), get_absolute_angle(other), rtol=rtol)
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
        _is_resultant: Internal flag indicating if this is a resultant vector
    """

    magnitude: Quantity | EllipsisType
    angle: Quantity | EllipsisType
    wrt: str = "+x"
    coordinate_system: CoordinateSystem = field(default_factory=Cartesian)
    name: str | None = None
    _is_resultant: bool = field(default=False, repr=False)

    @property
    def is_resultant(self) -> bool:
        """Check if this vector is a resultant of other vectors."""
        return self._is_resultant

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

    def to_dto(
        self,
        magnitude_unit: str = "N",
        angle_unit: str = "degree",
    ) -> VectorDTO:
        """
        Convert this VectorUnknown to a JSON-serializable VectorDTO.

        If magnitude or angle are unknown (ellipsis), they will be converted
        to float('nan') in the DTO.

        Args:
            magnitude_unit: Target unit for magnitude (e.g., "N", "lbf", "kN")
            angle_unit: Target unit for angle (e.g., "degree", "radian")

        Returns:
            VectorDTO with converted values (NaN for unknowns)

        Raises:
            ValueError: If trying to convert an unsolved VectorUnknown
        """
        if self.magnitude is ... or self.angle is ...:
            raise ValueError("Cannot convert VectorUnknown with unknown values to DTO. Solve the problem first.")

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
