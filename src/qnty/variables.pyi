"""
Type stubs for consolidated variables module - Complete Edition.

Provides complete type hints for IDE autocomplete and type checking
for the fluent API with dimension-specific unit properties for all
107 variable types with 871 total units.

Auto-generated from the same source of truth as consolidated_new.py.
"""

from typing import Any

from .unit_system.dimension import DimensionSignature
from .variable_system.core import TypeSafeSetter
from .variable_system.typed_variable import TypedVariable

# ============================================================================
# ABSORBED RADIATION DOSE
# ============================================================================

class AbsorbedDoseSetter(TypeSafeSetter):
    """Absorbed Radiation Dose-specific setter with only absorbed radiation dose unit properties."""
    
    def __init__(self, variable: AbsorbedDose, value: float) -> None: ...
    
    # All absorbed radiation dose unit properties - provides fluent API with full type hints
    @property
    def erg_per_gram(self) -> AbsorbedDose: ...
    @property
    def erg_per_g(self) -> AbsorbedDose: ...
    @property
    def gram_rad(self) -> AbsorbedDose: ...
    @property
    def g_rad(self) -> AbsorbedDose: ...
    @property
    def gray(self) -> AbsorbedDose: ...
    @property
    def Gy(self) -> AbsorbedDose: ...
    @property
    def rad(self) -> AbsorbedDose: ...
    @property
    def milligray(self) -> AbsorbedDose: ...
    @property
    def mGy(self) -> AbsorbedDose: ...
    @property
    def microgray(self) -> AbsorbedDose: ...

class AbsorbedDose(TypedVariable):
    """Type-safe absorbed radiation dose variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AbsorbedDoseSetter:
        """
        Create a absorbed radiation dose setter for fluent unit assignment.
        
        Example:
            absorbeddose.set(100).erg_per_gram
            absorbeddose.set(100).gram_rad
            absorbeddose.set(100).gray
        """
        ...

# ============================================================================
# ACCELERATION
# ============================================================================

class AccelerationSetter(TypeSafeSetter):
    """Acceleration-specific setter with only acceleration unit properties."""
    
    def __init__(self, variable: Acceleration, value: float) -> None: ...
    
    # All acceleration unit properties - provides fluent API with full type hints
    @property
    def meter_per_second_squared(self) -> Acceleration: ...
    @property
    def m_per_s2(self) -> Acceleration: ...
    @property
    def foot_per_second_squared(self) -> Acceleration: ...
    @property
    def ft_per_s2(self) -> Acceleration: ...
    @property
    def fps2(self) -> Acceleration: ...

class Acceleration(TypedVariable):
    """Type-safe acceleration variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AccelerationSetter:
        """
        Create a acceleration setter for fluent unit assignment.
        
        Example:
            acceleration.set(100).meter_per_second_squared
            acceleration.set(100).foot_per_second_squared
        """
        ...

# ============================================================================
# ACTIVATION ENERGY
# ============================================================================

class ActivationEnergySetter(TypeSafeSetter):
    """Activation Energy-specific setter with only activation energy unit properties."""
    
    def __init__(self, variable: ActivationEnergy, value: float) -> None: ...
    
    # All activation energy unit properties - provides fluent API with full type hints
    @property
    def Btu_per_pound_mole(self) -> ActivationEnergy: ...
    @property
    def btu_per_lbmol(self) -> ActivationEnergy: ...
    @property
    def calorie_mean_per_gram_mole(self) -> ActivationEnergy: ...
    @property
    def cal_mean_per_gmol(self) -> ActivationEnergy: ...
    @property
    def joule_per_gram_mole(self) -> ActivationEnergy: ...
    @property
    def joule_per_kilogram_mole(self) -> ActivationEnergy: ...
    @property
    def kilocalorie_per_kilogram_mole(self) -> ActivationEnergy: ...

class ActivationEnergy(TypedVariable):
    """Type-safe activation energy variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ActivationEnergySetter:
        """
        Create a activation energy setter for fluent unit assignment.
        
        Example:
            activationenergy.set(100).Btu_per_pound_mole
            activationenergy.set(100).calorie_mean_per_gram_mole
            activationenergy.set(100).joule_per_gram_mole
        """
        ...

# ============================================================================
# AMOUNT OF SUBSTANCE
# ============================================================================

class AmountOfSubstanceSetter(TypeSafeSetter):
    """Amount of Substance-specific setter with only amount of substance unit properties."""
    
    def __init__(self, variable: AmountOfSubstance, value: float) -> None: ...
    
    # All amount of substance unit properties - provides fluent API with full type hints
    @property
    def kilogram_mol_or_kmol(self) -> AmountOfSubstance: ...
    @property
    def kmol(self) -> AmountOfSubstance: ...
    @property
    def mole_gram(self) -> AmountOfSubstance: ...
    @property
    def mol(self) -> AmountOfSubstance: ...
    @property
    def pound_mole(self) -> AmountOfSubstance: ...
    @property
    def lb_mol(self) -> AmountOfSubstance: ...
    @property
    def mole(self) -> AmountOfSubstance: ...
    @property
    def millimole_gram(self) -> AmountOfSubstance: ...
    @property
    def mmol(self) -> AmountOfSubstance: ...
    @property
    def micromole_gram(self) -> AmountOfSubstance: ...

class AmountOfSubstance(TypedVariable):
    """Type-safe amount of substance variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AmountOfSubstanceSetter:
        """
        Create a amount of substance setter for fluent unit assignment.
        
        Example:
            amountofsubstance.set(100).kilogram_mol_or_kmol
            amountofsubstance.set(100).mole_gram
            amountofsubstance.set(100).pound_mole
        """
        ...

# ============================================================================
# ANGLE, PLANE
# ============================================================================

class AnglePlaneSetter(TypeSafeSetter):
    """Angle, Plane-specific setter with only angle, plane unit properties."""
    
    def __init__(self, variable: AnglePlane, value: float) -> None: ...
    
    # All angle, plane unit properties - provides fluent API with full type hints
    @property
    def degree(self) -> AnglePlane: ...
    @property
    def gon(self) -> AnglePlane: ...
    @property
    def grade(self) -> AnglePlane: ...
    @property
    def minute_new(self) -> AnglePlane: ...
    @property
    def c(self) -> AnglePlane: ...
    @property
    def minute_of_angle(self) -> AnglePlane: ...
    @property
    def percent(self) -> AnglePlane: ...
    @property
    def plane_angle(self) -> AnglePlane: ...
    @property
    def quadrant(self) -> AnglePlane: ...
    @property
    def radian(self) -> AnglePlane: ...
    @property
    def rad(self) -> AnglePlane: ...
    @property
    def right_angle(self) -> AnglePlane: ...
    @property
    def perp(self) -> AnglePlane: ...
    @property
    def round(self) -> AnglePlane: ...
    @property
    def tr(self) -> AnglePlane: ...
    @property
    def r(self) -> AnglePlane: ...
    @property
    def second_new(self) -> AnglePlane: ...
    @property
    def cc(self) -> AnglePlane: ...
    @property
    def second_of_angle(self) -> AnglePlane: ...
    @property
    def thousandth_US(self) -> AnglePlane: ...
    @property
    def turn(self) -> AnglePlane: ...
    @property
    def rev(self) -> AnglePlane: ...

class AnglePlane(TypedVariable):
    """Type-safe angle, plane variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AnglePlaneSetter:
        """
        Create a angle, plane setter for fluent unit assignment.
        
        Example:
            angleplane.set(100).degree
            angleplane.set(100).gon
            angleplane.set(100).grade
        """
        ...

# ============================================================================
# ANGLE, SOLID
# ============================================================================

class AngleSolidSetter(TypeSafeSetter):
    """Angle, Solid-specific setter with only angle, solid unit properties."""
    
    def __init__(self, variable: AngleSolid, value: float) -> None: ...
    
    # All angle, solid unit properties - provides fluent API with full type hints
    @property
    def spat(self) -> AngleSolid: ...
    @property
    def square_degree(self) -> AngleSolid: ...
    @property
    def square_gon(self) -> AngleSolid: ...
    @property
    def steradian(self) -> AngleSolid: ...
    @property
    def sr(self) -> AngleSolid: ...

class AngleSolid(TypedVariable):
    """Type-safe angle, solid variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AngleSolidSetter:
        """
        Create a angle, solid setter for fluent unit assignment.
        
        Example:
            anglesolid.set(100).spat
            anglesolid.set(100).square_degree
            anglesolid.set(100).square_gon
        """
        ...

# ============================================================================
# ANGULAR ACCELERATION
# ============================================================================

class AngularAccelerationSetter(TypeSafeSetter):
    """Angular Acceleration-specific setter with only angular acceleration unit properties."""
    
    def __init__(self, variable: AngularAcceleration, value: float) -> None: ...
    
    # All angular acceleration unit properties - provides fluent API with full type hints
    @property
    def radian_per_second_squared(self) -> AngularAcceleration: ...
    @property
    def revolution_per_second_squared(self) -> AngularAcceleration: ...
    @property
    def rpm_or_revolution_per_minute_per_minute(self) -> AngularAcceleration: ...
    @property
    def rev_min_2(self) -> AngularAcceleration: ...
    @property
    def rpm_min(self) -> AngularAcceleration: ...

class AngularAcceleration(TypedVariable):
    """Type-safe angular acceleration variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AngularAccelerationSetter:
        """
        Create a angular acceleration setter for fluent unit assignment.
        
        Example:
            angularacceleration.set(100).radian_per_second_squared
            angularacceleration.set(100).revolution_per_second_squared
            angularacceleration.set(100).rpm_or_revolution_per_minute_per_minute
        """
        ...

# ============================================================================
# ANGULAR MOMENTUM
# ============================================================================

class AngularMomentumSetter(TypeSafeSetter):
    """Angular Momentum-specific setter with only angular momentum unit properties."""
    
    def __init__(self, variable: AngularMomentum, value: float) -> None: ...
    
    # All angular momentum unit properties - provides fluent API with full type hints
    @property
    def gram_centimeter_squared_per_second(self) -> AngularMomentum: ...
    @property
    def kilogram_meter_squared_per_second(self) -> AngularMomentum: ...
    @property
    def pound_force_square_foot_per_second(self) -> AngularMomentum: ...

class AngularMomentum(TypedVariable):
    """Type-safe angular momentum variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AngularMomentumSetter:
        """
        Create a angular momentum setter for fluent unit assignment.
        
        Example:
            angularmomentum.set(100).gram_centimeter_squared_per_second
            angularmomentum.set(100).kilogram_meter_squared_per_second
            angularmomentum.set(100).pound_force_square_foot_per_second
        """
        ...

# ============================================================================
# AREA
# ============================================================================

class AreaSetter(TypeSafeSetter):
    """Area-specific setter with only area unit properties."""
    
    def __init__(self, variable: Area, value: float) -> None: ...
    
    # All area unit properties - provides fluent API with full type hints
    @property
    def acre_general(self) -> Area: ...
    @property
    def ac(self) -> Area: ...
    @property
    def are(self) -> Area: ...
    @property
    def a(self) -> Area: ...
    @property
    def arpent_Quebec(self) -> Area: ...
    @property
    def arp(self) -> Area: ...
    @property
    def barn(self) -> Area: ...
    @property
    def b(self) -> Area: ...
    @property
    def circular_inch(self) -> Area: ...
    @property
    def cin(self) -> Area: ...
    @property
    def circular_mil(self) -> Area: ...
    @property
    def cmil(self) -> Area: ...
    @property
    def hectare(self) -> Area: ...
    @property
    def ha(self) -> Area: ...
    @property
    def shed(self) -> Area: ...
    @property
    def square_centimeter(self) -> Area: ...
    @property
    def square_chain_Ramsden(self) -> Area: ...
    @property
    def square_chain_Survey_Gunter_s(self) -> Area: ...
    @property
    def square_decimeter(self) -> Area: ...
    @property
    def square_fermi(self) -> Area: ...
    @property
    def square_foot(self) -> Area: ...
    @property
    def sq_ft(self) -> Area: ...
    @property
    def ft_2(self) -> Area: ...
    @property
    def square_hectometer(self) -> Area: ...
    @property
    def square_inch(self) -> Area: ...
    @property
    def sq_in(self) -> Area: ...
    @property
    def in_2(self) -> Area: ...
    @property
    def square_kilometer(self) -> Area: ...
    @property
    def square_league_statute(self) -> Area: ...
    @property
    def square_meter(self) -> Area: ...
    @property
    def square_micron(self) -> Area: ...
    @property
    def mu_m_2(self) -> Area: ...
    @property
    def mu_2(self) -> Area: ...
    @property
    def square_mile_statute(self) -> Area: ...
    @property
    def square_mile_US_survey(self) -> Area: ...
    @property
    def square_millimeter(self) -> Area: ...
    @property
    def square_nanometer(self) -> Area: ...
    @property
    def square_yard(self) -> Area: ...
    @property
    def township_US(self) -> Area: ...

class Area(TypedVariable):
    """Type-safe area variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AreaSetter:
        """
        Create a area setter for fluent unit assignment.
        
        Example:
            area.set(100).acre_general
            area.set(100).are
            area.set(100).arpent_Quebec
        """
        ...

# ============================================================================
# AREA PER UNIT VOLUME
# ============================================================================

class AreaPerUnitVolumeSetter(TypeSafeSetter):
    """Area per Unit Volume-specific setter with only area per unit volume unit properties."""
    
    def __init__(self, variable: AreaPerUnitVolume, value: float) -> None: ...
    
    # All area per unit volume unit properties - provides fluent API with full type hints
    @property
    def square_centimeter_per_cubic_centimeter(self) -> AreaPerUnitVolume: ...
    @property
    def square_foot_per_cubic_foot(self) -> AreaPerUnitVolume: ...
    @property
    def ft_2_ft_3(self) -> AreaPerUnitVolume: ...
    @property
    def sqft_cft(self) -> AreaPerUnitVolume: ...
    @property
    def square_inch_per_cubic_inch(self) -> AreaPerUnitVolume: ...
    @property
    def in_2_in_3(self) -> AreaPerUnitVolume: ...
    @property
    def sq_in_cu_in(self) -> AreaPerUnitVolume: ...
    @property
    def square_meter_per_cubic_meter(self) -> AreaPerUnitVolume: ...
    @property
    def m_2_m_3(self) -> AreaPerUnitVolume: ...
    @property
    def _1_m_3(self) -> AreaPerUnitVolume: ...

class AreaPerUnitVolume(TypedVariable):
    """Type-safe area per unit volume variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AreaPerUnitVolumeSetter:
        """
        Create a area per unit volume setter for fluent unit assignment.
        
        Example:
            areaperunitvolume.set(100).square_centimeter_per_cubic_centimeter
            areaperunitvolume.set(100).square_foot_per_cubic_foot
            areaperunitvolume.set(100).square_inch_per_cubic_inch
        """
        ...

# ============================================================================
# ATOMIC WEIGHT
# ============================================================================

class AtomicWeightSetter(TypeSafeSetter):
    """Atomic Weight-specific setter with only atomic weight unit properties."""
    
    def __init__(self, variable: AtomicWeight, value: float) -> None: ...
    
    # All atomic weight unit properties - provides fluent API with full type hints
    @property
    def atomic_mass_unit_12C(self) -> AtomicWeight: ...
    @property
    def amu(self) -> AtomicWeight: ...
    @property
    def grams_per_mole(self) -> AtomicWeight: ...
    @property
    def kilograms_per_kilomole(self) -> AtomicWeight: ...
    @property
    def pounds_per_pound_mole(self) -> AtomicWeight: ...
    @property
    def lb_lb_mol(self) -> AtomicWeight: ...
    @property
    def lb_mole(self) -> AtomicWeight: ...

class AtomicWeight(TypedVariable):
    """Type-safe atomic weight variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AtomicWeightSetter:
        """
        Create a atomic weight setter for fluent unit assignment.
        
        Example:
            atomicweight.set(100).atomic_mass_unit_12C
            atomicweight.set(100).grams_per_mole
            atomicweight.set(100).kilograms_per_kilomole
        """
        ...

# ============================================================================
# CONCENTRATION
# ============================================================================

class ConcentrationSetter(TypeSafeSetter):
    """Concentration-specific setter with only concentration unit properties."""
    
    def __init__(self, variable: Concentration, value: float) -> None: ...
    
    # All concentration unit properties - provides fluent API with full type hints
    @property
    def grains_of_i_per_cubic_foot(self) -> Concentration: ...
    @property
    def gr_ft_3(self) -> Concentration: ...
    @property
    def gr_cft(self) -> Concentration: ...
    @property
    def grains_of_i_per_gallon_US(self) -> Concentration: ...

class Concentration(TypedVariable):
    """Type-safe concentration variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ConcentrationSetter:
        """
        Create a concentration setter for fluent unit assignment.
        
        Example:
            concentration.set(100).grains_of_i_per_cubic_foot
            concentration.set(100).grains_of_i_per_gallon_US
        """
        ...

# ============================================================================
# DIMENSIONLESS
# ============================================================================

class DimensionlessSetter(TypeSafeSetter):
    """Dimensionless-specific setter with only dimensionless unit properties."""
    
    def __init__(self, variable: Dimensionless, value: float) -> None: ...
    
    # All dimensionless unit properties - provides fluent API with full type hints
    @property
    def dimensionless(self) -> Dimensionless: ...
    @property
    def ratio(self) -> Dimensionless: ...
    @property
    def parts_per_million(self) -> Dimensionless: ...
    @property
    def ppm(self) -> Dimensionless: ...
    @property
    def parts_per_billion(self) -> Dimensionless: ...
    @property
    def ppb(self) -> Dimensionless: ...

class Dimensionless(TypedVariable):
    """Type-safe dimensionless variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> DimensionlessSetter:
        """
        Create a dimensionless setter for fluent unit assignment.
        
        Example:
            dimensionless.set(100).dimensionless
            dimensionless.set(100).ratio
            dimensionless.set(100).parts_per_million
        """
        ...

# ============================================================================
# DYNAMIC FLUIDITY
# ============================================================================

class DynamicFluiditySetter(TypeSafeSetter):
    """Dynamic Fluidity-specific setter with only dynamic fluidity unit properties."""
    
    def __init__(self, variable: DynamicFluidity, value: float) -> None: ...
    
    # All dynamic fluidity unit properties - provides fluent API with full type hints
    @property
    def meter_seconds_per_kilogram(self) -> DynamicFluidity: ...
    @property
    def rhe(self) -> DynamicFluidity: ...
    @property
    def square_foot_per_pound_second(self) -> DynamicFluidity: ...
    @property
    def square_meters_per_newton_per_second(self) -> DynamicFluidity: ...

class DynamicFluidity(TypedVariable):
    """Type-safe dynamic fluidity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> DynamicFluiditySetter:
        """
        Create a dynamic fluidity setter for fluent unit assignment.
        
        Example:
            dynamicfluidity.set(100).meter_seconds_per_kilogram
            dynamicfluidity.set(100).rhe
            dynamicfluidity.set(100).square_foot_per_pound_second
        """
        ...

# ============================================================================
# ELECTRIC CAPACITANCE
# ============================================================================

class ElectricCapacitanceSetter(TypeSafeSetter):
    """Electric Capacitance-specific setter with only electric capacitance unit properties."""
    
    def __init__(self, variable: ElectricCapacitance, value: float) -> None: ...
    
    # All electric capacitance unit properties - provides fluent API with full type hints
    @property
    def cm(self) -> ElectricCapacitance: ...
    @property
    def abfarad(self) -> ElectricCapacitance: ...
    @property
    def farad(self) -> ElectricCapacitance: ...
    @property
    def F(self) -> ElectricCapacitance: ...
    @property
    def farad_intl(self) -> ElectricCapacitance: ...
    @property
    def jar(self) -> ElectricCapacitance: ...
    @property
    def puff(self) -> ElectricCapacitance: ...
    @property
    def statfarad(self) -> ElectricCapacitance: ...
    @property
    def millifarad(self) -> ElectricCapacitance: ...
    @property
    def mF(self) -> ElectricCapacitance: ...
    @property
    def microfarad(self) -> ElectricCapacitance: ...
    @property
    def nanofarad(self) -> ElectricCapacitance: ...
    @property
    def nF(self) -> ElectricCapacitance: ...
    @property
    def picofarad(self) -> ElectricCapacitance: ...
    @property
    def pF(self) -> ElectricCapacitance: ...

class ElectricCapacitance(TypedVariable):
    """Type-safe electric capacitance variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricCapacitanceSetter:
        """
        Create a electric capacitance setter for fluent unit assignment.
        
        Example:
            electriccapacitance.set(100).cm
            electriccapacitance.set(100).abfarad
            electriccapacitance.set(100).farad
        """
        ...

# ============================================================================
# ELECTRIC CHARGE
# ============================================================================

class ElectricChargeSetter(TypeSafeSetter):
    """Electric Charge-specific setter with only electric charge unit properties."""
    
    def __init__(self, variable: ElectricCharge, value: float) -> None: ...
    
    # All electric charge unit properties - provides fluent API with full type hints
    @property
    def abcoulomb(self) -> ElectricCharge: ...
    @property
    def ampere_hour(self) -> ElectricCharge: ...
    @property
    def Ah(self) -> ElectricCharge: ...
    @property
    def coulomb(self) -> ElectricCharge: ...
    @property
    def C(self) -> ElectricCharge: ...
    @property
    def faraday_C12(self) -> ElectricCharge: ...
    @property
    def F(self) -> ElectricCharge: ...
    @property
    def franklin(self) -> ElectricCharge: ...
    @property
    def Fr(self) -> ElectricCharge: ...
    @property
    def statcoulomb(self) -> ElectricCharge: ...
    @property
    def u_a_charge(self) -> ElectricCharge: ...
    @property
    def kilocoulomb(self) -> ElectricCharge: ...
    @property
    def kC(self) -> ElectricCharge: ...
    @property
    def millicoulomb(self) -> ElectricCharge: ...
    @property
    def mC(self) -> ElectricCharge: ...
    @property
    def microcoulomb(self) -> ElectricCharge: ...
    @property
    def nanocoulomb(self) -> ElectricCharge: ...
    @property
    def nC(self) -> ElectricCharge: ...
    @property
    def picocoulomb(self) -> ElectricCharge: ...
    @property
    def pC(self) -> ElectricCharge: ...

class ElectricCharge(TypedVariable):
    """Type-safe electric charge variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricChargeSetter:
        """
        Create a electric charge setter for fluent unit assignment.
        
        Example:
            electriccharge.set(100).abcoulomb
            electriccharge.set(100).ampere_hour
            electriccharge.set(100).coulomb
        """
        ...

# ============================================================================
# ELECTRIC CURRENT INTENSITY
# ============================================================================

class ElectricCurrentIntensitySetter(TypeSafeSetter):
    """Electric Current Intensity-specific setter with only electric current intensity unit properties."""
    
    def __init__(self, variable: ElectricCurrentIntensity, value: float) -> None: ...
    
    # All electric current intensity unit properties - provides fluent API with full type hints
    @property
    def abampere(self) -> ElectricCurrentIntensity: ...
    @property
    def ampere_intl_mean(self) -> ElectricCurrentIntensity: ...
    @property
    def ampere_intl_US(self) -> ElectricCurrentIntensity: ...
    @property
    def ampere_or_amp(self) -> ElectricCurrentIntensity: ...
    @property
    def A(self) -> ElectricCurrentIntensity: ...
    @property
    def biot(self) -> ElectricCurrentIntensity: ...
    @property
    def statampere(self) -> ElectricCurrentIntensity: ...
    @property
    def u_a_or_current(self) -> ElectricCurrentIntensity: ...

class ElectricCurrentIntensity(TypedVariable):
    """Type-safe electric current intensity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricCurrentIntensitySetter:
        """
        Create a electric current intensity setter for fluent unit assignment.
        
        Example:
            electriccurrentintensity.set(100).abampere
            electriccurrentintensity.set(100).ampere_intl_mean
            electriccurrentintensity.set(100).ampere_intl_US
        """
        ...

# ============================================================================
# ELECTRIC DIPOLE MOMENT
# ============================================================================

class ElectricDipoleMomentSetter(TypeSafeSetter):
    """Electric Dipole Moment-specific setter with only electric dipole moment unit properties."""
    
    def __init__(self, variable: ElectricDipoleMoment, value: float) -> None: ...
    
    # All electric dipole moment unit properties - provides fluent API with full type hints
    @property
    def ampere_meter_second(self) -> ElectricDipoleMoment: ...
    @property
    def coulomb_meter(self) -> ElectricDipoleMoment: ...
    @property
    def debye(self) -> ElectricDipoleMoment: ...
    @property
    def D(self) -> ElectricDipoleMoment: ...
    @property
    def electron_meter(self) -> ElectricDipoleMoment: ...

class ElectricDipoleMoment(TypedVariable):
    """Type-safe electric dipole moment variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricDipoleMomentSetter:
        """
        Create a electric dipole moment setter for fluent unit assignment.
        
        Example:
            electricdipolemoment.set(100).ampere_meter_second
            electricdipolemoment.set(100).coulomb_meter
            electricdipolemoment.set(100).debye
        """
        ...

# ============================================================================
# ELECTRIC FIELD STRENGTH
# ============================================================================

class ElectricFieldStrengthSetter(TypeSafeSetter):
    """Electric Field Strength-specific setter with only electric field strength unit properties."""
    
    def __init__(self, variable: ElectricFieldStrength, value: float) -> None: ...
    
    # All electric field strength unit properties - provides fluent API with full type hints
    @property
    def volt_per_centimeter(self) -> ElectricFieldStrength: ...
    @property
    def volt_per_meter(self) -> ElectricFieldStrength: ...

class ElectricFieldStrength(TypedVariable):
    """Type-safe electric field strength variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricFieldStrengthSetter:
        """
        Create a electric field strength setter for fluent unit assignment.
        
        Example:
            electricfieldstrength.set(100).volt_per_centimeter
            electricfieldstrength.set(100).volt_per_meter
        """
        ...

# ============================================================================
# ELECTRIC INDUCTANCE
# ============================================================================

class ElectricInductanceSetter(TypeSafeSetter):
    """Electric Inductance-specific setter with only electric inductance unit properties."""
    
    def __init__(self, variable: ElectricInductance, value: float) -> None: ...
    
    # All electric inductance unit properties - provides fluent API with full type hints
    @property
    def abhenry(self) -> ElectricInductance: ...
    @property
    def cm(self) -> ElectricInductance: ...
    @property
    def henry(self) -> ElectricInductance: ...
    @property
    def H(self) -> ElectricInductance: ...
    @property
    def henry_intl_mean(self) -> ElectricInductance: ...
    @property
    def henry_intl_US(self) -> ElectricInductance: ...
    @property
    def mic(self) -> ElectricInductance: ...
    @property
    def stathenry(self) -> ElectricInductance: ...
    @property
    def millihenry(self) -> ElectricInductance: ...
    @property
    def mH(self) -> ElectricInductance: ...
    @property
    def microhenry(self) -> ElectricInductance: ...
    @property
    def nanohenry(self) -> ElectricInductance: ...
    @property
    def nH(self) -> ElectricInductance: ...

class ElectricInductance(TypedVariable):
    """Type-safe electric inductance variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricInductanceSetter:
        """
        Create a electric inductance setter for fluent unit assignment.
        
        Example:
            electricinductance.set(100).abhenry
            electricinductance.set(100).cm
            electricinductance.set(100).henry
        """
        ...

# ============================================================================
# ELECTRIC POTENTIAL
# ============================================================================

class ElectricPotentialSetter(TypeSafeSetter):
    """Electric Potential-specific setter with only electric potential unit properties."""
    
    def __init__(self, variable: ElectricPotential, value: float) -> None: ...
    
    # All electric potential unit properties - provides fluent API with full type hints
    @property
    def abvolt(self) -> ElectricPotential: ...
    @property
    def statvolt(self) -> ElectricPotential: ...
    @property
    def u_a_potential(self) -> ElectricPotential: ...
    @property
    def volt(self) -> ElectricPotential: ...
    @property
    def V(self) -> ElectricPotential: ...
    @property
    def volt_intl_mean(self) -> ElectricPotential: ...
    @property
    def volt_US(self) -> ElectricPotential: ...
    @property
    def kilovolt(self) -> ElectricPotential: ...
    @property
    def kV(self) -> ElectricPotential: ...
    @property
    def millivolt(self) -> ElectricPotential: ...
    @property
    def mV(self) -> ElectricPotential: ...
    @property
    def microvolt(self) -> ElectricPotential: ...
    @property
    def nanovolt(self) -> ElectricPotential: ...
    @property
    def nV(self) -> ElectricPotential: ...
    @property
    def picovolt(self) -> ElectricPotential: ...
    @property
    def pV(self) -> ElectricPotential: ...

class ElectricPotential(TypedVariable):
    """Type-safe electric potential variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricPotentialSetter:
        """
        Create a electric potential setter for fluent unit assignment.
        
        Example:
            electricpotential.set(100).abvolt
            electricpotential.set(100).statvolt
            electricpotential.set(100).u_a_potential
        """
        ...

# ============================================================================
# ELECTRIC RESISTANCE
# ============================================================================

class ElectricResistanceSetter(TypeSafeSetter):
    """Electric Resistance-specific setter with only electric resistance unit properties."""
    
    def __init__(self, variable: ElectricResistance, value: float) -> None: ...
    
    # All electric resistance unit properties - provides fluent API with full type hints
    @property
    def abohm(self) -> ElectricResistance: ...
    @property
    def jacobi(self) -> ElectricResistance: ...
    @property
    def lenz(self) -> ElectricResistance: ...
    @property
    def ohm(self) -> ElectricResistance: ...
    @property
    def ohm_intl_mean(self) -> ElectricResistance: ...
    @property
    def ohm_intl_US(self) -> ElectricResistance: ...
    @property
    def ohm_legal(self) -> ElectricResistance: ...
    @property
    def preece(self) -> ElectricResistance: ...
    @property
    def statohm(self) -> ElectricResistance: ...
    @property
    def wheatstone(self) -> ElectricResistance: ...
    @property
    def kiloohm(self) -> ElectricResistance: ...
    @property
    def k_Omega(self) -> ElectricResistance: ...
    @property
    def megaohm(self) -> ElectricResistance: ...
    @property
    def M_Omega(self) -> ElectricResistance: ...
    @property
    def milliohm(self) -> ElectricResistance: ...
    @property
    def m_Omega(self) -> ElectricResistance: ...

class ElectricResistance(TypedVariable):
    """Type-safe electric resistance variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricResistanceSetter:
        """
        Create a electric resistance setter for fluent unit assignment.
        
        Example:
            electricresistance.set(100).abohm
            electricresistance.set(100).jacobi
            electricresistance.set(100).lenz
        """
        ...

# ============================================================================
# ELECTRICAL CONDUCTANCE
# ============================================================================

class ElectricalConductanceSetter(TypeSafeSetter):
    """Electrical Conductance-specific setter with only electrical conductance unit properties."""
    
    def __init__(self, variable: ElectricalConductance, value: float) -> None: ...
    
    # All electrical conductance unit properties - provides fluent API with full type hints
    @property
    def emu_cgs(self) -> ElectricalConductance: ...
    @property
    def esu_cgs(self) -> ElectricalConductance: ...
    @property
    def mho(self) -> ElectricalConductance: ...
    @property
    def microsiemens(self) -> ElectricalConductance: ...
    @property
    def siemens(self) -> ElectricalConductance: ...
    @property
    def S(self) -> ElectricalConductance: ...
    @property
    def millisiemens(self) -> ElectricalConductance: ...
    @property
    def mS(self) -> ElectricalConductance: ...

class ElectricalConductance(TypedVariable):
    """Type-safe electrical conductance variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricalConductanceSetter:
        """
        Create a electrical conductance setter for fluent unit assignment.
        
        Example:
            electricalconductance.set(100).emu_cgs
            electricalconductance.set(100).esu_cgs
            electricalconductance.set(100).mho
        """
        ...

# ============================================================================
# ELECTRICAL PERMITTIVITY
# ============================================================================

class ElectricalPermittivitySetter(TypeSafeSetter):
    """Electrical Permittivity-specific setter with only electrical permittivity unit properties."""
    
    def __init__(self, variable: ElectricalPermittivity, value: float) -> None: ...
    
    # All electrical permittivity unit properties - provides fluent API with full type hints
    @property
    def farad_per_meter(self) -> ElectricalPermittivity: ...

class ElectricalPermittivity(TypedVariable):
    """Type-safe electrical permittivity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricalPermittivitySetter:
        """
        Create a electrical permittivity setter for fluent unit assignment.
        
        Example:
            electricalpermittivity.set(100).farad_per_meter
        """
        ...

# ============================================================================
# ELECTRICAL RESISTIVITY
# ============================================================================

class ElectricalResistivitySetter(TypeSafeSetter):
    """Electrical Resistivity-specific setter with only electrical resistivity unit properties."""
    
    def __init__(self, variable: ElectricalResistivity, value: float) -> None: ...
    
    # All electrical resistivity unit properties - provides fluent API with full type hints
    @property
    def circular_mil_ohm_per_foot(self) -> ElectricalResistivity: ...
    @property
    def emu_cgs(self) -> ElectricalResistivity: ...
    @property
    def microhm_inch(self) -> ElectricalResistivity: ...
    @property
    def ohm_centimeter(self) -> ElectricalResistivity: ...
    @property
    def ohm_meter(self) -> ElectricalResistivity: ...

class ElectricalResistivity(TypedVariable):
    """Type-safe electrical resistivity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricalResistivitySetter:
        """
        Create a electrical resistivity setter for fluent unit assignment.
        
        Example:
            electricalresistivity.set(100).circular_mil_ohm_per_foot
            electricalresistivity.set(100).emu_cgs
            electricalresistivity.set(100).microhm_inch
        """
        ...

# ============================================================================
# ENERGY FLUX
# ============================================================================

class EnergyFluxSetter(TypeSafeSetter):
    """Energy Flux-specific setter with only energy flux unit properties."""
    
    def __init__(self, variable: EnergyFlux, value: float) -> None: ...
    
    # All energy flux unit properties - provides fluent API with full type hints
    @property
    def Btu_per_square_foot_per_hour(self) -> EnergyFlux: ...
    @property
    def calorie_per_square_centimeter_per_second(self) -> EnergyFlux: ...
    @property
    def cal_cm_2_s(self) -> EnergyFlux: ...
    @property
    def Celsius_heat_units_Chu_per_square_foot_per_hour(self) -> EnergyFlux: ...
    @property
    def kilocalorie_per_square_foot_per_hour(self) -> EnergyFlux: ...
    @property
    def kilocalorie_per_square_meter_per_hour(self) -> EnergyFlux: ...
    @property
    def watt_per_square_meter(self) -> EnergyFlux: ...

class EnergyFlux(TypedVariable):
    """Type-safe energy flux variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> EnergyFluxSetter:
        """
        Create a energy flux setter for fluent unit assignment.
        
        Example:
            energyflux.set(100).Btu_per_square_foot_per_hour
            energyflux.set(100).calorie_per_square_centimeter_per_second
            energyflux.set(100).Celsius_heat_units_Chu_per_square_foot_per_hour
        """
        ...

# ============================================================================
# ENERGY, HEAT, WORK
# ============================================================================

class EnergyHeatWorkSetter(TypeSafeSetter):
    """Energy, Heat, Work-specific setter with only energy, heat, work unit properties."""
    
    def __init__(self, variable: EnergyHeatWork, value: float) -> None: ...
    
    # All energy, heat, work unit properties - provides fluent API with full type hints
    @property
    def barrel_oil_equivalent_or_equivalent_barrel(self) -> EnergyHeatWork: ...
    @property
    def bboe(self) -> EnergyHeatWork: ...
    @property
    def boe(self) -> EnergyHeatWork: ...
    @property
    def billion_electronvolt(self) -> EnergyHeatWork: ...
    @property
    def BeV(self) -> EnergyHeatWork: ...
    @property
    def British_thermal_unit_4_circ_mathrm_C(self) -> EnergyHeatWork: ...
    @property
    def British_thermal_unit_60_circ_mathrm_F(self) -> EnergyHeatWork: ...
    @property
    def British_thermal_unit_international_steam_tables(self) -> EnergyHeatWork: ...
    @property
    def British_thermal_unit_ISO_TC_12(self) -> EnergyHeatWork: ...
    @property
    def British_thermal_unit_mean(self) -> EnergyHeatWork: ...
    @property
    def Btu_mean(self) -> EnergyHeatWork: ...
    @property
    def Btu(self) -> EnergyHeatWork: ...
    @property
    def British_thermal_unit_thermochemical(self) -> EnergyHeatWork: ...
    @property
    def calorie_20_circ_mathrm_C(self) -> EnergyHeatWork: ...
    @property
    def calorie_4_circ_mathrm_C(self) -> EnergyHeatWork: ...
    @property
    def calorie_international_steam_tables(self) -> EnergyHeatWork: ...
    @property
    def calorie_mean(self) -> EnergyHeatWork: ...
    @property
    def Calorie_nutritional(self) -> EnergyHeatWork: ...
    @property
    def calorie_thermochemical(self) -> EnergyHeatWork: ...
    @property
    def Celsius_heat_unit(self) -> EnergyHeatWork: ...
    @property
    def Chu(self) -> EnergyHeatWork: ...
    @property
    def Celsius_heat_unit_15_circ_mathrm_C(self) -> EnergyHeatWork: ...
    @property
    def electron_volt(self) -> EnergyHeatWork: ...
    @property
    def eV(self) -> EnergyHeatWork: ...
    @property
    def erg(self) -> EnergyHeatWork: ...
    @property
    def foot_pound_force_duty(self) -> EnergyHeatWork: ...
    @property
    def foot_poundal(self) -> EnergyHeatWork: ...
    @property
    def frigorie(self) -> EnergyHeatWork: ...
    @property
    def fg(self) -> EnergyHeatWork: ...
    @property
    def hartree_atomic_unit_of_energy(self) -> EnergyHeatWork: ...
    @property
    def joule(self) -> EnergyHeatWork: ...
    @property
    def J(self) -> EnergyHeatWork: ...
    @property
    def joule_international(self) -> EnergyHeatWork: ...
    @property
    def kilocalorie_thermal(self) -> EnergyHeatWork: ...
    @property
    def kilogram_force_meter(self) -> EnergyHeatWork: ...
    @property
    def kiloton_TNT(self) -> EnergyHeatWork: ...
    @property
    def kilowatt_hour(self) -> EnergyHeatWork: ...
    @property
    def kWh(self) -> EnergyHeatWork: ...
    @property
    def liter_atmosphere(self) -> EnergyHeatWork: ...
    @property
    def megaton_TNT(self) -> EnergyHeatWork: ...
    @property
    def pound_centigrade_unit_15_circ_mathrm_C(self) -> EnergyHeatWork: ...
    @property
    def prout(self) -> EnergyHeatWork: ...
    @property
    def Q_unit(self) -> EnergyHeatWork: ...
    @property
    def Q(self) -> EnergyHeatWork: ...
    @property
    def quad_quadrillion_Btu(self) -> EnergyHeatWork: ...
    @property
    def quad(self) -> EnergyHeatWork: ...
    @property
    def rydberg(self) -> EnergyHeatWork: ...
    @property
    def Ry(self) -> EnergyHeatWork: ...
    @property
    def therm_EEG(self) -> EnergyHeatWork: ...
    @property
    def therm_refineries(self) -> EnergyHeatWork: ...
    @property
    def therm_refy(self) -> EnergyHeatWork: ...
    @property
    def therm(self) -> EnergyHeatWork: ...
    @property
    def therm_US(self) -> EnergyHeatWork: ...
    @property
    def ton_coal_equivalent(self) -> EnergyHeatWork: ...
    @property
    def ton_oil_equivalent(self) -> EnergyHeatWork: ...
    @property
    def kilojoule(self) -> EnergyHeatWork: ...
    @property
    def kJ(self) -> EnergyHeatWork: ...
    @property
    def megajoule(self) -> EnergyHeatWork: ...
    @property
    def MJ(self) -> EnergyHeatWork: ...
    @property
    def gigajoule(self) -> EnergyHeatWork: ...
    @property
    def GJ(self) -> EnergyHeatWork: ...

class EnergyHeatWork(TypedVariable):
    """Type-safe energy, heat, work variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> EnergyHeatWorkSetter:
        """
        Create a energy, heat, work setter for fluent unit assignment.
        
        Example:
            energyheatwork.set(100).barrel_oil_equivalent_or_equivalent_barrel
            energyheatwork.set(100).billion_electronvolt
            energyheatwork.set(100).British_thermal_unit_4_circ_mathrm_C
        """
        ...

# ============================================================================
# ENERGY PER UNIT AREA
# ============================================================================

class EnergyPerUnitAreaSetter(TypeSafeSetter):
    """Energy per Unit Area-specific setter with only energy per unit area unit properties."""
    
    def __init__(self, variable: EnergyPerUnitArea, value: float) -> None: ...
    
    # All energy per unit area unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_square_foot(self) -> EnergyPerUnitArea: ...
    @property
    def Btu_ft_2(self) -> EnergyPerUnitArea: ...
    @property
    def Btu_sq_ft(self) -> EnergyPerUnitArea: ...
    @property
    def joule_per_square_meter(self) -> EnergyPerUnitArea: ...
    @property
    def Langley(self) -> EnergyPerUnitArea: ...
    @property
    def Ly(self) -> EnergyPerUnitArea: ...

class EnergyPerUnitArea(TypedVariable):
    """Type-safe energy per unit area variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> EnergyPerUnitAreaSetter:
        """
        Create a energy per unit area setter for fluent unit assignment.
        
        Example:
            energyperunitarea.set(100).British_thermal_unit_per_square_foot
            energyperunitarea.set(100).joule_per_square_meter
            energyperunitarea.set(100).Langley
        """
        ...

# ============================================================================
# FORCE
# ============================================================================

class ForceSetter(TypeSafeSetter):
    """Force-specific setter with only force unit properties."""
    
    def __init__(self, variable: Force, value: float) -> None: ...
    
    # All force unit properties - provides fluent API with full type hints
    @property
    def crinal(self) -> Force: ...
    @property
    def dyne(self) -> Force: ...
    @property
    def dyn(self) -> Force: ...
    @property
    def funal(self) -> Force: ...
    @property
    def kilogram_force(self) -> Force: ...
    @property
    def kip_force(self) -> Force: ...
    @property
    def newton(self) -> Force: ...
    @property
    def N(self) -> Force: ...
    @property
    def ounce_force(self) -> Force: ...
    @property
    def oz_f(self) -> Force: ...
    @property
    def oz(self) -> Force: ...
    @property
    def pond(self) -> Force: ...
    @property
    def p(self) -> Force: ...
    @property
    def pound_force(self) -> Force: ...
    @property
    def lb_f(self) -> Force: ...
    @property
    def lb(self) -> Force: ...
    @property
    def poundal(self) -> Force: ...
    @property
    def pdl(self) -> Force: ...
    @property
    def slug_force(self) -> Force: ...
    @property
    def sth_ne(self) -> Force: ...
    @property
    def sn(self) -> Force: ...
    @property
    def ton_force_long(self) -> Force: ...
    @property
    def LT(self) -> Force: ...
    @property
    def ton_force_metric(self) -> Force: ...
    @property
    def MT(self) -> Force: ...
    @property
    def ton_force_short(self) -> Force: ...
    @property
    def T(self) -> Force: ...
    @property
    def kilonewton(self) -> Force: ...
    @property
    def kN(self) -> Force: ...
    @property
    def millinewton(self) -> Force: ...
    @property
    def mN(self) -> Force: ...

class Force(TypedVariable):
    """Type-safe force variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ForceSetter:
        """
        Create a force setter for fluent unit assignment.
        
        Example:
            force.set(100).crinal
            force.set(100).dyne
            force.set(100).funal
        """
        ...

# ============================================================================
# FORCE (BODY)
# ============================================================================

class ForceBodySetter(TypeSafeSetter):
    """Force (Body)-specific setter with only force (body) unit properties."""
    
    def __init__(self, variable: ForceBody, value: float) -> None: ...
    
    # All force (body) unit properties - provides fluent API with full type hints
    @property
    def dyne_per_cubic_centimeter(self) -> ForceBody: ...
    @property
    def dyn_cc(self) -> ForceBody: ...
    @property
    def dyn_cm_3(self) -> ForceBody: ...
    @property
    def kilogram_force_per_cubic_centimeter(self) -> ForceBody: ...
    @property
    def kilogram_force_per_cubic_meter(self) -> ForceBody: ...
    @property
    def newton_per_cubic_meter(self) -> ForceBody: ...
    @property
    def pound_force_per_cubic_foot(self) -> ForceBody: ...
    @property
    def pound_force_per_cubic_inch(self) -> ForceBody: ...
    @property
    def ton_force_per_cubic_foot(self) -> ForceBody: ...

class ForceBody(TypedVariable):
    """Type-safe force (body) variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ForceBodySetter:
        """
        Create a force (body) setter for fluent unit assignment.
        
        Example:
            forcebody.set(100).dyne_per_cubic_centimeter
            forcebody.set(100).kilogram_force_per_cubic_centimeter
            forcebody.set(100).kilogram_force_per_cubic_meter
        """
        ...

# ============================================================================
# FORCE PER UNIT MASS
# ============================================================================

class ForcePerUnitMassSetter(TypeSafeSetter):
    """Force per Unit Mass-specific setter with only force per unit mass unit properties."""
    
    def __init__(self, variable: ForcePerUnitMass, value: float) -> None: ...
    
    # All force per unit mass unit properties - provides fluent API with full type hints
    @property
    def dyne_per_gram(self) -> ForcePerUnitMass: ...
    @property
    def kilogram_force_per_kilogram(self) -> ForcePerUnitMass: ...
    @property
    def newton_per_kilogram(self) -> ForcePerUnitMass: ...
    @property
    def pound_force_per_pound_mass(self) -> ForcePerUnitMass: ...
    @property
    def lb_f_lb(self) -> ForcePerUnitMass: ...
    @property
    def lb_f_lb_m(self) -> ForcePerUnitMass: ...
    @property
    def pound_force_per_slug(self) -> ForcePerUnitMass: ...

class ForcePerUnitMass(TypedVariable):
    """Type-safe force per unit mass variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ForcePerUnitMassSetter:
        """
        Create a force per unit mass setter for fluent unit assignment.
        
        Example:
            forceperunitmass.set(100).dyne_per_gram
            forceperunitmass.set(100).kilogram_force_per_kilogram
            forceperunitmass.set(100).newton_per_kilogram
        """
        ...

# ============================================================================
# FREQUENCY VOLTAGE RATIO
# ============================================================================

class FrequencyVoltageRatioSetter(TypeSafeSetter):
    """Frequency Voltage Ratio-specific setter with only frequency voltage ratio unit properties."""
    
    def __init__(self, variable: FrequencyVoltageRatio, value: float) -> None: ...
    
    # All frequency voltage ratio unit properties - provides fluent API with full type hints
    @property
    def cycles_per_second_per_volt(self) -> FrequencyVoltageRatio: ...
    @property
    def hertz_per_volt(self) -> FrequencyVoltageRatio: ...
    @property
    def terahertz_per_volt(self) -> FrequencyVoltageRatio: ...

class FrequencyVoltageRatio(TypedVariable):
    """Type-safe frequency voltage ratio variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> FrequencyVoltageRatioSetter:
        """
        Create a frequency voltage ratio setter for fluent unit assignment.
        
        Example:
            frequencyvoltageratio.set(100).cycles_per_second_per_volt
            frequencyvoltageratio.set(100).hertz_per_volt
            frequencyvoltageratio.set(100).terahertz_per_volt
        """
        ...

# ============================================================================
# FUEL CONSUMPTION
# ============================================================================

class FuelConsumptionSetter(TypeSafeSetter):
    """Fuel Consumption-specific setter with only fuel consumption unit properties."""
    
    def __init__(self, variable: FuelConsumption, value: float) -> None: ...
    
    # All fuel consumption unit properties - provides fluent API with full type hints
    @property
    def _100_km_per_liter(self) -> FuelConsumption: ...
    @property
    def gallons_UK_per_100_miles(self) -> FuelConsumption: ...
    @property
    def gallons_US_per_100_miles(self) -> FuelConsumption: ...
    @property
    def kilometers_per_gallon_UK(self) -> FuelConsumption: ...
    @property
    def kilometers_per_gallon_US(self) -> FuelConsumption: ...
    @property
    def kilometers_per_liter(self) -> FuelConsumption: ...
    @property
    def liters_per_100_km(self) -> FuelConsumption: ...
    @property
    def liters_per_kilometer(self) -> FuelConsumption: ...
    @property
    def meters_per_gallon_UK(self) -> FuelConsumption: ...
    @property
    def meters_per_gallon_US(self) -> FuelConsumption: ...
    @property
    def miles_per_gallon_UK(self) -> FuelConsumption: ...
    @property
    def mi_gal_UK(self) -> FuelConsumption: ...
    @property
    def mpg_UK(self) -> FuelConsumption: ...
    @property
    def miles_per_gallon_US(self) -> FuelConsumption: ...
    @property
    def mi_gal_US(self) -> FuelConsumption: ...
    @property
    def mpg_US(self) -> FuelConsumption: ...
    @property
    def miles_per_liter(self) -> FuelConsumption: ...

class FuelConsumption(TypedVariable):
    """Type-safe fuel consumption variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> FuelConsumptionSetter:
        """
        Create a fuel consumption setter for fluent unit assignment.
        
        Example:
            fuelconsumption.set(100)._100_km_per_liter
            fuelconsumption.set(100).gallons_UK_per_100_miles
            fuelconsumption.set(100).gallons_US_per_100_miles
        """
        ...

# ============================================================================
# HEAT OF COMBUSTION
# ============================================================================

class HeatOfCombustionSetter(TypeSafeSetter):
    """Heat of Combustion-specific setter with only heat of combustion unit properties."""
    
    def __init__(self, variable: HeatOfCombustion, value: float) -> None: ...
    
    # All heat of combustion unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_pound(self) -> HeatOfCombustion: ...
    @property
    def calorie_per_gram(self) -> HeatOfCombustion: ...
    @property
    def Chu_per_pound(self) -> HeatOfCombustion: ...
    @property
    def joule_per_kilogram(self) -> HeatOfCombustion: ...

class HeatOfCombustion(TypedVariable):
    """Type-safe heat of combustion variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatOfCombustionSetter:
        """
        Create a heat of combustion setter for fluent unit assignment.
        
        Example:
            heatofcombustion.set(100).British_thermal_unit_per_pound
            heatofcombustion.set(100).calorie_per_gram
            heatofcombustion.set(100).Chu_per_pound
        """
        ...

# ============================================================================
# HEAT OF FUSION
# ============================================================================

class HeatOfFusionSetter(TypeSafeSetter):
    """Heat of Fusion-specific setter with only heat of fusion unit properties."""
    
    def __init__(self, variable: HeatOfFusion, value: float) -> None: ...
    
    # All heat of fusion unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_mean_per_pound(self) -> HeatOfFusion: ...
    @property
    def British_thermal_unit_per_pound(self) -> HeatOfFusion: ...
    @property
    def calorie_per_gram(self) -> HeatOfFusion: ...
    @property
    def Chu_per_pound(self) -> HeatOfFusion: ...
    @property
    def joule_per_kilogram(self) -> HeatOfFusion: ...

class HeatOfFusion(TypedVariable):
    """Type-safe heat of fusion variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatOfFusionSetter:
        """
        Create a heat of fusion setter for fluent unit assignment.
        
        Example:
            heatoffusion.set(100).British_thermal_unit_mean_per_pound
            heatoffusion.set(100).British_thermal_unit_per_pound
            heatoffusion.set(100).calorie_per_gram
        """
        ...

# ============================================================================
# HEAT OF VAPORIZATION
# ============================================================================

class HeatOfVaporizationSetter(TypeSafeSetter):
    """Heat of Vaporization-specific setter with only heat of vaporization unit properties."""
    
    def __init__(self, variable: HeatOfVaporization, value: float) -> None: ...
    
    # All heat of vaporization unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_pound(self) -> HeatOfVaporization: ...
    @property
    def calorie_per_gram(self) -> HeatOfVaporization: ...
    @property
    def Chu_per_pound(self) -> HeatOfVaporization: ...
    @property
    def joule_per_kilogram(self) -> HeatOfVaporization: ...

class HeatOfVaporization(TypedVariable):
    """Type-safe heat of vaporization variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatOfVaporizationSetter:
        """
        Create a heat of vaporization setter for fluent unit assignment.
        
        Example:
            heatofvaporization.set(100).British_thermal_unit_per_pound
            heatofvaporization.set(100).calorie_per_gram
            heatofvaporization.set(100).Chu_per_pound
        """
        ...

# ============================================================================
# HEAT TRANSFER COEFFICIENT
# ============================================================================

class HeatTransferCoefficientSetter(TypeSafeSetter):
    """Heat Transfer Coefficient-specific setter with only heat transfer coefficient unit properties."""
    
    def __init__(self, variable: HeatTransferCoefficient, value: float) -> None: ...
    
    # All heat transfer coefficient unit properties - provides fluent API with full type hints
    @property
    def Btu_per_square_foot_per_hour_per_degree_Fahrenheit_or_Rankine(self) -> HeatTransferCoefficient: ...
    @property
    def watt_per_square_meter_per_degree_Celsius_or_kelvin(self) -> HeatTransferCoefficient: ...

class HeatTransferCoefficient(TypedVariable):
    """Type-safe heat transfer coefficient variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatTransferCoefficientSetter:
        """
        Create a heat transfer coefficient setter for fluent unit assignment.
        
        Example:
            heattransfercoefficient.set(100).Btu_per_square_foot_per_hour_per_degree_Fahrenheit_or_Rankine
            heattransfercoefficient.set(100).watt_per_square_meter_per_degree_Celsius_or_kelvin
        """
        ...

# ============================================================================
# ILLUMINANCE
# ============================================================================

class IlluminanceSetter(TypeSafeSetter):
    """Illuminance-specific setter with only illuminance unit properties."""
    
    def __init__(self, variable: Illuminance, value: float) -> None: ...
    
    # All illuminance unit properties - provides fluent API with full type hints
    @property
    def foot_candle(self) -> Illuminance: ...
    @property
    def ft_C(self) -> Illuminance: ...
    @property
    def ft_Cd(self) -> Illuminance: ...
    @property
    def lux(self) -> Illuminance: ...
    @property
    def lx(self) -> Illuminance: ...
    @property
    def nox(self) -> Illuminance: ...
    @property
    def phot(self) -> Illuminance: ...
    @property
    def ph(self) -> Illuminance: ...
    @property
    def skot(self) -> Illuminance: ...

class Illuminance(TypedVariable):
    """Type-safe illuminance variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> IlluminanceSetter:
        """
        Create a illuminance setter for fluent unit assignment.
        
        Example:
            illuminance.set(100).foot_candle
            illuminance.set(100).lux
            illuminance.set(100).nox
        """
        ...

# ============================================================================
# KINETIC ENERGY OF TURBULENCE
# ============================================================================

class KineticEnergyOfTurbulenceSetter(TypeSafeSetter):
    """Kinetic Energy of Turbulence-specific setter with only kinetic energy of turbulence unit properties."""
    
    def __init__(self, variable: KineticEnergyOfTurbulence, value: float) -> None: ...
    
    # All kinetic energy of turbulence unit properties - provides fluent API with full type hints
    @property
    def square_foot_per_second_squared(self) -> KineticEnergyOfTurbulence: ...
    @property
    def ft_2_s_2(self) -> KineticEnergyOfTurbulence: ...
    @property
    def sqft_sec_2(self) -> KineticEnergyOfTurbulence: ...
    @property
    def square_meters_per_second_squared(self) -> KineticEnergyOfTurbulence: ...

class KineticEnergyOfTurbulence(TypedVariable):
    """Type-safe kinetic energy of turbulence variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> KineticEnergyOfTurbulenceSetter:
        """
        Create a kinetic energy of turbulence setter for fluent unit assignment.
        
        Example:
            kineticenergyofturbulence.set(100).square_foot_per_second_squared
            kineticenergyofturbulence.set(100).square_meters_per_second_squared
        """
        ...

# ============================================================================
# LENGTH
# ============================================================================

class LengthSetter(TypeSafeSetter):
    """Length-specific setter with only length unit properties."""
    
    def __init__(self, variable: Length, value: float) -> None: ...
    
    # All length unit properties - provides fluent API with full type hints
    @property
    def ngstr_m(self) -> Length: ...
    @property
    def AA(self) -> Length: ...
    @property
    def arpent_Quebec(self) -> Length: ...
    @property
    def arp(self) -> Length: ...
    @property
    def astronomic_unit(self) -> Length: ...
    @property
    def AU(self) -> Length: ...
    @property
    def attometer(self) -> Length: ...
    @property
    def am(self) -> Length: ...
    @property
    def calibre_centinch(self) -> Length: ...
    @property
    def cin(self) -> Length: ...
    @property
    def centimeter(self) -> Length: ...
    @property
    def cm(self) -> Length: ...
    @property
    def chain_Engr_s_or_Ramsden(self) -> Length: ...
    @property
    def ch_eng(self) -> Length: ...
    @property
    def Rams(self) -> Length: ...
    @property
    def chain_Gunter_s(self) -> Length: ...
    @property
    def chain_surveyors(self) -> Length: ...
    @property
    def cubit_UK(self) -> Length: ...
    @property
    def ell(self) -> Length: ...
    @property
    def fathom(self) -> Length: ...
    @property
    def fath(self) -> Length: ...
    @property
    def femtometre(self) -> Length: ...
    @property
    def fm(self) -> Length: ...
    @property
    def fermi(self) -> Length: ...
    @property
    def F(self) -> Length: ...
    @property
    def foot(self) -> Length: ...
    @property
    def ft(self) -> Length: ...
    @property
    def furlong_UK_and_US(self) -> Length: ...
    @property
    def fur(self) -> Length: ...
    @property
    def inch(self) -> Length: ...
    @property
    def in_unit(self) -> Length: ...
    @property
    def kilometer(self) -> Length: ...
    @property
    def km(self) -> Length: ...
    @property
    def league_US_statute(self) -> Length: ...
    @property
    def lieue_metric(self) -> Length: ...
    @property
    def ligne_metric(self) -> Length: ...
    @property
    def line_US(self) -> Length: ...
    @property
    def link_surveyors(self) -> Length: ...
    @property
    def meter(self) -> Length: ...
    @property
    def m(self) -> Length: ...
    @property
    def micrometer(self) -> Length: ...
    @property
    def micron(self) -> Length: ...
    @property
    def mu(self) -> Length: ...
    @property
    def mil(self) -> Length: ...
    @property
    def mile_geographical(self) -> Length: ...
    @property
    def mi(self) -> Length: ...
    @property
    def mile_US_nautical(self) -> Length: ...
    @property
    def mile_US_statute(self) -> Length: ...
    @property
    def mile_US_survey(self) -> Length: ...
    @property
    def millimeter(self) -> Length: ...
    @property
    def mm(self) -> Length: ...
    @property
    def millimicron(self) -> Length: ...
    @property
    def nanometer_or_nanon(self) -> Length: ...
    @property
    def nm(self) -> Length: ...
    @property
    def parsec(self) -> Length: ...
    @property
    def pc(self) -> Length: ...
    @property
    def perche(self) -> Length: ...
    @property
    def rod(self) -> Length: ...
    @property
    def pica(self) -> Length: ...
    @property
    def picometer(self) -> Length: ...
    @property
    def pm(self) -> Length: ...
    @property
    def point_Didot(self) -> Length: ...
    @property
    def point_US(self) -> Length: ...
    @property
    def rod_or_pole(self) -> Length: ...
    @property
    def span(self) -> Length: ...
    @property
    def thou_millinch(self) -> Length: ...
    @property
    def thou(self) -> Length: ...
    @property
    def toise_metric(self) -> Length: ...
    @property
    def yard(self) -> Length: ...
    @property
    def yd(self) -> Length: ...
    @property
    def nanometer(self) -> Length: ...

class Length(TypedVariable):
    """Type-safe length variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LengthSetter:
        """
        Create a length setter for fluent unit assignment.
        
        Example:
            length.set(100).ngstr_m
            length.set(100).arpent_Quebec
            length.set(100).astronomic_unit
        """
        ...

# ============================================================================
# LINEAR MASS DENSITY
# ============================================================================

class LinearMassDensitySetter(TypeSafeSetter):
    """Linear Mass Density-specific setter with only linear mass density unit properties."""
    
    def __init__(self, variable: LinearMassDensity, value: float) -> None: ...
    
    # All linear mass density unit properties - provides fluent API with full type hints
    @property
    def denier(self) -> LinearMassDensity: ...
    @property
    def kilogram_per_centimeter(self) -> LinearMassDensity: ...
    @property
    def kilogram_per_meter(self) -> LinearMassDensity: ...
    @property
    def pound_per_foot(self) -> LinearMassDensity: ...
    @property
    def pound_per_inch(self) -> LinearMassDensity: ...
    @property
    def pound_per_yard(self) -> LinearMassDensity: ...
    @property
    def ton_metric_per_kilometer(self) -> LinearMassDensity: ...
    @property
    def t_km(self) -> LinearMassDensity: ...
    @property
    def MT_km(self) -> LinearMassDensity: ...
    @property
    def ton_metric_per_meter(self) -> LinearMassDensity: ...
    @property
    def t_m(self) -> LinearMassDensity: ...
    @property
    def MT_m(self) -> LinearMassDensity: ...

class LinearMassDensity(TypedVariable):
    """Type-safe linear mass density variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LinearMassDensitySetter:
        """
        Create a linear mass density setter for fluent unit assignment.
        
        Example:
            linearmassdensity.set(100).denier
            linearmassdensity.set(100).kilogram_per_centimeter
            linearmassdensity.set(100).kilogram_per_meter
        """
        ...

# ============================================================================
# LINEAR MOMENTUM
# ============================================================================

class LinearMomentumSetter(TypeSafeSetter):
    """Linear Momentum-specific setter with only linear momentum unit properties."""
    
    def __init__(self, variable: LinearMomentum, value: float) -> None: ...
    
    # All linear momentum unit properties - provides fluent API with full type hints
    @property
    def foot_pounds_force_per_hour(self) -> LinearMomentum: ...
    @property
    def ft_lb_f_h(self) -> LinearMomentum: ...
    @property
    def ft_lb_hr(self) -> LinearMomentum: ...
    @property
    def foot_pounds_force_per_minute(self) -> LinearMomentum: ...
    @property
    def ft_lb_f_min(self) -> LinearMomentum: ...
    @property
    def ft_lb_min(self) -> LinearMomentum: ...
    @property
    def foot_pounds_force_per_second(self) -> LinearMomentum: ...
    @property
    def ft_lb_f_s(self) -> LinearMomentum: ...
    @property
    def ft_lb_sec(self) -> LinearMomentum: ...
    @property
    def gram_centimeters_per_second(self) -> LinearMomentum: ...
    @property
    def kilogram_meters_per_second(self) -> LinearMomentum: ...

class LinearMomentum(TypedVariable):
    """Type-safe linear momentum variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LinearMomentumSetter:
        """
        Create a linear momentum setter for fluent unit assignment.
        
        Example:
            linearmomentum.set(100).foot_pounds_force_per_hour
            linearmomentum.set(100).foot_pounds_force_per_minute
            linearmomentum.set(100).foot_pounds_force_per_second
        """
        ...

# ============================================================================
# LUMINANCE (SELF)
# ============================================================================

class LuminanceSelfSetter(TypeSafeSetter):
    """Luminance (self)-specific setter with only luminance (self) unit properties."""
    
    def __init__(self, variable: LuminanceSelf, value: float) -> None: ...
    
    # All luminance (self) unit properties - provides fluent API with full type hints
    @property
    def apostilb(self) -> LuminanceSelf: ...
    @property
    def asb(self) -> LuminanceSelf: ...
    @property
    def blondel(self) -> LuminanceSelf: ...
    @property
    def candela_per_square_meter(self) -> LuminanceSelf: ...
    @property
    def foot_lambert(self) -> LuminanceSelf: ...
    @property
    def lambert(self) -> LuminanceSelf: ...
    @property
    def L(self) -> LuminanceSelf: ...
    @property
    def luxon(self) -> LuminanceSelf: ...
    @property
    def nit(self) -> LuminanceSelf: ...
    @property
    def stilb(self) -> LuminanceSelf: ...
    @property
    def sb(self) -> LuminanceSelf: ...
    @property
    def troland(self) -> LuminanceSelf: ...

class LuminanceSelf(TypedVariable):
    """Type-safe luminance (self) variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LuminanceSelfSetter:
        """
        Create a luminance (self) setter for fluent unit assignment.
        
        Example:
            luminanceself.set(100).apostilb
            luminanceself.set(100).blondel
            luminanceself.set(100).candela_per_square_meter
        """
        ...

# ============================================================================
# LUMINOUS FLUX
# ============================================================================

class LuminousFluxSetter(TypeSafeSetter):
    """Luminous Flux-specific setter with only luminous flux unit properties."""
    
    def __init__(self, variable: LuminousFlux, value: float) -> None: ...
    
    # All luminous flux unit properties - provides fluent API with full type hints
    @property
    def candela_steradian(self) -> LuminousFlux: ...
    @property
    def lumen(self) -> LuminousFlux: ...

class LuminousFlux(TypedVariable):
    """Type-safe luminous flux variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LuminousFluxSetter:
        """
        Create a luminous flux setter for fluent unit assignment.
        
        Example:
            luminousflux.set(100).candela_steradian
            luminousflux.set(100).lumen
        """
        ...

# ============================================================================
# LUMINOUS INTENSITY
# ============================================================================

class LuminousIntensitySetter(TypeSafeSetter):
    """Luminous Intensity-specific setter with only luminous intensity unit properties."""
    
    def __init__(self, variable: LuminousIntensity, value: float) -> None: ...
    
    # All luminous intensity unit properties - provides fluent API with full type hints
    @property
    def candela(self) -> LuminousIntensity: ...
    @property
    def cd(self) -> LuminousIntensity: ...
    @property
    def candle_international(self) -> LuminousIntensity: ...
    @property
    def carcel(self) -> LuminousIntensity: ...
    @property
    def Hefner_unit(self) -> LuminousIntensity: ...
    @property
    def HK(self) -> LuminousIntensity: ...

class LuminousIntensity(TypedVariable):
    """Type-safe luminous intensity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LuminousIntensitySetter:
        """
        Create a luminous intensity setter for fluent unit assignment.
        
        Example:
            luminousintensity.set(100).candela
            luminousintensity.set(100).candle_international
            luminousintensity.set(100).carcel
        """
        ...

# ============================================================================
# MAGNETIC FIELD
# ============================================================================

class MagneticFieldSetter(TypeSafeSetter):
    """Magnetic Field-specific setter with only magnetic field unit properties."""
    
    def __init__(self, variable: MagneticField, value: float) -> None: ...
    
    # All magnetic field unit properties - provides fluent API with full type hints
    @property
    def ampere_per_meter(self) -> MagneticField: ...
    @property
    def lenz(self) -> MagneticField: ...
    @property
    def oersted(self) -> MagneticField: ...
    @property
    def Oe(self) -> MagneticField: ...
    @property
    def praoersted(self) -> MagneticField: ...

class MagneticField(TypedVariable):
    """Type-safe magnetic field variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticFieldSetter:
        """
        Create a magnetic field setter for fluent unit assignment.
        
        Example:
            magneticfield.set(100).ampere_per_meter
            magneticfield.set(100).lenz
            magneticfield.set(100).oersted
        """
        ...

# ============================================================================
# MAGNETIC FLUX
# ============================================================================

class MagneticFluxSetter(TypeSafeSetter):
    """Magnetic Flux-specific setter with only magnetic flux unit properties."""
    
    def __init__(self, variable: MagneticFlux, value: float) -> None: ...
    
    # All magnetic flux unit properties - provides fluent API with full type hints
    @property
    def kapp_line(self) -> MagneticFlux: ...
    @property
    def line(self) -> MagneticFlux: ...
    @property
    def maxwell(self) -> MagneticFlux: ...
    @property
    def Mx(self) -> MagneticFlux: ...
    @property
    def unit_pole(self) -> MagneticFlux: ...
    @property
    def weber(self) -> MagneticFlux: ...
    @property
    def Wb(self) -> MagneticFlux: ...
    @property
    def milliweber(self) -> MagneticFlux: ...
    @property
    def mWb(self) -> MagneticFlux: ...
    @property
    def microweber(self) -> MagneticFlux: ...

class MagneticFlux(TypedVariable):
    """Type-safe magnetic flux variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticFluxSetter:
        """
        Create a magnetic flux setter for fluent unit assignment.
        
        Example:
            magneticflux.set(100).kapp_line
            magneticflux.set(100).line
            magneticflux.set(100).maxwell
        """
        ...

# ============================================================================
# MAGNETIC INDUCTION FIELD STRENGTH
# ============================================================================

class MagneticInductionFieldStrengthSetter(TypeSafeSetter):
    """Magnetic Induction Field Strength-specific setter with only magnetic induction field strength unit properties."""
    
    def __init__(self, variable: MagneticInductionFieldStrength, value: float) -> None: ...
    
    # All magnetic induction field strength unit properties - provides fluent API with full type hints
    @property
    def gamma(self) -> MagneticInductionFieldStrength: ...
    @property
    def gauss(self) -> MagneticInductionFieldStrength: ...
    @property
    def G(self) -> MagneticInductionFieldStrength: ...
    @property
    def line_per_square_centimeter(self) -> MagneticInductionFieldStrength: ...
    @property
    def maxwell_per_square_centimeter(self) -> MagneticInductionFieldStrength: ...
    @property
    def tesla(self) -> MagneticInductionFieldStrength: ...
    @property
    def T(self) -> MagneticInductionFieldStrength: ...
    @property
    def u_a(self) -> MagneticInductionFieldStrength: ...
    @property
    def weber_per_square_meter(self) -> MagneticInductionFieldStrength: ...
    @property
    def millitesla(self) -> MagneticInductionFieldStrength: ...
    @property
    def mT(self) -> MagneticInductionFieldStrength: ...
    @property
    def microtesla(self) -> MagneticInductionFieldStrength: ...
    @property
    def nanotesla(self) -> MagneticInductionFieldStrength: ...
    @property
    def nT(self) -> MagneticInductionFieldStrength: ...

class MagneticInductionFieldStrength(TypedVariable):
    """Type-safe magnetic induction field strength variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticInductionFieldStrengthSetter:
        """
        Create a magnetic induction field strength setter for fluent unit assignment.
        
        Example:
            magneticinductionfieldstrength.set(100).gamma
            magneticinductionfieldstrength.set(100).gauss
            magneticinductionfieldstrength.set(100).line_per_square_centimeter
        """
        ...

# ============================================================================
# MAGNETIC MOMENT
# ============================================================================

class MagneticMomentSetter(TypeSafeSetter):
    """Magnetic Moment-specific setter with only magnetic moment unit properties."""
    
    def __init__(self, variable: MagneticMoment, value: float) -> None: ...
    
    # All magnetic moment unit properties - provides fluent API with full type hints
    @property
    def Bohr_magneton(self) -> MagneticMoment: ...
    @property
    def joule_per_tesla(self) -> MagneticMoment: ...
    @property
    def nuclear_magneton(self) -> MagneticMoment: ...

class MagneticMoment(TypedVariable):
    """Type-safe magnetic moment variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticMomentSetter:
        """
        Create a magnetic moment setter for fluent unit assignment.
        
        Example:
            magneticmoment.set(100).Bohr_magneton
            magneticmoment.set(100).joule_per_tesla
            magneticmoment.set(100).nuclear_magneton
        """
        ...

# ============================================================================
# MAGNETIC PERMEABILITY
# ============================================================================

class MagneticPermeabilitySetter(TypeSafeSetter):
    """Magnetic Permeability-specific setter with only magnetic permeability unit properties."""
    
    def __init__(self, variable: MagneticPermeability, value: float) -> None: ...
    
    # All magnetic permeability unit properties - provides fluent API with full type hints
    @property
    def henrys_per_meter(self) -> MagneticPermeability: ...
    @property
    def newton_per_square_ampere(self) -> MagneticPermeability: ...

class MagneticPermeability(TypedVariable):
    """Type-safe magnetic permeability variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticPermeabilitySetter:
        """
        Create a magnetic permeability setter for fluent unit assignment.
        
        Example:
            magneticpermeability.set(100).henrys_per_meter
            magneticpermeability.set(100).newton_per_square_ampere
        """
        ...

# ============================================================================
# MAGNETOMOTIVE FORCE
# ============================================================================

class MagnetomotiveForceSetter(TypeSafeSetter):
    """Magnetomotive Force-specific setter with only magnetomotive force unit properties."""
    
    def __init__(self, variable: MagnetomotiveForce, value: float) -> None: ...
    
    # All magnetomotive force unit properties - provides fluent API with full type hints
    @property
    def abampere_turn(self) -> MagnetomotiveForce: ...
    @property
    def ampere(self) -> MagnetomotiveForce: ...
    @property
    def A(self) -> MagnetomotiveForce: ...
    @property
    def ampere_turn(self) -> MagnetomotiveForce: ...
    @property
    def gilbert(self) -> MagnetomotiveForce: ...
    @property
    def Gb(self) -> MagnetomotiveForce: ...
    @property
    def kiloampere(self) -> MagnetomotiveForce: ...
    @property
    def kA(self) -> MagnetomotiveForce: ...
    @property
    def milliampere(self) -> MagnetomotiveForce: ...
    @property
    def mA(self) -> MagnetomotiveForce: ...
    @property
    def microampere(self) -> MagnetomotiveForce: ...
    @property
    def nanoampere(self) -> MagnetomotiveForce: ...
    @property
    def nA(self) -> MagnetomotiveForce: ...
    @property
    def picoampere(self) -> MagnetomotiveForce: ...
    @property
    def pA(self) -> MagnetomotiveForce: ...

class MagnetomotiveForce(TypedVariable):
    """Type-safe magnetomotive force variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagnetomotiveForceSetter:
        """
        Create a magnetomotive force setter for fluent unit assignment.
        
        Example:
            magnetomotiveforce.set(100).abampere_turn
            magnetomotiveforce.set(100).ampere
            magnetomotiveforce.set(100).ampere_turn
        """
        ...

# ============================================================================
# MASS
# ============================================================================

class MassSetter(TypeSafeSetter):
    """Mass-specific setter with only mass unit properties."""
    
    def __init__(self, variable: Mass, value: float) -> None: ...
    
    # All mass unit properties - provides fluent API with full type hints
    @property
    def slug(self) -> Mass: ...
    @property
    def sl(self) -> Mass: ...
    @property
    def atomic_mass_unit_12_mathrm_C(self) -> Mass: ...
    @property
    def uleft_12_Cright(self) -> Mass: ...
    @property
    def amu(self) -> Mass: ...
    @property
    def carat_metric(self) -> Mass: ...
    @property
    def ct(self) -> Mass: ...
    @property
    def cental(self) -> Mass: ...
    @property
    def centigram(self) -> Mass: ...
    @property
    def cg(self) -> Mass: ...
    @property
    def clove_UK(self) -> Mass: ...
    @property
    def cl(self) -> Mass: ...
    @property
    def drachm_apothecary(self) -> Mass: ...
    @property
    def dram_avoirdupois(self) -> Mass: ...
    @property
    def dram_troy(self) -> Mass: ...
    @property
    def grain(self) -> Mass: ...
    @property
    def gr(self) -> Mass: ...
    @property
    def gram(self) -> Mass: ...
    @property
    def g(self) -> Mass: ...
    @property
    def hundredweight_long_or_gross(self) -> Mass: ...
    @property
    def hundredweight_short_or_net(self) -> Mass: ...
    @property
    def kilogram(self) -> Mass: ...
    @property
    def kg(self) -> Mass: ...
    @property
    def kip(self) -> Mass: ...
    @property
    def microgram(self) -> Mass: ...
    @property
    def milligram(self) -> Mass: ...
    @property
    def mg(self) -> Mass: ...
    @property
    def ounce_apothecary(self) -> Mass: ...
    @property
    def ounce_avoirdupois(self) -> Mass: ...
    @property
    def oz(self) -> Mass: ...
    @property
    def ounce_troy(self) -> Mass: ...
    @property
    def pennyweight_troy(self) -> Mass: ...
    @property
    def pood_Russia(self) -> Mass: ...
    @property
    def pood(self) -> Mass: ...
    @property
    def pound_apothecary(self) -> Mass: ...
    @property
    def pound_avoirdupois(self) -> Mass: ...
    @property
    def pound_troy(self) -> Mass: ...
    @property
    def pound_mass(self) -> Mass: ...
    @property
    def quarter_UK(self) -> Mass: ...
    @property
    def qt(self) -> Mass: ...
    @property
    def quintal_metric(self) -> Mass: ...
    @property
    def quital_US(self) -> Mass: ...
    @property
    def scruple_avoirdupois(self) -> Mass: ...
    @property
    def scf(self) -> Mass: ...
    @property
    def stone_UK(self) -> Mass: ...
    @property
    def st(self) -> Mass: ...
    @property
    def ton_metric(self) -> Mass: ...
    @property
    def t(self) -> Mass: ...
    @property
    def ton_US_long(self) -> Mass: ...
    @property
    def ton_US_short(self) -> Mass: ...

class Mass(TypedVariable):
    """Type-safe mass variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassSetter:
        """
        Create a mass setter for fluent unit assignment.
        
        Example:
            mass.set(100).slug
            mass.set(100).atomic_mass_unit_12_mathrm_C
            mass.set(100).carat_metric
        """
        ...

# ============================================================================
# MASS DENSITY
# ============================================================================

class MassDensitySetter(TypeSafeSetter):
    """Mass Density-specific setter with only mass density unit properties."""
    
    def __init__(self, variable: MassDensity, value: float) -> None: ...
    
    # All mass density unit properties - provides fluent API with full type hints
    @property
    def gram_per_cubic_centimeter(self) -> MassDensity: ...
    @property
    def g_cc(self) -> MassDensity: ...
    @property
    def g_ml(self) -> MassDensity: ...
    @property
    def gram_per_cubic_decimeter(self) -> MassDensity: ...
    @property
    def gram_per_cubic_meter(self) -> MassDensity: ...
    @property
    def gram_per_liter(self) -> MassDensity: ...
    @property
    def g_l(self) -> MassDensity: ...
    @property
    def g_L(self) -> MassDensity: ...
    @property
    def kilogram_per_cubic_meter(self) -> MassDensity: ...
    @property
    def ounce_avdp_per_US_gallon(self) -> MassDensity: ...
    @property
    def pound_avdp_per_cubic_foot(self) -> MassDensity: ...
    @property
    def lb_cu_ft(self) -> MassDensity: ...
    @property
    def lb_ft_3(self) -> MassDensity: ...
    @property
    def pound_avdp_per_US_gallon(self) -> MassDensity: ...
    @property
    def pound_mass_per_cubic_inch(self) -> MassDensity: ...
    @property
    def lb_cu_in(self) -> MassDensity: ...
    @property
    def lb_in_3(self) -> MassDensity: ...
    @property
    def ton_metric_per_cubic_meter(self) -> MassDensity: ...
    @property
    def t_m_3(self) -> MassDensity: ...
    @property
    def MT_m_3(self) -> MassDensity: ...

class MassDensity(TypedVariable):
    """Type-safe mass density variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassDensitySetter:
        """
        Create a mass density setter for fluent unit assignment.
        
        Example:
            massdensity.set(100).gram_per_cubic_centimeter
            massdensity.set(100).gram_per_cubic_decimeter
            massdensity.set(100).gram_per_cubic_meter
        """
        ...

# ============================================================================
# MASS FLOW RATE
# ============================================================================

class MassFlowRateSetter(TypeSafeSetter):
    """Mass Flow Rate-specific setter with only mass flow rate unit properties."""
    
    def __init__(self, variable: MassFlowRate, value: float) -> None: ...
    
    # All mass flow rate unit properties - provides fluent API with full type hints
    @property
    def kilograms_per_day(self) -> MassFlowRate: ...
    @property
    def kilograms_per_hour(self) -> MassFlowRate: ...
    @property
    def kilograms_per_minute(self) -> MassFlowRate: ...
    @property
    def kilograms_per_second(self) -> MassFlowRate: ...
    @property
    def metric_tons_per_day(self) -> MassFlowRate: ...
    @property
    def MT_d(self) -> MassFlowRate: ...
    @property
    def MTD(self) -> MassFlowRate: ...
    @property
    def metric_tons_per_hour(self) -> MassFlowRate: ...
    @property
    def MT_h(self) -> MassFlowRate: ...
    @property
    def metric_tons_per_minute(self) -> MassFlowRate: ...
    @property
    def metric_tons_per_second(self) -> MassFlowRate: ...
    @property
    def metric_tons_per_year_365_d(self) -> MassFlowRate: ...
    @property
    def MT_yr(self) -> MassFlowRate: ...
    @property
    def MTY(self) -> MassFlowRate: ...
    @property
    def pounds_per_day(self) -> MassFlowRate: ...
    @property
    def lb_d(self) -> MassFlowRate: ...
    @property
    def lb_da(self) -> MassFlowRate: ...
    @property
    def PPD(self) -> MassFlowRate: ...
    @property
    def pounds_per_hour(self) -> MassFlowRate: ...
    @property
    def lb_h(self) -> MassFlowRate: ...
    @property
    def lb_hr(self) -> MassFlowRate: ...
    @property
    def PPH(self) -> MassFlowRate: ...
    @property
    def pounds_per_minute(self) -> MassFlowRate: ...
    @property
    def lb_min(self) -> MassFlowRate: ...
    @property
    def PPM(self) -> MassFlowRate: ...
    @property
    def pounds_per_second(self) -> MassFlowRate: ...
    @property
    def lb_s(self) -> MassFlowRate: ...
    @property
    def lb_sec(self) -> MassFlowRate: ...
    @property
    def PPS(self) -> MassFlowRate: ...

class MassFlowRate(TypedVariable):
    """Type-safe mass flow rate variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassFlowRateSetter:
        """
        Create a mass flow rate setter for fluent unit assignment.
        
        Example:
            massflowrate.set(100).kilograms_per_day
            massflowrate.set(100).kilograms_per_hour
            massflowrate.set(100).kilograms_per_minute
        """
        ...

# ============================================================================
# MASS FLUX
# ============================================================================

class MassFluxSetter(TypeSafeSetter):
    """Mass Flux-specific setter with only mass flux unit properties."""
    
    def __init__(self, variable: MassFlux, value: float) -> None: ...
    
    # All mass flux unit properties - provides fluent API with full type hints
    @property
    def kilogram_per_square_meter_per_day(self) -> MassFlux: ...
    @property
    def kilogram_per_square_meter_per_hour(self) -> MassFlux: ...
    @property
    def kilogram_per_square_meter_per_minute(self) -> MassFlux: ...
    @property
    def kilogram_per_square_meter_per_second(self) -> MassFlux: ...
    @property
    def pound_per_square_foot_per_day(self) -> MassFlux: ...
    @property
    def lb_left_ft_2_dright(self) -> MassFlux: ...
    @property
    def lb_sqft_da(self) -> MassFlux: ...
    @property
    def pound_per_square_foot_per_hour(self) -> MassFlux: ...
    @property
    def lb_left_ft_2_hright(self) -> MassFlux: ...
    @property
    def lb_sqft_hr(self) -> MassFlux: ...
    @property
    def pound_per_square_foot_per_minute(self) -> MassFlux: ...
    @property
    def lb_left_ft_2_min_right(self) -> MassFlux: ...
    @property
    def lb_sqft_min(self) -> MassFlux: ...
    @property
    def pound_per_square_foot_per_second(self) -> MassFlux: ...
    @property
    def lb_left_ft_2_sright(self) -> MassFlux: ...
    @property
    def lb_sqft_sec(self) -> MassFlux: ...

class MassFlux(TypedVariable):
    """Type-safe mass flux variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassFluxSetter:
        """
        Create a mass flux setter for fluent unit assignment.
        
        Example:
            massflux.set(100).kilogram_per_square_meter_per_day
            massflux.set(100).kilogram_per_square_meter_per_hour
            massflux.set(100).kilogram_per_square_meter_per_minute
        """
        ...

# ============================================================================
# MASS FRACTION OF "I"
# ============================================================================

class MassFractionOfISetter(TypeSafeSetter):
    """Mass Fraction of "i"-specific setter with only mass fraction of "i" unit properties."""
    
    def __init__(self, variable: MassFractionOfI, value: float) -> None: ...
    
    # All mass fraction of "i" unit properties - provides fluent API with full type hints
    @property
    def grains_of_i_per_pound_total(self) -> MassFractionOfI: ...
    @property
    def gram_of_i_per_kilogram_total(self) -> MassFractionOfI: ...
    @property
    def kilogram_of_i_per_kilogram_total(self) -> MassFractionOfI: ...
    @property
    def pound_of_i_per_pound_total(self) -> MassFractionOfI: ...

class MassFractionOfI(TypedVariable):
    """Type-safe mass fraction of "i" variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassFractionOfISetter:
        """
        Create a mass fraction of "i" setter for fluent unit assignment.
        
        Example:
            massfractionofi.set(100).grains_of_i_per_pound_total
            massfractionofi.set(100).gram_of_i_per_kilogram_total
            massfractionofi.set(100).kilogram_of_i_per_kilogram_total
        """
        ...

# ============================================================================
# MASS TRANSFER COEFFICIENT
# ============================================================================

class MassTransferCoefficientSetter(TypeSafeSetter):
    """Mass Transfer Coefficient-specific setter with only mass transfer coefficient unit properties."""
    
    def __init__(self, variable: MassTransferCoefficient, value: float) -> None: ...
    
    # All mass transfer coefficient unit properties - provides fluent API with full type hints
    @property
    def gram_per_square_centimeter_per_second(self) -> MassTransferCoefficient: ...
    @property
    def kilogram_per_square_meter_per_second(self) -> MassTransferCoefficient: ...
    @property
    def pounds_force_per_cubic_foot_per_hour(self) -> MassTransferCoefficient: ...
    @property
    def lb_f_ft_3_h(self) -> MassTransferCoefficient: ...
    @property
    def lb_f_cft_hr(self) -> MassTransferCoefficient: ...
    @property
    def pounds_mass_per_square_foot_per_hour(self) -> MassTransferCoefficient: ...
    @property
    def lb_ft_2_hr(self) -> MassTransferCoefficient: ...
    @property
    def lb_sqft_hr(self) -> MassTransferCoefficient: ...
    @property
    def pounds_mass_per_square_foot_per_second(self) -> MassTransferCoefficient: ...
    @property
    def lb_left_ft_2_sright(self) -> MassTransferCoefficient: ...
    @property
    def lb_sqft_sec(self) -> MassTransferCoefficient: ...

class MassTransferCoefficient(TypedVariable):
    """Type-safe mass transfer coefficient variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassTransferCoefficientSetter:
        """
        Create a mass transfer coefficient setter for fluent unit assignment.
        
        Example:
            masstransfercoefficient.set(100).gram_per_square_centimeter_per_second
            masstransfercoefficient.set(100).kilogram_per_square_meter_per_second
            masstransfercoefficient.set(100).pounds_force_per_cubic_foot_per_hour
        """
        ...

# ============================================================================
# MOLALITY OF SOLUTE "I"
# ============================================================================

class MolalityOfSoluteISetter(TypeSafeSetter):
    """Molality of Solute "i"-specific setter with only molality of solute "i" unit properties."""
    
    def __init__(self, variable: MolalityOfSoluteI, value: float) -> None: ...
    
    # All molality of solute "i" unit properties - provides fluent API with full type hints
    @property
    def gram_moles_of_i_per_kilogram(self) -> MolalityOfSoluteI: ...
    @property
    def kilogram_mols_of_i_per_kilogram(self) -> MolalityOfSoluteI: ...
    @property
    def kmols_of_i_per_kilogram(self) -> MolalityOfSoluteI: ...
    @property
    def mols_of_i_per_gram(self) -> MolalityOfSoluteI: ...
    @property
    def pound_moles_of_i_per_pound_mass(self) -> MolalityOfSoluteI: ...

class MolalityOfSoluteI(TypedVariable):
    """Type-safe molality of solute "i" variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolalityOfSoluteISetter:
        """
        Create a molality of solute "i" setter for fluent unit assignment.
        
        Example:
            molalityofsolutei.set(100).gram_moles_of_i_per_kilogram
            molalityofsolutei.set(100).kilogram_mols_of_i_per_kilogram
            molalityofsolutei.set(100).kmols_of_i_per_kilogram
        """
        ...

# ============================================================================
# MOLAR CONCENTRATION BY MASS
# ============================================================================

class MolarConcentrationByMassSetter(TypeSafeSetter):
    """Molar Concentration by Mass-specific setter with only molar concentration by mass unit properties."""
    
    def __init__(self, variable: MolarConcentrationByMass, value: float) -> None: ...
    
    # All molar concentration by mass unit properties - provides fluent API with full type hints
    @property
    def gram_mole_or_mole_per_gram(self) -> MolarConcentrationByMass: ...
    @property
    def gram_mole_or_mole_per_kilogram(self) -> MolarConcentrationByMass: ...
    @property
    def kilogram_mole_or_kmol_per_kilogram(self) -> MolarConcentrationByMass: ...
    @property
    def micromole_per_gram(self) -> MolarConcentrationByMass: ...
    @property
    def millimole_per_gram(self) -> MolarConcentrationByMass: ...
    @property
    def picomole_per_gram(self) -> MolarConcentrationByMass: ...
    @property
    def pound_mole_per_pound(self) -> MolarConcentrationByMass: ...
    @property
    def lb_mol_lb(self) -> MolarConcentrationByMass: ...
    @property
    def mole_lb(self) -> MolarConcentrationByMass: ...

class MolarConcentrationByMass(TypedVariable):
    """Type-safe molar concentration by mass variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarConcentrationByMassSetter:
        """
        Create a molar concentration by mass setter for fluent unit assignment.
        
        Example:
            molarconcentrationbymass.set(100).gram_mole_or_mole_per_gram
            molarconcentrationbymass.set(100).gram_mole_or_mole_per_kilogram
            molarconcentrationbymass.set(100).kilogram_mole_or_kmol_per_kilogram
        """
        ...

# ============================================================================
# MOLAR FLOW RATE
# ============================================================================

class MolarFlowRateSetter(TypeSafeSetter):
    """Molar Flow Rate-specific setter with only molar flow rate unit properties."""
    
    def __init__(self, variable: MolarFlowRate, value: float) -> None: ...
    
    # All molar flow rate unit properties - provides fluent API with full type hints
    @property
    def gram_mole_per_day(self) -> MolarFlowRate: ...
    @property
    def gram_mole_per_hour(self) -> MolarFlowRate: ...
    @property
    def gram_mole_per_minute(self) -> MolarFlowRate: ...
    @property
    def gram_mole_per_second(self) -> MolarFlowRate: ...
    @property
    def kilogram_mole_or_kmol_per_day(self) -> MolarFlowRate: ...
    @property
    def kilogram_mole_or_kmol_per_hour(self) -> MolarFlowRate: ...
    @property
    def kilogram_mole_or_kmol_per_minute(self) -> MolarFlowRate: ...
    @property
    def kilogram_mole_or_kmol_per_second(self) -> MolarFlowRate: ...
    @property
    def pound_mole_or_lb_mol_per_day(self) -> MolarFlowRate: ...
    @property
    def lb_mol_d(self) -> MolarFlowRate: ...
    @property
    def mole_da(self) -> MolarFlowRate: ...
    @property
    def pound_mole_or_lb_mol_per_hour(self) -> MolarFlowRate: ...
    @property
    def lb_mol_h(self) -> MolarFlowRate: ...
    @property
    def mole_hr(self) -> MolarFlowRate: ...
    @property
    def pound_mole_or_lb_mol_per_minute(self) -> MolarFlowRate: ...
    @property
    def lb_mol_min(self) -> MolarFlowRate: ...
    @property
    def mole_min(self) -> MolarFlowRate: ...
    @property
    def pound_mole_or_lb_mol_per_second(self) -> MolarFlowRate: ...
    @property
    def lb_mol_s(self) -> MolarFlowRate: ...
    @property
    def mole_sec(self) -> MolarFlowRate: ...

class MolarFlowRate(TypedVariable):
    """Type-safe molar flow rate variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarFlowRateSetter:
        """
        Create a molar flow rate setter for fluent unit assignment.
        
        Example:
            molarflowrate.set(100).gram_mole_per_day
            molarflowrate.set(100).gram_mole_per_hour
            molarflowrate.set(100).gram_mole_per_minute
        """
        ...

# ============================================================================
# MOLAR FLUX
# ============================================================================

class MolarFluxSetter(TypeSafeSetter):
    """Molar Flux-specific setter with only molar flux unit properties."""
    
    def __init__(self, variable: MolarFlux, value: float) -> None: ...
    
    # All molar flux unit properties - provides fluent API with full type hints
    @property
    def kmol_per_square_meter_per_day(self) -> MolarFlux: ...
    @property
    def kmol_per_square_meter_per_hour(self) -> MolarFlux: ...
    @property
    def kmol_per_square_meter_per_minute(self) -> MolarFlux: ...
    @property
    def kmol_per_square_meter_per_second(self) -> MolarFlux: ...
    @property
    def pound_mole_per_square_foot_per_day(self) -> MolarFlux: ...
    @property
    def lb_mol_left_ft_2_dright(self) -> MolarFlux: ...
    @property
    def mole_sqft_da(self) -> MolarFlux: ...
    @property
    def pound_mole_per_square_foot_per_hour(self) -> MolarFlux: ...
    @property
    def lb_mol_left_ft_2_hright(self) -> MolarFlux: ...
    @property
    def mole_sqft_hr(self) -> MolarFlux: ...
    @property
    def pound_mole_per_square_foot_per_minute(self) -> MolarFlux: ...
    @property
    def lb_mol_left_ft_2_minright(self) -> MolarFlux: ...
    @property
    def mole_sqft_min(self) -> MolarFlux: ...
    @property
    def pound_mole_per_square_foot_per_second(self) -> MolarFlux: ...
    @property
    def lb_mol_left_ft_2_sright(self) -> MolarFlux: ...
    @property
    def mole_sqft_sec(self) -> MolarFlux: ...

class MolarFlux(TypedVariable):
    """Type-safe molar flux variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarFluxSetter:
        """
        Create a molar flux setter for fluent unit assignment.
        
        Example:
            molarflux.set(100).kmol_per_square_meter_per_day
            molarflux.set(100).kmol_per_square_meter_per_hour
            molarflux.set(100).kmol_per_square_meter_per_minute
        """
        ...

# ============================================================================
# MOLAR HEAT CAPACITY
# ============================================================================

class MolarHeatCapacitySetter(TypeSafeSetter):
    """Molar Heat Capacity-specific setter with only molar heat capacity unit properties."""
    
    def __init__(self, variable: MolarHeatCapacity, value: float) -> None: ...
    
    # All molar heat capacity unit properties - provides fluent API with full type hints
    @property
    def Btu_per_pound_mole_per_degree_Fahrenheit_or_degree_Rankine(self) -> MolarHeatCapacity: ...
    @property
    def calories_per_gram_mole_per_kelvin_or_degree_Celsius(self) -> MolarHeatCapacity: ...
    @property
    def joule_per_gram_mole_per_kelvin_or_degree_Celsius(self) -> MolarHeatCapacity: ...

class MolarHeatCapacity(TypedVariable):
    """Type-safe molar heat capacity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarHeatCapacitySetter:
        """
        Create a molar heat capacity setter for fluent unit assignment.
        
        Example:
            molarheatcapacity.set(100).Btu_per_pound_mole_per_degree_Fahrenheit_or_degree_Rankine
            molarheatcapacity.set(100).calories_per_gram_mole_per_kelvin_or_degree_Celsius
            molarheatcapacity.set(100).joule_per_gram_mole_per_kelvin_or_degree_Celsius
        """
        ...

# ============================================================================
# MOLARITY OF "I"
# ============================================================================

class MolarityOfISetter(TypeSafeSetter):
    """Molarity of "i"-specific setter with only molarity of "i" unit properties."""
    
    def __init__(self, variable: MolarityOfI, value: float) -> None: ...
    
    # All molarity of "i" unit properties - provides fluent API with full type hints
    @property
    def gram_moles_of_i_per_cubic_meter(self) -> MolarityOfI: ...
    @property
    def mol_i_m_3(self) -> MolarityOfI: ...
    @property
    def c_i(self) -> MolarityOfI: ...
    @property
    def gram_moles_of_i_per_liter(self) -> MolarityOfI: ...
    @property
    def kilogram_moles_of_i_per_cubic_meter(self) -> MolarityOfI: ...
    @property
    def kilogram_moles_of_i_per_liter(self) -> MolarityOfI: ...
    @property
    def pound_moles_of_i_per_cubic_foot(self) -> MolarityOfI: ...
    @property
    def lb_mol_i_ft_3(self) -> MolarityOfI: ...
    @property
    def mole_i_cft(self) -> MolarityOfI: ...
    @property
    def pound_moles_of_i_per_gallon_US(self) -> MolarityOfI: ...
    @property
    def lb_mol_i_gal(self) -> MolarityOfI: ...
    @property
    def mole_i_gal(self) -> MolarityOfI: ...

class MolarityOfI(TypedVariable):
    """Type-safe molarity of "i" variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarityOfISetter:
        """
        Create a molarity of "i" setter for fluent unit assignment.
        
        Example:
            molarityofi.set(100).gram_moles_of_i_per_cubic_meter
            molarityofi.set(100).gram_moles_of_i_per_liter
            molarityofi.set(100).kilogram_moles_of_i_per_cubic_meter
        """
        ...

# ============================================================================
# MOLE FRACTION OF "I"
# ============================================================================

class MoleFractionOfISetter(TypeSafeSetter):
    """Mole Fraction of "i"-specific setter with only mole fraction of "i" unit properties."""
    
    def __init__(self, variable: MoleFractionOfI, value: float) -> None: ...
    
    # All mole fraction of "i" unit properties - provides fluent API with full type hints
    @property
    def gram_mole_of_i_per_gram_mole_total(self) -> MoleFractionOfI: ...
    @property
    def kilogram_mole_of_i_per_kilogram_mole_total(self) -> MoleFractionOfI: ...
    @property
    def kilomole_of_i_per_kilomole_total(self) -> MoleFractionOfI: ...
    @property
    def pound_mole_of_i_per_pound_mole_total(self) -> MoleFractionOfI: ...

class MoleFractionOfI(TypedVariable):
    """Type-safe mole fraction of "i" variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MoleFractionOfISetter:
        """
        Create a mole fraction of "i" setter for fluent unit assignment.
        
        Example:
            molefractionofi.set(100).gram_mole_of_i_per_gram_mole_total
            molefractionofi.set(100).kilogram_mole_of_i_per_kilogram_mole_total
            molefractionofi.set(100).kilomole_of_i_per_kilomole_total
        """
        ...

# ============================================================================
# MOMENT OF INERTIA
# ============================================================================

class MomentOfInertiaSetter(TypeSafeSetter):
    """Moment of Inertia-specific setter with only moment of inertia unit properties."""
    
    def __init__(self, variable: MomentOfInertia, value: float) -> None: ...
    
    # All moment of inertia unit properties - provides fluent API with full type hints
    @property
    def gram_force_centimeter_square_second(self) -> MomentOfInertia: ...
    @property
    def gram_square_centimeter(self) -> MomentOfInertia: ...
    @property
    def kilogram_force_centimeter_square_second(self) -> MomentOfInertia: ...
    @property
    def kilogram_force_meter_square_second(self) -> MomentOfInertia: ...
    @property
    def kilogram_square_centimeter(self) -> MomentOfInertia: ...
    @property
    def kilogram_square_meter(self) -> MomentOfInertia: ...
    @property
    def ounce_force_inch_square_second(self) -> MomentOfInertia: ...
    @property
    def ounce_mass_square_inch(self) -> MomentOfInertia: ...
    @property
    def pound_mass_square_foot(self) -> MomentOfInertia: ...
    @property
    def lb_ft_2(self) -> MomentOfInertia: ...
    @property
    def lb_sq_ft(self) -> MomentOfInertia: ...
    @property
    def pound_mass_square_inch(self) -> MomentOfInertia: ...

class MomentOfInertia(TypedVariable):
    """Type-safe moment of inertia variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MomentOfInertiaSetter:
        """
        Create a moment of inertia setter for fluent unit assignment.
        
        Example:
            momentofinertia.set(100).gram_force_centimeter_square_second
            momentofinertia.set(100).gram_square_centimeter
            momentofinertia.set(100).kilogram_force_centimeter_square_second
        """
        ...

# ============================================================================
# MOMENTUM FLOW RATE
# ============================================================================

class MomentumFlowRateSetter(TypeSafeSetter):
    """Momentum Flow Rate-specific setter with only momentum flow rate unit properties."""
    
    def __init__(self, variable: MomentumFlowRate, value: float) -> None: ...
    
    # All momentum flow rate unit properties - provides fluent API with full type hints
    @property
    def foot_pounds_per_square_hour(self) -> MomentumFlowRate: ...
    @property
    def ft_lb_h_2(self) -> MomentumFlowRate: ...
    @property
    def ft_lb_hr_2(self) -> MomentumFlowRate: ...
    @property
    def foot_pounds_per_square_minute(self) -> MomentumFlowRate: ...
    @property
    def foot_pounds_per_square_second(self) -> MomentumFlowRate: ...
    @property
    def ft_lb_s_2(self) -> MomentumFlowRate: ...
    @property
    def ft_lb_sec_2(self) -> MomentumFlowRate: ...
    @property
    def gram_centimeters_per_square_second(self) -> MomentumFlowRate: ...
    @property
    def kilogram_meters_per_square_second(self) -> MomentumFlowRate: ...

class MomentumFlowRate(TypedVariable):
    """Type-safe momentum flow rate variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MomentumFlowRateSetter:
        """
        Create a momentum flow rate setter for fluent unit assignment.
        
        Example:
            momentumflowrate.set(100).foot_pounds_per_square_hour
            momentumflowrate.set(100).foot_pounds_per_square_minute
            momentumflowrate.set(100).foot_pounds_per_square_second
        """
        ...

# ============================================================================
# MOMENTUM FLUX
# ============================================================================

class MomentumFluxSetter(TypeSafeSetter):
    """Momentum Flux-specific setter with only momentum flux unit properties."""
    
    def __init__(self, variable: MomentumFlux, value: float) -> None: ...
    
    # All momentum flux unit properties - provides fluent API with full type hints
    @property
    def dyne_per_square_centimeter(self) -> MomentumFlux: ...
    @property
    def gram_per_centimeter_per_square_second(self) -> MomentumFlux: ...
    @property
    def newton_per_square_meter(self) -> MomentumFlux: ...
    @property
    def pound_force_per_square_foot(self) -> MomentumFlux: ...
    @property
    def pound_mass_per_foot_per_square_second(self) -> MomentumFlux: ...
    @property
    def lb_m_ft_s_2(self) -> MomentumFlux: ...
    @property
    def lb_ft_sec_2(self) -> MomentumFlux: ...

class MomentumFlux(TypedVariable):
    """Type-safe momentum flux variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MomentumFluxSetter:
        """
        Create a momentum flux setter for fluent unit assignment.
        
        Example:
            momentumflux.set(100).dyne_per_square_centimeter
            momentumflux.set(100).gram_per_centimeter_per_square_second
            momentumflux.set(100).newton_per_square_meter
        """
        ...

# ============================================================================
# NORMALITY OF SOLUTION
# ============================================================================

class NormalityOfSolutionSetter(TypeSafeSetter):
    """Normality of Solution-specific setter with only normality of solution unit properties."""
    
    def __init__(self, variable: NormalityOfSolution, value: float) -> None: ...
    
    # All normality of solution unit properties - provides fluent API with full type hints
    @property
    def gram_equivalents_per_cubic_meter(self) -> NormalityOfSolution: ...
    @property
    def gram_equivalents_per_liter(self) -> NormalityOfSolution: ...
    @property
    def pound_equivalents_per_cubic_foot(self) -> NormalityOfSolution: ...
    @property
    def lb_eq_ft_3(self) -> NormalityOfSolution: ...
    @property
    def lb_eq_cft(self) -> NormalityOfSolution: ...
    @property
    def pound_equivalents_per_gallon(self) -> NormalityOfSolution: ...

class NormalityOfSolution(TypedVariable):
    """Type-safe normality of solution variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> NormalityOfSolutionSetter:
        """
        Create a normality of solution setter for fluent unit assignment.
        
        Example:
            normalityofsolution.set(100).gram_equivalents_per_cubic_meter
            normalityofsolution.set(100).gram_equivalents_per_liter
            normalityofsolution.set(100).pound_equivalents_per_cubic_foot
        """
        ...

# ============================================================================
# PARTICLE DENSITY
# ============================================================================

class ParticleDensitySetter(TypeSafeSetter):
    """Particle Density-specific setter with only particle density unit properties."""
    
    def __init__(self, variable: ParticleDensity, value: float) -> None: ...
    
    # All particle density unit properties - provides fluent API with full type hints
    @property
    def particles_per_cubic_centimeter(self) -> ParticleDensity: ...
    @property
    def part_cm_3(self) -> ParticleDensity: ...
    @property
    def part_cc(self) -> ParticleDensity: ...
    @property
    def particles_per_cubic_foot(self) -> ParticleDensity: ...
    @property
    def part_ft_3(self) -> ParticleDensity: ...
    @property
    def part_cft(self) -> ParticleDensity: ...
    @property
    def particles_per_cubic_meter(self) -> ParticleDensity: ...
    @property
    def particles_per_gallon_US(self) -> ParticleDensity: ...
    @property
    def particles_per_liter(self) -> ParticleDensity: ...
    @property
    def particles_per_milliliter(self) -> ParticleDensity: ...

class ParticleDensity(TypedVariable):
    """Type-safe particle density variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ParticleDensitySetter:
        """
        Create a particle density setter for fluent unit assignment.
        
        Example:
            particledensity.set(100).particles_per_cubic_centimeter
            particledensity.set(100).particles_per_cubic_foot
            particledensity.set(100).particles_per_cubic_meter
        """
        ...

# ============================================================================
# PERCENT
# ============================================================================

class PercentSetter(TypeSafeSetter):
    """Percent-specific setter with only percent unit properties."""
    
    def __init__(self, variable: Percent, value: float) -> None: ...
    
    # All percent unit properties - provides fluent API with full type hints
    @property
    def percent(self) -> Percent: ...
    @property
    def unit(self) -> Percent: ...
    @property
    def per_mille(self) -> Percent: ...
    @property
    def basis_point(self) -> Percent: ...
    @property
    def bp(self) -> Percent: ...
    @property
    def bps(self) -> Percent: ...

class Percent(TypedVariable):
    """Type-safe percent variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PercentSetter:
        """
        Create a percent setter for fluent unit assignment.
        
        Example:
            percent.set(100).percent
            percent.set(100).per_mille
            percent.set(100).basis_point
        """
        ...

# ============================================================================
# PERMEABILITY
# ============================================================================

class PermeabilitySetter(TypeSafeSetter):
    """Permeability-specific setter with only permeability unit properties."""
    
    def __init__(self, variable: Permeability, value: float) -> None: ...
    
    # All permeability unit properties - provides fluent API with full type hints
    @property
    def darcy(self) -> Permeability: ...
    @property
    def square_feet(self) -> Permeability: ...
    @property
    def ft_2(self) -> Permeability: ...
    @property
    def sq_ft(self) -> Permeability: ...
    @property
    def square_meters(self) -> Permeability: ...

class Permeability(TypedVariable):
    """Type-safe permeability variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PermeabilitySetter:
        """
        Create a permeability setter for fluent unit assignment.
        
        Example:
            permeability.set(100).darcy
            permeability.set(100).square_feet
            permeability.set(100).square_meters
        """
        ...

# ============================================================================
# PHOTON EMISSION RATE
# ============================================================================

class PhotonEmissionRateSetter(TypeSafeSetter):
    """Photon Emission Rate-specific setter with only photon emission rate unit properties."""
    
    def __init__(self, variable: PhotonEmissionRate, value: float) -> None: ...
    
    # All photon emission rate unit properties - provides fluent API with full type hints
    @property
    def rayleigh(self) -> PhotonEmissionRate: ...
    @property
    def R(self) -> PhotonEmissionRate: ...
    @property
    def reciprocal_square_meter_second(self) -> PhotonEmissionRate: ...

class PhotonEmissionRate(TypedVariable):
    """Type-safe photon emission rate variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PhotonEmissionRateSetter:
        """
        Create a photon emission rate setter for fluent unit assignment.
        
        Example:
            photonemissionrate.set(100).rayleigh
            photonemissionrate.set(100).reciprocal_square_meter_second
        """
        ...

# ============================================================================
# POWER PER UNIT MASS OR SPECIFIC POWER
# ============================================================================

class PowerPerUnitMassSetter(TypeSafeSetter):
    """Power per Unit Mass or Specific Power-specific setter with only power per unit mass or specific power unit properties."""
    
    def __init__(self, variable: PowerPerUnitMass, value: float) -> None: ...
    
    # All power per unit mass or specific power unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_hour_per_pound_mass(self) -> PowerPerUnitMass: ...
    @property
    def Btu_h_lb(self) -> PowerPerUnitMass: ...
    @property
    def Btu_lb_hr(self) -> PowerPerUnitMass: ...
    @property
    def calorie_per_second_per_gram(self) -> PowerPerUnitMass: ...
    @property
    def cal_s_g(self) -> PowerPerUnitMass: ...
    @property
    def cal_g_sec(self) -> PowerPerUnitMass: ...
    @property
    def kilocalorie_per_hour_per_kilogram(self) -> PowerPerUnitMass: ...
    @property
    def kcal_h_kg(self) -> PowerPerUnitMass: ...
    @property
    def kcal_kg_hr(self) -> PowerPerUnitMass: ...
    @property
    def watt_per_kilogram(self) -> PowerPerUnitMass: ...

class PowerPerUnitMass(TypedVariable):
    """Type-safe power per unit mass or specific power variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PowerPerUnitMassSetter:
        """
        Create a power per unit mass or specific power setter for fluent unit assignment.
        
        Example:
            powerperunitmass.set(100).British_thermal_unit_per_hour_per_pound_mass
            powerperunitmass.set(100).calorie_per_second_per_gram
            powerperunitmass.set(100).kilocalorie_per_hour_per_kilogram
        """
        ...

# ============================================================================
# POWER PER UNIT VOLUME OR POWER DENSITY
# ============================================================================

class PowerPerUnitVolumeSetter(TypeSafeSetter):
    """Power per Unit Volume or Power Density-specific setter with only power per unit volume or power density unit properties."""
    
    def __init__(self, variable: PowerPerUnitVolume, value: float) -> None: ...
    
    # All power per unit volume or power density unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_hour_per_cubic_foot(self) -> PowerPerUnitVolume: ...
    @property
    def Btu_h_ft_3(self) -> PowerPerUnitVolume: ...
    @property
    def Btu_hr_cft(self) -> PowerPerUnitVolume: ...
    @property
    def calorie_per_second_per_cubic_centimeter(self) -> PowerPerUnitVolume: ...
    @property
    def cal_s_cm_3(self) -> PowerPerUnitVolume: ...
    @property
    def cal_s_cc(self) -> PowerPerUnitVolume: ...
    @property
    def Chu_per_hour_per_cubic_foot(self) -> PowerPerUnitVolume: ...
    @property
    def Chu_h_ft3(self) -> PowerPerUnitVolume: ...
    @property
    def Chu_hr_cft(self) -> PowerPerUnitVolume: ...
    @property
    def kilocalorie_per_hour_per_cubic_centimeter(self) -> PowerPerUnitVolume: ...
    @property
    def kcal_h_cm_3(self) -> PowerPerUnitVolume: ...
    @property
    def kcal_hr_cc(self) -> PowerPerUnitVolume: ...
    @property
    def kilocalorie_per_hour_per_cubic_foot(self) -> PowerPerUnitVolume: ...
    @property
    def kcal_h_ft_3(self) -> PowerPerUnitVolume: ...
    @property
    def kcal_hr_cft(self) -> PowerPerUnitVolume: ...
    @property
    def kilocalorie_per_second_per_cubic_centimeter(self) -> PowerPerUnitVolume: ...
    @property
    def kcal_s_cm_3(self) -> PowerPerUnitVolume: ...
    @property
    def kcal_s_cc(self) -> PowerPerUnitVolume: ...
    @property
    def watt_per_cubic_meter(self) -> PowerPerUnitVolume: ...

class PowerPerUnitVolume(TypedVariable):
    """Type-safe power per unit volume or power density variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PowerPerUnitVolumeSetter:
        """
        Create a power per unit volume or power density setter for fluent unit assignment.
        
        Example:
            powerperunitvolume.set(100).British_thermal_unit_per_hour_per_cubic_foot
            powerperunitvolume.set(100).calorie_per_second_per_cubic_centimeter
            powerperunitvolume.set(100).Chu_per_hour_per_cubic_foot
        """
        ...

# ============================================================================
# POWER, THERMAL DUTY
# ============================================================================

class PowerThermalDutySetter(TypeSafeSetter):
    """Power, Thermal Duty-specific setter with only power, thermal duty unit properties."""
    
    def __init__(self, variable: PowerThermalDuty, value: float) -> None: ...
    
    # All power, thermal duty unit properties - provides fluent API with full type hints
    @property
    def abwatt_emu_of_power(self) -> PowerThermalDuty: ...
    @property
    def emu(self) -> PowerThermalDuty: ...
    @property
    def boiler_horsepower(self) -> PowerThermalDuty: ...
    @property
    def British_thermal_unit_mean_per_hour(self) -> PowerThermalDuty: ...
    @property
    def Btu_mean_hr(self) -> PowerThermalDuty: ...
    @property
    def Btu_hr(self) -> PowerThermalDuty: ...
    @property
    def British_thermal_unit_mean_per_minute(self) -> PowerThermalDuty: ...
    @property
    def Btu_min(self) -> PowerThermalDuty: ...
    @property
    def Btu_mean_min(self) -> PowerThermalDuty: ...
    @property
    def British_thermal_unit_thermochemical_per_hour(self) -> PowerThermalDuty: ...
    @property
    def Btu_therm_hr(self) -> PowerThermalDuty: ...
    @property
    def British_thermal_unit_thermochemical_per_minute(self) -> PowerThermalDuty: ...
    @property
    def Btu_therm_min(self) -> PowerThermalDuty: ...
    @property
    def calorie_mean_per_hour(self) -> PowerThermalDuty: ...
    @property
    def calorie_thermochemical_per_hour(self) -> PowerThermalDuty: ...
    @property
    def donkey(self) -> PowerThermalDuty: ...
    @property
    def erg_per_second(self) -> PowerThermalDuty: ...
    @property
    def foot_pondal_per_second(self) -> PowerThermalDuty: ...
    @property
    def foot_pound_force_per_hour(self) -> PowerThermalDuty: ...
    @property
    def foot_pound_force_per_minute(self) -> PowerThermalDuty: ...
    @property
    def foot_pound_force_per_second(self) -> PowerThermalDuty: ...
    @property
    def horsepower_550_mathrm_ft_mathrm_lb_mathrm_f_mathrm_s(self) -> PowerThermalDuty: ...
    @property
    def HP(self) -> PowerThermalDuty: ...
    @property
    def horsepower_electric(self) -> PowerThermalDuty: ...
    @property
    def horsepower_UK(self) -> PowerThermalDuty: ...
    @property
    def kcal_per_hour(self) -> PowerThermalDuty: ...
    @property
    def kilogram_force_meter_per_second(self) -> PowerThermalDuty: ...
    @property
    def kilowatt(self) -> PowerThermalDuty: ...
    @property
    def kW(self) -> PowerThermalDuty: ...
    @property
    def megawatt(self) -> PowerThermalDuty: ...
    @property
    def MW(self) -> PowerThermalDuty: ...
    @property
    def metric_horsepower(self) -> PowerThermalDuty: ...
    @property
    def million_British_thermal_units_per_hour_petroleum(self) -> PowerThermalDuty: ...
    @property
    def million_kilocalorie_per_hour(self) -> PowerThermalDuty: ...
    @property
    def prony(self) -> PowerThermalDuty: ...
    @property
    def ton_of_refrigeration_US(self) -> PowerThermalDuty: ...
    @property
    def ton_or_refrigeration_UK(self) -> PowerThermalDuty: ...
    @property
    def volt_ampere(self) -> PowerThermalDuty: ...
    @property
    def VA(self) -> PowerThermalDuty: ...
    @property
    def water_horsepower(self) -> PowerThermalDuty: ...
    @property
    def watt(self) -> PowerThermalDuty: ...
    @property
    def W(self) -> PowerThermalDuty: ...
    @property
    def watt_international_mean(self) -> PowerThermalDuty: ...
    @property
    def watt_international_US(self) -> PowerThermalDuty: ...
    @property
    def gigawatt(self) -> PowerThermalDuty: ...
    @property
    def GW(self) -> PowerThermalDuty: ...
    @property
    def milliwatt(self) -> PowerThermalDuty: ...
    @property
    def mW(self) -> PowerThermalDuty: ...
    @property
    def microwatt(self) -> PowerThermalDuty: ...

class PowerThermalDuty(TypedVariable):
    """Type-safe power, thermal duty variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PowerThermalDutySetter:
        """
        Create a power, thermal duty setter for fluent unit assignment.
        
        Example:
            powerthermalduty.set(100).abwatt_emu_of_power
            powerthermalduty.set(100).boiler_horsepower
            powerthermalduty.set(100).British_thermal_unit_mean_per_hour
        """
        ...

# ============================================================================
# PRESSURE
# ============================================================================

class PressureSetter(TypeSafeSetter):
    """Pressure-specific setter with only pressure unit properties."""
    
    def __init__(self, variable: Pressure, value: float) -> None: ...
    
    # All pressure unit properties - provides fluent API with full type hints
    @property
    def atmosphere_standard(self) -> Pressure: ...
    @property
    def atm(self) -> Pressure: ...
    @property
    def bar(self) -> Pressure: ...
    @property
    def barye(self) -> Pressure: ...
    @property
    def dyne_per_square_centimeter(self) -> Pressure: ...
    @property
    def foot_of_mercury_60_circ_mathrm_F(self) -> Pressure: ...
    @property
    def foot_of_water_60_circ_mathrm_F(self) -> Pressure: ...
    @property
    def gigapascal(self) -> Pressure: ...
    @property
    def GPa(self) -> Pressure: ...
    @property
    def hectopascal(self) -> Pressure: ...
    @property
    def hPa(self) -> Pressure: ...
    @property
    def inch_of_mercury_60_circ_mathrm_F(self) -> Pressure: ...
    @property
    def inch_of_water_60_circ_mathrm_F(self) -> Pressure: ...
    @property
    def kilogram_force_per_square_centimeter(self) -> Pressure: ...
    @property
    def at(self) -> Pressure: ...
    @property
    def kg_f_cm_2(self) -> Pressure: ...
    @property
    def kilogram_force_per_square_meter(self) -> Pressure: ...
    @property
    def kip_force_per_square_inch(self) -> Pressure: ...
    @property
    def KSI(self) -> Pressure: ...
    @property
    def ksi(self) -> Pressure: ...
    @property
    def kip_f_in_2(self) -> Pressure: ...
    @property
    def megapascal(self) -> Pressure: ...
    @property
    def MPa(self) -> Pressure: ...
    @property
    def meter_of_water_4_circ_mathrm_C(self) -> Pressure: ...
    @property
    def microbar(self) -> Pressure: ...
    @property
    def millibar(self) -> Pressure: ...
    @property
    def mbar(self) -> Pressure: ...
    @property
    def millimeter_of_mercury_4_circ_mathrm_C(self) -> Pressure: ...
    @property
    def millimeter_of_water_4_circ_mathrm_C(self) -> Pressure: ...
    @property
    def newton_per_square_meter(self) -> Pressure: ...
    @property
    def ounce_force_per_square_inch(self) -> Pressure: ...
    @property
    def OSI(self) -> Pressure: ...
    @property
    def osi(self) -> Pressure: ...
    @property
    def pascal(self) -> Pressure: ...
    @property
    def Pa(self) -> Pressure: ...
    @property
    def pi_ze(self) -> Pressure: ...
    @property
    def pz(self) -> Pressure: ...
    @property
    def pound_force_per_square_foot(self) -> Pressure: ...
    @property
    def psf(self) -> Pressure: ...
    @property
    def pound_force_per_square_inch(self) -> Pressure: ...
    @property
    def psi(self) -> Pressure: ...
    @property
    def torr(self) -> Pressure: ...
    @property
    def mm_Hg_0_circ_C(self) -> Pressure: ...
    @property
    def kilopascal(self) -> Pressure: ...
    @property
    def kPa(self) -> Pressure: ...

class Pressure(TypedVariable):
    """Type-safe pressure variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PressureSetter:
        """
        Create a pressure setter for fluent unit assignment.
        
        Example:
            pressure.set(100).atmosphere_standard
            pressure.set(100).bar
            pressure.set(100).barye
        """
        ...

# ============================================================================
# RADIATION DOSE EQUIVALENT
# ============================================================================

class RadiationDoseEquivalentSetter(TypeSafeSetter):
    """Radiation Dose Equivalent-specific setter with only radiation dose equivalent unit properties."""
    
    def __init__(self, variable: RadiationDoseEquivalent, value: float) -> None: ...
    
    # All radiation dose equivalent unit properties - provides fluent API with full type hints
    @property
    def rem(self) -> RadiationDoseEquivalent: ...
    @property
    def sievert(self) -> RadiationDoseEquivalent: ...
    @property
    def Sv(self) -> RadiationDoseEquivalent: ...
    @property
    def millisievert(self) -> RadiationDoseEquivalent: ...
    @property
    def mSv(self) -> RadiationDoseEquivalent: ...
    @property
    def microsievert(self) -> RadiationDoseEquivalent: ...

class RadiationDoseEquivalent(TypedVariable):
    """Type-safe radiation dose equivalent variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> RadiationDoseEquivalentSetter:
        """
        Create a radiation dose equivalent setter for fluent unit assignment.
        
        Example:
            radiationdoseequivalent.set(100).rem
            radiationdoseequivalent.set(100).sievert
            radiationdoseequivalent.set(100).millisievert
        """
        ...

# ============================================================================
# RADIATION EXPOSURE
# ============================================================================

class RadiationExposureSetter(TypeSafeSetter):
    """Radiation Exposure-specific setter with only radiation exposure unit properties."""
    
    def __init__(self, variable: RadiationExposure, value: float) -> None: ...
    
    # All radiation exposure unit properties - provides fluent API with full type hints
    @property
    def coulomb_per_kilogram(self) -> RadiationExposure: ...
    @property
    def D_unit(self) -> RadiationExposure: ...
    @property
    def pastille_dose_B_unit(self) -> RadiationExposure: ...
    @property
    def r_entgen(self) -> RadiationExposure: ...
    @property
    def R(self) -> RadiationExposure: ...

class RadiationExposure(TypedVariable):
    """Type-safe radiation exposure variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> RadiationExposureSetter:
        """
        Create a radiation exposure setter for fluent unit assignment.
        
        Example:
            radiationexposure.set(100).coulomb_per_kilogram
            radiationexposure.set(100).D_unit
            radiationexposure.set(100).pastille_dose_B_unit
        """
        ...

# ============================================================================
# RADIOACTIVITY
# ============================================================================

class RadioactivitySetter(TypeSafeSetter):
    """Radioactivity-specific setter with only radioactivity unit properties."""
    
    def __init__(self, variable: Radioactivity, value: float) -> None: ...
    
    # All radioactivity unit properties - provides fluent API with full type hints
    @property
    def becquerel(self) -> Radioactivity: ...
    @property
    def Bq(self) -> Radioactivity: ...
    @property
    def curie(self) -> Radioactivity: ...
    @property
    def Ci(self) -> Radioactivity: ...
    @property
    def Mache_unit(self) -> Radioactivity: ...
    @property
    def rutherford(self) -> Radioactivity: ...
    @property
    def Rd(self) -> Radioactivity: ...
    @property
    def stat(self) -> Radioactivity: ...
    @property
    def kilobecquerel(self) -> Radioactivity: ...
    @property
    def kBq(self) -> Radioactivity: ...
    @property
    def megabecquerel(self) -> Radioactivity: ...
    @property
    def MBq(self) -> Radioactivity: ...
    @property
    def gigabecquerel(self) -> Radioactivity: ...
    @property
    def GBq(self) -> Radioactivity: ...

class Radioactivity(TypedVariable):
    """Type-safe radioactivity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> RadioactivitySetter:
        """
        Create a radioactivity setter for fluent unit assignment.
        
        Example:
            radioactivity.set(100).becquerel
            radioactivity.set(100).curie
            radioactivity.set(100).Mache_unit
        """
        ...

# ============================================================================
# SECOND MOMENT OF AREA
# ============================================================================

class SecondMomentOfAreaSetter(TypeSafeSetter):
    """Second Moment of Area-specific setter with only second moment of area unit properties."""
    
    def __init__(self, variable: SecondMomentOfArea, value: float) -> None: ...
    
    # All second moment of area unit properties - provides fluent API with full type hints
    @property
    def inch_quadrupled(self) -> SecondMomentOfArea: ...
    @property
    def centimeter_quadrupled(self) -> SecondMomentOfArea: ...
    @property
    def foot_quadrupled(self) -> SecondMomentOfArea: ...
    @property
    def meter_quadrupled(self) -> SecondMomentOfArea: ...

class SecondMomentOfArea(TypedVariable):
    """Type-safe second moment of area variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SecondMomentOfAreaSetter:
        """
        Create a second moment of area setter for fluent unit assignment.
        
        Example:
            secondmomentofarea.set(100).inch_quadrupled
            secondmomentofarea.set(100).centimeter_quadrupled
            secondmomentofarea.set(100).foot_quadrupled
        """
        ...

# ============================================================================
# SECOND RADIATION CONSTANT (PLANCK)
# ============================================================================

class SecondRadiationConstantPlanckSetter(TypeSafeSetter):
    """Second Radiation Constant (Planck)-specific setter with only second radiation constant (planck) unit properties."""
    
    def __init__(self, variable: SecondRadiationConstantPlanck, value: float) -> None: ...
    
    # All second radiation constant (planck) unit properties - provides fluent API with full type hints
    @property
    def meter_kelvin(self) -> SecondRadiationConstantPlanck: ...

class SecondRadiationConstantPlanck(TypedVariable):
    """Type-safe second radiation constant (planck) variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SecondRadiationConstantPlanckSetter:
        """
        Create a second radiation constant (planck) setter for fluent unit assignment.
        
        Example:
            secondradiationconstantplanck.set(100).meter_kelvin
        """
        ...

# ============================================================================
# SPECIFIC ENTHALPY
# ============================================================================

class SpecificEnthalpySetter(TypeSafeSetter):
    """Specific Enthalpy-specific setter with only specific enthalpy unit properties."""
    
    def __init__(self, variable: SpecificEnthalpy, value: float) -> None: ...
    
    # All specific enthalpy unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_mean_per_pound(self) -> SpecificEnthalpy: ...
    @property
    def British_thermal_unit_per_pound(self) -> SpecificEnthalpy: ...
    @property
    def calorie_per_gram(self) -> SpecificEnthalpy: ...
    @property
    def Chu_per_pound(self) -> SpecificEnthalpy: ...
    @property
    def joule_per_kilogram(self) -> SpecificEnthalpy: ...
    @property
    def kilojoule_per_kilogram(self) -> SpecificEnthalpy: ...

class SpecificEnthalpy(TypedVariable):
    """Type-safe specific enthalpy variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificEnthalpySetter:
        """
        Create a specific enthalpy setter for fluent unit assignment.
        
        Example:
            specificenthalpy.set(100).British_thermal_unit_mean_per_pound
            specificenthalpy.set(100).British_thermal_unit_per_pound
            specificenthalpy.set(100).calorie_per_gram
        """
        ...

# ============================================================================
# SPECIFIC GRAVITY
# ============================================================================

class SpecificGravitySetter(TypeSafeSetter):
    """Specific Gravity-specific setter with only specific gravity unit properties."""
    
    def __init__(self, variable: SpecificGravity, value: float) -> None: ...
    
    # All specific gravity unit properties - provides fluent API with full type hints
    @property
    def Dimensionless(self) -> SpecificGravity: ...
    @property
    def Dmls(self) -> SpecificGravity: ...

class SpecificGravity(TypedVariable):
    """Type-safe specific gravity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificGravitySetter:
        """
        Create a specific gravity setter for fluent unit assignment.
        
        Example:
            specificgravity.set(100).Dimensionless
        """
        ...

# ============================================================================
# SPECIFIC HEAT CAPACITY (CONSTANT PRESSURE)
# ============================================================================

class SpecificHeatCapacityConstantPressureSetter(TypeSafeSetter):
    """Specific Heat Capacity (Constant Pressure)-specific setter with only specific heat capacity (constant pressure) unit properties."""
    
    def __init__(self, variable: SpecificHeatCapacityConstantPressure, value: float) -> None: ...
    
    # All specific heat capacity (constant pressure) unit properties - provides fluent API with full type hints
    @property
    def Btu_per_pound_per_degree_Fahrenheit_or_degree_Rankine(self) -> SpecificHeatCapacityConstantPressure: ...
    @property
    def calories_per_gram_per_kelvin_or_degree_Celsius(self) -> SpecificHeatCapacityConstantPressure: ...
    @property
    def joules_per_kilogram_per_kelvin_or_degree_Celsius(self) -> SpecificHeatCapacityConstantPressure: ...

class SpecificHeatCapacityConstantPressure(TypedVariable):
    """Type-safe specific heat capacity (constant pressure) variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificHeatCapacityConstantPressureSetter:
        """
        Create a specific heat capacity (constant pressure) setter for fluent unit assignment.
        
        Example:
            specificheatcapacityconstantpressure.set(100).Btu_per_pound_per_degree_Fahrenheit_or_degree_Rankine
            specificheatcapacityconstantpressure.set(100).calories_per_gram_per_kelvin_or_degree_Celsius
            specificheatcapacityconstantpressure.set(100).joules_per_kilogram_per_kelvin_or_degree_Celsius
        """
        ...

# ============================================================================
# SPECIFIC LENGTH
# ============================================================================

class SpecificLengthSetter(TypeSafeSetter):
    """Specific Length-specific setter with only specific length unit properties."""
    
    def __init__(self, variable: SpecificLength, value: float) -> None: ...
    
    # All specific length unit properties - provides fluent API with full type hints
    @property
    def centimeter_per_gram(self) -> SpecificLength: ...
    @property
    def cotton_count(self) -> SpecificLength: ...
    @property
    def cc(self) -> SpecificLength: ...
    @property
    def ft_per_pound(self) -> SpecificLength: ...
    @property
    def meters_per_kilogram(self) -> SpecificLength: ...
    @property
    def newton_meter(self) -> SpecificLength: ...
    @property
    def Nm(self) -> SpecificLength: ...
    @property
    def worsted(self) -> SpecificLength: ...

class SpecificLength(TypedVariable):
    """Type-safe specific length variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificLengthSetter:
        """
        Create a specific length setter for fluent unit assignment.
        
        Example:
            specificlength.set(100).centimeter_per_gram
            specificlength.set(100).cotton_count
            specificlength.set(100).ft_per_pound
        """
        ...

# ============================================================================
# SPECIFIC SURFACE
# ============================================================================

class SpecificSurfaceSetter(TypeSafeSetter):
    """Specific Surface-specific setter with only specific surface unit properties."""
    
    def __init__(self, variable: SpecificSurface, value: float) -> None: ...
    
    # All specific surface unit properties - provides fluent API with full type hints
    @property
    def square_centimeter_per_gram(self) -> SpecificSurface: ...
    @property
    def square_foot_per_kilogram(self) -> SpecificSurface: ...
    @property
    def ft_2_kg(self) -> SpecificSurface: ...
    @property
    def sq_ft_kg(self) -> SpecificSurface: ...
    @property
    def square_foot_per_pound(self) -> SpecificSurface: ...
    @property
    def ft_2_lb(self) -> SpecificSurface: ...
    @property
    def sq_ft_lb(self) -> SpecificSurface: ...
    @property
    def square_meter_per_gram(self) -> SpecificSurface: ...
    @property
    def square_meter_per_kilogram(self) -> SpecificSurface: ...

class SpecificSurface(TypedVariable):
    """Type-safe specific surface variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificSurfaceSetter:
        """
        Create a specific surface setter for fluent unit assignment.
        
        Example:
            specificsurface.set(100).square_centimeter_per_gram
            specificsurface.set(100).square_foot_per_kilogram
            specificsurface.set(100).square_foot_per_pound
        """
        ...

# ============================================================================
# SPECIFIC VOLUME
# ============================================================================

class SpecificVolumeSetter(TypeSafeSetter):
    """Specific Volume-specific setter with only specific volume unit properties."""
    
    def __init__(self, variable: SpecificVolume, value: float) -> None: ...
    
    # All specific volume unit properties - provides fluent API with full type hints
    @property
    def cubic_centimeter_per_gram(self) -> SpecificVolume: ...
    @property
    def cm_3_g(self) -> SpecificVolume: ...
    @property
    def cc_g(self) -> SpecificVolume: ...
    @property
    def cubic_foot_per_kilogram(self) -> SpecificVolume: ...
    @property
    def ft_3_kg(self) -> SpecificVolume: ...
    @property
    def cft_kg(self) -> SpecificVolume: ...
    @property
    def cubic_foot_per_pound(self) -> SpecificVolume: ...
    @property
    def ft_3_lb(self) -> SpecificVolume: ...
    @property
    def cft_lb(self) -> SpecificVolume: ...
    @property
    def cubic_meter_per_kilogram(self) -> SpecificVolume: ...

class SpecificVolume(TypedVariable):
    """Type-safe specific volume variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificVolumeSetter:
        """
        Create a specific volume setter for fluent unit assignment.
        
        Example:
            specificvolume.set(100).cubic_centimeter_per_gram
            specificvolume.set(100).cubic_foot_per_kilogram
            specificvolume.set(100).cubic_foot_per_pound
        """
        ...

# ============================================================================
# STRESS
# ============================================================================

class StressSetter(TypeSafeSetter):
    """Stress-specific setter with only stress unit properties."""
    
    def __init__(self, variable: Stress, value: float) -> None: ...
    
    # All stress unit properties - provides fluent API with full type hints
    @property
    def dyne_per_square_centimeter(self) -> Stress: ...
    @property
    def gigapascal(self) -> Stress: ...
    @property
    def GPa(self) -> Stress: ...
    @property
    def hectopascal(self) -> Stress: ...
    @property
    def hPa(self) -> Stress: ...
    @property
    def kilogram_force_per_square_centimeter(self) -> Stress: ...
    @property
    def at(self) -> Stress: ...
    @property
    def kg_f_cm_2(self) -> Stress: ...
    @property
    def kilogram_force_per_square_meter(self) -> Stress: ...
    @property
    def kip_force_per_square_inch(self) -> Stress: ...
    @property
    def KSI(self) -> Stress: ...
    @property
    def ksi(self) -> Stress: ...
    @property
    def kip_f_in_2(self) -> Stress: ...
    @property
    def megapascal(self) -> Stress: ...
    @property
    def MPa(self) -> Stress: ...
    @property
    def newton_per_square_meter(self) -> Stress: ...
    @property
    def ounce_force_per_square_inch(self) -> Stress: ...
    @property
    def OSI(self) -> Stress: ...
    @property
    def osi(self) -> Stress: ...
    @property
    def oz_f_in_2(self) -> Stress: ...
    @property
    def pascal(self) -> Stress: ...
    @property
    def Pa(self) -> Stress: ...
    @property
    def pound_force_per_square_foot(self) -> Stress: ...
    @property
    def PSF(self) -> Stress: ...
    @property
    def psf(self) -> Stress: ...
    @property
    def lb_f_ft_2(self) -> Stress: ...
    @property
    def pound_force_per_square_inch(self) -> Stress: ...
    @property
    def psi(self) -> Stress: ...

class Stress(TypedVariable):
    """Type-safe stress variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> StressSetter:
        """
        Create a stress setter for fluent unit assignment.
        
        Example:
            stress.set(100).dyne_per_square_centimeter
            stress.set(100).gigapascal
            stress.set(100).hectopascal
        """
        ...

# ============================================================================
# SURFACE MASS DENSITY
# ============================================================================

class SurfaceMassDensitySetter(TypeSafeSetter):
    """Surface Mass Density-specific setter with only surface mass density unit properties."""
    
    def __init__(self, variable: SurfaceMassDensity, value: float) -> None: ...
    
    # All surface mass density unit properties - provides fluent API with full type hints
    @property
    def gram_per_square_centimeter(self) -> SurfaceMassDensity: ...
    @property
    def gram_per_square_meter(self) -> SurfaceMassDensity: ...
    @property
    def kilogram_per_square_meter(self) -> SurfaceMassDensity: ...
    @property
    def pound_mass_per_square_foot(self) -> SurfaceMassDensity: ...
    @property
    def pound_mass_per_square_inch(self) -> SurfaceMassDensity: ...

class SurfaceMassDensity(TypedVariable):
    """Type-safe surface mass density variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SurfaceMassDensitySetter:
        """
        Create a surface mass density setter for fluent unit assignment.
        
        Example:
            surfacemassdensity.set(100).gram_per_square_centimeter
            surfacemassdensity.set(100).gram_per_square_meter
            surfacemassdensity.set(100).kilogram_per_square_meter
        """
        ...

# ============================================================================
# SURFACE TENSION
# ============================================================================

class SurfaceTensionSetter(TypeSafeSetter):
    """Surface Tension-specific setter with only surface tension unit properties."""
    
    def __init__(self, variable: SurfaceTension, value: float) -> None: ...
    
    # All surface tension unit properties - provides fluent API with full type hints
    @property
    def dyne_per_centimeter(self) -> SurfaceTension: ...
    @property
    def gram_force_per_centimeter(self) -> SurfaceTension: ...
    @property
    def newton_per_meter(self) -> SurfaceTension: ...
    @property
    def pound_force_per_foot(self) -> SurfaceTension: ...
    @property
    def pound_force_per_inch(self) -> SurfaceTension: ...

class SurfaceTension(TypedVariable):
    """Type-safe surface tension variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SurfaceTensionSetter:
        """
        Create a surface tension setter for fluent unit assignment.
        
        Example:
            surfacetension.set(100).dyne_per_centimeter
            surfacetension.set(100).gram_force_per_centimeter
            surfacetension.set(100).newton_per_meter
        """
        ...

# ============================================================================
# TEMPERATURE
# ============================================================================

class TemperatureSetter(TypeSafeSetter):
    """Temperature-specific setter with only temperature unit properties."""
    
    def __init__(self, variable: Temperature, value: float) -> None: ...
    
    # All temperature unit properties - provides fluent API with full type hints
    @property
    def degree_Celsius_unit_size(self) -> Temperature: ...
    @property
    def degree_Fahrenheit_unit_size(self) -> Temperature: ...
    @property
    def degree_R_aumur_unit_size(self) -> Temperature: ...
    @property
    def kelvin_absolute_scale(self) -> Temperature: ...
    @property
    def K(self) -> Temperature: ...
    @property
    def Rankine_absolute_scale(self) -> Temperature: ...

class Temperature(TypedVariable):
    """Type-safe temperature variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TemperatureSetter:
        """
        Create a temperature setter for fluent unit assignment.
        
        Example:
            temperature.set(100).degree_Celsius_unit_size
            temperature.set(100).degree_Fahrenheit_unit_size
            temperature.set(100).degree_R_aumur_unit_size
        """
        ...

# ============================================================================
# THERMAL CONDUCTIVITY
# ============================================================================

class ThermalConductivitySetter(TypeSafeSetter):
    """Thermal Conductivity-specific setter with only thermal conductivity unit properties."""
    
    def __init__(self, variable: ThermalConductivity, value: float) -> None: ...
    
    # All thermal conductivity unit properties - provides fluent API with full type hints
    @property
    def Btu_IT_per_inch_per_hour_per_degree_Fahrenheit(self) -> ThermalConductivity: ...
    @property
    def Btu_therm_per_foot_per_hour_per_degree_Fahrenheit(self) -> ThermalConductivity: ...
    @property
    def Btu_therm_per_inch_per_hour_per_degree_Fahrenheit(self) -> ThermalConductivity: ...
    @property
    def calorie_therm_per_centimeter_per_second_per_degree_Celsius(self) -> ThermalConductivity: ...
    @property
    def joule_per_second_per_centimeter_per_kelvin(self) -> ThermalConductivity: ...
    @property
    def watt_per_centimeter_per_kelvin(self) -> ThermalConductivity: ...
    @property
    def watt_per_meter_per_kelvin(self) -> ThermalConductivity: ...

class ThermalConductivity(TypedVariable):
    """Type-safe thermal conductivity variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ThermalConductivitySetter:
        """
        Create a thermal conductivity setter for fluent unit assignment.
        
        Example:
            thermalconductivity.set(100).Btu_IT_per_inch_per_hour_per_degree_Fahrenheit
            thermalconductivity.set(100).Btu_therm_per_foot_per_hour_per_degree_Fahrenheit
            thermalconductivity.set(100).Btu_therm_per_inch_per_hour_per_degree_Fahrenheit
        """
        ...

# ============================================================================
# TIME
# ============================================================================

class TimeSetter(TypeSafeSetter):
    """Time-specific setter with only time unit properties."""
    
    def __init__(self, variable: Time, value: float) -> None: ...
    
    # All time unit properties - provides fluent API with full type hints
    @property
    def blink(self) -> Time: ...
    @property
    def century(self) -> Time: ...
    @property
    def chronon_or_tempon(self) -> Time: ...
    @property
    def gigan_or_eon(self) -> Time: ...
    @property
    def Ga(self) -> Time: ...
    @property
    def eon(self) -> Time: ...
    @property
    def hour(self) -> Time: ...
    @property
    def h(self) -> Time: ...
    @property
    def hr(self) -> Time: ...
    @property
    def Julian_year(self) -> Time: ...
    @property
    def a_jul(self) -> Time: ...
    @property
    def yr(self) -> Time: ...
    @property
    def mean_solar_day(self) -> Time: ...
    @property
    def da(self) -> Time: ...
    @property
    def d(self) -> Time: ...
    @property
    def millenium(self) -> Time: ...
    @property
    def minute(self) -> Time: ...
    @property
    def min(self) -> Time: ...
    @property
    def second(self) -> Time: ...
    @property
    def s(self) -> Time: ...
    @property
    def shake(self) -> Time: ...
    @property
    def sidereal_year_1900_AD(self) -> Time: ...
    @property
    def a_sider(self) -> Time: ...
    @property
    def tropical_year(self) -> Time: ...
    @property
    def wink(self) -> Time: ...
    @property
    def year(self) -> Time: ...
    @property
    def a(self) -> Time: ...
    @property
    def y(self) -> Time: ...
    @property
    def millisecond(self) -> Time: ...
    @property
    def ms(self) -> Time: ...
    @property
    def microsecond(self) -> Time: ...
    @property
    def nanosecond(self) -> Time: ...
    @property
    def ns(self) -> Time: ...
    @property
    def picosecond(self) -> Time: ...
    @property
    def ps(self) -> Time: ...

class Time(TypedVariable):
    """Type-safe time variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TimeSetter:
        """
        Create a time setter for fluent unit assignment.
        
        Example:
            time.set(100).blink
            time.set(100).century
            time.set(100).chronon_or_tempon
        """
        ...

# ============================================================================
# TORQUE
# ============================================================================

class TorqueSetter(TypeSafeSetter):
    """Torque-specific setter with only torque unit properties."""
    
    def __init__(self, variable: Torque, value: float) -> None: ...
    
    # All torque unit properties - provides fluent API with full type hints
    @property
    def centimeter_kilogram_force(self) -> Torque: ...
    @property
    def dyne_centimeter(self) -> Torque: ...
    @property
    def foot_kilogram_force(self) -> Torque: ...
    @property
    def foot_pound_force(self) -> Torque: ...
    @property
    def foot_poundal(self) -> Torque: ...
    @property
    def in_pound_force(self) -> Torque: ...
    @property
    def inch_ounce_force(self) -> Torque: ...
    @property
    def meter_kilogram_force(self) -> Torque: ...
    @property
    def newton_centimeter(self) -> Torque: ...
    @property
    def newton_meter(self) -> Torque: ...

class Torque(TypedVariable):
    """Type-safe torque variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TorqueSetter:
        """
        Create a torque setter for fluent unit assignment.
        
        Example:
            torque.set(100).centimeter_kilogram_force
            torque.set(100).dyne_centimeter
            torque.set(100).foot_kilogram_force
        """
        ...

# ============================================================================
# TURBULENCE ENERGY DISSIPATION RATE
# ============================================================================

class TurbulenceEnergyDissipationRateSetter(TypeSafeSetter):
    """Turbulence Energy Dissipation Rate-specific setter with only turbulence energy dissipation rate unit properties."""
    
    def __init__(self, variable: TurbulenceEnergyDissipationRate, value: float) -> None: ...
    
    # All turbulence energy dissipation rate unit properties - provides fluent API with full type hints
    @property
    def square_foot_per_cubic_second(self) -> TurbulenceEnergyDissipationRate: ...
    @property
    def ft_2_s_3(self) -> TurbulenceEnergyDissipationRate: ...
    @property
    def sq_ft_sec_3(self) -> TurbulenceEnergyDissipationRate: ...
    @property
    def square_meter_per_cubic_second(self) -> TurbulenceEnergyDissipationRate: ...

class TurbulenceEnergyDissipationRate(TypedVariable):
    """Type-safe turbulence energy dissipation rate variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TurbulenceEnergyDissipationRateSetter:
        """
        Create a turbulence energy dissipation rate setter for fluent unit assignment.
        
        Example:
            turbulenceenergydissipationrate.set(100).square_foot_per_cubic_second
            turbulenceenergydissipationrate.set(100).square_meter_per_cubic_second
        """
        ...

# ============================================================================
# VELOCITY, ANGULAR
# ============================================================================

class VelocityAngularSetter(TypeSafeSetter):
    """Velocity, Angular-specific setter with only velocity, angular unit properties."""
    
    def __init__(self, variable: VelocityAngular, value: float) -> None: ...
    
    # All velocity, angular unit properties - provides fluent API with full type hints
    @property
    def degree_per_minute(self) -> VelocityAngular: ...
    @property
    def deg_min(self) -> VelocityAngular: ...
    @property
    def circ_min(self) -> VelocityAngular: ...
    @property
    def degree_per_second(self) -> VelocityAngular: ...
    @property
    def deg_s(self) -> VelocityAngular: ...
    @property
    def circ_s(self) -> VelocityAngular: ...
    @property
    def grade_per_minute(self) -> VelocityAngular: ...
    @property
    def gon_min(self) -> VelocityAngular: ...
    @property
    def grad_min(self) -> VelocityAngular: ...
    @property
    def radian_per_minute(self) -> VelocityAngular: ...
    @property
    def radian_per_second(self) -> VelocityAngular: ...
    @property
    def revolution_per_minute(self) -> VelocityAngular: ...
    @property
    def rev_m(self) -> VelocityAngular: ...
    @property
    def rpm(self) -> VelocityAngular: ...
    @property
    def revolution_per_second(self) -> VelocityAngular: ...
    @property
    def rev_s(self) -> VelocityAngular: ...
    @property
    def rps(self) -> VelocityAngular: ...
    @property
    def turn_per_minute(self) -> VelocityAngular: ...

class VelocityAngular(TypedVariable):
    """Type-safe velocity, angular variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VelocityAngularSetter:
        """
        Create a velocity, angular setter for fluent unit assignment.
        
        Example:
            velocityangular.set(100).degree_per_minute
            velocityangular.set(100).degree_per_second
            velocityangular.set(100).grade_per_minute
        """
        ...

# ============================================================================
# VELOCITY, LINEAR
# ============================================================================

class VelocityLinearSetter(TypeSafeSetter):
    """Velocity, Linear-specific setter with only velocity, linear unit properties."""
    
    def __init__(self, variable: VelocityLinear, value: float) -> None: ...
    
    # All velocity, linear unit properties - provides fluent API with full type hints
    @property
    def foot_per_hour(self) -> VelocityLinear: ...
    @property
    def ft_h(self) -> VelocityLinear: ...
    @property
    def ft_hr(self) -> VelocityLinear: ...
    @property
    def fph(self) -> VelocityLinear: ...
    @property
    def foot_per_minute(self) -> VelocityLinear: ...
    @property
    def ft_min(self) -> VelocityLinear: ...
    @property
    def fpm(self) -> VelocityLinear: ...
    @property
    def foot_per_second(self) -> VelocityLinear: ...
    @property
    def ft_s(self) -> VelocityLinear: ...
    @property
    def fps(self) -> VelocityLinear: ...
    @property
    def inch_per_second(self) -> VelocityLinear: ...
    @property
    def in_s(self) -> VelocityLinear: ...
    @property
    def ips(self) -> VelocityLinear: ...
    @property
    def international_knot(self) -> VelocityLinear: ...
    @property
    def knot(self) -> VelocityLinear: ...
    @property
    def kilometer_per_hour(self) -> VelocityLinear: ...
    @property
    def kilometer_per_second(self) -> VelocityLinear: ...
    @property
    def meter_per_second(self) -> VelocityLinear: ...
    @property
    def mile_per_hour(self) -> VelocityLinear: ...
    @property
    def mi_h(self) -> VelocityLinear: ...
    @property
    def mi_hr(self) -> VelocityLinear: ...
    @property
    def mph(self) -> VelocityLinear: ...

class VelocityLinear(TypedVariable):
    """Type-safe velocity, linear variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VelocityLinearSetter:
        """
        Create a velocity, linear setter for fluent unit assignment.
        
        Example:
            velocitylinear.set(100).foot_per_hour
            velocitylinear.set(100).foot_per_minute
            velocitylinear.set(100).foot_per_second
        """
        ...

# ============================================================================
# VISCOSITY, DYNAMIC
# ============================================================================

class ViscosityDynamicSetter(TypeSafeSetter):
    """Viscosity, Dynamic-specific setter with only viscosity, dynamic unit properties."""
    
    def __init__(self, variable: ViscosityDynamic, value: float) -> None: ...
    
    # All viscosity, dynamic unit properties - provides fluent API with full type hints
    @property
    def centipoise(self) -> ViscosityDynamic: ...
    @property
    def cP(self) -> ViscosityDynamic: ...
    @property
    def cPo(self) -> ViscosityDynamic: ...
    @property
    def dyne_second_per_square_centimeter(self) -> ViscosityDynamic: ...
    @property
    def kilopound_second_per_square_meter(self) -> ViscosityDynamic: ...
    @property
    def millipoise(self) -> ViscosityDynamic: ...
    @property
    def mP(self) -> ViscosityDynamic: ...
    @property
    def mPo(self) -> ViscosityDynamic: ...
    @property
    def newton_second_per_square_meter(self) -> ViscosityDynamic: ...
    @property
    def pascal_second(self) -> ViscosityDynamic: ...
    @property
    def Pa_s(self) -> ViscosityDynamic: ...
    @property
    def PI(self) -> ViscosityDynamic: ...
    @property
    def poise(self) -> ViscosityDynamic: ...
    @property
    def P(self) -> ViscosityDynamic: ...
    @property
    def Po(self) -> ViscosityDynamic: ...
    @property
    def pound_force_hour_per_square_foot(self) -> ViscosityDynamic: ...
    @property
    def lb_f_h_ft_2(self) -> ViscosityDynamic: ...
    @property
    def lb_hr_sq_ft(self) -> ViscosityDynamic: ...
    @property
    def pound_force_second_per_square_foot(self) -> ViscosityDynamic: ...
    @property
    def lb_f_s_ft_2(self) -> ViscosityDynamic: ...
    @property
    def lb_sec_sq_ft(self) -> ViscosityDynamic: ...

class ViscosityDynamic(TypedVariable):
    """Type-safe viscosity, dynamic variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ViscosityDynamicSetter:
        """
        Create a viscosity, dynamic setter for fluent unit assignment.
        
        Example:
            viscositydynamic.set(100).centipoise
            viscositydynamic.set(100).dyne_second_per_square_centimeter
            viscositydynamic.set(100).kilopound_second_per_square_meter
        """
        ...

# ============================================================================
# VISCOSITY, KINEMATIC
# ============================================================================

class ViscosityKinematicSetter(TypeSafeSetter):
    """Viscosity, Kinematic-specific setter with only viscosity, kinematic unit properties."""
    
    def __init__(self, variable: ViscosityKinematic, value: float) -> None: ...
    
    # All viscosity, kinematic unit properties - provides fluent API with full type hints
    @property
    def centistokes(self) -> ViscosityKinematic: ...
    @property
    def cSt(self) -> ViscosityKinematic: ...
    @property
    def millistokes(self) -> ViscosityKinematic: ...
    @property
    def mSt(self) -> ViscosityKinematic: ...
    @property
    def square_centimeter_per_second(self) -> ViscosityKinematic: ...
    @property
    def square_foot_per_hour(self) -> ViscosityKinematic: ...
    @property
    def ft_2_h(self) -> ViscosityKinematic: ...
    @property
    def ft_2_hr(self) -> ViscosityKinematic: ...
    @property
    def square_foot_per_second(self) -> ViscosityKinematic: ...
    @property
    def square_meters_per_second(self) -> ViscosityKinematic: ...
    @property
    def stokes(self) -> ViscosityKinematic: ...
    @property
    def St(self) -> ViscosityKinematic: ...

class ViscosityKinematic(TypedVariable):
    """Type-safe viscosity, kinematic variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ViscosityKinematicSetter:
        """
        Create a viscosity, kinematic setter for fluent unit assignment.
        
        Example:
            viscositykinematic.set(100).centistokes
            viscositykinematic.set(100).millistokes
            viscositykinematic.set(100).square_centimeter_per_second
        """
        ...

# ============================================================================
# VOLUME
# ============================================================================

class VolumeSetter(TypeSafeSetter):
    """Volume-specific setter with only volume unit properties."""
    
    def __init__(self, variable: Volume, value: float) -> None: ...
    
    # All volume unit properties - provides fluent API with full type hints
    @property
    def acre_foot(self) -> Volume: ...
    @property
    def acre_inch(self) -> Volume: ...
    @property
    def barrel_US_Liquid(self) -> Volume: ...
    @property
    def barrel_US_Petro(self) -> Volume: ...
    @property
    def bbl(self) -> Volume: ...
    @property
    def board_foot_measure(self) -> Volume: ...
    @property
    def BM(self) -> Volume: ...
    @property
    def fbm(self) -> Volume: ...
    @property
    def bushel_US_Dry(self) -> Volume: ...
    @property
    def centiliter(self) -> Volume: ...
    @property
    def cl(self) -> Volume: ...
    @property
    def cL(self) -> Volume: ...
    @property
    def cord(self) -> Volume: ...
    @property
    def cd(self) -> Volume: ...
    @property
    def cord_foot(self) -> Volume: ...
    @property
    def cubic_centimeter(self) -> Volume: ...
    @property
    def cm_3(self) -> Volume: ...
    @property
    def cc(self) -> Volume: ...
    @property
    def cubic_decameter(self) -> Volume: ...
    @property
    def cubic_decimeter(self) -> Volume: ...
    @property
    def cubic_foot(self) -> Volume: ...
    @property
    def cu_ft(self) -> Volume: ...
    @property
    def ft_3(self) -> Volume: ...
    @property
    def cubic_inch(self) -> Volume: ...
    @property
    def cu_in(self) -> Volume: ...
    @property
    def in_3(self) -> Volume: ...
    @property
    def cubic_kilometer(self) -> Volume: ...
    @property
    def cubic_meter(self) -> Volume: ...
    @property
    def cubic_micrometer(self) -> Volume: ...
    @property
    def cubic_mile_US_Intl(self) -> Volume: ...
    @property
    def cubic_millimeter(self) -> Volume: ...
    @property
    def cubic_yard(self) -> Volume: ...
    @property
    def cu_yd(self) -> Volume: ...
    @property
    def yd_3(self) -> Volume: ...
    @property
    def decast_re(self) -> Volume: ...
    @property
    def dast(self) -> Volume: ...
    @property
    def deciliter(self) -> Volume: ...
    @property
    def dl(self) -> Volume: ...
    @property
    def dL(self) -> Volume: ...
    @property
    def fluid_drachm_UK(self) -> Volume: ...
    @property
    def fluid_dram_US(self) -> Volume: ...
    @property
    def fluid_ounce_US(self) -> Volume: ...
    @property
    def gallon_Imperial_UK(self) -> Volume: ...
    @property
    def gal_UK(self) -> Volume: ...
    @property
    def Imp_gal(self) -> Volume: ...
    @property
    def gallon_US_Dry(self) -> Volume: ...
    @property
    def gallon_US_Liquid(self) -> Volume: ...
    @property
    def gal(self) -> Volume: ...
    @property
    def last(self) -> Volume: ...
    @property
    def liter(self) -> Volume: ...
    @property
    def _1(self) -> Volume: ...
    @property
    def L(self) -> Volume: ...
    @property
    def microliter(self) -> Volume: ...
    @property
    def mu_l(self) -> Volume: ...
    @property
    def mu_L(self) -> Volume: ...
    @property
    def milliliter(self) -> Volume: ...
    @property
    def ml(self) -> Volume: ...
    @property
    def Mohr_centicube(self) -> Volume: ...
    @property
    def pint_UK(self) -> Volume: ...
    @property
    def pint_US_Dry(self) -> Volume: ...
    @property
    def pint_US_Liquid(self) -> Volume: ...
    @property
    def pt(self) -> Volume: ...
    @property
    def quart_US_Dry(self) -> Volume: ...
    @property
    def st_re(self) -> Volume: ...
    @property
    def st(self) -> Volume: ...
    @property
    def tablespoon_Metric(self) -> Volume: ...
    @property
    def tablespoon_US(self) -> Volume: ...
    @property
    def tbsp(self) -> Volume: ...
    @property
    def teaspoon_US(self) -> Volume: ...
    @property
    def tsp(self) -> Volume: ...

class Volume(TypedVariable):
    """Type-safe volume variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumeSetter:
        """
        Create a volume setter for fluent unit assignment.
        
        Example:
            volume.set(100).acre_foot
            volume.set(100).acre_inch
            volume.set(100).barrel_US_Liquid
        """
        ...

# ============================================================================
# VOLUME FRACTION OF "I"
# ============================================================================

class VolumeFractionOfISetter(TypeSafeSetter):
    """Volume Fraction of "i"-specific setter with only volume fraction of "i" unit properties."""
    
    def __init__(self, variable: VolumeFractionOfI, value: float) -> None: ...
    
    # All volume fraction of "i" unit properties - provides fluent API with full type hints
    @property
    def cubic_centimeters_of_i_per_cubic_meter_total(self) -> VolumeFractionOfI: ...
    @property
    def cm_i_3_m_3(self) -> VolumeFractionOfI: ...
    @property
    def cc_i_m_3(self) -> VolumeFractionOfI: ...
    @property
    def cubic_foot_of_i_per_cubic_foot_total(self) -> VolumeFractionOfI: ...
    @property
    def ft_i_3_ft_3(self) -> VolumeFractionOfI: ...
    @property
    def cft_i_cft(self) -> VolumeFractionOfI: ...
    @property
    def cubic_meters_of_i_per_cubic_meter_total(self) -> VolumeFractionOfI: ...
    @property
    def gallons_of_i_per_gallon_total(self) -> VolumeFractionOfI: ...

class VolumeFractionOfI(TypedVariable):
    """Type-safe volume fraction of "i" variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumeFractionOfISetter:
        """
        Create a volume fraction of "i" setter for fluent unit assignment.
        
        Example:
            volumefractionofi.set(100).cubic_centimeters_of_i_per_cubic_meter_total
            volumefractionofi.set(100).cubic_foot_of_i_per_cubic_foot_total
            volumefractionofi.set(100).cubic_meters_of_i_per_cubic_meter_total
        """
        ...

# ============================================================================
# VOLUMETRIC CALORIFIC (HEATING) VALUE
# ============================================================================

class VolumetricCalorificHeatingValueSetter(TypeSafeSetter):
    """Volumetric Calorific (Heating) Value-specific setter with only volumetric calorific (heating) value unit properties."""
    
    def __init__(self, variable: VolumetricCalorificHeatingValue, value: float) -> None: ...
    
    # All volumetric calorific (heating) value unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_cubic_foot(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def Btu_ft_3(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def Btu_cft(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def British_thermal_unit_per_gallon_UK(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def British_thermal_unit_per_gallon_US(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def calorie_per_cubic_centimeter(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def cal_cm_3(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def cal_cc(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def Chu_per_cubic_foot(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def Chu_ft_3(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def Chu_cft(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def joule_per_cubic_meter(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def kilocalorie_per_cubic_foot(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def kcal_ft_3(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def kcal_cft(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def kilocalorie_per_cubic_meter(self) -> VolumetricCalorificHeatingValue: ...
    @property
    def therm_100_K_Btu_per_cubic_foot(self) -> VolumetricCalorificHeatingValue: ...

class VolumetricCalorificHeatingValue(TypedVariable):
    """Type-safe volumetric calorific (heating) value variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricCalorificHeatingValueSetter:
        """
        Create a volumetric calorific (heating) value setter for fluent unit assignment.
        
        Example:
            volumetriccalorificheatingvalue.set(100).British_thermal_unit_per_cubic_foot
            volumetriccalorificheatingvalue.set(100).British_thermal_unit_per_gallon_UK
            volumetriccalorificheatingvalue.set(100).British_thermal_unit_per_gallon_US
        """
        ...

# ============================================================================
# VOLUMETRIC COEFFICIENT OF EXPANSION
# ============================================================================

class VolumetricCoefficientOfExpansionSetter(TypeSafeSetter):
    """Volumetric Coefficient of Expansion-specific setter with only volumetric coefficient of expansion unit properties."""
    
    def __init__(self, variable: VolumetricCoefficientOfExpansion, value: float) -> None: ...
    
    # All volumetric coefficient of expansion unit properties - provides fluent API with full type hints
    @property
    def gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def g_cm_3_K(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def g_cc_circ_C(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def kg_m_3_K(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def kg_m_3_circ_C(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankine(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def lb_ft_3_circ_R(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def lb_cft_circ_F(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def pound_per_cubic_foot_per_kelvin_or_degree_Celsius(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def lb_ft_3_K(self) -> VolumetricCoefficientOfExpansion: ...
    @property
    def lb_cft_circ_C(self) -> VolumetricCoefficientOfExpansion: ...

class VolumetricCoefficientOfExpansion(TypedVariable):
    """Type-safe volumetric coefficient of expansion variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricCoefficientOfExpansionSetter:
        """
        Create a volumetric coefficient of expansion setter for fluent unit assignment.
        
        Example:
            volumetriccoefficientofexpansion.set(100).gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius
            volumetriccoefficientofexpansion.set(100).kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius
            volumetriccoefficientofexpansion.set(100).pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankine
        """
        ...

# ============================================================================
# VOLUMETRIC FLOW RATE
# ============================================================================

class VolumetricFlowRateSetter(TypeSafeSetter):
    """Volumetric Flow Rate-specific setter with only volumetric flow rate unit properties."""
    
    def __init__(self, variable: VolumetricFlowRate, value: float) -> None: ...
    
    # All volumetric flow rate unit properties - provides fluent API with full type hints
    @property
    def cubic_feet_per_day(self) -> VolumetricFlowRate: ...
    @property
    def ft_3_d(self) -> VolumetricFlowRate: ...
    @property
    def cft_da(self) -> VolumetricFlowRate: ...
    @property
    def cfd(self) -> VolumetricFlowRate: ...
    @property
    def cubic_feet_per_hour(self) -> VolumetricFlowRate: ...
    @property
    def ft_3_h(self) -> VolumetricFlowRate: ...
    @property
    def cft_hr(self) -> VolumetricFlowRate: ...
    @property
    def cfh(self) -> VolumetricFlowRate: ...
    @property
    def cubic_feet_per_minute(self) -> VolumetricFlowRate: ...
    @property
    def ft_3_min(self) -> VolumetricFlowRate: ...
    @property
    def cft_min(self) -> VolumetricFlowRate: ...
    @property
    def cfm(self) -> VolumetricFlowRate: ...
    @property
    def cubic_feet_per_second(self) -> VolumetricFlowRate: ...
    @property
    def ft_3_s(self) -> VolumetricFlowRate: ...
    @property
    def cft_sec(self) -> VolumetricFlowRate: ...
    @property
    def cfs(self) -> VolumetricFlowRate: ...
    @property
    def cubic_meters_per_day(self) -> VolumetricFlowRate: ...
    @property
    def cubic_meters_per_hour(self) -> VolumetricFlowRate: ...
    @property
    def cubic_meters_per_minute(self) -> VolumetricFlowRate: ...
    @property
    def cubic_meters_per_second(self) -> VolumetricFlowRate: ...
    @property
    def gallons_per_day(self) -> VolumetricFlowRate: ...
    @property
    def gal_d(self) -> VolumetricFlowRate: ...
    @property
    def gpd(self) -> VolumetricFlowRate: ...
    @property
    def gal_da(self) -> VolumetricFlowRate: ...
    @property
    def gallons_per_hour(self) -> VolumetricFlowRate: ...
    @property
    def gal_h(self) -> VolumetricFlowRate: ...
    @property
    def gph(self) -> VolumetricFlowRate: ...
    @property
    def gal_hr(self) -> VolumetricFlowRate: ...
    @property
    def gallons_per_minute(self) -> VolumetricFlowRate: ...
    @property
    def gal_min(self) -> VolumetricFlowRate: ...
    @property
    def gpm(self) -> VolumetricFlowRate: ...
    @property
    def gallons_per_second(self) -> VolumetricFlowRate: ...
    @property
    def gal_s(self) -> VolumetricFlowRate: ...
    @property
    def gps(self) -> VolumetricFlowRate: ...
    @property
    def gal_sec(self) -> VolumetricFlowRate: ...
    @property
    def liters_per_day(self) -> VolumetricFlowRate: ...
    @property
    def liters_per_hour(self) -> VolumetricFlowRate: ...
    @property
    def liters_per_minute(self) -> VolumetricFlowRate: ...
    @property
    def liters_per_second(self) -> VolumetricFlowRate: ...

class VolumetricFlowRate(TypedVariable):
    """Type-safe volumetric flow rate variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricFlowRateSetter:
        """
        Create a volumetric flow rate setter for fluent unit assignment.
        
        Example:
            volumetricflowrate.set(100).cubic_feet_per_day
            volumetricflowrate.set(100).cubic_feet_per_hour
            volumetricflowrate.set(100).cubic_feet_per_minute
        """
        ...

# ============================================================================
# VOLUMETRIC FLUX
# ============================================================================

class VolumetricFluxSetter(TypeSafeSetter):
    """Volumetric Flux-specific setter with only volumetric flux unit properties."""
    
    def __init__(self, variable: VolumetricFlux, value: float) -> None: ...
    
    # All volumetric flux unit properties - provides fluent API with full type hints
    @property
    def cubic_feet_per_square_foot_per_day(self) -> VolumetricFlux: ...
    @property
    def ft_3_left_ft_2_dright(self) -> VolumetricFlux: ...
    @property
    def cft_sqft_da(self) -> VolumetricFlux: ...
    @property
    def cubic_feet_per_square_foot_per_hour(self) -> VolumetricFlux: ...
    @property
    def ft_3_left_ft_2_hright(self) -> VolumetricFlux: ...
    @property
    def cft_sqft_hr(self) -> VolumetricFlux: ...
    @property
    def cubic_feet_per_square_foot_per_minute(self) -> VolumetricFlux: ...
    @property
    def ft_3_left_ft_2_min_right(self) -> VolumetricFlux: ...
    @property
    def cft_sqft_min(self) -> VolumetricFlux: ...
    @property
    def cubic_feet_per_square_foot_per_second(self) -> VolumetricFlux: ...
    @property
    def ft_3_left_ft_2_sright(self) -> VolumetricFlux: ...
    @property
    def cft_sqft_sec(self) -> VolumetricFlux: ...
    @property
    def cubic_meters_per_square_meter_per_day(self) -> VolumetricFlux: ...
    @property
    def cubic_meters_per_square_meter_per_hour(self) -> VolumetricFlux: ...
    @property
    def cubic_meters_per_square_meter_per_minute(self) -> VolumetricFlux: ...
    @property
    def cubic_meters_per_square_meter_per_second(self) -> VolumetricFlux: ...
    @property
    def gallons_per_square_foot_per_day(self) -> VolumetricFlux: ...
    @property
    def gal_left_ft_2_dright(self) -> VolumetricFlux: ...
    @property
    def gal_sqft_da(self) -> VolumetricFlux: ...
    @property
    def gallons_per_square_foot_per_hour(self) -> VolumetricFlux: ...
    @property
    def gal_left_ft_2_hright(self) -> VolumetricFlux: ...
    @property
    def gal_sqft_hr(self) -> VolumetricFlux: ...
    @property
    def gallons_per_square_foot_per_minute(self) -> VolumetricFlux: ...
    @property
    def gal_left_ft_2_minright(self) -> VolumetricFlux: ...
    @property
    def gal_sqft_min(self) -> VolumetricFlux: ...
    @property
    def gpm_sqft(self) -> VolumetricFlux: ...
    @property
    def gallons_per_square_foot_per_second(self) -> VolumetricFlux: ...
    @property
    def gal_left_ft_2_sright(self) -> VolumetricFlux: ...
    @property
    def gal_sqft_sec(self) -> VolumetricFlux: ...
    @property
    def liters_per_square_meter_per_day(self) -> VolumetricFlux: ...
    @property
    def liters_per_square_meter_per_hour(self) -> VolumetricFlux: ...
    @property
    def liters_per_square_meter_per_minute(self) -> VolumetricFlux: ...
    @property
    def liters_per_square_meter_per_second(self) -> VolumetricFlux: ...

class VolumetricFlux(TypedVariable):
    """Type-safe volumetric flux variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricFluxSetter:
        """
        Create a volumetric flux setter for fluent unit assignment.
        
        Example:
            volumetricflux.set(100).cubic_feet_per_square_foot_per_day
            volumetricflux.set(100).cubic_feet_per_square_foot_per_hour
            volumetricflux.set(100).cubic_feet_per_square_foot_per_minute
        """
        ...

# ============================================================================
# VOLUMETRIC MASS FLOW RATE
# ============================================================================

class VolumetricMassFlowRateSetter(TypeSafeSetter):
    """Volumetric Mass Flow Rate-specific setter with only volumetric mass flow rate unit properties."""
    
    def __init__(self, variable: VolumetricMassFlowRate, value: float) -> None: ...
    
    # All volumetric mass flow rate unit properties - provides fluent API with full type hints
    @property
    def gram_per_second_per_cubic_centimeter(self) -> VolumetricMassFlowRate: ...
    @property
    def g_left_s_cm_3right(self) -> VolumetricMassFlowRate: ...
    @property
    def g_s_cc(self) -> VolumetricMassFlowRate: ...
    @property
    def g_cc_sec(self) -> VolumetricMassFlowRate: ...
    @property
    def kilogram_per_hour_per_cubic_foot(self) -> VolumetricMassFlowRate: ...
    @property
    def kg_h_ft_3(self) -> VolumetricMassFlowRate: ...
    @property
    def kg_hr_cft(self) -> VolumetricMassFlowRate: ...
    @property
    def kilogram_per_hour_per_cubic_meter(self) -> VolumetricMassFlowRate: ...
    @property
    def kg_h_m3(self) -> VolumetricMassFlowRate: ...
    @property
    def kg_hr_cu_m(self) -> VolumetricMassFlowRate: ...
    @property
    def kilogram_per_second_per_cubic_meter(self) -> VolumetricMassFlowRate: ...
    @property
    def kg_left_s_m_3right(self) -> VolumetricMassFlowRate: ...
    @property
    def kg_sec_cu_m(self) -> VolumetricMassFlowRate: ...
    @property
    def pound_per_hour_per_cubic_foot(self) -> VolumetricMassFlowRate: ...
    @property
    def lb_left_h_ft_3right(self) -> VolumetricMassFlowRate: ...
    @property
    def lb_hr_cft(self) -> VolumetricMassFlowRate: ...
    @property
    def PPH_cft(self) -> VolumetricMassFlowRate: ...
    @property
    def pound_per_minute_per_cubic_foot(self) -> VolumetricMassFlowRate: ...
    @property
    def lb_min_ft_3(self) -> VolumetricMassFlowRate: ...
    @property
    def lb_min_cft(self) -> VolumetricMassFlowRate: ...
    @property
    def pound_per_second_per_cubic_foot(self) -> VolumetricMassFlowRate: ...
    @property
    def b_s_ft_3(self) -> VolumetricMassFlowRate: ...
    @property
    def lb_sec_cft(self) -> VolumetricMassFlowRate: ...

class VolumetricMassFlowRate(TypedVariable):
    """Type-safe volumetric mass flow rate variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricMassFlowRateSetter:
        """
        Create a volumetric mass flow rate setter for fluent unit assignment.
        
        Example:
            volumetricmassflowrate.set(100).gram_per_second_per_cubic_centimeter
            volumetricmassflowrate.set(100).kilogram_per_hour_per_cubic_foot
            volumetricmassflowrate.set(100).kilogram_per_hour_per_cubic_meter
        """
        ...

# ============================================================================
# WAVENUMBER
# ============================================================================

class WavenumberSetter(TypeSafeSetter):
    """Wavenumber-specific setter with only wavenumber unit properties."""
    
    def __init__(self, variable: Wavenumber, value: float) -> None: ...
    
    # All wavenumber unit properties - provides fluent API with full type hints
    @property
    def diopter(self) -> Wavenumber: ...
    @property
    def D(self) -> Wavenumber: ...
    @property
    def kayser(self) -> Wavenumber: ...
    @property
    def K(self) -> Wavenumber: ...
    @property
    def reciprocal_meter(self) -> Wavenumber: ...

class Wavenumber(TypedVariable):
    """Type-safe wavenumber variable with expression capabilities."""
    
    _setter_class: type[TypeSafeSetter] | None
    _expected_dimension: DimensionSignature | None
    _default_unit_property: str | None
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> WavenumberSetter:
        """
        Create a wavenumber setter for fluent unit assignment.
        
        Example:
            wavenumber.set(100).diopter
            wavenumber.set(100).kayser
            wavenumber.set(100).reciprocal_meter
        """
        ...

# ============================================================================
# Module-level definitions
# ============================================================================

VARIABLE_DEFINITIONS: dict[str, dict[str, Any]]

def create_setter_class(class_name: str, variable_name: str, definition: dict[str, Any]) -> type: ...

def create_variable_class(class_name: str, definition: dict[str, Any], setter_class: type) -> type: ...

def get_consolidated_variable_modules() -> list[Any]: ...

# All classes are defined above - no additional exports needed in type stubs

