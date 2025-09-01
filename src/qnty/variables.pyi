"""
Type stubs for consolidated variables module - Complete Edition.

Provides complete type hints for IDE autocomplete and type checking
for the fluent API with dimension-specific unit properties for all
105 variable types with 810 total units.

Auto-generated from the same source of truth as consolidated_new.py.
"""

from typing import Dict, Any, Type, List, Tuple
from .dimension import DimensionSignature
from .variable import TypeSafeSetter
from .variable_types.typed_variable import TypedVariable

# ============================================================================
# SPECIAL DIMENSIONLESS VARIABLE
# ============================================================================

class DimensionlessSetter(TypeSafeSetter):
    """Dimensionless-specific setter with only dimensionless units."""
    
    def __init__(self, variable: 'Dimensionless', value: float) -> None: ...
    
    @property
    def dimensionless(self) -> 'Dimensionless': ...
    
    @property
    def unitless(self) -> 'Dimensionless': ...


class Dimensionless(TypedVariable):
    """Type-safe dimensionless variable with expression capabilities."""

    _setter_class: Type[DimensionlessSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> DimensionlessSetter:
        """
        Create a dimensionless setter for fluent unit assignment.
        
        Example:
            dimensionless.set(1.0).dimensionless
            dimensionless.set(2.5).unitless
        """
        ...


# ============================================================================
# ABSORBED RADIATION DOSE
# ============================================================================

class AbsorbedDoseSetter(TypeSafeSetter):
    """Absorbed Radiation Dose-specific setter with only absorbed radiation dose unit properties."""
    
    def __init__(self, variable: 'AbsorbedDose', value: float) -> None: ...
    
    # All absorbed radiation dose unit properties - provides fluent API with full type hints
    @property
    def erg_per_grams(self) -> 'AbsorbedDose': ...
    @property
    def gram_rads(self) -> 'AbsorbedDose': ...
    @property
    def grays(self) -> 'AbsorbedDose': ...
    @property
    def rads(self) -> 'AbsorbedDose': ...

class AbsorbedDose(TypedVariable):
    """Type-safe absorbed radiation dose variable with expression capabilities."""
    
    _setter_class: Type[AbsorbedDoseSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AbsorbedDoseSetter:
        """
        Create a absorbed radiation dose setter for fluent unit assignment.
        
        Example:
            absorbeddose.set(100).erg_per_grams
            absorbeddose.set(100).gram_rads
            absorbeddose.set(100).grays
        """
        ...

# ============================================================================
# ACCELERATION
# ============================================================================

class AccelerationSetter(TypeSafeSetter):
    """Acceleration-specific setter with only acceleration unit properties."""
    
    def __init__(self, variable: 'Acceleration', value: float) -> None: ...
    
    # All acceleration unit properties - provides fluent API with full type hints
    @property
    def foot_per_second_squareds(self) -> 'Acceleration': ...
    @property
    def meter_per_second_squareds(self) -> 'Acceleration': ...

class Acceleration(TypedVariable):
    """Type-safe acceleration variable with expression capabilities."""
    
    _setter_class: Type[AccelerationSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AccelerationSetter:
        """
        Create a acceleration setter for fluent unit assignment.
        
        Example:
            acceleration.set(100).foot_per_second_squareds
            acceleration.set(100).meter_per_second_squareds
        """
        ...

# ============================================================================
# ACTIVATION ENERGY
# ============================================================================

class ActivationEnergySetter(TypeSafeSetter):
    """Activation Energy-specific setter with only activation energy unit properties."""
    
    def __init__(self, variable: 'ActivationEnergy', value: float) -> None: ...
    
    # All activation energy unit properties - provides fluent API with full type hints
    @property
    def Btu_per_pound_moles(self) -> 'ActivationEnergy': ...
    @property
    def calorie_mean_per_gram_moles(self) -> 'ActivationEnergy': ...
    @property
    def joule_per_gram_moles(self) -> 'ActivationEnergy': ...
    @property
    def joule_per_kilogram_moles(self) -> 'ActivationEnergy': ...
    @property
    def kilocalorie_per_kilogram_moles(self) -> 'ActivationEnergy': ...

class ActivationEnergy(TypedVariable):
    """Type-safe activation energy variable with expression capabilities."""
    
    _setter_class: Type[ActivationEnergySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ActivationEnergySetter:
        """
        Create a activation energy setter for fluent unit assignment.
        
        Example:
            activationenergy.set(100).Btu_per_pound_moles
            activationenergy.set(100).calorie_mean_per_gram_moles
            activationenergy.set(100).joule_per_gram_moles
        """
        ...

# ============================================================================
# AMOUNT OF SUBSTANCE
# ============================================================================

class AmountOfSubstanceSetter(TypeSafeSetter):
    """Amount of Substance-specific setter with only amount of substance unit properties."""
    
    def __init__(self, variable: 'AmountOfSubstance', value: float) -> None: ...
    
    # All amount of substance unit properties - provides fluent API with full type hints
    @property
    def kilogram_mol_or_kmols(self) -> 'AmountOfSubstance': ...
    @property
    def mole_grams(self) -> 'AmountOfSubstance': ...
    @property
    def pound_moles(self) -> 'AmountOfSubstance': ...

class AmountOfSubstance(TypedVariable):
    """Type-safe amount of substance variable with expression capabilities."""
    
    _setter_class: Type[AmountOfSubstanceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AmountOfSubstanceSetter:
        """
        Create a amount of substance setter for fluent unit assignment.
        
        Example:
            amountofsubstance.set(100).kilogram_mol_or_kmols
            amountofsubstance.set(100).mole_grams
            amountofsubstance.set(100).pound_moles
        """
        ...

# ============================================================================
# ANGLE, PLANE
# ============================================================================

class AnglePlaneSetter(TypeSafeSetter):
    """Angle, Plane-specific setter with only angle, plane unit properties."""
    
    def __init__(self, variable: 'AnglePlane', value: float) -> None: ...
    
    # All angle, plane unit properties - provides fluent API with full type hints
    @property
    def degrees(self) -> 'AnglePlane': ...
    @property
    def gons(self) -> 'AnglePlane': ...
    @property
    def grades(self) -> 'AnglePlane': ...
    @property
    def minute_news(self) -> 'AnglePlane': ...
    @property
    def minute_of_angles(self) -> 'AnglePlane': ...
    @property
    def percents(self) -> 'AnglePlane': ...
    @property
    def plane_angles(self) -> 'AnglePlane': ...
    @property
    def quadrants(self) -> 'AnglePlane': ...
    @property
    def radians(self) -> 'AnglePlane': ...
    @property
    def right_angles(self) -> 'AnglePlane': ...
    @property
    def rounds(self) -> 'AnglePlane': ...
    @property
    def second_news(self) -> 'AnglePlane': ...
    @property
    def second_of_angles(self) -> 'AnglePlane': ...
    @property
    def thousandth_USs(self) -> 'AnglePlane': ...
    @property
    def turns(self) -> 'AnglePlane': ...

class AnglePlane(TypedVariable):
    """Type-safe angle, plane variable with expression capabilities."""
    
    _setter_class: Type[AnglePlaneSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AnglePlaneSetter:
        """
        Create a angle, plane setter for fluent unit assignment.
        
        Example:
            angleplane.set(100).degrees
            angleplane.set(100).gons
            angleplane.set(100).grades
        """
        ...

# ============================================================================
# ANGLE, SOLID
# ============================================================================

class AngleSolidSetter(TypeSafeSetter):
    """Angle, Solid-specific setter with only angle, solid unit properties."""
    
    def __init__(self, variable: 'AngleSolid', value: float) -> None: ...
    
    # All angle, solid unit properties - provides fluent API with full type hints
    @property
    def spats(self) -> 'AngleSolid': ...
    @property
    def square_degrees(self) -> 'AngleSolid': ...
    @property
    def square_gons(self) -> 'AngleSolid': ...
    @property
    def steradians(self) -> 'AngleSolid': ...

class AngleSolid(TypedVariable):
    """Type-safe angle, solid variable with expression capabilities."""
    
    _setter_class: Type[AngleSolidSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AngleSolidSetter:
        """
        Create a angle, solid setter for fluent unit assignment.
        
        Example:
            anglesolid.set(100).spats
            anglesolid.set(100).square_degrees
            anglesolid.set(100).square_gons
        """
        ...

# ============================================================================
# ANGULAR ACCELERATION
# ============================================================================

class AngularAccelerationSetter(TypeSafeSetter):
    """Angular Acceleration-specific setter with only angular acceleration unit properties."""
    
    def __init__(self, variable: 'AngularAcceleration', value: float) -> None: ...
    
    # All angular acceleration unit properties - provides fluent API with full type hints
    @property
    def radian_per_second_squareds(self) -> 'AngularAcceleration': ...
    @property
    def revolution_per_second_squareds(self) -> 'AngularAcceleration': ...
    @property
    def rpm_or_revolution_per_minute_per_minutes(self) -> 'AngularAcceleration': ...

class AngularAcceleration(TypedVariable):
    """Type-safe angular acceleration variable with expression capabilities."""
    
    _setter_class: Type[AngularAccelerationSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AngularAccelerationSetter:
        """
        Create a angular acceleration setter for fluent unit assignment.
        
        Example:
            angularacceleration.set(100).radian_per_second_squareds
            angularacceleration.set(100).revolution_per_second_squareds
            angularacceleration.set(100).rpm_or_revolution_per_minute_per_minutes
        """
        ...

# ============================================================================
# ANGULAR MOMENTUM
# ============================================================================

class AngularMomentumSetter(TypeSafeSetter):
    """Angular Momentum-specific setter with only angular momentum unit properties."""
    
    def __init__(self, variable: 'AngularMomentum', value: float) -> None: ...
    
    # All angular momentum unit properties - provides fluent API with full type hints
    @property
    def gram_centimeter_squared_per_seconds(self) -> 'AngularMomentum': ...
    @property
    def kilogram_meter_squared_per_seconds(self) -> 'AngularMomentum': ...
    @property
    def pound_force_square_foot_per_seconds(self) -> 'AngularMomentum': ...

class AngularMomentum(TypedVariable):
    """Type-safe angular momentum variable with expression capabilities."""
    
    _setter_class: Type[AngularMomentumSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AngularMomentumSetter:
        """
        Create a angular momentum setter for fluent unit assignment.
        
        Example:
            angularmomentum.set(100).gram_centimeter_squared_per_seconds
            angularmomentum.set(100).kilogram_meter_squared_per_seconds
            angularmomentum.set(100).pound_force_square_foot_per_seconds
        """
        ...

# ============================================================================
# AREA
# ============================================================================

class AreaSetter(TypeSafeSetter):
    """Area-specific setter with only area unit properties."""
    
    def __init__(self, variable: 'Area', value: float) -> None: ...
    
    # All area unit properties - provides fluent API with full type hints
    @property
    def acre_generals(self) -> 'Area': ...
    @property
    def ares(self) -> 'Area': ...
    @property
    def arpent_Quebecs(self) -> 'Area': ...
    @property
    def barns(self) -> 'Area': ...
    @property
    def circular_inchs(self) -> 'Area': ...
    @property
    def circular_mils(self) -> 'Area': ...
    @property
    def hectares(self) -> 'Area': ...
    @property
    def sheds(self) -> 'Area': ...
    @property
    def square_centimeters(self) -> 'Area': ...
    @property
    def square_chain_Ramsdens(self) -> 'Area': ...
    @property
    def square_chain_Survey_Gunter_s(self) -> 'Area': ...
    @property
    def square_decimeters(self) -> 'Area': ...
    @property
    def square_fermis(self) -> 'Area': ...
    @property
    def square_foots(self) -> 'Area': ...
    @property
    def square_hectometers(self) -> 'Area': ...
    @property
    def square_inchs(self) -> 'Area': ...
    @property
    def square_kilometers(self) -> 'Area': ...
    @property
    def square_league_statutes(self) -> 'Area': ...
    @property
    def square_meters(self) -> 'Area': ...
    @property
    def square_microns(self) -> 'Area': ...
    @property
    def square_mile_statutes(self) -> 'Area': ...
    @property
    def square_mile_US_surveys(self) -> 'Area': ...
    @property
    def square_millimeters(self) -> 'Area': ...
    @property
    def square_nanometers(self) -> 'Area': ...
    @property
    def square_yards(self) -> 'Area': ...
    @property
    def township_USs(self) -> 'Area': ...

class Area(TypedVariable):
    """Type-safe area variable with expression capabilities."""
    
    _setter_class: Type[AreaSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AreaSetter:
        """
        Create a area setter for fluent unit assignment.
        
        Example:
            area.set(100).acre_generals
            area.set(100).ares
            area.set(100).arpent_Quebecs
        """
        ...

# ============================================================================
# AREA PER UNIT VOLUME
# ============================================================================

class AreaPerUnitVolumeSetter(TypeSafeSetter):
    """Area per Unit Volume-specific setter with only area per unit volume unit properties."""
    
    def __init__(self, variable: 'AreaPerUnitVolume', value: float) -> None: ...
    
    # All area per unit volume unit properties - provides fluent API with full type hints
    @property
    def square_centimeter_per_cubic_centimeters(self) -> 'AreaPerUnitVolume': ...
    @property
    def square_foot_per_cubic_foots(self) -> 'AreaPerUnitVolume': ...
    @property
    def square_inch_per_cubic_inchs(self) -> 'AreaPerUnitVolume': ...
    @property
    def square_meter_per_cubic_meters(self) -> 'AreaPerUnitVolume': ...

class AreaPerUnitVolume(TypedVariable):
    """Type-safe area per unit volume variable with expression capabilities."""
    
    _setter_class: Type[AreaPerUnitVolumeSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AreaPerUnitVolumeSetter:
        """
        Create a area per unit volume setter for fluent unit assignment.
        
        Example:
            areaperunitvolume.set(100).square_centimeter_per_cubic_centimeters
            areaperunitvolume.set(100).square_foot_per_cubic_foots
            areaperunitvolume.set(100).square_inch_per_cubic_inchs
        """
        ...

# ============================================================================
# ATOMIC WEIGHT
# ============================================================================

class AtomicWeightSetter(TypeSafeSetter):
    """Atomic Weight-specific setter with only atomic weight unit properties."""
    
    def __init__(self, variable: 'AtomicWeight', value: float) -> None: ...
    
    # All atomic weight unit properties - provides fluent API with full type hints
    @property
    def atomic_mass_unit_12Cs(self) -> 'AtomicWeight': ...
    @property
    def grams_per_moles(self) -> 'AtomicWeight': ...
    @property
    def kilograms_per_kilomoles(self) -> 'AtomicWeight': ...
    @property
    def pounds_per_pound_moles(self) -> 'AtomicWeight': ...

class AtomicWeight(TypedVariable):
    """Type-safe atomic weight variable with expression capabilities."""
    
    _setter_class: Type[AtomicWeightSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> AtomicWeightSetter:
        """
        Create a atomic weight setter for fluent unit assignment.
        
        Example:
            atomicweight.set(100).atomic_mass_unit_12Cs
            atomicweight.set(100).grams_per_moles
            atomicweight.set(100).kilograms_per_kilomoles
        """
        ...

# ============================================================================
# CONCENTRATION
# ============================================================================

class ConcentrationSetter(TypeSafeSetter):
    """Concentration-specific setter with only concentration unit properties."""
    
    def __init__(self, variable: 'Concentration', value: float) -> None: ...
    
    # All concentration unit properties - provides fluent API with full type hints
    @property
    def grains_of_i_per_cubic_foots(self) -> 'Concentration': ...
    @property
    def grains_of_i_per_gallon_USs(self) -> 'Concentration': ...

class Concentration(TypedVariable):
    """Type-safe concentration variable with expression capabilities."""
    
    _setter_class: Type[ConcentrationSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ConcentrationSetter:
        """
        Create a concentration setter for fluent unit assignment.
        
        Example:
            concentration.set(100).grains_of_i_per_cubic_foots
            concentration.set(100).grains_of_i_per_gallon_USs
        """
        ...

# ============================================================================
# DYNAMIC FLUIDITY
# ============================================================================

class DynamicFluiditySetter(TypeSafeSetter):
    """Dynamic Fluidity-specific setter with only dynamic fluidity unit properties."""
    
    def __init__(self, variable: 'DynamicFluidity', value: float) -> None: ...
    
    # All dynamic fluidity unit properties - provides fluent API with full type hints
    @property
    def meter_seconds_per_kilograms(self) -> 'DynamicFluidity': ...
    @property
    def rhes(self) -> 'DynamicFluidity': ...
    @property
    def square_foot_per_pound_seconds(self) -> 'DynamicFluidity': ...
    @property
    def square_meters_per_newton_per_seconds(self) -> 'DynamicFluidity': ...

class DynamicFluidity(TypedVariable):
    """Type-safe dynamic fluidity variable with expression capabilities."""
    
    _setter_class: Type[DynamicFluiditySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> DynamicFluiditySetter:
        """
        Create a dynamic fluidity setter for fluent unit assignment.
        
        Example:
            dynamicfluidity.set(100).meter_seconds_per_kilograms
            dynamicfluidity.set(100).rhes
            dynamicfluidity.set(100).square_foot_per_pound_seconds
        """
        ...

# ============================================================================
# ELECTRIC CAPACITANCE
# ============================================================================

class ElectricCapacitanceSetter(TypeSafeSetter):
    """Electric Capacitance-specific setter with only electric capacitance unit properties."""
    
    def __init__(self, variable: 'ElectricCapacitance', value: float) -> None: ...
    
    # All electric capacitance unit properties - provides fluent API with full type hints
    @property
    def cms(self) -> 'ElectricCapacitance': ...
    @property
    def abfarads(self) -> 'ElectricCapacitance': ...
    @property
    def farads(self) -> 'ElectricCapacitance': ...
    @property
    def farad_intls(self) -> 'ElectricCapacitance': ...
    @property
    def jars(self) -> 'ElectricCapacitance': ...
    @property
    def puffs(self) -> 'ElectricCapacitance': ...
    @property
    def statfarads(self) -> 'ElectricCapacitance': ...

class ElectricCapacitance(TypedVariable):
    """Type-safe electric capacitance variable with expression capabilities."""
    
    _setter_class: Type[ElectricCapacitanceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricCapacitanceSetter:
        """
        Create a electric capacitance setter for fluent unit assignment.
        
        Example:
            electriccapacitance.set(100).cms
            electriccapacitance.set(100).abfarads
            electriccapacitance.set(100).farads
        """
        ...

# ============================================================================
# ELECTRIC CHARGE
# ============================================================================

class ElectricChargeSetter(TypeSafeSetter):
    """Electric Charge-specific setter with only electric charge unit properties."""
    
    def __init__(self, variable: 'ElectricCharge', value: float) -> None: ...
    
    # All electric charge unit properties - provides fluent API with full type hints
    @property
    def abcoulombs(self) -> 'ElectricCharge': ...
    @property
    def ampere_hours(self) -> 'ElectricCharge': ...
    @property
    def coulombs(self) -> 'ElectricCharge': ...
    @property
    def faraday_C12s(self) -> 'ElectricCharge': ...
    @property
    def franklins(self) -> 'ElectricCharge': ...
    @property
    def statcoulombs(self) -> 'ElectricCharge': ...
    @property
    def u_a_charges(self) -> 'ElectricCharge': ...

class ElectricCharge(TypedVariable):
    """Type-safe electric charge variable with expression capabilities."""
    
    _setter_class: Type[ElectricChargeSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricChargeSetter:
        """
        Create a electric charge setter for fluent unit assignment.
        
        Example:
            electriccharge.set(100).abcoulombs
            electriccharge.set(100).ampere_hours
            electriccharge.set(100).coulombs
        """
        ...

# ============================================================================
# ELECTRIC CURRENT INTENSITY
# ============================================================================

class ElectricCurrentIntensitySetter(TypeSafeSetter):
    """Electric Current Intensity-specific setter with only electric current intensity unit properties."""
    
    def __init__(self, variable: 'ElectricCurrentIntensity', value: float) -> None: ...
    
    # All electric current intensity unit properties - provides fluent API with full type hints
    @property
    def abamperes(self) -> 'ElectricCurrentIntensity': ...
    @property
    def ampere_intl_means(self) -> 'ElectricCurrentIntensity': ...
    @property
    def ampere_intl_USs(self) -> 'ElectricCurrentIntensity': ...
    @property
    def ampere_or_amps(self) -> 'ElectricCurrentIntensity': ...
    @property
    def biots(self) -> 'ElectricCurrentIntensity': ...
    @property
    def statamperes(self) -> 'ElectricCurrentIntensity': ...
    @property
    def u_a_or_currents(self) -> 'ElectricCurrentIntensity': ...

class ElectricCurrentIntensity(TypedVariable):
    """Type-safe electric current intensity variable with expression capabilities."""
    
    _setter_class: Type[ElectricCurrentIntensitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricCurrentIntensitySetter:
        """
        Create a electric current intensity setter for fluent unit assignment.
        
        Example:
            electriccurrentintensity.set(100).abamperes
            electriccurrentintensity.set(100).ampere_intl_means
            electriccurrentintensity.set(100).ampere_intl_USs
        """
        ...

# ============================================================================
# ELECTRIC DIPOLE MOMENT
# ============================================================================

class ElectricDipoleMomentSetter(TypeSafeSetter):
    """Electric Dipole Moment-specific setter with only electric dipole moment unit properties."""
    
    def __init__(self, variable: 'ElectricDipoleMoment', value: float) -> None: ...
    
    # All electric dipole moment unit properties - provides fluent API with full type hints
    @property
    def ampere_meter_seconds(self) -> 'ElectricDipoleMoment': ...
    @property
    def coulomb_meters(self) -> 'ElectricDipoleMoment': ...
    @property
    def debyes(self) -> 'ElectricDipoleMoment': ...
    @property
    def electron_meters(self) -> 'ElectricDipoleMoment': ...

class ElectricDipoleMoment(TypedVariable):
    """Type-safe electric dipole moment variable with expression capabilities."""
    
    _setter_class: Type[ElectricDipoleMomentSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricDipoleMomentSetter:
        """
        Create a electric dipole moment setter for fluent unit assignment.
        
        Example:
            electricdipolemoment.set(100).ampere_meter_seconds
            electricdipolemoment.set(100).coulomb_meters
            electricdipolemoment.set(100).debyes
        """
        ...

# ============================================================================
# ELECTRIC FIELD STRENGTH
# ============================================================================

class ElectricFieldStrengthSetter(TypeSafeSetter):
    """Electric Field Strength-specific setter with only electric field strength unit properties."""
    
    def __init__(self, variable: 'ElectricFieldStrength', value: float) -> None: ...
    
    # All electric field strength unit properties - provides fluent API with full type hints
    @property
    def volt_per_centimeters(self) -> 'ElectricFieldStrength': ...
    @property
    def volt_per_meters(self) -> 'ElectricFieldStrength': ...

class ElectricFieldStrength(TypedVariable):
    """Type-safe electric field strength variable with expression capabilities."""
    
    _setter_class: Type[ElectricFieldStrengthSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricFieldStrengthSetter:
        """
        Create a electric field strength setter for fluent unit assignment.
        
        Example:
            electricfieldstrength.set(100).volt_per_centimeters
            electricfieldstrength.set(100).volt_per_meters
        """
        ...

# ============================================================================
# ELECTRIC INDUCTANCE
# ============================================================================

class ElectricInductanceSetter(TypeSafeSetter):
    """Electric Inductance-specific setter with only electric inductance unit properties."""
    
    def __init__(self, variable: 'ElectricInductance', value: float) -> None: ...
    
    # All electric inductance unit properties - provides fluent API with full type hints
    @property
    def abhenrys(self) -> 'ElectricInductance': ...
    @property
    def cms(self) -> 'ElectricInductance': ...
    @property
    def henrys(self) -> 'ElectricInductance': ...
    @property
    def henry_intl_means(self) -> 'ElectricInductance': ...
    @property
    def henry_intl_USs(self) -> 'ElectricInductance': ...
    @property
    def mics(self) -> 'ElectricInductance': ...
    @property
    def stathenrys(self) -> 'ElectricInductance': ...

class ElectricInductance(TypedVariable):
    """Type-safe electric inductance variable with expression capabilities."""
    
    _setter_class: Type[ElectricInductanceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricInductanceSetter:
        """
        Create a electric inductance setter for fluent unit assignment.
        
        Example:
            electricinductance.set(100).abhenrys
            electricinductance.set(100).cms
            electricinductance.set(100).henrys
        """
        ...

# ============================================================================
# ELECTRIC POTENTIAL
# ============================================================================

class ElectricPotentialSetter(TypeSafeSetter):
    """Electric Potential-specific setter with only electric potential unit properties."""
    
    def __init__(self, variable: 'ElectricPotential', value: float) -> None: ...
    
    # All electric potential unit properties - provides fluent API with full type hints
    @property
    def abvolts(self) -> 'ElectricPotential': ...
    @property
    def statvolts(self) -> 'ElectricPotential': ...
    @property
    def u_a_potentials(self) -> 'ElectricPotential': ...
    @property
    def volts(self) -> 'ElectricPotential': ...
    @property
    def volt_intl_means(self) -> 'ElectricPotential': ...
    @property
    def volt_USs(self) -> 'ElectricPotential': ...

class ElectricPotential(TypedVariable):
    """Type-safe electric potential variable with expression capabilities."""
    
    _setter_class: Type[ElectricPotentialSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricPotentialSetter:
        """
        Create a electric potential setter for fluent unit assignment.
        
        Example:
            electricpotential.set(100).abvolts
            electricpotential.set(100).statvolts
            electricpotential.set(100).u_a_potentials
        """
        ...

# ============================================================================
# ELECTRIC RESISTANCE
# ============================================================================

class ElectricResistanceSetter(TypeSafeSetter):
    """Electric Resistance-specific setter with only electric resistance unit properties."""
    
    def __init__(self, variable: 'ElectricResistance', value: float) -> None: ...
    
    # All electric resistance unit properties - provides fluent API with full type hints
    @property
    def abohms(self) -> 'ElectricResistance': ...
    @property
    def jacobis(self) -> 'ElectricResistance': ...
    @property
    def lenzs(self) -> 'ElectricResistance': ...
    @property
    def ohms(self) -> 'ElectricResistance': ...
    @property
    def ohm_intl_means(self) -> 'ElectricResistance': ...
    @property
    def ohm_intl_USs(self) -> 'ElectricResistance': ...
    @property
    def ohm_legals(self) -> 'ElectricResistance': ...
    @property
    def preeces(self) -> 'ElectricResistance': ...
    @property
    def statohms(self) -> 'ElectricResistance': ...
    @property
    def wheatstones(self) -> 'ElectricResistance': ...

class ElectricResistance(TypedVariable):
    """Type-safe electric resistance variable with expression capabilities."""
    
    _setter_class: Type[ElectricResistanceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricResistanceSetter:
        """
        Create a electric resistance setter for fluent unit assignment.
        
        Example:
            electricresistance.set(100).abohms
            electricresistance.set(100).jacobis
            electricresistance.set(100).lenzs
        """
        ...

# ============================================================================
# ELECTRICAL CONDUCTANCE
# ============================================================================

class ElectricalConductanceSetter(TypeSafeSetter):
    """Electrical Conductance-specific setter with only electrical conductance unit properties."""
    
    def __init__(self, variable: 'ElectricalConductance', value: float) -> None: ...
    
    # All electrical conductance unit properties - provides fluent API with full type hints
    @property
    def emu_cgs(self) -> 'ElectricalConductance': ...
    @property
    def esu_cgs(self) -> 'ElectricalConductance': ...
    @property
    def mhos(self) -> 'ElectricalConductance': ...
    @property
    def microsiemens(self) -> 'ElectricalConductance': ...
    @property
    def siemens(self) -> 'ElectricalConductance': ...

class ElectricalConductance(TypedVariable):
    """Type-safe electrical conductance variable with expression capabilities."""
    
    _setter_class: Type[ElectricalConductanceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricalConductanceSetter:
        """
        Create a electrical conductance setter for fluent unit assignment.
        
        Example:
            electricalconductance.set(100).emu_cgs
            electricalconductance.set(100).esu_cgs
            electricalconductance.set(100).mhos
        """
        ...

# ============================================================================
# ELECTRICAL PERMITTIVITY
# ============================================================================

class ElectricalPermittivitySetter(TypeSafeSetter):
    """Electrical Permittivity-specific setter with only electrical permittivity unit properties."""
    
    def __init__(self, variable: 'ElectricalPermittivity', value: float) -> None: ...
    
    # All electrical permittivity unit properties - provides fluent API with full type hints
    @property
    def farad_per_meters(self) -> 'ElectricalPermittivity': ...

class ElectricalPermittivity(TypedVariable):
    """Type-safe electrical permittivity variable with expression capabilities."""
    
    _setter_class: Type[ElectricalPermittivitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricalPermittivitySetter:
        """
        Create a electrical permittivity setter for fluent unit assignment.
        
        Example:
            electricalpermittivity.set(100).farad_per_meters
        """
        ...

# ============================================================================
# ELECTRICAL RESISTIVITY
# ============================================================================

class ElectricalResistivitySetter(TypeSafeSetter):
    """Electrical Resistivity-specific setter with only electrical resistivity unit properties."""
    
    def __init__(self, variable: 'ElectricalResistivity', value: float) -> None: ...
    
    # All electrical resistivity unit properties - provides fluent API with full type hints
    @property
    def circular_mil_ohm_per_foots(self) -> 'ElectricalResistivity': ...
    @property
    def emu_cgs(self) -> 'ElectricalResistivity': ...
    @property
    def microhm_inchs(self) -> 'ElectricalResistivity': ...
    @property
    def ohm_centimeters(self) -> 'ElectricalResistivity': ...
    @property
    def ohm_meters(self) -> 'ElectricalResistivity': ...

class ElectricalResistivity(TypedVariable):
    """Type-safe electrical resistivity variable with expression capabilities."""
    
    _setter_class: Type[ElectricalResistivitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ElectricalResistivitySetter:
        """
        Create a electrical resistivity setter for fluent unit assignment.
        
        Example:
            electricalresistivity.set(100).circular_mil_ohm_per_foots
            electricalresistivity.set(100).emu_cgs
            electricalresistivity.set(100).microhm_inchs
        """
        ...

# ============================================================================
# ENERGY FLUX
# ============================================================================

class EnergyFluxSetter(TypeSafeSetter):
    """Energy Flux-specific setter with only energy flux unit properties."""
    
    def __init__(self, variable: 'EnergyFlux', value: float) -> None: ...
    
    # All energy flux unit properties - provides fluent API with full type hints
    @property
    def Btu_per_square_foot_per_hours(self) -> 'EnergyFlux': ...
    @property
    def calorie_per_square_centimeter_per_seconds(self) -> 'EnergyFlux': ...
    @property
    def Celsius_heat_units_Chu_per_square_foot_per_hours(self) -> 'EnergyFlux': ...
    @property
    def kilocalorie_per_square_foot_per_hours(self) -> 'EnergyFlux': ...
    @property
    def kilocalorie_per_square_meter_per_hours(self) -> 'EnergyFlux': ...
    @property
    def watt_per_square_meters(self) -> 'EnergyFlux': ...

class EnergyFlux(TypedVariable):
    """Type-safe energy flux variable with expression capabilities."""
    
    _setter_class: Type[EnergyFluxSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> EnergyFluxSetter:
        """
        Create a energy flux setter for fluent unit assignment.
        
        Example:
            energyflux.set(100).Btu_per_square_foot_per_hours
            energyflux.set(100).calorie_per_square_centimeter_per_seconds
            energyflux.set(100).Celsius_heat_units_Chu_per_square_foot_per_hours
        """
        ...

# ============================================================================
# ENERGY, HEAT, WORK
# ============================================================================

class EnergyHeatWorkSetter(TypeSafeSetter):
    """Energy, Heat, Work-specific setter with only energy, heat, work unit properties."""
    
    def __init__(self, variable: 'EnergyHeatWork', value: float) -> None: ...
    
    # All energy, heat, work unit properties - provides fluent API with full type hints
    @property
    def barrel_oil_equivalent_or_equivalent_barrels(self) -> 'EnergyHeatWork': ...
    @property
    def billion_electronvolts(self) -> 'EnergyHeatWork': ...
    @property
    def British_thermal_unit_4_circ_mathrm_Cs(self) -> 'EnergyHeatWork': ...
    @property
    def British_thermal_unit_60_circ_mathrm_Fs(self) -> 'EnergyHeatWork': ...
    @property
    def British_thermal_unit_international_steam_tables(self) -> 'EnergyHeatWork': ...
    @property
    def British_thermal_unit_ISO_TC_12s(self) -> 'EnergyHeatWork': ...
    @property
    def British_thermal_unit_means(self) -> 'EnergyHeatWork': ...
    @property
    def British_thermal_unit_thermochemicals(self) -> 'EnergyHeatWork': ...
    @property
    def calorie_20_circ_mathrm_Cs(self) -> 'EnergyHeatWork': ...
    @property
    def calorie_4_circ_mathrm_Cs(self) -> 'EnergyHeatWork': ...
    @property
    def calorie_international_steam_tables(self) -> 'EnergyHeatWork': ...
    @property
    def calorie_means(self) -> 'EnergyHeatWork': ...
    @property
    def Calorie_nutritionals(self) -> 'EnergyHeatWork': ...
    @property
    def calorie_thermochemicals(self) -> 'EnergyHeatWork': ...
    @property
    def Celsius_heat_units(self) -> 'EnergyHeatWork': ...
    @property
    def Celsius_heat_unit_15_circ_mathrm_Cs(self) -> 'EnergyHeatWork': ...
    @property
    def electron_volts(self) -> 'EnergyHeatWork': ...
    @property
    def ergs(self) -> 'EnergyHeatWork': ...
    @property
    def foot_pound_force_dutys(self) -> 'EnergyHeatWork': ...
    @property
    def foot_poundals(self) -> 'EnergyHeatWork': ...
    @property
    def frigories(self) -> 'EnergyHeatWork': ...
    @property
    def hartree_atomic_unit_of_energys(self) -> 'EnergyHeatWork': ...
    @property
    def joules(self) -> 'EnergyHeatWork': ...
    @property
    def joule_internationals(self) -> 'EnergyHeatWork': ...
    @property
    def kilocalorie_thermals(self) -> 'EnergyHeatWork': ...
    @property
    def kilogram_force_meters(self) -> 'EnergyHeatWork': ...
    @property
    def kiloton_TNTs(self) -> 'EnergyHeatWork': ...
    @property
    def kilowatt_hours(self) -> 'EnergyHeatWork': ...
    @property
    def liter_atmospheres(self) -> 'EnergyHeatWork': ...
    @property
    def megaton_TNTs(self) -> 'EnergyHeatWork': ...
    @property
    def pound_centigrade_unit_15_circ_mathrm_Cs(self) -> 'EnergyHeatWork': ...
    @property
    def prouts(self) -> 'EnergyHeatWork': ...
    @property
    def Q_units(self) -> 'EnergyHeatWork': ...
    @property
    def quad_quadrillion_Btus(self) -> 'EnergyHeatWork': ...
    @property
    def rydbergs(self) -> 'EnergyHeatWork': ...
    @property
    def therm_EEGs(self) -> 'EnergyHeatWork': ...
    @property
    def therm_refineries(self) -> 'EnergyHeatWork': ...
    @property
    def therm_USs(self) -> 'EnergyHeatWork': ...
    @property
    def ton_coal_equivalents(self) -> 'EnergyHeatWork': ...
    @property
    def ton_oil_equivalents(self) -> 'EnergyHeatWork': ...

class EnergyHeatWork(TypedVariable):
    """Type-safe energy, heat, work variable with expression capabilities."""
    
    _setter_class: Type[EnergyHeatWorkSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> EnergyHeatWorkSetter:
        """
        Create a energy, heat, work setter for fluent unit assignment.
        
        Example:
            energyheatwork.set(100).barrel_oil_equivalent_or_equivalent_barrels
            energyheatwork.set(100).billion_electronvolts
            energyheatwork.set(100).British_thermal_unit_4_circ_mathrm_Cs
        """
        ...

# ============================================================================
# ENERGY PER UNIT AREA
# ============================================================================

class EnergyPerUnitAreaSetter(TypeSafeSetter):
    """Energy per Unit Area-specific setter with only energy per unit area unit properties."""
    
    def __init__(self, variable: 'EnergyPerUnitArea', value: float) -> None: ...
    
    # All energy per unit area unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_square_foots(self) -> 'EnergyPerUnitArea': ...
    @property
    def joule_per_square_meters(self) -> 'EnergyPerUnitArea': ...
    @property
    def Langleys(self) -> 'EnergyPerUnitArea': ...

class EnergyPerUnitArea(TypedVariable):
    """Type-safe energy per unit area variable with expression capabilities."""
    
    _setter_class: Type[EnergyPerUnitAreaSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> EnergyPerUnitAreaSetter:
        """
        Create a energy per unit area setter for fluent unit assignment.
        
        Example:
            energyperunitarea.set(100).British_thermal_unit_per_square_foots
            energyperunitarea.set(100).joule_per_square_meters
            energyperunitarea.set(100).Langleys
        """
        ...

# ============================================================================
# FORCE
# ============================================================================

class ForceSetter(TypeSafeSetter):
    """Force-specific setter with only force unit properties."""
    
    def __init__(self, variable: 'Force', value: float) -> None: ...
    
    # All force unit properties - provides fluent API with full type hints
    @property
    def crinals(self) -> 'Force': ...
    @property
    def dynes(self) -> 'Force': ...
    @property
    def funals(self) -> 'Force': ...
    @property
    def kilogram_forces(self) -> 'Force': ...
    @property
    def kip_forces(self) -> 'Force': ...
    @property
    def newtons(self) -> 'Force': ...
    @property
    def ounce_forces(self) -> 'Force': ...
    @property
    def ponds(self) -> 'Force': ...
    @property
    def pound_forces(self) -> 'Force': ...
    @property
    def poundals(self) -> 'Force': ...
    @property
    def slug_forces(self) -> 'Force': ...
    @property
    def sth_nes(self) -> 'Force': ...
    @property
    def ton_force_longs(self) -> 'Force': ...
    @property
    def ton_force_metrics(self) -> 'Force': ...
    @property
    def ton_force_shorts(self) -> 'Force': ...

class Force(TypedVariable):
    """Type-safe force variable with expression capabilities."""
    
    _setter_class: Type[ForceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ForceSetter:
        """
        Create a force setter for fluent unit assignment.
        
        Example:
            force.set(100).crinals
            force.set(100).dynes
            force.set(100).funals
        """
        ...

# ============================================================================
# FORCE (BODY)
# ============================================================================

class ForceBodySetter(TypeSafeSetter):
    """Force (Body)-specific setter with only force (body) unit properties."""
    
    def __init__(self, variable: 'ForceBody', value: float) -> None: ...
    
    # All force (body) unit properties - provides fluent API with full type hints
    @property
    def dyne_per_cubic_centimeters(self) -> 'ForceBody': ...
    @property
    def kilogram_force_per_cubic_centimeters(self) -> 'ForceBody': ...
    @property
    def kilogram_force_per_cubic_meters(self) -> 'ForceBody': ...
    @property
    def newton_per_cubic_meters(self) -> 'ForceBody': ...
    @property
    def pound_force_per_cubic_foots(self) -> 'ForceBody': ...
    @property
    def pound_force_per_cubic_inchs(self) -> 'ForceBody': ...
    @property
    def ton_force_per_cubic_foots(self) -> 'ForceBody': ...

class ForceBody(TypedVariable):
    """Type-safe force (body) variable with expression capabilities."""
    
    _setter_class: Type[ForceBodySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ForceBodySetter:
        """
        Create a force (body) setter for fluent unit assignment.
        
        Example:
            forcebody.set(100).dyne_per_cubic_centimeters
            forcebody.set(100).kilogram_force_per_cubic_centimeters
            forcebody.set(100).kilogram_force_per_cubic_meters
        """
        ...

# ============================================================================
# FORCE PER UNIT MASS
# ============================================================================

class ForcePerUnitMassSetter(TypeSafeSetter):
    """Force per Unit Mass-specific setter with only force per unit mass unit properties."""
    
    def __init__(self, variable: 'ForcePerUnitMass', value: float) -> None: ...
    
    # All force per unit mass unit properties - provides fluent API with full type hints
    @property
    def dyne_per_grams(self) -> 'ForcePerUnitMass': ...
    @property
    def kilogram_force_per_kilograms(self) -> 'ForcePerUnitMass': ...
    @property
    def newton_per_kilograms(self) -> 'ForcePerUnitMass': ...
    @property
    def pound_force_per_pound_mass(self) -> 'ForcePerUnitMass': ...
    @property
    def pound_force_per_slugs(self) -> 'ForcePerUnitMass': ...

class ForcePerUnitMass(TypedVariable):
    """Type-safe force per unit mass variable with expression capabilities."""
    
    _setter_class: Type[ForcePerUnitMassSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ForcePerUnitMassSetter:
        """
        Create a force per unit mass setter for fluent unit assignment.
        
        Example:
            forceperunitmass.set(100).dyne_per_grams
            forceperunitmass.set(100).kilogram_force_per_kilograms
            forceperunitmass.set(100).newton_per_kilograms
        """
        ...

# ============================================================================
# FREQUENCY VOLTAGE RATIO
# ============================================================================

class FrequencyVoltageRatioSetter(TypeSafeSetter):
    """Frequency Voltage Ratio-specific setter with only frequency voltage ratio unit properties."""
    
    def __init__(self, variable: 'FrequencyVoltageRatio', value: float) -> None: ...
    
    # All frequency voltage ratio unit properties - provides fluent API with full type hints
    @property
    def cycles_per_second_per_volts(self) -> 'FrequencyVoltageRatio': ...
    @property
    def hertz_per_volts(self) -> 'FrequencyVoltageRatio': ...
    @property
    def terahertz_per_volts(self) -> 'FrequencyVoltageRatio': ...

class FrequencyVoltageRatio(TypedVariable):
    """Type-safe frequency voltage ratio variable with expression capabilities."""
    
    _setter_class: Type[FrequencyVoltageRatioSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> FrequencyVoltageRatioSetter:
        """
        Create a frequency voltage ratio setter for fluent unit assignment.
        
        Example:
            frequencyvoltageratio.set(100).cycles_per_second_per_volts
            frequencyvoltageratio.set(100).hertz_per_volts
            frequencyvoltageratio.set(100).terahertz_per_volts
        """
        ...

# ============================================================================
# FUEL CONSUMPTION
# ============================================================================

class FuelConsumptionSetter(TypeSafeSetter):
    """Fuel Consumption-specific setter with only fuel consumption unit properties."""
    
    def __init__(self, variable: 'FuelConsumption', value: float) -> None: ...
    
    # All fuel consumption unit properties - provides fluent API with full type hints
    @property
    def _100_km_per_liters(self) -> 'FuelConsumption': ...
    @property
    def gallons_UK_per_100_miles(self) -> 'FuelConsumption': ...
    @property
    def gallons_US_per_100_miles(self) -> 'FuelConsumption': ...
    @property
    def kilometers_per_gallon_UKs(self) -> 'FuelConsumption': ...
    @property
    def kilometers_per_gallon_USs(self) -> 'FuelConsumption': ...
    @property
    def kilometers_per_liters(self) -> 'FuelConsumption': ...
    @property
    def liters_per_100_kms(self) -> 'FuelConsumption': ...
    @property
    def liters_per_kilometers(self) -> 'FuelConsumption': ...
    @property
    def meters_per_gallon_UKs(self) -> 'FuelConsumption': ...
    @property
    def meters_per_gallon_USs(self) -> 'FuelConsumption': ...
    @property
    def miles_per_gallon_UKs(self) -> 'FuelConsumption': ...
    @property
    def miles_per_gallon_USs(self) -> 'FuelConsumption': ...
    @property
    def miles_per_liters(self) -> 'FuelConsumption': ...

class FuelConsumption(TypedVariable):
    """Type-safe fuel consumption variable with expression capabilities."""
    
    _setter_class: Type[FuelConsumptionSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> FuelConsumptionSetter:
        """
        Create a fuel consumption setter for fluent unit assignment.
        
        Example:
            fuelconsumption.set(100)._100_km_per_liters
            fuelconsumption.set(100).gallons_UK_per_100_miles
            fuelconsumption.set(100).gallons_US_per_100_miles
        """
        ...

# ============================================================================
# HEAT OF COMBUSTION
# ============================================================================

class HeatOfCombustionSetter(TypeSafeSetter):
    """Heat of Combustion-specific setter with only heat of combustion unit properties."""
    
    def __init__(self, variable: 'HeatOfCombustion', value: float) -> None: ...
    
    # All heat of combustion unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_pounds(self) -> 'HeatOfCombustion': ...
    @property
    def calorie_per_grams(self) -> 'HeatOfCombustion': ...
    @property
    def Chu_per_pounds(self) -> 'HeatOfCombustion': ...
    @property
    def joule_per_kilograms(self) -> 'HeatOfCombustion': ...

class HeatOfCombustion(TypedVariable):
    """Type-safe heat of combustion variable with expression capabilities."""
    
    _setter_class: Type[HeatOfCombustionSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatOfCombustionSetter:
        """
        Create a heat of combustion setter for fluent unit assignment.
        
        Example:
            heatofcombustion.set(100).British_thermal_unit_per_pounds
            heatofcombustion.set(100).calorie_per_grams
            heatofcombustion.set(100).Chu_per_pounds
        """
        ...

# ============================================================================
# HEAT OF FUSION
# ============================================================================

class HeatOfFusionSetter(TypeSafeSetter):
    """Heat of Fusion-specific setter with only heat of fusion unit properties."""
    
    def __init__(self, variable: 'HeatOfFusion', value: float) -> None: ...
    
    # All heat of fusion unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_mean_per_pounds(self) -> 'HeatOfFusion': ...
    @property
    def British_thermal_unit_per_pounds(self) -> 'HeatOfFusion': ...
    @property
    def calorie_per_grams(self) -> 'HeatOfFusion': ...
    @property
    def Chu_per_pounds(self) -> 'HeatOfFusion': ...
    @property
    def joule_per_kilograms(self) -> 'HeatOfFusion': ...

class HeatOfFusion(TypedVariable):
    """Type-safe heat of fusion variable with expression capabilities."""
    
    _setter_class: Type[HeatOfFusionSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatOfFusionSetter:
        """
        Create a heat of fusion setter for fluent unit assignment.
        
        Example:
            heatoffusion.set(100).British_thermal_unit_mean_per_pounds
            heatoffusion.set(100).British_thermal_unit_per_pounds
            heatoffusion.set(100).calorie_per_grams
        """
        ...

# ============================================================================
# HEAT OF VAPORIZATION
# ============================================================================

class HeatOfVaporizationSetter(TypeSafeSetter):
    """Heat of Vaporization-specific setter with only heat of vaporization unit properties."""
    
    def __init__(self, variable: 'HeatOfVaporization', value: float) -> None: ...
    
    # All heat of vaporization unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_pounds(self) -> 'HeatOfVaporization': ...
    @property
    def calorie_per_grams(self) -> 'HeatOfVaporization': ...
    @property
    def Chu_per_pounds(self) -> 'HeatOfVaporization': ...
    @property
    def joule_per_kilograms(self) -> 'HeatOfVaporization': ...

class HeatOfVaporization(TypedVariable):
    """Type-safe heat of vaporization variable with expression capabilities."""
    
    _setter_class: Type[HeatOfVaporizationSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatOfVaporizationSetter:
        """
        Create a heat of vaporization setter for fluent unit assignment.
        
        Example:
            heatofvaporization.set(100).British_thermal_unit_per_pounds
            heatofvaporization.set(100).calorie_per_grams
            heatofvaporization.set(100).Chu_per_pounds
        """
        ...

# ============================================================================
# HEAT TRANSFER COEFFICIENT
# ============================================================================

class HeatTransferCoefficientSetter(TypeSafeSetter):
    """Heat Transfer Coefficient-specific setter with only heat transfer coefficient unit properties."""
    
    def __init__(self, variable: 'HeatTransferCoefficient', value: float) -> None: ...
    
    # All heat transfer coefficient unit properties - provides fluent API with full type hints
    @property
    def Btu_per_square_foot_per_hour_per_degree_Fahrenheit_or_Rankines(self) -> 'HeatTransferCoefficient': ...
    @property
    def watt_per_square_meter_per_degree_Celsius_or_kelvins(self) -> 'HeatTransferCoefficient': ...

class HeatTransferCoefficient(TypedVariable):
    """Type-safe heat transfer coefficient variable with expression capabilities."""
    
    _setter_class: Type[HeatTransferCoefficientSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> HeatTransferCoefficientSetter:
        """
        Create a heat transfer coefficient setter for fluent unit assignment.
        
        Example:
            heattransfercoefficient.set(100).Btu_per_square_foot_per_hour_per_degree_Fahrenheit_or_Rankines
            heattransfercoefficient.set(100).watt_per_square_meter_per_degree_Celsius_or_kelvins
        """
        ...

# ============================================================================
# ILLUMINANCE
# ============================================================================

class IlluminanceSetter(TypeSafeSetter):
    """Illuminance-specific setter with only illuminance unit properties."""
    
    def __init__(self, variable: 'Illuminance', value: float) -> None: ...
    
    # All illuminance unit properties - provides fluent API with full type hints
    @property
    def foot_candles(self) -> 'Illuminance': ...
    @property
    def luxs(self) -> 'Illuminance': ...
    @property
    def noxs(self) -> 'Illuminance': ...
    @property
    def phots(self) -> 'Illuminance': ...
    @property
    def skots(self) -> 'Illuminance': ...

class Illuminance(TypedVariable):
    """Type-safe illuminance variable with expression capabilities."""
    
    _setter_class: Type[IlluminanceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> IlluminanceSetter:
        """
        Create a illuminance setter for fluent unit assignment.
        
        Example:
            illuminance.set(100).foot_candles
            illuminance.set(100).luxs
            illuminance.set(100).noxs
        """
        ...

# ============================================================================
# KINETIC ENERGY OF TURBULENCE
# ============================================================================

class KineticEnergyOfTurbulenceSetter(TypeSafeSetter):
    """Kinetic Energy of Turbulence-specific setter with only kinetic energy of turbulence unit properties."""
    
    def __init__(self, variable: 'KineticEnergyOfTurbulence', value: float) -> None: ...
    
    # All kinetic energy of turbulence unit properties - provides fluent API with full type hints
    @property
    def square_foot_per_second_squareds(self) -> 'KineticEnergyOfTurbulence': ...
    @property
    def square_meters_per_second_squareds(self) -> 'KineticEnergyOfTurbulence': ...

class KineticEnergyOfTurbulence(TypedVariable):
    """Type-safe kinetic energy of turbulence variable with expression capabilities."""
    
    _setter_class: Type[KineticEnergyOfTurbulenceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> KineticEnergyOfTurbulenceSetter:
        """
        Create a kinetic energy of turbulence setter for fluent unit assignment.
        
        Example:
            kineticenergyofturbulence.set(100).square_foot_per_second_squareds
            kineticenergyofturbulence.set(100).square_meters_per_second_squareds
        """
        ...

# ============================================================================
# LENGTH
# ============================================================================

class LengthSetter(TypeSafeSetter):
    """Length-specific setter with only length unit properties."""
    
    def __init__(self, variable: 'Length', value: float) -> None: ...
    
    # All length unit properties - provides fluent API with full type hints
    @property
    def ngstr_ms(self) -> 'Length': ...
    @property
    def arpent_Quebecs(self) -> 'Length': ...
    @property
    def astronomic_units(self) -> 'Length': ...
    @property
    def attometers(self) -> 'Length': ...
    @property
    def calibre_centinchs(self) -> 'Length': ...
    @property
    def centimeters(self) -> 'Length': ...
    @property
    def chain_Engr_s_or_Ramsdens(self) -> 'Length': ...
    @property
    def chain_Gunter_s(self) -> 'Length': ...
    @property
    def chain_surveyors(self) -> 'Length': ...
    @property
    def cubit_UKs(self) -> 'Length': ...
    @property
    def ells(self) -> 'Length': ...
    @property
    def fathoms(self) -> 'Length': ...
    @property
    def femtometres(self) -> 'Length': ...
    @property
    def fermis(self) -> 'Length': ...
    @property
    def feet(self) -> 'Length': ...
    @property
    def furlong_UK_and_USs(self) -> 'Length': ...
    @property
    def inches(self) -> 'Length': ...
    @property
    def kilometers(self) -> 'Length': ...
    @property
    def league_US_statutes(self) -> 'Length': ...
    @property
    def lieue_metrics(self) -> 'Length': ...
    @property
    def ligne_metrics(self) -> 'Length': ...
    @property
    def line_USs(self) -> 'Length': ...
    @property
    def link_surveyors(self) -> 'Length': ...
    @property
    def meters(self) -> 'Length': ...
    @property
    def micrometers(self) -> 'Length': ...
    @property
    def microns(self) -> 'Length': ...
    @property
    def mils(self) -> 'Length': ...
    @property
    def mile_geographicals(self) -> 'Length': ...
    @property
    def mile_US_nauticals(self) -> 'Length': ...
    @property
    def mile_US_statutes(self) -> 'Length': ...
    @property
    def mile_US_surveys(self) -> 'Length': ...
    @property
    def millimeters(self) -> 'Length': ...
    @property
    def millimicrons(self) -> 'Length': ...
    @property
    def nanometer_or_nanons(self) -> 'Length': ...
    @property
    def parsecs(self) -> 'Length': ...
    @property
    def perches(self) -> 'Length': ...
    @property
    def picas(self) -> 'Length': ...
    @property
    def picometers(self) -> 'Length': ...
    @property
    def point_Didots(self) -> 'Length': ...
    @property
    def point_USs(self) -> 'Length': ...
    @property
    def rod_or_poles(self) -> 'Length': ...
    @property
    def spans(self) -> 'Length': ...
    @property
    def thou_millinchs(self) -> 'Length': ...
    @property
    def toise_metrics(self) -> 'Length': ...
    @property
    def yards(self) -> 'Length': ...

class Length(TypedVariable):
    """Type-safe length variable with expression capabilities."""
    
    _setter_class: Type[LengthSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LengthSetter:
        """
        Create a length setter for fluent unit assignment.
        
        Example:
            length.set(100).ngstr_ms
            length.set(100).arpent_Quebecs
            length.set(100).astronomic_units
        """
        ...

# ============================================================================
# LINEAR MASS DENSITY
# ============================================================================

class LinearMassDensitySetter(TypeSafeSetter):
    """Linear Mass Density-specific setter with only linear mass density unit properties."""
    
    def __init__(self, variable: 'LinearMassDensity', value: float) -> None: ...
    
    # All linear mass density unit properties - provides fluent API with full type hints
    @property
    def deniers(self) -> 'LinearMassDensity': ...
    @property
    def kilogram_per_centimeters(self) -> 'LinearMassDensity': ...
    @property
    def kilogram_per_meters(self) -> 'LinearMassDensity': ...
    @property
    def pound_per_foots(self) -> 'LinearMassDensity': ...
    @property
    def pound_per_inchs(self) -> 'LinearMassDensity': ...
    @property
    def pound_per_yards(self) -> 'LinearMassDensity': ...
    @property
    def ton_metric_per_kilometers(self) -> 'LinearMassDensity': ...
    @property
    def ton_metric_per_meters(self) -> 'LinearMassDensity': ...

class LinearMassDensity(TypedVariable):
    """Type-safe linear mass density variable with expression capabilities."""
    
    _setter_class: Type[LinearMassDensitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LinearMassDensitySetter:
        """
        Create a linear mass density setter for fluent unit assignment.
        
        Example:
            linearmassdensity.set(100).deniers
            linearmassdensity.set(100).kilogram_per_centimeters
            linearmassdensity.set(100).kilogram_per_meters
        """
        ...

# ============================================================================
# LINEAR MOMENTUM
# ============================================================================

class LinearMomentumSetter(TypeSafeSetter):
    """Linear Momentum-specific setter with only linear momentum unit properties."""
    
    def __init__(self, variable: 'LinearMomentum', value: float) -> None: ...
    
    # All linear momentum unit properties - provides fluent API with full type hints
    @property
    def foot_pounds_force_per_hours(self) -> 'LinearMomentum': ...
    @property
    def foot_pounds_force_per_minutes(self) -> 'LinearMomentum': ...
    @property
    def foot_pounds_force_per_seconds(self) -> 'LinearMomentum': ...
    @property
    def gram_centimeters_per_seconds(self) -> 'LinearMomentum': ...
    @property
    def kilogram_meters_per_seconds(self) -> 'LinearMomentum': ...

class LinearMomentum(TypedVariable):
    """Type-safe linear momentum variable with expression capabilities."""
    
    _setter_class: Type[LinearMomentumSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LinearMomentumSetter:
        """
        Create a linear momentum setter for fluent unit assignment.
        
        Example:
            linearmomentum.set(100).foot_pounds_force_per_hours
            linearmomentum.set(100).foot_pounds_force_per_minutes
            linearmomentum.set(100).foot_pounds_force_per_seconds
        """
        ...

# ============================================================================
# LUMINANCE (SELF)
# ============================================================================

class LuminanceSelfSetter(TypeSafeSetter):
    """Luminance (self)-specific setter with only luminance (self) unit properties."""
    
    def __init__(self, variable: 'LuminanceSelf', value: float) -> None: ...
    
    # All luminance (self) unit properties - provides fluent API with full type hints
    @property
    def apostilbs(self) -> 'LuminanceSelf': ...
    @property
    def blondels(self) -> 'LuminanceSelf': ...
    @property
    def candela_per_square_meters(self) -> 'LuminanceSelf': ...
    @property
    def foot_lamberts(self) -> 'LuminanceSelf': ...
    @property
    def lamberts(self) -> 'LuminanceSelf': ...
    @property
    def luxons(self) -> 'LuminanceSelf': ...
    @property
    def nits(self) -> 'LuminanceSelf': ...
    @property
    def stilbs(self) -> 'LuminanceSelf': ...
    @property
    def trolands(self) -> 'LuminanceSelf': ...

class LuminanceSelf(TypedVariable):
    """Type-safe luminance (self) variable with expression capabilities."""
    
    _setter_class: Type[LuminanceSelfSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LuminanceSelfSetter:
        """
        Create a luminance (self) setter for fluent unit assignment.
        
        Example:
            luminanceself.set(100).apostilbs
            luminanceself.set(100).blondels
            luminanceself.set(100).candela_per_square_meters
        """
        ...

# ============================================================================
# LUMINOUS FLUX
# ============================================================================

class LuminousFluxSetter(TypeSafeSetter):
    """Luminous Flux-specific setter with only luminous flux unit properties."""
    
    def __init__(self, variable: 'LuminousFlux', value: float) -> None: ...
    
    # All luminous flux unit properties - provides fluent API with full type hints
    @property
    def candela_steradians(self) -> 'LuminousFlux': ...
    @property
    def lumens(self) -> 'LuminousFlux': ...

class LuminousFlux(TypedVariable):
    """Type-safe luminous flux variable with expression capabilities."""
    
    _setter_class: Type[LuminousFluxSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LuminousFluxSetter:
        """
        Create a luminous flux setter for fluent unit assignment.
        
        Example:
            luminousflux.set(100).candela_steradians
            luminousflux.set(100).lumens
        """
        ...

# ============================================================================
# LUMINOUS INTENSITY
# ============================================================================

class LuminousIntensitySetter(TypeSafeSetter):
    """Luminous Intensity-specific setter with only luminous intensity unit properties."""
    
    def __init__(self, variable: 'LuminousIntensity', value: float) -> None: ...
    
    # All luminous intensity unit properties - provides fluent API with full type hints
    @property
    def candelas(self) -> 'LuminousIntensity': ...
    @property
    def candle_internationals(self) -> 'LuminousIntensity': ...
    @property
    def carcels(self) -> 'LuminousIntensity': ...
    @property
    def Hefner_units(self) -> 'LuminousIntensity': ...

class LuminousIntensity(TypedVariable):
    """Type-safe luminous intensity variable with expression capabilities."""
    
    _setter_class: Type[LuminousIntensitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> LuminousIntensitySetter:
        """
        Create a luminous intensity setter for fluent unit assignment.
        
        Example:
            luminousintensity.set(100).candelas
            luminousintensity.set(100).candle_internationals
            luminousintensity.set(100).carcels
        """
        ...

# ============================================================================
# MAGNETIC FIELD
# ============================================================================

class MagneticFieldSetter(TypeSafeSetter):
    """Magnetic Field-specific setter with only magnetic field unit properties."""
    
    def __init__(self, variable: 'MagneticField', value: float) -> None: ...
    
    # All magnetic field unit properties - provides fluent API with full type hints
    @property
    def ampere_per_meters(self) -> 'MagneticField': ...
    @property
    def lenzs(self) -> 'MagneticField': ...
    @property
    def oersteds(self) -> 'MagneticField': ...
    @property
    def praoersteds(self) -> 'MagneticField': ...

class MagneticField(TypedVariable):
    """Type-safe magnetic field variable with expression capabilities."""
    
    _setter_class: Type[MagneticFieldSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticFieldSetter:
        """
        Create a magnetic field setter for fluent unit assignment.
        
        Example:
            magneticfield.set(100).ampere_per_meters
            magneticfield.set(100).lenzs
            magneticfield.set(100).oersteds
        """
        ...

# ============================================================================
# MAGNETIC FLUX
# ============================================================================

class MagneticFluxSetter(TypeSafeSetter):
    """Magnetic Flux-specific setter with only magnetic flux unit properties."""
    
    def __init__(self, variable: 'MagneticFlux', value: float) -> None: ...
    
    # All magnetic flux unit properties - provides fluent API with full type hints
    @property
    def kapp_lines(self) -> 'MagneticFlux': ...
    @property
    def lines(self) -> 'MagneticFlux': ...
    @property
    def maxwells(self) -> 'MagneticFlux': ...
    @property
    def unit_poles(self) -> 'MagneticFlux': ...
    @property
    def webers(self) -> 'MagneticFlux': ...

class MagneticFlux(TypedVariable):
    """Type-safe magnetic flux variable with expression capabilities."""
    
    _setter_class: Type[MagneticFluxSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticFluxSetter:
        """
        Create a magnetic flux setter for fluent unit assignment.
        
        Example:
            magneticflux.set(100).kapp_lines
            magneticflux.set(100).lines
            magneticflux.set(100).maxwells
        """
        ...

# ============================================================================
# MAGNETIC INDUCTION FIELD STRENGTH
# ============================================================================

class MagneticInductionFieldStrengthSetter(TypeSafeSetter):
    """Magnetic Induction Field Strength-specific setter with only magnetic induction field strength unit properties."""
    
    def __init__(self, variable: 'MagneticInductionFieldStrength', value: float) -> None: ...
    
    # All magnetic induction field strength unit properties - provides fluent API with full type hints
    @property
    def gammas(self) -> 'MagneticInductionFieldStrength': ...
    @property
    def gauss(self) -> 'MagneticInductionFieldStrength': ...
    @property
    def line_per_square_centimeters(self) -> 'MagneticInductionFieldStrength': ...
    @property
    def maxwell_per_square_centimeters(self) -> 'MagneticInductionFieldStrength': ...
    @property
    def teslas(self) -> 'MagneticInductionFieldStrength': ...
    @property
    def u_as(self) -> 'MagneticInductionFieldStrength': ...
    @property
    def weber_per_square_meters(self) -> 'MagneticInductionFieldStrength': ...

class MagneticInductionFieldStrength(TypedVariable):
    """Type-safe magnetic induction field strength variable with expression capabilities."""
    
    _setter_class: Type[MagneticInductionFieldStrengthSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticInductionFieldStrengthSetter:
        """
        Create a magnetic induction field strength setter for fluent unit assignment.
        
        Example:
            magneticinductionfieldstrength.set(100).gammas
            magneticinductionfieldstrength.set(100).gauss
            magneticinductionfieldstrength.set(100).line_per_square_centimeters
        """
        ...

# ============================================================================
# MAGNETIC MOMENT
# ============================================================================

class MagneticMomentSetter(TypeSafeSetter):
    """Magnetic Moment-specific setter with only magnetic moment unit properties."""
    
    def __init__(self, variable: 'MagneticMoment', value: float) -> None: ...
    
    # All magnetic moment unit properties - provides fluent API with full type hints
    @property
    def Bohr_magnetons(self) -> 'MagneticMoment': ...
    @property
    def joule_per_teslas(self) -> 'MagneticMoment': ...
    @property
    def nuclear_magnetons(self) -> 'MagneticMoment': ...

class MagneticMoment(TypedVariable):
    """Type-safe magnetic moment variable with expression capabilities."""
    
    _setter_class: Type[MagneticMomentSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticMomentSetter:
        """
        Create a magnetic moment setter for fluent unit assignment.
        
        Example:
            magneticmoment.set(100).Bohr_magnetons
            magneticmoment.set(100).joule_per_teslas
            magneticmoment.set(100).nuclear_magnetons
        """
        ...

# ============================================================================
# MAGNETIC PERMEABILITY
# ============================================================================

class MagneticPermeabilitySetter(TypeSafeSetter):
    """Magnetic Permeability-specific setter with only magnetic permeability unit properties."""
    
    def __init__(self, variable: 'MagneticPermeability', value: float) -> None: ...
    
    # All magnetic permeability unit properties - provides fluent API with full type hints
    @property
    def henrys_per_meters(self) -> 'MagneticPermeability': ...
    @property
    def newton_per_square_amperes(self) -> 'MagneticPermeability': ...

class MagneticPermeability(TypedVariable):
    """Type-safe magnetic permeability variable with expression capabilities."""
    
    _setter_class: Type[MagneticPermeabilitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagneticPermeabilitySetter:
        """
        Create a magnetic permeability setter for fluent unit assignment.
        
        Example:
            magneticpermeability.set(100).henrys_per_meters
            magneticpermeability.set(100).newton_per_square_amperes
        """
        ...

# ============================================================================
# MAGNETOMOTIVE FORCE
# ============================================================================

class MagnetomotiveForceSetter(TypeSafeSetter):
    """Magnetomotive Force-specific setter with only magnetomotive force unit properties."""
    
    def __init__(self, variable: 'MagnetomotiveForce', value: float) -> None: ...
    
    # All magnetomotive force unit properties - provides fluent API with full type hints
    @property
    def abampere_turns(self) -> 'MagnetomotiveForce': ...
    @property
    def amperes(self) -> 'MagnetomotiveForce': ...
    @property
    def ampere_turns(self) -> 'MagnetomotiveForce': ...
    @property
    def gilberts(self) -> 'MagnetomotiveForce': ...

class MagnetomotiveForce(TypedVariable):
    """Type-safe magnetomotive force variable with expression capabilities."""
    
    _setter_class: Type[MagnetomotiveForceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MagnetomotiveForceSetter:
        """
        Create a magnetomotive force setter for fluent unit assignment.
        
        Example:
            magnetomotiveforce.set(100).abampere_turns
            magnetomotiveforce.set(100).amperes
            magnetomotiveforce.set(100).ampere_turns
        """
        ...

# ============================================================================
# MASS
# ============================================================================

class MassSetter(TypeSafeSetter):
    """Mass-specific setter with only mass unit properties."""
    
    def __init__(self, variable: 'Mass', value: float) -> None: ...
    
    # All mass unit properties - provides fluent API with full type hints
    @property
    def slugs(self) -> 'Mass': ...
    @property
    def atomic_mass_unit_12_mathrm_Cs(self) -> 'Mass': ...
    @property
    def carat_metrics(self) -> 'Mass': ...
    @property
    def centals(self) -> 'Mass': ...
    @property
    def centigrams(self) -> 'Mass': ...
    @property
    def clove_UKs(self) -> 'Mass': ...
    @property
    def drachm_apothecarys(self) -> 'Mass': ...
    @property
    def dram_avoirdupois(self) -> 'Mass': ...
    @property
    def dram_troys(self) -> 'Mass': ...
    @property
    def grains(self) -> 'Mass': ...
    @property
    def grams(self) -> 'Mass': ...
    @property
    def hundredweight_long_or_gross(self) -> 'Mass': ...
    @property
    def hundredweight_short_or_nets(self) -> 'Mass': ...
    @property
    def kilograms(self) -> 'Mass': ...
    @property
    def kips(self) -> 'Mass': ...
    @property
    def micrograms(self) -> 'Mass': ...
    @property
    def milligrams(self) -> 'Mass': ...
    @property
    def ounce_apothecarys(self) -> 'Mass': ...
    @property
    def ounce_avoirdupois(self) -> 'Mass': ...
    @property
    def ounce_troys(self) -> 'Mass': ...
    @property
    def pennyweight_troys(self) -> 'Mass': ...
    @property
    def pood_Russias(self) -> 'Mass': ...
    @property
    def pound_apothecarys(self) -> 'Mass': ...
    @property
    def pound_avoirdupois(self) -> 'Mass': ...
    @property
    def pound_troys(self) -> 'Mass': ...
    @property
    def pound_mass(self) -> 'Mass': ...
    @property
    def quarter_UKs(self) -> 'Mass': ...
    @property
    def quintal_metrics(self) -> 'Mass': ...
    @property
    def quital_USs(self) -> 'Mass': ...
    @property
    def scruple_avoirdupois(self) -> 'Mass': ...
    @property
    def stone_UKs(self) -> 'Mass': ...
    @property
    def ton_metrics(self) -> 'Mass': ...
    @property
    def ton_US_longs(self) -> 'Mass': ...
    @property
    def ton_US_shorts(self) -> 'Mass': ...

class Mass(TypedVariable):
    """Type-safe mass variable with expression capabilities."""
    
    _setter_class: Type[MassSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassSetter:
        """
        Create a mass setter for fluent unit assignment.
        
        Example:
            mass.set(100).slugs
            mass.set(100).atomic_mass_unit_12_mathrm_Cs
            mass.set(100).carat_metrics
        """
        ...

# ============================================================================
# MASS DENSITY
# ============================================================================

class MassDensitySetter(TypeSafeSetter):
    """Mass Density-specific setter with only mass density unit properties."""
    
    def __init__(self, variable: 'MassDensity', value: float) -> None: ...
    
    # All mass density unit properties - provides fluent API with full type hints
    @property
    def gram_per_cubic_centimeters(self) -> 'MassDensity': ...
    @property
    def gram_per_cubic_decimeters(self) -> 'MassDensity': ...
    @property
    def gram_per_cubic_meters(self) -> 'MassDensity': ...
    @property
    def gram_per_liters(self) -> 'MassDensity': ...
    @property
    def kilogram_per_cubic_meters(self) -> 'MassDensity': ...
    @property
    def ounce_avdp_per_US_gallons(self) -> 'MassDensity': ...
    @property
    def pound_avdp_per_cubic_foots(self) -> 'MassDensity': ...
    @property
    def pound_avdp_per_US_gallons(self) -> 'MassDensity': ...
    @property
    def pound_mass_per_cubic_inchs(self) -> 'MassDensity': ...
    @property
    def ton_metric_per_cubic_meters(self) -> 'MassDensity': ...

class MassDensity(TypedVariable):
    """Type-safe mass density variable with expression capabilities."""
    
    _setter_class: Type[MassDensitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassDensitySetter:
        """
        Create a mass density setter for fluent unit assignment.
        
        Example:
            massdensity.set(100).gram_per_cubic_centimeters
            massdensity.set(100).gram_per_cubic_decimeters
            massdensity.set(100).gram_per_cubic_meters
        """
        ...

# ============================================================================
# MASS FLOW RATE
# ============================================================================

class MassFlowRateSetter(TypeSafeSetter):
    """Mass Flow Rate-specific setter with only mass flow rate unit properties."""
    
    def __init__(self, variable: 'MassFlowRate', value: float) -> None: ...
    
    # All mass flow rate unit properties - provides fluent API with full type hints
    @property
    def kilograms_per_days(self) -> 'MassFlowRate': ...
    @property
    def kilograms_per_hours(self) -> 'MassFlowRate': ...
    @property
    def kilograms_per_minutes(self) -> 'MassFlowRate': ...
    @property
    def kilograms_per_seconds(self) -> 'MassFlowRate': ...
    @property
    def metric_tons_per_days(self) -> 'MassFlowRate': ...
    @property
    def metric_tons_per_hours(self) -> 'MassFlowRate': ...
    @property
    def metric_tons_per_minutes(self) -> 'MassFlowRate': ...
    @property
    def metric_tons_per_seconds(self) -> 'MassFlowRate': ...
    @property
    def metric_tons_per_year_365_ds(self) -> 'MassFlowRate': ...
    @property
    def pounds_per_days(self) -> 'MassFlowRate': ...
    @property
    def pounds_per_hours(self) -> 'MassFlowRate': ...
    @property
    def pounds_per_minutes(self) -> 'MassFlowRate': ...
    @property
    def pounds_per_seconds(self) -> 'MassFlowRate': ...

class MassFlowRate(TypedVariable):
    """Type-safe mass flow rate variable with expression capabilities."""
    
    _setter_class: Type[MassFlowRateSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassFlowRateSetter:
        """
        Create a mass flow rate setter for fluent unit assignment.
        
        Example:
            massflowrate.set(100).kilograms_per_days
            massflowrate.set(100).kilograms_per_hours
            massflowrate.set(100).kilograms_per_minutes
        """
        ...

# ============================================================================
# MASS FLUX
# ============================================================================

class MassFluxSetter(TypeSafeSetter):
    """Mass Flux-specific setter with only mass flux unit properties."""
    
    def __init__(self, variable: 'MassFlux', value: float) -> None: ...
    
    # All mass flux unit properties - provides fluent API with full type hints
    @property
    def kilogram_per_square_meter_per_days(self) -> 'MassFlux': ...
    @property
    def kilogram_per_square_meter_per_hours(self) -> 'MassFlux': ...
    @property
    def kilogram_per_square_meter_per_minutes(self) -> 'MassFlux': ...
    @property
    def kilogram_per_square_meter_per_seconds(self) -> 'MassFlux': ...
    @property
    def pound_per_square_foot_per_days(self) -> 'MassFlux': ...
    @property
    def pound_per_square_foot_per_hours(self) -> 'MassFlux': ...
    @property
    def pound_per_square_foot_per_minutes(self) -> 'MassFlux': ...
    @property
    def pound_per_square_foot_per_seconds(self) -> 'MassFlux': ...

class MassFlux(TypedVariable):
    """Type-safe mass flux variable with expression capabilities."""
    
    _setter_class: Type[MassFluxSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassFluxSetter:
        """
        Create a mass flux setter for fluent unit assignment.
        
        Example:
            massflux.set(100).kilogram_per_square_meter_per_days
            massflux.set(100).kilogram_per_square_meter_per_hours
            massflux.set(100).kilogram_per_square_meter_per_minutes
        """
        ...

# ============================================================================
# MASS FRACTION OF "I"
# ============================================================================

class MassFractionOfISetter(TypeSafeSetter):
    """Mass Fraction of "i"-specific setter with only mass fraction of "i" unit properties."""
    
    def __init__(self, variable: 'MassFractionOfI', value: float) -> None: ...
    
    # All mass fraction of "i" unit properties - provides fluent API with full type hints
    @property
    def grains_of_i_per_pound_totals(self) -> 'MassFractionOfI': ...
    @property
    def gram_of_i_per_kilogram_totals(self) -> 'MassFractionOfI': ...
    @property
    def kilogram_of_i_per_kilogram_totals(self) -> 'MassFractionOfI': ...
    @property
    def pound_of_i_per_pound_totals(self) -> 'MassFractionOfI': ...

class MassFractionOfI(TypedVariable):
    """Type-safe mass fraction of "i" variable with expression capabilities."""
    
    _setter_class: Type[MassFractionOfISetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassFractionOfISetter:
        """
        Create a mass fraction of "i" setter for fluent unit assignment.
        
        Example:
            massfractionofi.set(100).grains_of_i_per_pound_totals
            massfractionofi.set(100).gram_of_i_per_kilogram_totals
            massfractionofi.set(100).kilogram_of_i_per_kilogram_totals
        """
        ...

# ============================================================================
# MASS TRANSFER COEFFICIENT
# ============================================================================

class MassTransferCoefficientSetter(TypeSafeSetter):
    """Mass Transfer Coefficient-specific setter with only mass transfer coefficient unit properties."""
    
    def __init__(self, variable: 'MassTransferCoefficient', value: float) -> None: ...
    
    # All mass transfer coefficient unit properties - provides fluent API with full type hints
    @property
    def gram_per_square_centimeter_per_seconds(self) -> 'MassTransferCoefficient': ...
    @property
    def kilogram_per_square_meter_per_seconds(self) -> 'MassTransferCoefficient': ...
    @property
    def pounds_force_per_cubic_foot_per_hours(self) -> 'MassTransferCoefficient': ...
    @property
    def pounds_mass_per_square_foot_per_hours(self) -> 'MassTransferCoefficient': ...
    @property
    def pounds_mass_per_square_foot_per_seconds(self) -> 'MassTransferCoefficient': ...

class MassTransferCoefficient(TypedVariable):
    """Type-safe mass transfer coefficient variable with expression capabilities."""
    
    _setter_class: Type[MassTransferCoefficientSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MassTransferCoefficientSetter:
        """
        Create a mass transfer coefficient setter for fluent unit assignment.
        
        Example:
            masstransfercoefficient.set(100).gram_per_square_centimeter_per_seconds
            masstransfercoefficient.set(100).kilogram_per_square_meter_per_seconds
            masstransfercoefficient.set(100).pounds_force_per_cubic_foot_per_hours
        """
        ...

# ============================================================================
# MOLALITY OF SOLUTE "I"
# ============================================================================

class MolalityOfSoluteISetter(TypeSafeSetter):
    """Molality of Solute "i"-specific setter with only molality of solute "i" unit properties."""
    
    def __init__(self, variable: 'MolalityOfSoluteI', value: float) -> None: ...
    
    # All molality of solute "i" unit properties - provides fluent API with full type hints
    @property
    def gram_moles_of_i_per_kilograms(self) -> 'MolalityOfSoluteI': ...
    @property
    def kilogram_mols_of_i_per_kilograms(self) -> 'MolalityOfSoluteI': ...
    @property
    def kmols_of_i_per_kilograms(self) -> 'MolalityOfSoluteI': ...
    @property
    def mols_of_i_per_grams(self) -> 'MolalityOfSoluteI': ...
    @property
    def pound_moles_of_i_per_pound_mass(self) -> 'MolalityOfSoluteI': ...

class MolalityOfSoluteI(TypedVariable):
    """Type-safe molality of solute "i" variable with expression capabilities."""
    
    _setter_class: Type[MolalityOfSoluteISetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolalityOfSoluteISetter:
        """
        Create a molality of solute "i" setter for fluent unit assignment.
        
        Example:
            molalityofsolutei.set(100).gram_moles_of_i_per_kilograms
            molalityofsolutei.set(100).kilogram_mols_of_i_per_kilograms
            molalityofsolutei.set(100).kmols_of_i_per_kilograms
        """
        ...

# ============================================================================
# MOLAR CONCENTRATION BY MASS
# ============================================================================

class MolarConcentrationByMassSetter(TypeSafeSetter):
    """Molar Concentration by Mass-specific setter with only molar concentration by mass unit properties."""
    
    def __init__(self, variable: 'MolarConcentrationByMass', value: float) -> None: ...
    
    # All molar concentration by mass unit properties - provides fluent API with full type hints
    @property
    def gram_mole_or_mole_per_grams(self) -> 'MolarConcentrationByMass': ...
    @property
    def gram_mole_or_mole_per_kilograms(self) -> 'MolarConcentrationByMass': ...
    @property
    def kilogram_mole_or_kmol_per_kilograms(self) -> 'MolarConcentrationByMass': ...
    @property
    def micromole_per_grams(self) -> 'MolarConcentrationByMass': ...
    @property
    def millimole_per_grams(self) -> 'MolarConcentrationByMass': ...
    @property
    def picomole_per_grams(self) -> 'MolarConcentrationByMass': ...
    @property
    def pound_mole_per_pounds(self) -> 'MolarConcentrationByMass': ...

class MolarConcentrationByMass(TypedVariable):
    """Type-safe molar concentration by mass variable with expression capabilities."""
    
    _setter_class: Type[MolarConcentrationByMassSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarConcentrationByMassSetter:
        """
        Create a molar concentration by mass setter for fluent unit assignment.
        
        Example:
            molarconcentrationbymass.set(100).gram_mole_or_mole_per_grams
            molarconcentrationbymass.set(100).gram_mole_or_mole_per_kilograms
            molarconcentrationbymass.set(100).kilogram_mole_or_kmol_per_kilograms
        """
        ...

# ============================================================================
# MOLAR FLOW RATE
# ============================================================================

class MolarFlowRateSetter(TypeSafeSetter):
    """Molar Flow Rate-specific setter with only molar flow rate unit properties."""
    
    def __init__(self, variable: 'MolarFlowRate', value: float) -> None: ...
    
    # All molar flow rate unit properties - provides fluent API with full type hints
    @property
    def gram_mole_per_days(self) -> 'MolarFlowRate': ...
    @property
    def gram_mole_per_hours(self) -> 'MolarFlowRate': ...
    @property
    def gram_mole_per_minutes(self) -> 'MolarFlowRate': ...
    @property
    def gram_mole_per_seconds(self) -> 'MolarFlowRate': ...
    @property
    def kilogram_mole_or_kmol_per_days(self) -> 'MolarFlowRate': ...
    @property
    def kilogram_mole_or_kmol_per_hours(self) -> 'MolarFlowRate': ...
    @property
    def kilogram_mole_or_kmol_per_minutes(self) -> 'MolarFlowRate': ...
    @property
    def kilogram_mole_or_kmol_per_seconds(self) -> 'MolarFlowRate': ...
    @property
    def pound_mole_or_lb_mol_per_days(self) -> 'MolarFlowRate': ...
    @property
    def pound_mole_or_lb_mol_per_hours(self) -> 'MolarFlowRate': ...
    @property
    def pound_mole_or_lb_mol_per_minutes(self) -> 'MolarFlowRate': ...
    @property
    def pound_mole_or_lb_mol_per_seconds(self) -> 'MolarFlowRate': ...

class MolarFlowRate(TypedVariable):
    """Type-safe molar flow rate variable with expression capabilities."""
    
    _setter_class: Type[MolarFlowRateSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarFlowRateSetter:
        """
        Create a molar flow rate setter for fluent unit assignment.
        
        Example:
            molarflowrate.set(100).gram_mole_per_days
            molarflowrate.set(100).gram_mole_per_hours
            molarflowrate.set(100).gram_mole_per_minutes
        """
        ...

# ============================================================================
# MOLAR FLUX
# ============================================================================

class MolarFluxSetter(TypeSafeSetter):
    """Molar Flux-specific setter with only molar flux unit properties."""
    
    def __init__(self, variable: 'MolarFlux', value: float) -> None: ...
    
    # All molar flux unit properties - provides fluent API with full type hints
    @property
    def kmol_per_square_meter_per_days(self) -> 'MolarFlux': ...
    @property
    def kmol_per_square_meter_per_hours(self) -> 'MolarFlux': ...
    @property
    def kmol_per_square_meter_per_minutes(self) -> 'MolarFlux': ...
    @property
    def kmol_per_square_meter_per_seconds(self) -> 'MolarFlux': ...
    @property
    def pound_mole_per_square_foot_per_days(self) -> 'MolarFlux': ...
    @property
    def pound_mole_per_square_foot_per_hours(self) -> 'MolarFlux': ...
    @property
    def pound_mole_per_square_foot_per_minutes(self) -> 'MolarFlux': ...
    @property
    def pound_mole_per_square_foot_per_seconds(self) -> 'MolarFlux': ...

class MolarFlux(TypedVariable):
    """Type-safe molar flux variable with expression capabilities."""
    
    _setter_class: Type[MolarFluxSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarFluxSetter:
        """
        Create a molar flux setter for fluent unit assignment.
        
        Example:
            molarflux.set(100).kmol_per_square_meter_per_days
            molarflux.set(100).kmol_per_square_meter_per_hours
            molarflux.set(100).kmol_per_square_meter_per_minutes
        """
        ...

# ============================================================================
# MOLAR HEAT CAPACITY
# ============================================================================

class MolarHeatCapacitySetter(TypeSafeSetter):
    """Molar Heat Capacity-specific setter with only molar heat capacity unit properties."""
    
    def __init__(self, variable: 'MolarHeatCapacity', value: float) -> None: ...
    
    # All molar heat capacity unit properties - provides fluent API with full type hints
    @property
    def Btu_per_pound_mole_per_degree_Fahrenheit_or_degree_Rankines(self) -> 'MolarHeatCapacity': ...
    @property
    def calories_per_gram_mole_per_kelvin_or_degree_Celsius(self) -> 'MolarHeatCapacity': ...
    @property
    def joule_per_gram_mole_per_kelvin_or_degree_Celsius(self) -> 'MolarHeatCapacity': ...

class MolarHeatCapacity(TypedVariable):
    """Type-safe molar heat capacity variable with expression capabilities."""
    
    _setter_class: Type[MolarHeatCapacitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarHeatCapacitySetter:
        """
        Create a molar heat capacity setter for fluent unit assignment.
        
        Example:
            molarheatcapacity.set(100).Btu_per_pound_mole_per_degree_Fahrenheit_or_degree_Rankines
            molarheatcapacity.set(100).calories_per_gram_mole_per_kelvin_or_degree_Celsius
            molarheatcapacity.set(100).joule_per_gram_mole_per_kelvin_or_degree_Celsius
        """
        ...

# ============================================================================
# MOLARITY OF "I"
# ============================================================================

class MolarityOfISetter(TypeSafeSetter):
    """Molarity of "i"-specific setter with only molarity of "i" unit properties."""
    
    def __init__(self, variable: 'MolarityOfI', value: float) -> None: ...
    
    # All molarity of "i" unit properties - provides fluent API with full type hints
    @property
    def gram_moles_of_i_per_cubic_meters(self) -> 'MolarityOfI': ...
    @property
    def gram_moles_of_i_per_liters(self) -> 'MolarityOfI': ...
    @property
    def kilogram_moles_of_i_per_cubic_meters(self) -> 'MolarityOfI': ...
    @property
    def kilogram_moles_of_i_per_liters(self) -> 'MolarityOfI': ...
    @property
    def pound_moles_of_i_per_cubic_foots(self) -> 'MolarityOfI': ...
    @property
    def pound_moles_of_i_per_gallon_USs(self) -> 'MolarityOfI': ...

class MolarityOfI(TypedVariable):
    """Type-safe molarity of "i" variable with expression capabilities."""
    
    _setter_class: Type[MolarityOfISetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MolarityOfISetter:
        """
        Create a molarity of "i" setter for fluent unit assignment.
        
        Example:
            molarityofi.set(100).gram_moles_of_i_per_cubic_meters
            molarityofi.set(100).gram_moles_of_i_per_liters
            molarityofi.set(100).kilogram_moles_of_i_per_cubic_meters
        """
        ...

# ============================================================================
# MOLE FRACTION OF "I"
# ============================================================================

class MoleFractionOfISetter(TypeSafeSetter):
    """Mole Fraction of "i"-specific setter with only mole fraction of "i" unit properties."""
    
    def __init__(self, variable: 'MoleFractionOfI', value: float) -> None: ...
    
    # All mole fraction of "i" unit properties - provides fluent API with full type hints
    @property
    def gram_mole_of_i_per_gram_mole_totals(self) -> 'MoleFractionOfI': ...
    @property
    def kilogram_mole_of_i_per_kilogram_mole_totals(self) -> 'MoleFractionOfI': ...
    @property
    def kilomole_of_i_per_kilomole_totals(self) -> 'MoleFractionOfI': ...
    @property
    def pound_mole_of_i_per_pound_mole_totals(self) -> 'MoleFractionOfI': ...

class MoleFractionOfI(TypedVariable):
    """Type-safe mole fraction of "i" variable with expression capabilities."""
    
    _setter_class: Type[MoleFractionOfISetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MoleFractionOfISetter:
        """
        Create a mole fraction of "i" setter for fluent unit assignment.
        
        Example:
            molefractionofi.set(100).gram_mole_of_i_per_gram_mole_totals
            molefractionofi.set(100).kilogram_mole_of_i_per_kilogram_mole_totals
            molefractionofi.set(100).kilomole_of_i_per_kilomole_totals
        """
        ...

# ============================================================================
# MOMENT OF INERTIA
# ============================================================================

class MomentOfInertiaSetter(TypeSafeSetter):
    """Moment of Inertia-specific setter with only moment of inertia unit properties."""
    
    def __init__(self, variable: 'MomentOfInertia', value: float) -> None: ...
    
    # All moment of inertia unit properties - provides fluent API with full type hints
    @property
    def gram_force_centimeter_square_seconds(self) -> 'MomentOfInertia': ...
    @property
    def gram_square_centimeters(self) -> 'MomentOfInertia': ...
    @property
    def kilogram_force_centimeter_square_seconds(self) -> 'MomentOfInertia': ...
    @property
    def kilogram_force_meter_square_seconds(self) -> 'MomentOfInertia': ...
    @property
    def kilogram_square_centimeters(self) -> 'MomentOfInertia': ...
    @property
    def kilogram_square_meters(self) -> 'MomentOfInertia': ...
    @property
    def ounce_force_inch_square_seconds(self) -> 'MomentOfInertia': ...
    @property
    def ounce_mass_square_inchs(self) -> 'MomentOfInertia': ...
    @property
    def pound_mass_square_foots(self) -> 'MomentOfInertia': ...
    @property
    def pound_mass_square_inchs(self) -> 'MomentOfInertia': ...

class MomentOfInertia(TypedVariable):
    """Type-safe moment of inertia variable with expression capabilities."""
    
    _setter_class: Type[MomentOfInertiaSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MomentOfInertiaSetter:
        """
        Create a moment of inertia setter for fluent unit assignment.
        
        Example:
            momentofinertia.set(100).gram_force_centimeter_square_seconds
            momentofinertia.set(100).gram_square_centimeters
            momentofinertia.set(100).kilogram_force_centimeter_square_seconds
        """
        ...

# ============================================================================
# MOMENTUM FLOW RATE
# ============================================================================

class MomentumFlowRateSetter(TypeSafeSetter):
    """Momentum Flow Rate-specific setter with only momentum flow rate unit properties."""
    
    def __init__(self, variable: 'MomentumFlowRate', value: float) -> None: ...
    
    # All momentum flow rate unit properties - provides fluent API with full type hints
    @property
    def foot_pounds_per_square_hours(self) -> 'MomentumFlowRate': ...
    @property
    def foot_pounds_per_square_minutes(self) -> 'MomentumFlowRate': ...
    @property
    def foot_pounds_per_square_seconds(self) -> 'MomentumFlowRate': ...
    @property
    def gram_centimeters_per_square_seconds(self) -> 'MomentumFlowRate': ...
    @property
    def kilogram_meters_per_square_seconds(self) -> 'MomentumFlowRate': ...

class MomentumFlowRate(TypedVariable):
    """Type-safe momentum flow rate variable with expression capabilities."""
    
    _setter_class: Type[MomentumFlowRateSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MomentumFlowRateSetter:
        """
        Create a momentum flow rate setter for fluent unit assignment.
        
        Example:
            momentumflowrate.set(100).foot_pounds_per_square_hours
            momentumflowrate.set(100).foot_pounds_per_square_minutes
            momentumflowrate.set(100).foot_pounds_per_square_seconds
        """
        ...

# ============================================================================
# MOMENTUM FLUX
# ============================================================================

class MomentumFluxSetter(TypeSafeSetter):
    """Momentum Flux-specific setter with only momentum flux unit properties."""
    
    def __init__(self, variable: 'MomentumFlux', value: float) -> None: ...
    
    # All momentum flux unit properties - provides fluent API with full type hints
    @property
    def dyne_per_square_centimeters(self) -> 'MomentumFlux': ...
    @property
    def gram_per_centimeter_per_square_seconds(self) -> 'MomentumFlux': ...
    @property
    def newton_per_square_meters(self) -> 'MomentumFlux': ...
    @property
    def pound_force_per_square_foots(self) -> 'MomentumFlux': ...
    @property
    def pound_mass_per_foot_per_square_seconds(self) -> 'MomentumFlux': ...

class MomentumFlux(TypedVariable):
    """Type-safe momentum flux variable with expression capabilities."""
    
    _setter_class: Type[MomentumFluxSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> MomentumFluxSetter:
        """
        Create a momentum flux setter for fluent unit assignment.
        
        Example:
            momentumflux.set(100).dyne_per_square_centimeters
            momentumflux.set(100).gram_per_centimeter_per_square_seconds
            momentumflux.set(100).newton_per_square_meters
        """
        ...

# ============================================================================
# NORMALITY OF SOLUTION
# ============================================================================

class NormalityOfSolutionSetter(TypeSafeSetter):
    """Normality of Solution-specific setter with only normality of solution unit properties."""
    
    def __init__(self, variable: 'NormalityOfSolution', value: float) -> None: ...
    
    # All normality of solution unit properties - provides fluent API with full type hints
    @property
    def gram_equivalents_per_cubic_meters(self) -> 'NormalityOfSolution': ...
    @property
    def gram_equivalents_per_liters(self) -> 'NormalityOfSolution': ...
    @property
    def pound_equivalents_per_cubic_foots(self) -> 'NormalityOfSolution': ...
    @property
    def pound_equivalents_per_gallons(self) -> 'NormalityOfSolution': ...

class NormalityOfSolution(TypedVariable):
    """Type-safe normality of solution variable with expression capabilities."""
    
    _setter_class: Type[NormalityOfSolutionSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> NormalityOfSolutionSetter:
        """
        Create a normality of solution setter for fluent unit assignment.
        
        Example:
            normalityofsolution.set(100).gram_equivalents_per_cubic_meters
            normalityofsolution.set(100).gram_equivalents_per_liters
            normalityofsolution.set(100).pound_equivalents_per_cubic_foots
        """
        ...

# ============================================================================
# PARTICLE DENSITY
# ============================================================================

class ParticleDensitySetter(TypeSafeSetter):
    """Particle Density-specific setter with only particle density unit properties."""
    
    def __init__(self, variable: 'ParticleDensity', value: float) -> None: ...
    
    # All particle density unit properties - provides fluent API with full type hints
    @property
    def particles_per_cubic_centimeters(self) -> 'ParticleDensity': ...
    @property
    def particles_per_cubic_foots(self) -> 'ParticleDensity': ...
    @property
    def particles_per_cubic_meters(self) -> 'ParticleDensity': ...
    @property
    def particles_per_gallon_USs(self) -> 'ParticleDensity': ...
    @property
    def particles_per_liters(self) -> 'ParticleDensity': ...
    @property
    def particles_per_milliliters(self) -> 'ParticleDensity': ...

class ParticleDensity(TypedVariable):
    """Type-safe particle density variable with expression capabilities."""
    
    _setter_class: Type[ParticleDensitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ParticleDensitySetter:
        """
        Create a particle density setter for fluent unit assignment.
        
        Example:
            particledensity.set(100).particles_per_cubic_centimeters
            particledensity.set(100).particles_per_cubic_foots
            particledensity.set(100).particles_per_cubic_meters
        """
        ...

# ============================================================================
# PERMEABILITY
# ============================================================================

class PermeabilitySetter(TypeSafeSetter):
    """Permeability-specific setter with only permeability unit properties."""
    
    def __init__(self, variable: 'Permeability', value: float) -> None: ...
    
    # All permeability unit properties - provides fluent API with full type hints
    @property
    def darcys(self) -> 'Permeability': ...
    @property
    def square_feets(self) -> 'Permeability': ...
    @property
    def square_meters(self) -> 'Permeability': ...

class Permeability(TypedVariable):
    """Type-safe permeability variable with expression capabilities."""
    
    _setter_class: Type[PermeabilitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PermeabilitySetter:
        """
        Create a permeability setter for fluent unit assignment.
        
        Example:
            permeability.set(100).darcys
            permeability.set(100).square_feets
            permeability.set(100).square_meters
        """
        ...

# ============================================================================
# PHOTON EMISSION RATE
# ============================================================================

class PhotonEmissionRateSetter(TypeSafeSetter):
    """Photon Emission Rate-specific setter with only photon emission rate unit properties."""
    
    def __init__(self, variable: 'PhotonEmissionRate', value: float) -> None: ...
    
    # All photon emission rate unit properties - provides fluent API with full type hints
    @property
    def rayleighs(self) -> 'PhotonEmissionRate': ...
    @property
    def reciprocal_square_meter_seconds(self) -> 'PhotonEmissionRate': ...

class PhotonEmissionRate(TypedVariable):
    """Type-safe photon emission rate variable with expression capabilities."""
    
    _setter_class: Type[PhotonEmissionRateSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PhotonEmissionRateSetter:
        """
        Create a photon emission rate setter for fluent unit assignment.
        
        Example:
            photonemissionrate.set(100).rayleighs
            photonemissionrate.set(100).reciprocal_square_meter_seconds
        """
        ...

# ============================================================================
# POWER PER UNIT MASS OR SPECIFIC POWER
# ============================================================================

class PowerPerUnitMassSetter(TypeSafeSetter):
    """Power per Unit Mass or Specific Power-specific setter with only power per unit mass or specific power unit properties."""
    
    def __init__(self, variable: 'PowerPerUnitMass', value: float) -> None: ...
    
    # All power per unit mass or specific power unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_hour_per_pound_mass(self) -> 'PowerPerUnitMass': ...
    @property
    def calorie_per_second_per_grams(self) -> 'PowerPerUnitMass': ...
    @property
    def kilocalorie_per_hour_per_kilograms(self) -> 'PowerPerUnitMass': ...
    @property
    def watt_per_kilograms(self) -> 'PowerPerUnitMass': ...

class PowerPerUnitMass(TypedVariable):
    """Type-safe power per unit mass or specific power variable with expression capabilities."""
    
    _setter_class: Type[PowerPerUnitMassSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PowerPerUnitMassSetter:
        """
        Create a power per unit mass or specific power setter for fluent unit assignment.
        
        Example:
            powerperunitmass.set(100).British_thermal_unit_per_hour_per_pound_mass
            powerperunitmass.set(100).calorie_per_second_per_grams
            powerperunitmass.set(100).kilocalorie_per_hour_per_kilograms
        """
        ...

# ============================================================================
# POWER PER UNIT VOLUME OR POWER DENSITY
# ============================================================================

class PowerPerUnitVolumeSetter(TypeSafeSetter):
    """Power per Unit Volume or Power Density-specific setter with only power per unit volume or power density unit properties."""
    
    def __init__(self, variable: 'PowerPerUnitVolume', value: float) -> None: ...
    
    # All power per unit volume or power density unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_hour_per_cubic_foots(self) -> 'PowerPerUnitVolume': ...
    @property
    def calorie_per_second_per_cubic_centimeters(self) -> 'PowerPerUnitVolume': ...
    @property
    def Chu_per_hour_per_cubic_foots(self) -> 'PowerPerUnitVolume': ...
    @property
    def kilocalorie_per_hour_per_cubic_centimeters(self) -> 'PowerPerUnitVolume': ...
    @property
    def kilocalorie_per_hour_per_cubic_foots(self) -> 'PowerPerUnitVolume': ...
    @property
    def kilocalorie_per_second_per_cubic_centimeters(self) -> 'PowerPerUnitVolume': ...
    @property
    def watt_per_cubic_meters(self) -> 'PowerPerUnitVolume': ...

class PowerPerUnitVolume(TypedVariable):
    """Type-safe power per unit volume or power density variable with expression capabilities."""
    
    _setter_class: Type[PowerPerUnitVolumeSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PowerPerUnitVolumeSetter:
        """
        Create a power per unit volume or power density setter for fluent unit assignment.
        
        Example:
            powerperunitvolume.set(100).British_thermal_unit_per_hour_per_cubic_foots
            powerperunitvolume.set(100).calorie_per_second_per_cubic_centimeters
            powerperunitvolume.set(100).Chu_per_hour_per_cubic_foots
        """
        ...

# ============================================================================
# POWER, THERMAL DUTY
# ============================================================================

class PowerThermalDutySetter(TypeSafeSetter):
    """Power, Thermal Duty-specific setter with only power, thermal duty unit properties."""
    
    def __init__(self, variable: 'PowerThermalDuty', value: float) -> None: ...
    
    # All power, thermal duty unit properties - provides fluent API with full type hints
    @property
    def abwatt_emu_of_powers(self) -> 'PowerThermalDuty': ...
    @property
    def boiler_horsepowers(self) -> 'PowerThermalDuty': ...
    @property
    def British_thermal_unit_mean_per_hours(self) -> 'PowerThermalDuty': ...
    @property
    def British_thermal_unit_mean_per_minutes(self) -> 'PowerThermalDuty': ...
    @property
    def British_thermal_unit_thermochemical_per_hours(self) -> 'PowerThermalDuty': ...
    @property
    def British_thermal_unit_thermochemical_per_minutes(self) -> 'PowerThermalDuty': ...
    @property
    def calorie_mean_per_hours(self) -> 'PowerThermalDuty': ...
    @property
    def calorie_thermochemical_per_hours(self) -> 'PowerThermalDuty': ...
    @property
    def donkeys(self) -> 'PowerThermalDuty': ...
    @property
    def erg_per_seconds(self) -> 'PowerThermalDuty': ...
    @property
    def foot_pondal_per_seconds(self) -> 'PowerThermalDuty': ...
    @property
    def foot_pound_force_per_hours(self) -> 'PowerThermalDuty': ...
    @property
    def foot_pound_force_per_minutes(self) -> 'PowerThermalDuty': ...
    @property
    def foot_pound_force_per_seconds(self) -> 'PowerThermalDuty': ...
    @property
    def horsepower_550_mathrm_ft_mathrm_lb_mathrm_f_mathrm_s(self) -> 'PowerThermalDuty': ...
    @property
    def horsepower_electrics(self) -> 'PowerThermalDuty': ...
    @property
    def horsepower_UKs(self) -> 'PowerThermalDuty': ...
    @property
    def kcal_per_hours(self) -> 'PowerThermalDuty': ...
    @property
    def kilogram_force_meter_per_seconds(self) -> 'PowerThermalDuty': ...
    @property
    def kilowatts(self) -> 'PowerThermalDuty': ...
    @property
    def megawatts(self) -> 'PowerThermalDuty': ...
    @property
    def metric_horsepowers(self) -> 'PowerThermalDuty': ...
    @property
    def million_British_thermal_units_per_hour_petroleums(self) -> 'PowerThermalDuty': ...
    @property
    def million_kilocalorie_per_hours(self) -> 'PowerThermalDuty': ...
    @property
    def pronys(self) -> 'PowerThermalDuty': ...
    @property
    def ton_of_refrigeration_USs(self) -> 'PowerThermalDuty': ...
    @property
    def ton_or_refrigeration_UKs(self) -> 'PowerThermalDuty': ...
    @property
    def volt_amperes(self) -> 'PowerThermalDuty': ...
    @property
    def water_horsepowers(self) -> 'PowerThermalDuty': ...
    @property
    def watts(self) -> 'PowerThermalDuty': ...
    @property
    def watt_international_means(self) -> 'PowerThermalDuty': ...
    @property
    def watt_international_USs(self) -> 'PowerThermalDuty': ...

class PowerThermalDuty(TypedVariable):
    """Type-safe power, thermal duty variable with expression capabilities."""
    
    _setter_class: Type[PowerThermalDutySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PowerThermalDutySetter:
        """
        Create a power, thermal duty setter for fluent unit assignment.
        
        Example:
            powerthermalduty.set(100).abwatt_emu_of_powers
            powerthermalduty.set(100).boiler_horsepowers
            powerthermalduty.set(100).British_thermal_unit_mean_per_hours
        """
        ...

# ============================================================================
# PRESSURE
# ============================================================================

class PressureSetter(TypeSafeSetter):
    """Pressure-specific setter with only pressure unit properties."""
    
    def __init__(self, variable: 'Pressure', value: float) -> None: ...
    
    # All pressure unit properties - provides fluent API with full type hints
    @property
    def atmosphere_standards(self) -> 'Pressure': ...
    @property
    def bars(self) -> 'Pressure': ...
    @property
    def baryes(self) -> 'Pressure': ...
    @property
    def dyne_per_square_centimeters(self) -> 'Pressure': ...
    @property
    def foot_of_mercury_60_circ_mathrm_Fs(self) -> 'Pressure': ...
    @property
    def foot_of_water_60_circ_mathrm_Fs(self) -> 'Pressure': ...
    @property
    def gigapascals(self) -> 'Pressure': ...
    @property
    def hectopascals(self) -> 'Pressure': ...
    @property
    def inch_of_mercury_60_circ_mathrm_Fs(self) -> 'Pressure': ...
    @property
    def inch_of_water_60_circ_mathrm_Fs(self) -> 'Pressure': ...
    @property
    def kilogram_force_per_square_centimeters(self) -> 'Pressure': ...
    @property
    def kilogram_force_per_square_meters(self) -> 'Pressure': ...
    @property
    def kip_force_per_square_inchs(self) -> 'Pressure': ...
    @property
    def megapascals(self) -> 'Pressure': ...
    @property
    def meter_of_water_4_circ_mathrm_Cs(self) -> 'Pressure': ...
    @property
    def microbars(self) -> 'Pressure': ...
    @property
    def millibars(self) -> 'Pressure': ...
    @property
    def millimeter_of_mercury_4_circ_mathrm_Cs(self) -> 'Pressure': ...
    @property
    def millimeter_of_water_4_circ_mathrm_Cs(self) -> 'Pressure': ...
    @property
    def newton_per_square_meters(self) -> 'Pressure': ...
    @property
    def ounce_force_per_square_inchs(self) -> 'Pressure': ...
    @property
    def pascals(self) -> 'Pressure': ...
    @property
    def pi_zes(self) -> 'Pressure': ...
    @property
    def pound_force_per_square_foots(self) -> 'Pressure': ...
    @property
    def pound_force_per_square_inchs(self) -> 'Pressure': ...
    @property
    def torrs(self) -> 'Pressure': ...

class Pressure(TypedVariable):
    """Type-safe pressure variable with expression capabilities."""
    
    _setter_class: Type[PressureSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> PressureSetter:
        """
        Create a pressure setter for fluent unit assignment.
        
        Example:
            pressure.set(100).atmosphere_standards
            pressure.set(100).bars
            pressure.set(100).baryes
        """
        ...

# ============================================================================
# RADIATION DOSE EQUIVALENT
# ============================================================================

class RadiationDoseEquivalentSetter(TypeSafeSetter):
    """Radiation Dose Equivalent-specific setter with only radiation dose equivalent unit properties."""
    
    def __init__(self, variable: 'RadiationDoseEquivalent', value: float) -> None: ...
    
    # All radiation dose equivalent unit properties - provides fluent API with full type hints
    @property
    def rems(self) -> 'RadiationDoseEquivalent': ...
    @property
    def sieverts(self) -> 'RadiationDoseEquivalent': ...

class RadiationDoseEquivalent(TypedVariable):
    """Type-safe radiation dose equivalent variable with expression capabilities."""
    
    _setter_class: Type[RadiationDoseEquivalentSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> RadiationDoseEquivalentSetter:
        """
        Create a radiation dose equivalent setter for fluent unit assignment.
        
        Example:
            radiationdoseequivalent.set(100).rems
            radiationdoseequivalent.set(100).sieverts
        """
        ...

# ============================================================================
# RADIATION EXPOSURE
# ============================================================================

class RadiationExposureSetter(TypeSafeSetter):
    """Radiation Exposure-specific setter with only radiation exposure unit properties."""
    
    def __init__(self, variable: 'RadiationExposure', value: float) -> None: ...
    
    # All radiation exposure unit properties - provides fluent API with full type hints
    @property
    def coulomb_per_kilograms(self) -> 'RadiationExposure': ...
    @property
    def D_units(self) -> 'RadiationExposure': ...
    @property
    def pastille_dose_B_units(self) -> 'RadiationExposure': ...
    @property
    def r_entgens(self) -> 'RadiationExposure': ...

class RadiationExposure(TypedVariable):
    """Type-safe radiation exposure variable with expression capabilities."""
    
    _setter_class: Type[RadiationExposureSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> RadiationExposureSetter:
        """
        Create a radiation exposure setter for fluent unit assignment.
        
        Example:
            radiationexposure.set(100).coulomb_per_kilograms
            radiationexposure.set(100).D_units
            radiationexposure.set(100).pastille_dose_B_units
        """
        ...

# ============================================================================
# RADIOACTIVITY
# ============================================================================

class RadioactivitySetter(TypeSafeSetter):
    """Radioactivity-specific setter with only radioactivity unit properties."""
    
    def __init__(self, variable: 'Radioactivity', value: float) -> None: ...
    
    # All radioactivity unit properties - provides fluent API with full type hints
    @property
    def becquerels(self) -> 'Radioactivity': ...
    @property
    def curies(self) -> 'Radioactivity': ...
    @property
    def Mache_units(self) -> 'Radioactivity': ...
    @property
    def rutherfords(self) -> 'Radioactivity': ...
    @property
    def stats(self) -> 'Radioactivity': ...

class Radioactivity(TypedVariable):
    """Type-safe radioactivity variable with expression capabilities."""
    
    _setter_class: Type[RadioactivitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> RadioactivitySetter:
        """
        Create a radioactivity setter for fluent unit assignment.
        
        Example:
            radioactivity.set(100).becquerels
            radioactivity.set(100).curies
            radioactivity.set(100).Mache_units
        """
        ...

# ============================================================================
# SECOND MOMENT OF AREA
# ============================================================================

class SecondMomentOfAreaSetter(TypeSafeSetter):
    """Second Moment of Area-specific setter with only second moment of area unit properties."""
    
    def __init__(self, variable: 'SecondMomentOfArea', value: float) -> None: ...
    
    # All second moment of area unit properties - provides fluent API with full type hints
    @property
    def inch_quadrupleds(self) -> 'SecondMomentOfArea': ...
    @property
    def centimeter_quadrupleds(self) -> 'SecondMomentOfArea': ...
    @property
    def foot_quadrupleds(self) -> 'SecondMomentOfArea': ...
    @property
    def meter_quadrupleds(self) -> 'SecondMomentOfArea': ...

class SecondMomentOfArea(TypedVariable):
    """Type-safe second moment of area variable with expression capabilities."""
    
    _setter_class: Type[SecondMomentOfAreaSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SecondMomentOfAreaSetter:
        """
        Create a second moment of area setter for fluent unit assignment.
        
        Example:
            secondmomentofarea.set(100).inch_quadrupleds
            secondmomentofarea.set(100).centimeter_quadrupleds
            secondmomentofarea.set(100).foot_quadrupleds
        """
        ...

# ============================================================================
# SECOND RADIATION CONSTANT (PLANCK)
# ============================================================================

class SecondRadiationConstantPlanckSetter(TypeSafeSetter):
    """Second Radiation Constant (Planck)-specific setter with only second radiation constant (planck) unit properties."""
    
    def __init__(self, variable: 'SecondRadiationConstantPlanck', value: float) -> None: ...
    
    # All second radiation constant (planck) unit properties - provides fluent API with full type hints
    @property
    def meter_kelvins(self) -> 'SecondRadiationConstantPlanck': ...

class SecondRadiationConstantPlanck(TypedVariable):
    """Type-safe second radiation constant (planck) variable with expression capabilities."""
    
    _setter_class: Type[SecondRadiationConstantPlanckSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SecondRadiationConstantPlanckSetter:
        """
        Create a second radiation constant (planck) setter for fluent unit assignment.
        
        Example:
            secondradiationconstantplanck.set(100).meter_kelvins
        """
        ...

# ============================================================================
# SPECIFIC ENTHALPY
# ============================================================================

class SpecificEnthalpySetter(TypeSafeSetter):
    """Specific Enthalpy-specific setter with only specific enthalpy unit properties."""
    
    def __init__(self, variable: 'SpecificEnthalpy', value: float) -> None: ...
    
    # All specific enthalpy unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_mean_per_pounds(self) -> 'SpecificEnthalpy': ...
    @property
    def British_thermal_unit_per_pounds(self) -> 'SpecificEnthalpy': ...
    @property
    def calorie_per_grams(self) -> 'SpecificEnthalpy': ...
    @property
    def Chu_per_pounds(self) -> 'SpecificEnthalpy': ...
    @property
    def joule_per_kilograms(self) -> 'SpecificEnthalpy': ...
    @property
    def kilojoule_per_kilograms(self) -> 'SpecificEnthalpy': ...

class SpecificEnthalpy(TypedVariable):
    """Type-safe specific enthalpy variable with expression capabilities."""
    
    _setter_class: Type[SpecificEnthalpySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificEnthalpySetter:
        """
        Create a specific enthalpy setter for fluent unit assignment.
        
        Example:
            specificenthalpy.set(100).British_thermal_unit_mean_per_pounds
            specificenthalpy.set(100).British_thermal_unit_per_pounds
            specificenthalpy.set(100).calorie_per_grams
        """
        ...

# ============================================================================
# SPECIFIC GRAVITY
# ============================================================================

class SpecificGravitySetter(TypeSafeSetter):
    """Specific Gravity-specific setter with only specific gravity unit properties."""
    
    def __init__(self, variable: 'SpecificGravity', value: float) -> None: ...
    
    # All specific gravity unit properties - provides fluent API with full type hints
    @property
    def Dimensionless(self) -> 'SpecificGravity': ...

class SpecificGravity(TypedVariable):
    """Type-safe specific gravity variable with expression capabilities."""
    
    _setter_class: Type[SpecificGravitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
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
    
    def __init__(self, variable: 'SpecificHeatCapacityConstantPressure', value: float) -> None: ...
    
    # All specific heat capacity (constant pressure) unit properties - provides fluent API with full type hints
    @property
    def Btu_per_pound_per_degree_Fahrenheit_or_degree_Rankines(self) -> 'SpecificHeatCapacityConstantPressure': ...
    @property
    def calories_per_gram_per_kelvin_or_degree_Celsius(self) -> 'SpecificHeatCapacityConstantPressure': ...
    @property
    def joules_per_kilogram_per_kelvin_or_degree_Celsius(self) -> 'SpecificHeatCapacityConstantPressure': ...

class SpecificHeatCapacityConstantPressure(TypedVariable):
    """Type-safe specific heat capacity (constant pressure) variable with expression capabilities."""
    
    _setter_class: Type[SpecificHeatCapacityConstantPressureSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificHeatCapacityConstantPressureSetter:
        """
        Create a specific heat capacity (constant pressure) setter for fluent unit assignment.
        
        Example:
            specificheatcapacityconstantpressure.set(100).Btu_per_pound_per_degree_Fahrenheit_or_degree_Rankines
            specificheatcapacityconstantpressure.set(100).calories_per_gram_per_kelvin_or_degree_Celsius
            specificheatcapacityconstantpressure.set(100).joules_per_kilogram_per_kelvin_or_degree_Celsius
        """
        ...

# ============================================================================
# SPECIFIC LENGTH
# ============================================================================

class SpecificLengthSetter(TypeSafeSetter):
    """Specific Length-specific setter with only specific length unit properties."""
    
    def __init__(self, variable: 'SpecificLength', value: float) -> None: ...
    
    # All specific length unit properties - provides fluent API with full type hints
    @property
    def centimeter_per_grams(self) -> 'SpecificLength': ...
    @property
    def cotton_counts(self) -> 'SpecificLength': ...
    @property
    def ft_per_pounds(self) -> 'SpecificLength': ...
    @property
    def meters_per_kilograms(self) -> 'SpecificLength': ...
    @property
    def newton_meters(self) -> 'SpecificLength': ...
    @property
    def worsteds(self) -> 'SpecificLength': ...

class SpecificLength(TypedVariable):
    """Type-safe specific length variable with expression capabilities."""
    
    _setter_class: Type[SpecificLengthSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificLengthSetter:
        """
        Create a specific length setter for fluent unit assignment.
        
        Example:
            specificlength.set(100).centimeter_per_grams
            specificlength.set(100).cotton_counts
            specificlength.set(100).ft_per_pounds
        """
        ...

# ============================================================================
# SPECIFIC SURFACE
# ============================================================================

class SpecificSurfaceSetter(TypeSafeSetter):
    """Specific Surface-specific setter with only specific surface unit properties."""
    
    def __init__(self, variable: 'SpecificSurface', value: float) -> None: ...
    
    # All specific surface unit properties - provides fluent API with full type hints
    @property
    def square_centimeter_per_grams(self) -> 'SpecificSurface': ...
    @property
    def square_foot_per_kilograms(self) -> 'SpecificSurface': ...
    @property
    def square_foot_per_pounds(self) -> 'SpecificSurface': ...
    @property
    def square_meter_per_grams(self) -> 'SpecificSurface': ...
    @property
    def square_meter_per_kilograms(self) -> 'SpecificSurface': ...

class SpecificSurface(TypedVariable):
    """Type-safe specific surface variable with expression capabilities."""
    
    _setter_class: Type[SpecificSurfaceSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificSurfaceSetter:
        """
        Create a specific surface setter for fluent unit assignment.
        
        Example:
            specificsurface.set(100).square_centimeter_per_grams
            specificsurface.set(100).square_foot_per_kilograms
            specificsurface.set(100).square_foot_per_pounds
        """
        ...

# ============================================================================
# SPECIFIC VOLUME
# ============================================================================

class SpecificVolumeSetter(TypeSafeSetter):
    """Specific Volume-specific setter with only specific volume unit properties."""
    
    def __init__(self, variable: 'SpecificVolume', value: float) -> None: ...
    
    # All specific volume unit properties - provides fluent API with full type hints
    @property
    def cubic_centimeter_per_grams(self) -> 'SpecificVolume': ...
    @property
    def cubic_foot_per_kilograms(self) -> 'SpecificVolume': ...
    @property
    def cubic_foot_per_pounds(self) -> 'SpecificVolume': ...
    @property
    def cubic_meter_per_kilograms(self) -> 'SpecificVolume': ...

class SpecificVolume(TypedVariable):
    """Type-safe specific volume variable with expression capabilities."""
    
    _setter_class: Type[SpecificVolumeSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SpecificVolumeSetter:
        """
        Create a specific volume setter for fluent unit assignment.
        
        Example:
            specificvolume.set(100).cubic_centimeter_per_grams
            specificvolume.set(100).cubic_foot_per_kilograms
            specificvolume.set(100).cubic_foot_per_pounds
        """
        ...

# ============================================================================
# STRESS
# ============================================================================

class StressSetter(TypeSafeSetter):
    """Stress-specific setter with only stress unit properties."""
    
    def __init__(self, variable: 'Stress', value: float) -> None: ...
    
    # All stress unit properties - provides fluent API with full type hints
    @property
    def dyne_per_square_centimeters(self) -> 'Stress': ...
    @property
    def gigapascals(self) -> 'Stress': ...
    @property
    def hectopascals(self) -> 'Stress': ...
    @property
    def kilogram_force_per_square_centimeters(self) -> 'Stress': ...
    @property
    def kilogram_force_per_square_meters(self) -> 'Stress': ...
    @property
    def kip_force_per_square_inchs(self) -> 'Stress': ...
    @property
    def megapascals(self) -> 'Stress': ...
    @property
    def newton_per_square_meters(self) -> 'Stress': ...
    @property
    def ounce_force_per_square_inchs(self) -> 'Stress': ...
    @property
    def pascals(self) -> 'Stress': ...
    @property
    def pound_force_per_square_foots(self) -> 'Stress': ...
    @property
    def pound_force_per_square_inchs(self) -> 'Stress': ...

class Stress(TypedVariable):
    """Type-safe stress variable with expression capabilities."""
    
    _setter_class: Type[StressSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> StressSetter:
        """
        Create a stress setter for fluent unit assignment.
        
        Example:
            stress.set(100).dyne_per_square_centimeters
            stress.set(100).gigapascals
            stress.set(100).hectopascals
        """
        ...

# ============================================================================
# SURFACE MASS DENSITY
# ============================================================================

class SurfaceMassDensitySetter(TypeSafeSetter):
    """Surface Mass Density-specific setter with only surface mass density unit properties."""
    
    def __init__(self, variable: 'SurfaceMassDensity', value: float) -> None: ...
    
    # All surface mass density unit properties - provides fluent API with full type hints
    @property
    def gram_per_square_centimeters(self) -> 'SurfaceMassDensity': ...
    @property
    def gram_per_square_meters(self) -> 'SurfaceMassDensity': ...
    @property
    def kilogram_per_square_meters(self) -> 'SurfaceMassDensity': ...
    @property
    def pound_mass_per_square_foots(self) -> 'SurfaceMassDensity': ...
    @property
    def pound_mass_per_square_inchs(self) -> 'SurfaceMassDensity': ...

class SurfaceMassDensity(TypedVariable):
    """Type-safe surface mass density variable with expression capabilities."""
    
    _setter_class: Type[SurfaceMassDensitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SurfaceMassDensitySetter:
        """
        Create a surface mass density setter for fluent unit assignment.
        
        Example:
            surfacemassdensity.set(100).gram_per_square_centimeters
            surfacemassdensity.set(100).gram_per_square_meters
            surfacemassdensity.set(100).kilogram_per_square_meters
        """
        ...

# ============================================================================
# SURFACE TENSION
# ============================================================================

class SurfaceTensionSetter(TypeSafeSetter):
    """Surface Tension-specific setter with only surface tension unit properties."""
    
    def __init__(self, variable: 'SurfaceTension', value: float) -> None: ...
    
    # All surface tension unit properties - provides fluent API with full type hints
    @property
    def dyne_per_centimeters(self) -> 'SurfaceTension': ...
    @property
    def gram_force_per_centimeters(self) -> 'SurfaceTension': ...
    @property
    def newton_per_meters(self) -> 'SurfaceTension': ...
    @property
    def pound_force_per_foots(self) -> 'SurfaceTension': ...
    @property
    def pound_force_per_inchs(self) -> 'SurfaceTension': ...

class SurfaceTension(TypedVariable):
    """Type-safe surface tension variable with expression capabilities."""
    
    _setter_class: Type[SurfaceTensionSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> SurfaceTensionSetter:
        """
        Create a surface tension setter for fluent unit assignment.
        
        Example:
            surfacetension.set(100).dyne_per_centimeters
            surfacetension.set(100).gram_force_per_centimeters
            surfacetension.set(100).newton_per_meters
        """
        ...

# ============================================================================
# TEMPERATURE
# ============================================================================

class TemperatureSetter(TypeSafeSetter):
    """Temperature-specific setter with only temperature unit properties."""
    
    def __init__(self, variable: 'Temperature', value: float) -> None: ...
    
    # All temperature unit properties - provides fluent API with full type hints
    @property
    def degree_Celsius_unit_sizes(self) -> 'Temperature': ...
    @property
    def degree_Fahrenheit_unit_sizes(self) -> 'Temperature': ...
    @property
    def degree_R_aumur_unit_sizes(self) -> 'Temperature': ...
    @property
    def kelvin_absolute_scales(self) -> 'Temperature': ...
    @property
    def Rankine_absolute_scales(self) -> 'Temperature': ...

class Temperature(TypedVariable):
    """Type-safe temperature variable with expression capabilities."""
    
    _setter_class: Type[TemperatureSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TemperatureSetter:
        """
        Create a temperature setter for fluent unit assignment.
        
        Example:
            temperature.set(100).degree_Celsius_unit_sizes
            temperature.set(100).degree_Fahrenheit_unit_sizes
            temperature.set(100).degree_R_aumur_unit_sizes
        """
        ...

# ============================================================================
# THERMAL CONDUCTIVITY
# ============================================================================

class ThermalConductivitySetter(TypeSafeSetter):
    """Thermal Conductivity-specific setter with only thermal conductivity unit properties."""
    
    def __init__(self, variable: 'ThermalConductivity', value: float) -> None: ...
    
    # All thermal conductivity unit properties - provides fluent API with full type hints
    @property
    def Btu_IT_per_inch_per_hour_per_degree_Fahrenheits(self) -> 'ThermalConductivity': ...
    @property
    def Btu_therm_per_foot_per_hour_per_degree_Fahrenheits(self) -> 'ThermalConductivity': ...
    @property
    def Btu_therm_per_inch_per_hour_per_degree_Fahrenheits(self) -> 'ThermalConductivity': ...
    @property
    def calorie_therm_per_centimeter_per_second_per_degree_Celsius(self) -> 'ThermalConductivity': ...
    @property
    def joule_per_second_per_centimeter_per_kelvins(self) -> 'ThermalConductivity': ...
    @property
    def watt_per_centimeter_per_kelvins(self) -> 'ThermalConductivity': ...
    @property
    def watt_per_meter_per_kelvins(self) -> 'ThermalConductivity': ...

class ThermalConductivity(TypedVariable):
    """Type-safe thermal conductivity variable with expression capabilities."""
    
    _setter_class: Type[ThermalConductivitySetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ThermalConductivitySetter:
        """
        Create a thermal conductivity setter for fluent unit assignment.
        
        Example:
            thermalconductivity.set(100).Btu_IT_per_inch_per_hour_per_degree_Fahrenheits
            thermalconductivity.set(100).Btu_therm_per_foot_per_hour_per_degree_Fahrenheits
            thermalconductivity.set(100).Btu_therm_per_inch_per_hour_per_degree_Fahrenheits
        """
        ...

# ============================================================================
# TIME
# ============================================================================

class TimeSetter(TypeSafeSetter):
    """Time-specific setter with only time unit properties."""
    
    def __init__(self, variable: 'Time', value: float) -> None: ...
    
    # All time unit properties - provides fluent API with full type hints
    @property
    def blinks(self) -> 'Time': ...
    @property
    def centurys(self) -> 'Time': ...
    @property
    def chronon_or_tempons(self) -> 'Time': ...
    @property
    def gigan_or_eons(self) -> 'Time': ...
    @property
    def hours(self) -> 'Time': ...
    @property
    def Julian_years(self) -> 'Time': ...
    @property
    def mean_solar_days(self) -> 'Time': ...
    @property
    def milleniums(self) -> 'Time': ...
    @property
    def minutes(self) -> 'Time': ...
    @property
    def seconds(self) -> 'Time': ...
    @property
    def shakes(self) -> 'Time': ...
    @property
    def sidereal_year_1900_ADs(self) -> 'Time': ...
    @property
    def tropical_years(self) -> 'Time': ...
    @property
    def winks(self) -> 'Time': ...
    @property
    def years(self) -> 'Time': ...

class Time(TypedVariable):
    """Type-safe time variable with expression capabilities."""
    
    _setter_class: Type[TimeSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TimeSetter:
        """
        Create a time setter for fluent unit assignment.
        
        Example:
            time.set(100).blinks
            time.set(100).centurys
            time.set(100).chronon_or_tempons
        """
        ...

# ============================================================================
# TORQUE
# ============================================================================

class TorqueSetter(TypeSafeSetter):
    """Torque-specific setter with only torque unit properties."""
    
    def __init__(self, variable: 'Torque', value: float) -> None: ...
    
    # All torque unit properties - provides fluent API with full type hints
    @property
    def centimeter_kilogram_forces(self) -> 'Torque': ...
    @property
    def dyne_centimeters(self) -> 'Torque': ...
    @property
    def foot_kilogram_forces(self) -> 'Torque': ...
    @property
    def foot_pound_forces(self) -> 'Torque': ...
    @property
    def foot_poundals(self) -> 'Torque': ...
    @property
    def in_pound_forces(self) -> 'Torque': ...
    @property
    def inch_ounce_forces(self) -> 'Torque': ...
    @property
    def meter_kilogram_forces(self) -> 'Torque': ...
    @property
    def newton_centimeters(self) -> 'Torque': ...
    @property
    def newton_meters(self) -> 'Torque': ...

class Torque(TypedVariable):
    """Type-safe torque variable with expression capabilities."""
    
    _setter_class: Type[TorqueSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TorqueSetter:
        """
        Create a torque setter for fluent unit assignment.
        
        Example:
            torque.set(100).centimeter_kilogram_forces
            torque.set(100).dyne_centimeters
            torque.set(100).foot_kilogram_forces
        """
        ...

# ============================================================================
# TURBULENCE ENERGY DISSIPATION RATE
# ============================================================================

class TurbulenceEnergyDissipationRateSetter(TypeSafeSetter):
    """Turbulence Energy Dissipation Rate-specific setter with only turbulence energy dissipation rate unit properties."""
    
    def __init__(self, variable: 'TurbulenceEnergyDissipationRate', value: float) -> None: ...
    
    # All turbulence energy dissipation rate unit properties - provides fluent API with full type hints
    @property
    def square_foot_per_cubic_seconds(self) -> 'TurbulenceEnergyDissipationRate': ...
    @property
    def square_meter_per_cubic_seconds(self) -> 'TurbulenceEnergyDissipationRate': ...

class TurbulenceEnergyDissipationRate(TypedVariable):
    """Type-safe turbulence energy dissipation rate variable with expression capabilities."""
    
    _setter_class: Type[TurbulenceEnergyDissipationRateSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> TurbulenceEnergyDissipationRateSetter:
        """
        Create a turbulence energy dissipation rate setter for fluent unit assignment.
        
        Example:
            turbulenceenergydissipationrate.set(100).square_foot_per_cubic_seconds
            turbulenceenergydissipationrate.set(100).square_meter_per_cubic_seconds
        """
        ...

# ============================================================================
# VELOCITY, ANGULAR
# ============================================================================

class VelocityAngularSetter(TypeSafeSetter):
    """Velocity, Angular-specific setter with only velocity, angular unit properties."""
    
    def __init__(self, variable: 'VelocityAngular', value: float) -> None: ...
    
    # All velocity, angular unit properties - provides fluent API with full type hints
    @property
    def degree_per_minutes(self) -> 'VelocityAngular': ...
    @property
    def degree_per_seconds(self) -> 'VelocityAngular': ...
    @property
    def grade_per_minutes(self) -> 'VelocityAngular': ...
    @property
    def radian_per_minutes(self) -> 'VelocityAngular': ...
    @property
    def radian_per_seconds(self) -> 'VelocityAngular': ...
    @property
    def revolution_per_minutes(self) -> 'VelocityAngular': ...
    @property
    def revolution_per_seconds(self) -> 'VelocityAngular': ...
    @property
    def turn_per_minutes(self) -> 'VelocityAngular': ...

class VelocityAngular(TypedVariable):
    """Type-safe velocity, angular variable with expression capabilities."""
    
    _setter_class: Type[VelocityAngularSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VelocityAngularSetter:
        """
        Create a velocity, angular setter for fluent unit assignment.
        
        Example:
            velocityangular.set(100).degree_per_minutes
            velocityangular.set(100).degree_per_seconds
            velocityangular.set(100).grade_per_minutes
        """
        ...

# ============================================================================
# VELOCITY, LINEAR
# ============================================================================

class VelocityLinearSetter(TypeSafeSetter):
    """Velocity, Linear-specific setter with only velocity, linear unit properties."""
    
    def __init__(self, variable: 'VelocityLinear', value: float) -> None: ...
    
    # All velocity, linear unit properties - provides fluent API with full type hints
    @property
    def foot_per_hours(self) -> 'VelocityLinear': ...
    @property
    def foot_per_minutes(self) -> 'VelocityLinear': ...
    @property
    def foot_per_seconds(self) -> 'VelocityLinear': ...
    @property
    def inch_per_seconds(self) -> 'VelocityLinear': ...
    @property
    def international_knots(self) -> 'VelocityLinear': ...
    @property
    def kilometer_per_hours(self) -> 'VelocityLinear': ...
    @property
    def kilometer_per_seconds(self) -> 'VelocityLinear': ...
    @property
    def meter_per_seconds(self) -> 'VelocityLinear': ...
    @property
    def mile_per_hours(self) -> 'VelocityLinear': ...

class VelocityLinear(TypedVariable):
    """Type-safe velocity, linear variable with expression capabilities."""
    
    _setter_class: Type[VelocityLinearSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VelocityLinearSetter:
        """
        Create a velocity, linear setter for fluent unit assignment.
        
        Example:
            velocitylinear.set(100).foot_per_hours
            velocitylinear.set(100).foot_per_minutes
            velocitylinear.set(100).foot_per_seconds
        """
        ...

# ============================================================================
# VISCOSITY, DYNAMIC
# ============================================================================

class ViscosityDynamicSetter(TypeSafeSetter):
    """Viscosity, Dynamic-specific setter with only viscosity, dynamic unit properties."""
    
    def __init__(self, variable: 'ViscosityDynamic', value: float) -> None: ...
    
    # All viscosity, dynamic unit properties - provides fluent API with full type hints
    @property
    def centipoises(self) -> 'ViscosityDynamic': ...
    @property
    def dyne_second_per_square_centimeters(self) -> 'ViscosityDynamic': ...
    @property
    def kilopound_second_per_square_meters(self) -> 'ViscosityDynamic': ...
    @property
    def millipoises(self) -> 'ViscosityDynamic': ...
    @property
    def newton_second_per_square_meters(self) -> 'ViscosityDynamic': ...
    @property
    def pascal_seconds(self) -> 'ViscosityDynamic': ...
    @property
    def poises(self) -> 'ViscosityDynamic': ...
    @property
    def pound_force_hour_per_square_foots(self) -> 'ViscosityDynamic': ...
    @property
    def pound_force_second_per_square_foots(self) -> 'ViscosityDynamic': ...

class ViscosityDynamic(TypedVariable):
    """Type-safe viscosity, dynamic variable with expression capabilities."""
    
    _setter_class: Type[ViscosityDynamicSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ViscosityDynamicSetter:
        """
        Create a viscosity, dynamic setter for fluent unit assignment.
        
        Example:
            viscositydynamic.set(100).centipoises
            viscositydynamic.set(100).dyne_second_per_square_centimeters
            viscositydynamic.set(100).kilopound_second_per_square_meters
        """
        ...

# ============================================================================
# VISCOSITY, KINEMATIC
# ============================================================================

class ViscosityKinematicSetter(TypeSafeSetter):
    """Viscosity, Kinematic-specific setter with only viscosity, kinematic unit properties."""
    
    def __init__(self, variable: 'ViscosityKinematic', value: float) -> None: ...
    
    # All viscosity, kinematic unit properties - provides fluent API with full type hints
    @property
    def centistokes(self) -> 'ViscosityKinematic': ...
    @property
    def millistokes(self) -> 'ViscosityKinematic': ...
    @property
    def square_centimeter_per_seconds(self) -> 'ViscosityKinematic': ...
    @property
    def square_foot_per_hours(self) -> 'ViscosityKinematic': ...
    @property
    def square_foot_per_seconds(self) -> 'ViscosityKinematic': ...
    @property
    def square_meters_per_seconds(self) -> 'ViscosityKinematic': ...
    @property
    def stokes(self) -> 'ViscosityKinematic': ...

class ViscosityKinematic(TypedVariable):
    """Type-safe viscosity, kinematic variable with expression capabilities."""
    
    _setter_class: Type[ViscosityKinematicSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> ViscosityKinematicSetter:
        """
        Create a viscosity, kinematic setter for fluent unit assignment.
        
        Example:
            viscositykinematic.set(100).centistokes
            viscositykinematic.set(100).millistokes
            viscositykinematic.set(100).square_centimeter_per_seconds
        """
        ...

# ============================================================================
# VOLUME
# ============================================================================

class VolumeSetter(TypeSafeSetter):
    """Volume-specific setter with only volume unit properties."""
    
    def __init__(self, variable: 'Volume', value: float) -> None: ...
    
    # All volume unit properties - provides fluent API with full type hints
    @property
    def acre_foots(self) -> 'Volume': ...
    @property
    def acre_inchs(self) -> 'Volume': ...
    @property
    def barrel_US_Liquids(self) -> 'Volume': ...
    @property
    def barrel_US_Petros(self) -> 'Volume': ...
    @property
    def board_foot_measures(self) -> 'Volume': ...
    @property
    def bushel_US_Drys(self) -> 'Volume': ...
    @property
    def centiliters(self) -> 'Volume': ...
    @property
    def cords(self) -> 'Volume': ...
    @property
    def cord_foots(self) -> 'Volume': ...
    @property
    def cubic_centimeters(self) -> 'Volume': ...
    @property
    def cubic_decameters(self) -> 'Volume': ...
    @property
    def cubic_decimeters(self) -> 'Volume': ...
    @property
    def cubic_foots(self) -> 'Volume': ...
    @property
    def cubic_inchs(self) -> 'Volume': ...
    @property
    def cubic_kilometers(self) -> 'Volume': ...
    @property
    def cubic_meters(self) -> 'Volume': ...
    @property
    def cubic_micrometers(self) -> 'Volume': ...
    @property
    def cubic_mile_US_Intls(self) -> 'Volume': ...
    @property
    def cubic_millimeters(self) -> 'Volume': ...
    @property
    def cubic_yards(self) -> 'Volume': ...
    @property
    def decast_res(self) -> 'Volume': ...
    @property
    def deciliters(self) -> 'Volume': ...
    @property
    def fluid_drachm_UKs(self) -> 'Volume': ...
    @property
    def fluid_dram_USs(self) -> 'Volume': ...
    @property
    def fluid_ounce_USs(self) -> 'Volume': ...
    @property
    def gallon_Imperial_UKs(self) -> 'Volume': ...
    @property
    def gallon_US_Drys(self) -> 'Volume': ...
    @property
    def gallon_US_Liquids(self) -> 'Volume': ...
    @property
    def lasts(self) -> 'Volume': ...
    @property
    def liters(self) -> 'Volume': ...
    @property
    def microliters(self) -> 'Volume': ...
    @property
    def milliliters(self) -> 'Volume': ...
    @property
    def Mohr_centicubes(self) -> 'Volume': ...
    @property
    def pint_UKs(self) -> 'Volume': ...
    @property
    def pint_US_Drys(self) -> 'Volume': ...
    @property
    def pint_US_Liquids(self) -> 'Volume': ...
    @property
    def quart_US_Drys(self) -> 'Volume': ...
    @property
    def st_res(self) -> 'Volume': ...
    @property
    def tablespoon_Metrics(self) -> 'Volume': ...
    @property
    def tablespoon_USs(self) -> 'Volume': ...
    @property
    def teaspoon_USs(self) -> 'Volume': ...

class Volume(TypedVariable):
    """Type-safe volume variable with expression capabilities."""
    
    _setter_class: Type[VolumeSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumeSetter:
        """
        Create a volume setter for fluent unit assignment.
        
        Example:
            volume.set(100).acre_foots
            volume.set(100).acre_inchs
            volume.set(100).barrel_US_Liquids
        """
        ...

# ============================================================================
# VOLUME FRACTION OF "I"
# ============================================================================

class VolumeFractionOfISetter(TypeSafeSetter):
    """Volume Fraction of "i"-specific setter with only volume fraction of "i" unit properties."""
    
    def __init__(self, variable: 'VolumeFractionOfI', value: float) -> None: ...
    
    # All volume fraction of "i" unit properties - provides fluent API with full type hints
    @property
    def cubic_centimeters_of_i_per_cubic_meter_totals(self) -> 'VolumeFractionOfI': ...
    @property
    def cubic_foot_of_i_per_cubic_foot_totals(self) -> 'VolumeFractionOfI': ...
    @property
    def cubic_meters_of_i_per_cubic_meter_totals(self) -> 'VolumeFractionOfI': ...
    @property
    def gallons_of_i_per_gallon_totals(self) -> 'VolumeFractionOfI': ...

class VolumeFractionOfI(TypedVariable):
    """Type-safe volume fraction of "i" variable with expression capabilities."""
    
    _setter_class: Type[VolumeFractionOfISetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumeFractionOfISetter:
        """
        Create a volume fraction of "i" setter for fluent unit assignment.
        
        Example:
            volumefractionofi.set(100).cubic_centimeters_of_i_per_cubic_meter_totals
            volumefractionofi.set(100).cubic_foot_of_i_per_cubic_foot_totals
            volumefractionofi.set(100).cubic_meters_of_i_per_cubic_meter_totals
        """
        ...

# ============================================================================
# VOLUMETRIC CALORIFIC (HEATING) VALUE
# ============================================================================

class VolumetricCalorificHeatingValueSetter(TypeSafeSetter):
    """Volumetric Calorific (Heating) Value-specific setter with only volumetric calorific (heating) value unit properties."""
    
    def __init__(self, variable: 'VolumetricCalorificHeatingValue', value: float) -> None: ...
    
    # All volumetric calorific (heating) value unit properties - provides fluent API with full type hints
    @property
    def British_thermal_unit_per_cubic_foots(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def British_thermal_unit_per_gallon_UKs(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def British_thermal_unit_per_gallon_USs(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def calorie_per_cubic_centimeters(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def Chu_per_cubic_foots(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def joule_per_cubic_meters(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def kilocalorie_per_cubic_foots(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def kilocalorie_per_cubic_meters(self) -> 'VolumetricCalorificHeatingValue': ...
    @property
    def therm_100_K_Btu_per_cubic_foots(self) -> 'VolumetricCalorificHeatingValue': ...

class VolumetricCalorificHeatingValue(TypedVariable):
    """Type-safe volumetric calorific (heating) value variable with expression capabilities."""
    
    _setter_class: Type[VolumetricCalorificHeatingValueSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricCalorificHeatingValueSetter:
        """
        Create a volumetric calorific (heating) value setter for fluent unit assignment.
        
        Example:
            volumetriccalorificheatingvalue.set(100).British_thermal_unit_per_cubic_foots
            volumetriccalorificheatingvalue.set(100).British_thermal_unit_per_gallon_UKs
            volumetriccalorificheatingvalue.set(100).British_thermal_unit_per_gallon_USs
        """
        ...

# ============================================================================
# VOLUMETRIC COEFFICIENT OF EXPANSION
# ============================================================================

class VolumetricCoefficientOfExpansionSetter(TypeSafeSetter):
    """Volumetric Coefficient of Expansion-specific setter with only volumetric coefficient of expansion unit properties."""
    
    def __init__(self, variable: 'VolumetricCoefficientOfExpansion', value: float) -> None: ...
    
    # All volumetric coefficient of expansion unit properties - provides fluent API with full type hints
    @property
    def gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius(self) -> 'VolumetricCoefficientOfExpansion': ...
    @property
    def kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius(self) -> 'VolumetricCoefficientOfExpansion': ...
    @property
    def pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankines(self) -> 'VolumetricCoefficientOfExpansion': ...
    @property
    def pound_per_cubic_foot_per_kelvin_or_degree_Celsius(self) -> 'VolumetricCoefficientOfExpansion': ...

class VolumetricCoefficientOfExpansion(TypedVariable):
    """Type-safe volumetric coefficient of expansion variable with expression capabilities."""
    
    _setter_class: Type[VolumetricCoefficientOfExpansionSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricCoefficientOfExpansionSetter:
        """
        Create a volumetric coefficient of expansion setter for fluent unit assignment.
        
        Example:
            volumetriccoefficientofexpansion.set(100).gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius
            volumetriccoefficientofexpansion.set(100).kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius
            volumetriccoefficientofexpansion.set(100).pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankines
        """
        ...

# ============================================================================
# VOLUMETRIC FLOW RATE
# ============================================================================

class VolumetricFlowRateSetter(TypeSafeSetter):
    """Volumetric Flow Rate-specific setter with only volumetric flow rate unit properties."""
    
    def __init__(self, variable: 'VolumetricFlowRate', value: float) -> None: ...
    
    # All volumetric flow rate unit properties - provides fluent API with full type hints
    @property
    def cubic_feet_per_days(self) -> 'VolumetricFlowRate': ...
    @property
    def cubic_feet_per_hours(self) -> 'VolumetricFlowRate': ...
    @property
    def cubic_feet_per_minutes(self) -> 'VolumetricFlowRate': ...
    @property
    def cubic_feet_per_seconds(self) -> 'VolumetricFlowRate': ...
    @property
    def cubic_meters_per_days(self) -> 'VolumetricFlowRate': ...
    @property
    def cubic_meters_per_hours(self) -> 'VolumetricFlowRate': ...
    @property
    def cubic_meters_per_minutes(self) -> 'VolumetricFlowRate': ...
    @property
    def cubic_meters_per_seconds(self) -> 'VolumetricFlowRate': ...
    @property
    def gallons_per_days(self) -> 'VolumetricFlowRate': ...
    @property
    def gallons_per_hours(self) -> 'VolumetricFlowRate': ...
    @property
    def gallons_per_minutes(self) -> 'VolumetricFlowRate': ...
    @property
    def gallons_per_seconds(self) -> 'VolumetricFlowRate': ...
    @property
    def liters_per_days(self) -> 'VolumetricFlowRate': ...
    @property
    def liters_per_hours(self) -> 'VolumetricFlowRate': ...
    @property
    def liters_per_minutes(self) -> 'VolumetricFlowRate': ...
    @property
    def liters_per_seconds(self) -> 'VolumetricFlowRate': ...

class VolumetricFlowRate(TypedVariable):
    """Type-safe volumetric flow rate variable with expression capabilities."""
    
    _setter_class: Type[VolumetricFlowRateSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricFlowRateSetter:
        """
        Create a volumetric flow rate setter for fluent unit assignment.
        
        Example:
            volumetricflowrate.set(100).cubic_feet_per_days
            volumetricflowrate.set(100).cubic_feet_per_hours
            volumetricflowrate.set(100).cubic_feet_per_minutes
        """
        ...

# ============================================================================
# VOLUMETRIC FLUX
# ============================================================================

class VolumetricFluxSetter(TypeSafeSetter):
    """Volumetric Flux-specific setter with only volumetric flux unit properties."""
    
    def __init__(self, variable: 'VolumetricFlux', value: float) -> None: ...
    
    # All volumetric flux unit properties - provides fluent API with full type hints
    @property
    def cubic_feet_per_square_foot_per_days(self) -> 'VolumetricFlux': ...
    @property
    def cubic_feet_per_square_foot_per_hours(self) -> 'VolumetricFlux': ...
    @property
    def cubic_feet_per_square_foot_per_minutes(self) -> 'VolumetricFlux': ...
    @property
    def cubic_feet_per_square_foot_per_seconds(self) -> 'VolumetricFlux': ...
    @property
    def cubic_meters_per_square_meter_per_days(self) -> 'VolumetricFlux': ...
    @property
    def cubic_meters_per_square_meter_per_hours(self) -> 'VolumetricFlux': ...
    @property
    def cubic_meters_per_square_meter_per_minutes(self) -> 'VolumetricFlux': ...
    @property
    def cubic_meters_per_square_meter_per_seconds(self) -> 'VolumetricFlux': ...
    @property
    def gallons_per_square_foot_per_days(self) -> 'VolumetricFlux': ...
    @property
    def gallons_per_square_foot_per_hours(self) -> 'VolumetricFlux': ...
    @property
    def gallons_per_square_foot_per_minutes(self) -> 'VolumetricFlux': ...
    @property
    def gallons_per_square_foot_per_seconds(self) -> 'VolumetricFlux': ...
    @property
    def liters_per_square_meter_per_days(self) -> 'VolumetricFlux': ...
    @property
    def liters_per_square_meter_per_hours(self) -> 'VolumetricFlux': ...
    @property
    def liters_per_square_meter_per_minutes(self) -> 'VolumetricFlux': ...
    @property
    def liters_per_square_meter_per_seconds(self) -> 'VolumetricFlux': ...

class VolumetricFlux(TypedVariable):
    """Type-safe volumetric flux variable with expression capabilities."""
    
    _setter_class: Type[VolumetricFluxSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricFluxSetter:
        """
        Create a volumetric flux setter for fluent unit assignment.
        
        Example:
            volumetricflux.set(100).cubic_feet_per_square_foot_per_days
            volumetricflux.set(100).cubic_feet_per_square_foot_per_hours
            volumetricflux.set(100).cubic_feet_per_square_foot_per_minutes
        """
        ...

# ============================================================================
# VOLUMETRIC MASS FLOW RATE
# ============================================================================

class VolumetricMassFlowRateSetter(TypeSafeSetter):
    """Volumetric Mass Flow Rate-specific setter with only volumetric mass flow rate unit properties."""
    
    def __init__(self, variable: 'VolumetricMassFlowRate', value: float) -> None: ...
    
    # All volumetric mass flow rate unit properties - provides fluent API with full type hints
    @property
    def gram_per_second_per_cubic_centimeters(self) -> 'VolumetricMassFlowRate': ...
    @property
    def kilogram_per_hour_per_cubic_foots(self) -> 'VolumetricMassFlowRate': ...
    @property
    def kilogram_per_hour_per_cubic_meters(self) -> 'VolumetricMassFlowRate': ...
    @property
    def kilogram_per_second_per_cubic_meters(self) -> 'VolumetricMassFlowRate': ...
    @property
    def pound_per_hour_per_cubic_foots(self) -> 'VolumetricMassFlowRate': ...
    @property
    def pound_per_minute_per_cubic_foots(self) -> 'VolumetricMassFlowRate': ...
    @property
    def pound_per_second_per_cubic_foots(self) -> 'VolumetricMassFlowRate': ...

class VolumetricMassFlowRate(TypedVariable):
    """Type-safe volumetric mass flow rate variable with expression capabilities."""
    
    _setter_class: Type[VolumetricMassFlowRateSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> VolumetricMassFlowRateSetter:
        """
        Create a volumetric mass flow rate setter for fluent unit assignment.
        
        Example:
            volumetricmassflowrate.set(100).gram_per_second_per_cubic_centimeters
            volumetricmassflowrate.set(100).kilogram_per_hour_per_cubic_foots
            volumetricmassflowrate.set(100).kilogram_per_hour_per_cubic_meters
        """
        ...

# ============================================================================
# WAVENUMBER
# ============================================================================

class WavenumberSetter(TypeSafeSetter):
    """Wavenumber-specific setter with only wavenumber unit properties."""
    
    def __init__(self, variable: 'Wavenumber', value: float) -> None: ...
    
    # All wavenumber unit properties - provides fluent API with full type hints
    @property
    def diopters(self) -> 'Wavenumber': ...
    @property
    def kaysers(self) -> 'Wavenumber': ...
    @property
    def reciprocal_meters(self) -> 'Wavenumber': ...

class Wavenumber(TypedVariable):
    """Type-safe wavenumber variable with expression capabilities."""
    
    _setter_class: Type[WavenumberSetter]
    _expected_dimension: DimensionSignature
    _default_unit_property: str
    
    def __init__(self, *args, is_known: bool = True) -> None: ...
    
    def set(self, value: float) -> WavenumberSetter:
        """
        Create a wavenumber setter for fluent unit assignment.
        
        Example:
            wavenumber.set(100).diopters
            wavenumber.set(100).kaysers
            wavenumber.set(100).reciprocal_meters
        """
        ...

# ============================================================================
# Module-level definitions
# ============================================================================

VARIABLE_DEFINITIONS: Dict[str, Dict[str, Any]]

def create_setter_class(class_name: str, variable_name: str, definition: Dict[str, Any]) -> Type: ...

def create_variable_class(class_name: str, definition: Dict[str, Any], setter_class: Type) -> Type: ...

def get_consolidated_variable_modules() -> List[Any]: ...

# All classes are defined above - no additional exports needed in type stubs
