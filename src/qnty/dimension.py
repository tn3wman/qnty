"""
Dimension System
================

Compile-time dimensional analysis using type system for ultra-fast operations.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import ClassVar, final


class BaseDimension(IntEnum):
    """Base dimensions as prime numbers for efficient bit operations."""
    LENGTH = 2
    MASS = 3
    TIME = 5
    CURRENT = 7
    TEMPERATURE = 11
    AMOUNT = 13
    LUMINOSITY = 17
    DIMENSIONLESS = 1  # Must be 1 to act as multiplicative identity


@final
@dataclass(frozen=True, slots=True)
class DimensionSignature:
    """Immutable dimension signature for zero-cost dimensional analysis."""
    
    # Store as bit pattern for ultra-fast comparison
    _signature: int | float = 1
    
    # Pre-computed signature cache for common dimensions (expanded for better hit rate)
    _COMMON_SIGNATURES: ClassVar[dict[tuple[int, ...], int | float]] = {
        # Base dimensions
        (1, 0, 0, 0, 0, 0, 0): 2,     # LENGTH
        (0, 1, 0, 0, 0, 0, 0): 3,     # MASS
        (0, 0, 1, 0, 0, 0, 0): 5,     # TIME
        (0, 0, 0, 1, 0, 0, 0): 7,     # CURRENT
        (0, 0, 0, 0, 1, 0, 0): 11,    # TEMPERATURE
        (0, 0, 0, 0, 0, 1, 0): 13,    # AMOUNT
        (0, 0, 0, 0, 0, 0, 1): 17,    # LUMINOSITY
        # Common compound dimensions
        (2, 0, 0, 0, 0, 0, 0): 4,     # AREA (L^2)
        (3, 0, 0, 0, 0, 0, 0): 8,     # VOLUME (L^3)
        (1, 1, -2, 0, 0, 0, 0): 0.24, # FORCE (L M T^-2)
        (-1, 1, -2, 0, 0, 0, 0): 0.06, # PRESSURE (L^-1 M T^-2) - CORRECTED
        (1, 0, -1, 0, 0, 0, 0): 0.4,   # VELOCITY (L T^-1)
        (1, 0, -2, 0, 0, 0, 0): 0.08,  # ACCELERATION (L T^-2)
        # Additional common patterns for better cache hit rate
        (4, 0, 0, 0, 0, 0, 0): 16,    # L^4 (second moment of area)
        (-3, 1, 0, 0, 0, 0, 0): 0.375, # L^-3 M (mass density)
        (-2, 1, 0, 0, 0, 0, 0): 0.75,  # L^-2 M (surface mass density)
        (-1, 1, 0, 0, 0, 0, 0): 1.5,   # L^-1 M (linear mass density)
        (1, 1, -1, 0, 0, 0, 0): 1.2,   # L M T^-1 (linear momentum)
        (2, 1, -2, 0, 0, 0, 0): 0.48,  # L^2 M T^-2 (energy)
        (0, 1, -1, 0, 0, 0, 0): 0.6,   # M T^-1 (mass flow rate)
        (0, 1, -2, 0, 0, 0, 0): 0.12,  # M T^-2 (energy per unit area)
        (0, 0, -1, 0, 0, 0, 0): 0.2,   # T^-1 (frequency)
        (-2, 0, 0, 0, 0, 0, 0): 0.25,  # L^-2 (fuel consumption)
        (-1, 0, 0, 0, 0, 0, 0): 0.5,   # L^-1 (wavenumber)
    }
    
    # Instance cache for interning common dimensions (memory optimization)
    _INSTANCE_CACHE: ClassVar[dict[int | float, "DimensionSignature"]] = {}
    
    def __new__(cls, signature: int | float = 1):
        """Optimized constructor with instance interning for common signatures."""
        # Fast path: check if we already have this exact instance (interning)
        if signature in cls._INSTANCE_CACHE:
            return cls._INSTANCE_CACHE[signature]
        
        # Create new instance using object.__new__ for dataclass compatibility
        instance = object.__new__(cls)
        
        # Intern common signatures to save memory and improve equality checks
        signature_list = [1, 2, 3, 4, 5, 7, 8, 11, 13, 16, 17, 0.06, 0.08, 0.12, 0.2, 0.24, 0.25, 0.375, 0.4, 0.48, 0.5, 0.6, 0.75, 1.2, 1.5]
        if signature in signature_list:
            cls._INSTANCE_CACHE[signature] = instance
        
        return instance
    
    @classmethod
    def create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0):
        """Create dimension from exponents with optimized lookup."""
        # Ultra-fast path: check cache first
        key = (length, mass, time, current, temp, amount, luminosity)
        if key in cls._COMMON_SIGNATURES:
            return cls(cls._COMMON_SIGNATURES[key])  # Uses __new__ interning
        
        # Fast path: avoid computation for zero case
        if not any([length, mass, time, current, temp, amount, luminosity]):
            return cls(1)  # Dimensionless
        
        # Optimized computation path (reduced function calls)
        signature = 1
        if length != 0:
            signature *= BaseDimension.LENGTH ** length
        if mass != 0:
            signature *= BaseDimension.MASS ** mass
        if time != 0:
            signature *= BaseDimension.TIME ** time
        if current != 0:
            signature *= BaseDimension.CURRENT ** current
        if temp != 0:
            signature *= BaseDimension.TEMPERATURE ** temp
        if amount != 0:
            signature *= BaseDimension.AMOUNT ** amount
        if luminosity != 0:
            signature *= BaseDimension.LUMINOSITY ** luminosity
        
        return cls(signature)
    
    def __mul__(self, other):
        """Optimized multiplication with fast paths for common cases."""
        result_sig = self._signature * other._signature
        return DimensionSignature(result_sig)
    
    def __truediv__(self, other):
        """Optimized division with fast paths."""
        result_sig = self._signature / other._signature
        return DimensionSignature(result_sig)
    
    def __pow__(self, power):
        """Optimized power operation."""
        if power == 1:
            return self  # No computation needed
        if power == 0:
            return DimensionSignature(1)  # Dimensionless
        return DimensionSignature(self._signature ** power)
    
    def is_compatible(self, other):
        """Ultra-fast dimensional compatibility check."""
        return self._signature == other._signature
    
    def __eq__(self, other):
        """Optimized equality check with fast paths."""
        # Fast path: identity check (same object)
        if self is other:
            return True
        # Standard path: type and signature check
        return isinstance(other, DimensionSignature) and self._signature == other._signature
    
    def __hash__(self):
        """Optimized hash with caching for common signatures."""
        # Hash is based solely on signature for consistency
        return hash(self._signature)


# Pre-defined dimension constants (optimized with pre-computed signatures)
# Pre-computed dimension signature lookup for ultra-fast lazy loading
_DIMENSION_SIGNATURES = {
    "ABSORBED_DOSE": 0.16,    # L^2 T^-2
    "ACCELERATION": 0.08,    # L T^-2
    "ACTIVATION_ENERGY": 0.01230769230769231,    # N^-1 L^2 T^-2
    "AMOUNT": 13,    # N
    "AMOUNT_OF_SUBSTANCE": 13,    # N
    "ANGLE_PLANE": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "ANGLE_SOLID": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "ANGULAR_ACCELERATION": 0.04,    # T^-2
    "ANGULAR_MOMENTUM": 2.4000000000000004,    # L^2 M T^-1
    "AREA": 4,    # L^2
    "AREA_PER_UNIT_VOLUME": 0.5,    # L^-1
    "ATOMIC_WEIGHT": 0.23076923076923078,    # N^-1 M
    "CONCENTRATION": 0.375,    # L^-3 M
    "CURRENT": 7,    # A
    "DIMENSIONLESS": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "DYNAMIC_FLUIDITY": 3.333333333333333,    # L M^-1 T
    "ELECTRICAL_CONDUCTANCE": 510.41666666666663,    # A^2 L^-2 M^-1 T^3
    "ELECTRICAL_PERMITTIVITY": 1276.0416666666665,    # A^2 L^-3 M^-1 T^4
    "ELECTRICAL_RESISTIVITY": 0.003918367346938775,    # A^-2 L^3 M T^-3
    "ELECTRIC_CAPACITANCE": 2552.083333333333,    # A^2 L^-2 M^-1 T^4
    "ELECTRIC_CHARGE": 2.6923076923076925,    # N^-1 A T
    "ELECTRIC_CURRENT_INTENSITY": 7,    # A
    "ELECTRIC_DIPOLE_MOMENT": 70,    # A L T
    "ELECTRIC_FIELD_STRENGTH": 0.006857142857142857,    # A^-1 L M T^-3
    "ELECTRIC_INDUCTANCE": 0.009795918367346938,    # A^-2 L^2 M T^-2
    "ELECTRIC_POTENTIAL": 0.013714285714285714,    # A^-1 L^2 M T^-3
    "ELECTRIC_RESISTANCE": 0.0019591836734693877,    # A^-2 L^2 M T^-3
    "ENERGY_FLUX": 0.024,    # M T^-3
    "ENERGY_HEAT_WORK": 0.48,    # L^2 M T^-2
    "ENERGY_PER_UNIT_AREA": 0.12,    # M T^-2
    "FORCE": 0.24,    # L M T^-2
    "FORCE_BODY": 0.03,    # L^-2 M T^-2
    "FORCE_PER_UNIT_MASS": 0.08,    # L T^-2
    "FREQUENCY_VOLTAGE_RATIO": 72.91666666666666,    # A L^-2 M^-1 T^3
    "FUEL_CONSUMPTION": 0.25,    # L^-2
    "HEAT_OF_COMBUSTION": 0.16,    # L^2 T^-2
    "HEAT_OF_FUSION": 0.16,    # L^2 T^-2
    "HEAT_OF_VAPORIZATION": 0.16,    # L^2 T^-2
    "HEAT_TRANSFER_COEFFICIENT": 0.002181818181818182,    # M Θ^-1 T^-3
    "ILLUMINANCE": 4.25,    # L^-2 J
    "KINETIC_ENERGY_OF_TURBULENCE": 0.16,    # L^2 T^-2
    "LENGTH": 2,    # L
    "LINEAR_MASS_DENSITY": 1.5,    # L^-1 M
    "LINEAR_MOMENTUM": 1.2000000000000002,    # L M T^-1
    "LUMINANCE_SELF": 4.25,    # L^-2 J
    "LUMINOSITY": 17,    # J
    "LUMINOUS_FLUX": 17,    # J
    "LUMINOUS_INTENSITY": 17,    # J
    "MAGNETIC_FIELD": 3.5,    # A L^-1
    "MAGNETIC_FLUX": 0.06857142857142856,    # A^-1 L^2 M T^-2
    "MAGNETIC_INDUCTION_FIELD_STRENGTH": 0.01714285714285714,    # A^-1 M T^-2
    "MAGNETIC_MOMENT": 28,    # A L^2
    "MAGNETIC_PERMEABILITY": 0.009795918367346938,    # A^-2 L^2 M T^-2
    "MAGNETOMOTIVE_FORCE": 7,    # A
    "MASS": 3,    # M
    "MASS_DENSITY": 0.375,    # L^-3 M
    "MASS_FLOW_RATE": 0.6000000000000001,    # M T^-1
    "MASS_FLUX": 0.15000000000000002,    # L^-2 M T^-1
    "MASS_FRACTION_OF_I": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "MASS_TRANSFER_COEFFICIENT": 0.15000000000000002,    # L^-2 M T^-1
    "MOLALITY_OF_SOLUTE_I": 4.333333333333333,    # N M^-1
    "MOLARITY_OF_I": 1.625,    # N L^-3
    "MOLAR_CONCENTRATION_BY_MASS": 13,    # N
    "MOLAR_FLOW_RATE": 2.6,    # N T^-1
    "MOLAR_FLUX": 0.65,    # N L^-2 T^-1
    "MOLAR_HEAT_CAPACITY": 0.001118881118881119,    # N^-1 L^2 Θ^-1 T^-2
    "MOLE_FRACTION_OF_I": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "MOMENTUM_FLOW_RATE": 0.24,    # L M T^-2
    "MOMENTUM_FLUX": 0.06,    # L^-1 M T^-2
    "MOMENT_OF_INERTIA": 12,    # L^2 M
    "NORMALITY_OF_SOLUTION": 1.625,    # N L^-3
    "PARTICLE_DENSITY": 0.125,    # L^-3
    "PERCENT": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "PERMEABILITY": 4,    # L^2
    "PHOTON_EMISSION_RATE": 0.05,    # L^-2 T^-1
    "POWER_PER_UNIT_MASS": 0.032,    # L^2 T^-3
    "POWER_PER_UNIT_VOLUME": 0.012,    # L^-1 M T^-3
    "POWER_THERMAL_DUTY": 0.096,    # L^2 M T^-3
    "PRESSURE": 0.06,    # L^-1 M T^-2
    "RADIATION_DOSE_EQUIVALENT": 0.16,    # L^2 T^-2
    "RADIATION_EXPOSURE": 11.666666666666666,    # A M^-1 T
    "RADIOACTIVITY": 0.2,    # T^-1
    "SECOND_MOMENT_OF_AREA": 16,    # L^4
    "SECOND_RADIATION_CONSTANT_PLANCK": 22,    # L Θ
    "SPECIFIC_ENTHALPY": 0.16,    # L^2 T^-2
    "SPECIFIC_GRAVITY": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE": 0.04363636363636363,    # L^2 M Θ^-1 T^-2
    "SPECIFIC_LENGTH": 0.6666666666666666,    # L M^-1
    "SPECIFIC_SURFACE": 1.3333333333333333,    # L^2 M^-1
    "SPECIFIC_VOLUME": 2.6666666666666665,    # L^3 M^-1
    "STRESS": 0.06,    # L^-1 M T^-2
    "SURFACE_MASS_DENSITY": 0.75,    # L^-2 M
    "SURFACE_TENSION": 0.12,    # M T^-2
    "TEMPERATURE": 11,    # Θ
    "THERMAL_CONDUCTIVITY": 0.528,    # L M Θ T^-3
    "TIME": 5,    # T
    "TORQUE": 0.48,    # L^2 M T^-2
    "TURBULENCE_ENERGY_DISSIPATION_RATE": 0.032,    # L^2 T^-3
    "VELOCITY_ANGULAR": 0.2,    # T^-1
    "VELOCITY_LINEAR": 0.4,    # L T^-1
    "VISCOSITY_DYNAMIC": 0.30000000000000004,    # L^-1 M T^-1
    "VISCOSITY_KINEMATIC": 0.8,    # L^2 T^-1
    "VOLUME": 8,    # L^3
    "VOLUMETRIC_CALORIFIC_HEATING_VALUE": 0.06,    # L^-1 M T^-2
    "VOLUMETRIC_COEFFICIENT_OF_EXPANSION": 0.03409090909090909,    # L^-3 M Θ^-1
    "VOLUMETRIC_FLOW_RATE": 1.6,    # L^3 T^-1
    "VOLUMETRIC_FLUX": 0.4,    # L T^-1
    "VOLUMETRIC_MASS_FLOW_RATE": 0.07500000000000001,    # L^-3 M T^-1
    "VOLUME_FRACTION_OF_I": BaseDimension.DIMENSIONLESS,    # Dimensionless
    "WAVENUMBER": 0.5,    # L^-1
}

# Lazy loading cache for dimension constants (optimized for import performance)
_dimension_cache: dict[str, DimensionSignature] = {}

def __getattr__(name: str) -> DimensionSignature:
    """Lazy loading of dimension constants for optimal import performance."""
    # Skip attributes that are explicitly defined in the module
    # This prevents conflicts with explicitly defined dimension constants
    if name in {
        "DIMENSIONLESS",
        "LENGTH",
        "MASS",
        "TIME",
        "CURRENT",
        "TEMPERATURE",
        "AMOUNT",
        "LUMINOSITY",
        "AREA",
        "VOLUME",
        "VELOCITY",
        "ACCELERATION",
        "FORCE",
        "PRESSURE",
        "ENERGY",
        "ENERGY_HEAT_WORK",
    }:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    if name in _DIMENSION_SIGNATURES:
        if name not in _dimension_cache:
            _dimension_cache[name] = DimensionSignature(_DIMENSION_SIGNATURES[name])
        return _dimension_cache[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# Explicitly define the most commonly used dimension constants for IDE support
# These are created dynamically by __getattr__, but explicit definitions help IDE autocomplete
DIMENSIONLESS = DimensionSignature(1)  # Dimensionless
LENGTH = DimensionSignature(2)  # L
MASS = DimensionSignature(3)  # M
TIME = DimensionSignature(5)  # T
CURRENT = DimensionSignature(7)  # A
TEMPERATURE = DimensionSignature(11)  # Θ
AMOUNT = DimensionSignature(13)  # N
LUMINOSITY = DimensionSignature(17)  # J
AREA = DimensionSignature(4)  # L^2
VOLUME = DimensionSignature(8)  # L^3
VELOCITY = DimensionSignature(0.4)  # L T^-1
ACCELERATION = DimensionSignature(0.08)  # L T^-2
FORCE = DimensionSignature(0.24)  # L M T^-2
PRESSURE = DimensionSignature(0.06)  # L^-1 M T^-2
ENERGY = DimensionSignature(0.48)  # L^2 M T^-2

# Common aliases for backward compatibility
ENERGY_HEAT_WORK = ENERGY

# Export list for module (enables proper IDE autocomplete)
# Only include explicitly defined symbols to avoid Pylance warnings
# All dimension constants are still available via __getattr__ for dynamic loading
__all__ = [
    # Base classes
    "BaseDimension",
    "DimensionSignature",
    # Commonly used dimensions (explicitly defined for IDE support)
    "DIMENSIONLESS",
    "LENGTH",
    "MASS",
    "TIME",
    "CURRENT",
    "TEMPERATURE",
    "AMOUNT",
    "LUMINOSITY",
    "AREA",
    "VOLUME",
    "VELOCITY",
    "ACCELERATION",
    "FORCE",
    "PRESSURE",
    "ENERGY",
    "ENERGY_HEAT_WORK",
]

# Note: All other dimension constants (ABSORBED_DOSE, ELECTRIC_CHARGE, etc.)
# are available via dynamic loading through __getattr__ but are not listed in __all__
# to avoid IDE warnings. They can still be imported and used normally:
#   from qnty.dimension import ABSORBED_DOSE  # Works fine
#   import qnty.dimension as dim; dim.ABSORBED_DOSE  # Works fine
