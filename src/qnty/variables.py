"""
Optimized Variables Module - Static Class Edition
================================================

Static variable class definitions for maximum import performance.
Uses static class generation instead of dynamic type() calls.
Auto-generated from unit_data.json and dimension_mapping.json.
"""

from typing import TYPE_CHECKING

from . import units
from .unit_system.dimension import (
    ABSORBED_DOSE,
    ACCELERATION,
    ACTIVATION_ENERGY,
    AMOUNT_OF_SUBSTANCE,
    ANGLE_PLANE,
    ANGLE_SOLID,
    ANGULAR_ACCELERATION,
    ANGULAR_MOMENTUM,
    AREA,
    AREA_PER_UNIT_VOLUME,
    ATOMIC_WEIGHT,
    CONCENTRATION,
    DIMENSIONLESS,
    DYNAMIC_FLUIDITY,
    ELECTRIC_CAPACITANCE,
    ELECTRIC_CHARGE,
    ELECTRIC_CURRENT_INTENSITY,
    ELECTRIC_DIPOLE_MOMENT,
    ELECTRIC_FIELD_STRENGTH,
    ELECTRIC_INDUCTANCE,
    ELECTRIC_POTENTIAL,
    ELECTRIC_RESISTANCE,
    ELECTRICAL_CONDUCTANCE,
    ELECTRICAL_PERMITTIVITY,
    ELECTRICAL_RESISTIVITY,
    ENERGY_FLUX,
    ENERGY_HEAT_WORK,
    ENERGY_PER_UNIT_AREA,
    FORCE,
    FORCE_BODY,
    FORCE_PER_UNIT_MASS,
    FREQUENCY_VOLTAGE_RATIO,
    FUEL_CONSUMPTION,
    HEAT_OF_COMBUSTION,
    HEAT_OF_FUSION,
    HEAT_OF_VAPORIZATION,
    HEAT_TRANSFER_COEFFICIENT,
    ILLUMINANCE,
    KINETIC_ENERGY_OF_TURBULENCE,
    LENGTH,
    LINEAR_MASS_DENSITY,
    LINEAR_MOMENTUM,
    LUMINANCE_SELF,
    LUMINOUS_FLUX,
    LUMINOUS_INTENSITY,
    MAGNETIC_FIELD,
    MAGNETIC_FLUX,
    MAGNETIC_INDUCTION_FIELD_STRENGTH,
    MAGNETIC_MOMENT,
    MAGNETIC_PERMEABILITY,
    MAGNETOMOTIVE_FORCE,
    MASS,
    MASS_DENSITY,
    MASS_FLOW_RATE,
    MASS_FLUX,
    MASS_FRACTION_OF_I,
    MASS_TRANSFER_COEFFICIENT,
    MOLALITY_OF_SOLUTE_I,
    MOLAR_CONCENTRATION_BY_MASS,
    MOLAR_FLOW_RATE,
    MOLAR_FLUX,
    MOLAR_HEAT_CAPACITY,
    MOLARITY_OF_I,
    MOLE_FRACTION_OF_I,
    MOMENT_OF_INERTIA,
    MOMENTUM_FLOW_RATE,
    MOMENTUM_FLUX,
    NORMALITY_OF_SOLUTION,
    PARTICLE_DENSITY,
    PERCENT,
    PERMEABILITY,
    PHOTON_EMISSION_RATE,
    POWER_PER_UNIT_MASS,
    POWER_PER_UNIT_VOLUME,
    POWER_THERMAL_DUTY,
    PRESSURE,
    RADIATION_DOSE_EQUIVALENT,
    RADIATION_EXPOSURE,
    RADIOACTIVITY,
    SECOND_MOMENT_OF_AREA,
    SECOND_RADIATION_CONSTANT_PLANCK,
    SPECIFIC_ENTHALPY,
    SPECIFIC_GRAVITY,
    SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE,
    SPECIFIC_LENGTH,
    SPECIFIC_SURFACE,
    SPECIFIC_VOLUME,
    STRESS,
    SURFACE_MASS_DENSITY,
    SURFACE_TENSION,
    TEMPERATURE,
    THERMAL_CONDUCTIVITY,
    TIME,
    TORQUE,
    TURBULENCE_ENERGY_DISSIPATION_RATE,
    VELOCITY_ANGULAR,
    VELOCITY_LINEAR,
    VISCOSITY_DYNAMIC,
    VISCOSITY_KINEMATIC,
    VOLUME,
    VOLUME_FRACTION_OF_I,
    VOLUMETRIC_CALORIFIC_HEATING_VALUE,
    VOLUMETRIC_COEFFICIENT_OF_EXPANSION,
    VOLUMETRIC_FLOW_RATE,
    VOLUMETRIC_FLUX,
    VOLUMETRIC_MASS_FLOW_RATE,
    WAVENUMBER,
)
from .variable_system.core import FastQuantity, TypeSafeSetter
from .variable_system.typed_variable import TypedVariable

if TYPE_CHECKING:
    pass


# ===== SETTER CLASSES =====
# Static setter class definitions with __slots__ optimization

class AbsorbedDoseSetter(TypeSafeSetter):
    """AbsorbedDose-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def erg_per_gram(self):
        """Set value using erg per gram units."""
        unit_const = units.AbsorbedDoseUnits.erg_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def erg_per_g(self):
        """Set value using erg_per_g units (alias for erg per gram)."""
        return self.erg_per_gram
    
    @property
    def gram_rad(self):
        """Set value using gram-rad units."""
        unit_const = units.AbsorbedDoseUnits.gram_rad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_rad(self):
        """Set value using g_rad units (alias for gram-rad)."""
        return self.gram_rad
    
    @property
    def gray(self):
        """Set value using gray units."""
        unit_const = units.AbsorbedDoseUnits.gray
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Gy(self):
        """Set value using Gy units (alias for gray)."""
        return self.gray
    
    @property
    def rad(self):
        """Set value using rad units."""
        unit_const = units.AbsorbedDoseUnits.rad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def milligray(self):
        """Set value using milligray units."""
        unit_const = units.AbsorbedDoseUnits.milligray
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mGy(self):
        """Set value using mGy units (alias for milligray)."""
        return self.milligray
    
    @property
    def microgray(self):
        """Set value using microgray units."""
        unit_const = units.AbsorbedDoseUnits.microgray
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uGy(self):
        """Set value using μGy units (alias for microgray)."""
        return self.microgray
    

class AccelerationSetter(TypeSafeSetter):
    """Acceleration-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def meter_per_second_squared(self):
        """Set value using meter per second squared units."""
        unit_const = units.AccelerationUnits.meter_per_second_squared
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_per_s2(self):
        """Set value using m_per_s2 units (alias for meter per second squared)."""
        return self.meter_per_second_squared
    
    @property
    def foot_per_second_squared(self):
        """Set value using foot per second squared units."""
        unit_const = units.AccelerationUnits.foot_per_second_squared
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_per_s2(self):
        """Set value using ft_per_s2 units (alias for foot per second squared)."""
        return self.foot_per_second_squared
    
    @property
    def fps2(self):
        """Set value using fps2 units (alias for foot per second squared)."""
        return self.foot_per_second_squared
    

class ActivationEnergySetter(TypeSafeSetter):
    """ActivationEnergy-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Btu_per_pound_mole(self):
        """Set value using Btu per pound mole units."""
        unit_const = units.ActivationEnergyUnits.Btu_per_pound_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def btu_per_lbmol(self):
        """Set value using btu_per_lbmol units (alias for Btu per pound mole)."""
        return self.Btu_per_pound_mole
    
    @property
    def calorie_mean_per_gram_mole(self):
        """Set value using calorie (mean) per gram mole units."""
        unit_const = units.ActivationEnergyUnits.calorie_mean_per_gram_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_mean_per_gmol(self):
        """Set value using cal_mean_per_gmol units (alias for calorie (mean) per gram mole)."""
        return self.calorie_mean_per_gram_mole
    
    @property
    def joule_per_gram_mole(self):
        """Set value using joule per gram mole units."""
        unit_const = units.ActivationEnergyUnits.joule_per_gram_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_kilogram_mole(self):
        """Set value using joule per kilogram mole units."""
        unit_const = units.ActivationEnergyUnits.joule_per_kilogram_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilocalorie_per_kilogram_mole(self):
        """Set value using kilocalorie per kilogram mole units."""
        unit_const = units.ActivationEnergyUnits.kilocalorie_per_kilogram_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class AmountOfSubstanceSetter(TypeSafeSetter):
    """AmountOfSubstance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kilogram_mol_or_kmol(self):
        """Set value using kilogram mol or kmol units."""
        unit_const = units.AmountOfSubstanceUnits.kilogram_mol_or_kmol
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol(self):
        """Set value using kmol units (alias for kilogram mol or kmol)."""
        return self.kilogram_mol_or_kmol
    
    @property
    def mole_gram(self):
        """Set value using mole (gram) units."""
        unit_const = units.AmountOfSubstanceUnits.mole_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol(self):
        """Set value using mol units (alias for mole (gram))."""
        return self.mole_gram
    
    @property
    def pound_mole(self):
        """Set value using pound-mole units."""
        unit_const = units.AmountOfSubstanceUnits.pound_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol(self):
        """Set value using lb-mol units (alias for pound-mole)."""
        return self.pound_mole
    
    @property
    def mole(self):
        """Set value using mole units (alias for pound-mole)."""
        return self.pound_mole
    
    @property
    def millimole_gram(self):
        """Set value using millimole (gram) units."""
        unit_const = units.AmountOfSubstanceUnits.millimole_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mmol(self):
        """Set value using mmol units (alias for millimole (gram))."""
        return self.millimole_gram
    
    @property
    def micromole_gram(self):
        """Set value using micromole (gram) units."""
        unit_const = units.AmountOfSubstanceUnits.micromole_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def umol(self):
        """Set value using μmol units (alias for micromole (gram))."""
        return self.micromole_gram
    

class AnglePlaneSetter(TypeSafeSetter):
    """AnglePlane-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def degree(self):
        """Set value using degree units."""
        unit_const = units.AnglePlaneUnits.degree
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gon(self):
        """Set value using gon units."""
        unit_const = units.AnglePlaneUnits.gon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def grade(self):
        """Set value using grade units."""
        unit_const = units.AnglePlaneUnits.grade
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def minute_new(self):
        """Set value using minute (new) units."""
        unit_const = units.AnglePlaneUnits.minute_new
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def c(self):
        """Set value using c units (alias for minute (new))."""
        return self.minute_new
    
    @property
    def minute_of_angle(self):
        """Set value using minute of angle units."""
        unit_const = units.AnglePlaneUnits.minute_of_angle
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def percent(self):
        """Set value using percent units."""
        unit_const = units.AnglePlaneUnits.percent
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def plane_angle(self):
        """Set value using plane angle units."""
        unit_const = units.AnglePlaneUnits.plane_angle
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def quadrant(self):
        """Set value using quadrant units."""
        unit_const = units.AnglePlaneUnits.quadrant
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def radian(self):
        """Set value using radian units."""
        unit_const = units.AnglePlaneUnits.radian
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rad(self):
        """Set value using rad units (alias for radian)."""
        return self.radian
    
    @property
    def right_angle(self):
        """Set value using right angle units."""
        unit_const = units.AnglePlaneUnits.right_angle
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def perp(self):
        """Set value using perp units (alias for right angle)."""
        return self.right_angle
    
    @property
    def round(self):
        """Set value using round units."""
        unit_const = units.AnglePlaneUnits.round
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def tr(self):
        """Set value using tr units (alias for round)."""
        return self.round
    
    @property
    def r(self):
        """Set value using r units (alias for round)."""
        return self.round
    
    @property
    def second_new(self):
        """Set value using second (new) units."""
        unit_const = units.AnglePlaneUnits.second_new
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cc(self):
        """Set value using cc units (alias for second (new))."""
        return self.second_new
    
    @property
    def second_of_angle(self):
        """Set value using second of angle units."""
        unit_const = units.AnglePlaneUnits.second_of_angle
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def thousandth_US(self):
        """Set value using thousandth (US) units."""
        unit_const = units.AnglePlaneUnits.thousandth_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def turn(self):
        """Set value using turn units."""
        unit_const = units.AnglePlaneUnits.turn
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rev(self):
        """Set value using rev units (alias for turn)."""
        return self.turn
    

class AngleSolidSetter(TypeSafeSetter):
    """AngleSolid-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def spat(self):
        """Set value using spat units."""
        unit_const = units.AngleSolidUnits.spat
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_degree(self):
        """Set value using square degree units."""
        unit_const = units.AngleSolidUnits.square_degree
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_gon(self):
        """Set value using square gon units."""
        unit_const = units.AngleSolidUnits.square_gon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def steradian(self):
        """Set value using steradian units."""
        unit_const = units.AngleSolidUnits.steradian
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sr(self):
        """Set value using sr units (alias for steradian)."""
        return self.steradian
    

class AngularAccelerationSetter(TypeSafeSetter):
    """AngularAcceleration-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def radian_per_second_squared(self):
        """Set value using radian per second squared units."""
        unit_const = units.AngularAccelerationUnits.radian_per_second_squared
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def revolution_per_second_squared(self):
        """Set value using revolution per second squared units."""
        unit_const = units.AngularAccelerationUnits.revolution_per_second_squared
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rpm_or_revolution_per_minute_per_minute(self):
        """Set value using rpm (or revolution per minute) per minute units."""
        unit_const = units.AngularAccelerationUnits.rpm_or_revolution_per_minute_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rev_min_power_2(self):
        """Set value using rev / min^{2 units (alias for rpm (or revolution per minute) per minute)."""
        return self.rpm_or_revolution_per_minute_per_minute
    
    @property
    def rpm_min(self):
        """Set value using rpm/min units (alias for rpm (or revolution per minute) per minute)."""
        return self.rpm_or_revolution_per_minute_per_minute
    

class AngularMomentumSetter(TypeSafeSetter):
    """AngularMomentum-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_centimeter_squared_per_second(self):
        """Set value using gram centimeter squared per second units."""
        unit_const = units.AngularMomentumUnits.gram_centimeter_squared_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_meter_squared_per_second(self):
        """Set value using kilogram meter squared per second units."""
        unit_const = units.AngularMomentumUnits.kilogram_meter_squared_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_force_square_foot_per_second(self):
        """Set value using pound force square foot per second units."""
        unit_const = units.AngularMomentumUnits.pound_force_square_foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class AreaSetter(TypeSafeSetter):
    """Area-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def acre_general(self):
        """Set value using acre (general) units."""
        unit_const = units.AreaUnits.acre_general
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ac(self):
        """Set value using ac units (alias for acre (general))."""
        return self.acre_general
    
    @property
    def are(self):
        """Set value using are units."""
        unit_const = units.AreaUnits.are
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def a(self):
        """Set value using a units (alias for are)."""
        return self.are
    
    @property
    def arpent_Quebec(self):
        """Set value using arpent (Quebec) units."""
        unit_const = units.AreaUnits.arpent_Quebec
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def arp(self):
        """Set value using arp units (alias for arpent (Quebec))."""
        return self.arpent_Quebec
    
    @property
    def barn(self):
        """Set value using barn units."""
        unit_const = units.AreaUnits.barn
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def b(self):
        """Set value using b units (alias for barn)."""
        return self.barn
    
    @property
    def circular_inch(self):
        """Set value using circular inch units."""
        unit_const = units.AreaUnits.circular_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cin(self):
        """Set value using cin units (alias for circular inch)."""
        return self.circular_inch
    
    @property
    def circular_mil(self):
        """Set value using circular mil units."""
        unit_const = units.AreaUnits.circular_mil
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cmil(self):
        """Set value using cmil units (alias for circular mil)."""
        return self.circular_mil
    
    @property
    def hectare(self):
        """Set value using hectare units."""
        unit_const = units.AreaUnits.hectare
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ha(self):
        """Set value using ha units (alias for hectare)."""
        return self.hectare
    
    @property
    def shed(self):
        """Set value using shed units."""
        unit_const = units.AreaUnits.shed
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_centimeter(self):
        """Set value using square centimeter units."""
        unit_const = units.AreaUnits.square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_chain_Ramsden(self):
        """Set value using square chain (Ramsden) units."""
        unit_const = units.AreaUnits.square_chain_Ramsden
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_chain_Survey_Gunter_s(self):
        """Set value using square chain (Survey, Gunter's) units."""
        unit_const = units.AreaUnits.square_chain_Survey_Gunter_s
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_decimeter(self):
        """Set value using square decimeter units."""
        unit_const = units.AreaUnits.square_decimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_fermi(self):
        """Set value using square fermi units."""
        unit_const = units.AreaUnits.square_fermi
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_foot(self):
        """Set value using square foot units."""
        unit_const = units.AreaUnits.square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_ft(self):
        """Set value using sq ft units (alias for square foot)."""
        return self.square_foot
    
    @property
    def ft_power_2(self):
        """Set value using ft { ^{2 units (alias for square foot)."""
        return self.square_foot
    
    @property
    def square_hectometer(self):
        """Set value using square hectometer units."""
        unit_const = units.AreaUnits.square_hectometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_inch(self):
        """Set value using square inch units."""
        unit_const = units.AreaUnits.square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_in(self):
        """Set value using sq in units (alias for square inch)."""
        return self.square_inch
    
    @property
    def in_power_2(self):
        """Set value using in { ^{2 units (alias for square inch)."""
        return self.square_inch
    
    @property
    def square_kilometer(self):
        """Set value using square kilometer units."""
        unit_const = units.AreaUnits.square_kilometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_league_statute(self):
        """Set value using square league (statute) units."""
        unit_const = units.AreaUnits.square_league_statute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_meter(self):
        """Set value using square meter units."""
        unit_const = units.AreaUnits.square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_micron(self):
        """Set value using square micron units."""
        unit_const = units.AreaUnits.square_micron
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_m_power_2(self):
        """Set value using mu m^{2 units (alias for square micron)."""
        return self.square_micron
    
    @property
    def mu_power_2(self):
        """Set value using mu^{2 units (alias for square micron)."""
        return self.square_micron
    
    @property
    def square_mile_statute(self):
        """Set value using square mile (statute) units."""
        unit_const = units.AreaUnits.square_mile_statute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_mile_US_survey(self):
        """Set value using square mile (US survey) units."""
        unit_const = units.AreaUnits.square_mile_US_survey
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_millimeter(self):
        """Set value using square millimeter units."""
        unit_const = units.AreaUnits.square_millimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_nanometer(self):
        """Set value using square nanometer units."""
        unit_const = units.AreaUnits.square_nanometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_yard(self):
        """Set value using square yard units."""
        unit_const = units.AreaUnits.square_yard
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def township_US(self):
        """Set value using township (US) units."""
        unit_const = units.AreaUnits.township_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class AreaPerUnitVolumeSetter(TypeSafeSetter):
    """AreaPerUnitVolume-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_centimeter_per_cubic_centimeter(self):
        """Set value using square centimeter per cubic centimeter units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_centimeter_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_foot_per_cubic_foot(self):
        """Set value using square foot per cubic foot units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_foot_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_2_ft_power_3(self):
        """Set value using ft^{2 / ft^{3 units (alias for square foot per cubic foot)."""
        return self.square_foot_per_cubic_foot
    
    @property
    def sqft_cft(self):
        """Set value using sqft/cft units (alias for square foot per cubic foot)."""
        return self.square_foot_per_cubic_foot
    
    @property
    def square_inch_per_cubic_inch(self):
        """Set value using square inch per cubic inch units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_inch_per_cubic_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_power_2_in_power_3(self):
        """Set value using in^{2 / in^{3 units (alias for square inch per cubic inch)."""
        return self.square_inch_per_cubic_inch
    
    @property
    def sq_in_cu_in(self):
        """Set value using sq.in./cu. in. units (alias for square inch per cubic inch)."""
        return self.square_inch_per_cubic_inch
    
    @property
    def square_meter_per_cubic_meter(self):
        """Set value using square meter per cubic meter units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_meter_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_power_2_m_power_3(self):
        """Set value using m^{2 / m^{3 units (alias for square meter per cubic meter)."""
        return self.square_meter_per_cubic_meter
    
    @property
    def unit_1_m_power_3(self):
        """Set value using 1 / m^{3 units (alias for square meter per cubic meter)."""
        return self.square_meter_per_cubic_meter
    

class AtomicWeightSetter(TypeSafeSetter):
    """AtomicWeight-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def atomic_mass_unit_12C(self):
        """Set value using atomic mass unit (12C) units."""
        unit_const = units.AtomicWeightUnits.atomic_mass_unit_12C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def amu(self):
        """Set value using amu units (alias for atomic mass unit (12C))."""
        return self.atomic_mass_unit_12C
    
    @property
    def grams_per_mole(self):
        """Set value using grams per mole units."""
        unit_const = units.AtomicWeightUnits.grams_per_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilograms_per_kilomole(self):
        """Set value using kilograms per kilomole units."""
        unit_const = units.AtomicWeightUnits.kilograms_per_kilomole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pounds_per_pound_mole(self):
        """Set value using pounds per pound mole units."""
        unit_const = units.AtomicWeightUnits.pounds_per_pound_mole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_lb_mol(self):
        """Set value using lb / lb- mol units (alias for pounds per pound mole)."""
        return self.pounds_per_pound_mole
    
    @property
    def lb_mole(self):
        """Set value using lb / mole units (alias for pounds per pound mole)."""
        return self.pounds_per_pound_mole
    

class ConcentrationSetter(TypeSafeSetter):
    """Concentration-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def grains_of_i_per_cubic_foot(self):
        """Set value using grains of "i" per cubic foot units."""
        unit_const = units.ConcentrationUnits.grains_of_i_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gr_ft_power_3(self):
        """Set value using gr / ft^{3 units (alias for grains of "i" per cubic foot)."""
        return self.grains_of_i_per_cubic_foot
    
    @property
    def gr_cft(self):
        """Set value using gr/cft units (alias for grains of "i" per cubic foot)."""
        return self.grains_of_i_per_cubic_foot
    
    @property
    def grains_of_i_per_gallon_US(self):
        """Set value using grains of "i" per gallon (US) units."""
        unit_const = units.ConcentrationUnits.grains_of_i_per_gallon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class DimensionlessSetter(TypeSafeSetter):
    """Dimensionless-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dimensionless(self):
        """Set value using dimensionless units."""
        unit_const = units.DimensionlessUnits.dimensionless
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ratio(self):
        """Set value using ratio units."""
        unit_const = units.DimensionlessUnits.ratio
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def parts_per_million(self):
        """Set value using parts per million units."""
        unit_const = units.DimensionlessUnits.parts_per_million
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ppm(self):
        """Set value using ppm units (alias for parts per million)."""
        return self.parts_per_million
    
    @property
    def parts_per_billion(self):
        """Set value using parts per billion units."""
        unit_const = units.DimensionlessUnits.parts_per_billion
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ppb(self):
        """Set value using ppb units (alias for parts per billion)."""
        return self.parts_per_billion
    

class DynamicFluiditySetter(TypeSafeSetter):
    """DynamicFluidity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def meter_seconds_per_kilogram(self):
        """Set value using meter-seconds per kilogram units."""
        unit_const = units.DynamicFluidityUnits.meter_seconds_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rhe(self):
        """Set value using rhe units."""
        unit_const = units.DynamicFluidityUnits.rhe
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_foot_per_pound_second(self):
        """Set value using square foot per pound second units."""
        unit_const = units.DynamicFluidityUnits.square_foot_per_pound_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_meters_per_newton_per_second(self):
        """Set value using square meters per newton per second units."""
        unit_const = units.DynamicFluidityUnits.square_meters_per_newton_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ElectricCapacitanceSetter(TypeSafeSetter):
    """ElectricCapacitance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cm(self):
        """Set value using "cm" units."""
        unit_const = units.ElectricCapacitanceUnits.cm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def abfarad(self):
        """Set value using abfarad units."""
        unit_const = units.ElectricCapacitanceUnits.abfarad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def farad(self):
        """Set value using farad units."""
        unit_const = units.ElectricCapacitanceUnits.farad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def F(self):
        """Set value using F units (alias for farad)."""
        return self.farad
    
    @property
    def farad_intl(self):
        """Set value using farad (intl) units."""
        unit_const = units.ElectricCapacitanceUnits.farad_intl
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def jar(self):
        """Set value using jar units."""
        unit_const = units.ElectricCapacitanceUnits.jar
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def puff(self):
        """Set value using puff units."""
        unit_const = units.ElectricCapacitanceUnits.puff
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def statfarad(self):
        """Set value using statfarad units."""
        unit_const = units.ElectricCapacitanceUnits.statfarad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millifarad(self):
        """Set value using millifarad units."""
        unit_const = units.ElectricCapacitanceUnits.millifarad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mF(self):
        """Set value using mF units (alias for millifarad)."""
        return self.millifarad
    
    @property
    def microfarad(self):
        """Set value using microfarad units."""
        unit_const = units.ElectricCapacitanceUnits.microfarad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uF(self):
        """Set value using μF units (alias for microfarad)."""
        return self.microfarad
    
    @property
    def nanofarad(self):
        """Set value using nanofarad units."""
        unit_const = units.ElectricCapacitanceUnits.nanofarad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nF(self):
        """Set value using nF units (alias for nanofarad)."""
        return self.nanofarad
    
    @property
    def picofarad(self):
        """Set value using picofarad units."""
        unit_const = units.ElectricCapacitanceUnits.picofarad
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pF(self):
        """Set value using pF units (alias for picofarad)."""
        return self.picofarad
    

class ElectricChargeSetter(TypeSafeSetter):
    """ElectricCharge-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abcoulomb(self):
        """Set value using abcoulomb units."""
        unit_const = units.ElectricChargeUnits.abcoulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ampere_hour(self):
        """Set value using ampere-hour units."""
        unit_const = units.ElectricChargeUnits.ampere_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ah(self):
        """Set value using Ah units (alias for ampere-hour)."""
        return self.ampere_hour
    
    @property
    def coulomb(self):
        """Set value using coulomb units."""
        unit_const = units.ElectricChargeUnits.coulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def C(self):
        """Set value using C units (alias for coulomb)."""
        return self.coulomb
    
    @property
    def faraday_C12(self):
        """Set value using faraday (C12) units."""
        unit_const = units.ElectricChargeUnits.faraday_C12
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def F(self):
        """Set value using F units (alias for faraday (C12))."""
        return self.faraday_C12
    
    @property
    def franklin(self):
        """Set value using franklin units."""
        unit_const = units.ElectricChargeUnits.franklin
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Fr(self):
        """Set value using Fr units (alias for franklin)."""
        return self.franklin
    
    @property
    def statcoulomb(self):
        """Set value using statcoulomb units."""
        unit_const = units.ElectricChargeUnits.statcoulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def u_a_charge(self):
        """Set value using u.a. charge units."""
        unit_const = units.ElectricChargeUnits.u_a_charge
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilocoulomb(self):
        """Set value using kilocoulomb units."""
        unit_const = units.ElectricChargeUnits.kilocoulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kC(self):
        """Set value using kC units (alias for kilocoulomb)."""
        return self.kilocoulomb
    
    @property
    def millicoulomb(self):
        """Set value using millicoulomb units."""
        unit_const = units.ElectricChargeUnits.millicoulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mC(self):
        """Set value using mC units (alias for millicoulomb)."""
        return self.millicoulomb
    
    @property
    def microcoulomb(self):
        """Set value using microcoulomb units."""
        unit_const = units.ElectricChargeUnits.microcoulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uC(self):
        """Set value using μC units (alias for microcoulomb)."""
        return self.microcoulomb
    
    @property
    def nanocoulomb(self):
        """Set value using nanocoulomb units."""
        unit_const = units.ElectricChargeUnits.nanocoulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nC(self):
        """Set value using nC units (alias for nanocoulomb)."""
        return self.nanocoulomb
    
    @property
    def picocoulomb(self):
        """Set value using picocoulomb units."""
        unit_const = units.ElectricChargeUnits.picocoulomb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pC(self):
        """Set value using pC units (alias for picocoulomb)."""
        return self.picocoulomb
    

class ElectricCurrentIntensitySetter(TypeSafeSetter):
    """ElectricCurrentIntensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abampere(self):
        """Set value using abampere units."""
        unit_const = units.ElectricCurrentIntensityUnits.abampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ampere_intl_mean(self):
        """Set value using ampere (intl mean) units."""
        unit_const = units.ElectricCurrentIntensityUnits.ampere_intl_mean
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ampere_intl_US(self):
        """Set value using ampere (intl US) units."""
        unit_const = units.ElectricCurrentIntensityUnits.ampere_intl_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ampere_or_amp(self):
        """Set value using ampere or amp units."""
        unit_const = units.ElectricCurrentIntensityUnits.ampere_or_amp
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def A(self):
        """Set value using A units (alias for ampere or amp)."""
        return self.ampere_or_amp
    
    @property
    def biot(self):
        """Set value using biot units."""
        unit_const = units.ElectricCurrentIntensityUnits.biot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def statampere(self):
        """Set value using statampere units."""
        unit_const = units.ElectricCurrentIntensityUnits.statampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def u_a_or_current(self):
        """Set value using u.a. or current units."""
        unit_const = units.ElectricCurrentIntensityUnits.u_a_or_current
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ElectricDipoleMomentSetter(TypeSafeSetter):
    """ElectricDipoleMoment-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def ampere_meter_second(self):
        """Set value using ampere meter second units."""
        unit_const = units.ElectricDipoleMomentUnits.ampere_meter_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def coulomb_meter(self):
        """Set value using coulomb meter units."""
        unit_const = units.ElectricDipoleMomentUnits.coulomb_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def debye(self):
        """Set value using debye units."""
        unit_const = units.ElectricDipoleMomentUnits.debye
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def D(self):
        """Set value using D units (alias for debye)."""
        return self.debye
    
    @property
    def electron_meter(self):
        """Set value using electron meter units."""
        unit_const = units.ElectricDipoleMomentUnits.electron_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ElectricFieldStrengthSetter(TypeSafeSetter):
    """ElectricFieldStrength-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def volt_per_centimeter(self):
        """Set value using volt per centimeter units."""
        unit_const = units.ElectricFieldStrengthUnits.volt_per_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def volt_per_meter(self):
        """Set value using volt per meter units."""
        unit_const = units.ElectricFieldStrengthUnits.volt_per_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ElectricInductanceSetter(TypeSafeSetter):
    """ElectricInductance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abhenry(self):
        """Set value using abhenry units."""
        unit_const = units.ElectricInductanceUnits.abhenry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm(self):
        """Set value using cm units."""
        unit_const = units.ElectricInductanceUnits.cm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def henry(self):
        """Set value using henry units."""
        unit_const = units.ElectricInductanceUnits.henry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def H(self):
        """Set value using H units (alias for henry)."""
        return self.henry
    
    @property
    def henry_intl_mean(self):
        """Set value using henry (intl mean) units."""
        unit_const = units.ElectricInductanceUnits.henry_intl_mean
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def henry_intl_US(self):
        """Set value using henry (intl US) units."""
        unit_const = units.ElectricInductanceUnits.henry_intl_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mic(self):
        """Set value using mic units."""
        unit_const = units.ElectricInductanceUnits.mic
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def stathenry(self):
        """Set value using stathenry units."""
        unit_const = units.ElectricInductanceUnits.stathenry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millihenry(self):
        """Set value using millihenry units."""
        unit_const = units.ElectricInductanceUnits.millihenry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mH(self):
        """Set value using mH units (alias for millihenry)."""
        return self.millihenry
    
    @property
    def microhenry(self):
        """Set value using microhenry units."""
        unit_const = units.ElectricInductanceUnits.microhenry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uH(self):
        """Set value using μH units (alias for microhenry)."""
        return self.microhenry
    
    @property
    def nanohenry(self):
        """Set value using nanohenry units."""
        unit_const = units.ElectricInductanceUnits.nanohenry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nH(self):
        """Set value using nH units (alias for nanohenry)."""
        return self.nanohenry
    

class ElectricPotentialSetter(TypeSafeSetter):
    """ElectricPotential-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abvolt(self):
        """Set value using abvolt units."""
        unit_const = units.ElectricPotentialUnits.abvolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def statvolt(self):
        """Set value using statvolt units."""
        unit_const = units.ElectricPotentialUnits.statvolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def u_a_potential(self):
        """Set value using u.a. potential units."""
        unit_const = units.ElectricPotentialUnits.u_a_potential
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def volt(self):
        """Set value using volt units."""
        unit_const = units.ElectricPotentialUnits.volt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def V(self):
        """Set value using V units (alias for volt)."""
        return self.volt
    
    @property
    def volt_intl_mean(self):
        """Set value using volt (intl mean) units."""
        unit_const = units.ElectricPotentialUnits.volt_intl_mean
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def volt_US(self):
        """Set value using volt (US) units."""
        unit_const = units.ElectricPotentialUnits.volt_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilovolt(self):
        """Set value using kilovolt units."""
        unit_const = units.ElectricPotentialUnits.kilovolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kV(self):
        """Set value using kV units (alias for kilovolt)."""
        return self.kilovolt
    
    @property
    def millivolt(self):
        """Set value using millivolt units."""
        unit_const = units.ElectricPotentialUnits.millivolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mV(self):
        """Set value using mV units (alias for millivolt)."""
        return self.millivolt
    
    @property
    def microvolt(self):
        """Set value using microvolt units."""
        unit_const = units.ElectricPotentialUnits.microvolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uV(self):
        """Set value using μV units (alias for microvolt)."""
        return self.microvolt
    
    @property
    def nanovolt(self):
        """Set value using nanovolt units."""
        unit_const = units.ElectricPotentialUnits.nanovolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nV(self):
        """Set value using nV units (alias for nanovolt)."""
        return self.nanovolt
    
    @property
    def picovolt(self):
        """Set value using picovolt units."""
        unit_const = units.ElectricPotentialUnits.picovolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pV(self):
        """Set value using pV units (alias for picovolt)."""
        return self.picovolt
    

class ElectricResistanceSetter(TypeSafeSetter):
    """ElectricResistance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abohm(self):
        """Set value using abohm units."""
        unit_const = units.ElectricResistanceUnits.abohm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def jacobi(self):
        """Set value using jacobi units."""
        unit_const = units.ElectricResistanceUnits.jacobi
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lenz(self):
        """Set value using lenz units."""
        unit_const = units.ElectricResistanceUnits.lenz
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ohm(self):
        """Set value using ohm units."""
        unit_const = units.ElectricResistanceUnits.ohm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ohm_intl_mean(self):
        """Set value using ohm (intl mean) units."""
        unit_const = units.ElectricResistanceUnits.ohm_intl_mean
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ohm_intl_US(self):
        """Set value using ohm (intl US) units."""
        unit_const = units.ElectricResistanceUnits.ohm_intl_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ohm_legal(self):
        """Set value using ohm (legal) units."""
        unit_const = units.ElectricResistanceUnits.ohm_legal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def preece(self):
        """Set value using preece units."""
        unit_const = units.ElectricResistanceUnits.preece
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def statohm(self):
        """Set value using statohm units."""
        unit_const = units.ElectricResistanceUnits.statohm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def wheatstone(self):
        """Set value using wheatstone units."""
        unit_const = units.ElectricResistanceUnits.wheatstone
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kiloohm(self):
        """Set value using kiloohm units."""
        unit_const = units.ElectricResistanceUnits.kiloohm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def k_Omega(self):
        r"""Set value using k$\Omega$ units (alias for kiloohm)."""
        return self.kiloohm
    
    @property
    def megaohm(self):
        """Set value using megaohm units."""
        unit_const = units.ElectricResistanceUnits.megaohm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def M_Omega(self):
        r"""Set value using M$\Omega$ units (alias for megaohm)."""
        return self.megaohm
    
    @property
    def milliohm(self):
        """Set value using milliohm units."""
        unit_const = units.ElectricResistanceUnits.milliohm
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_Omega(self):
        r"""Set value using m$\Omega$ units (alias for milliohm)."""
        return self.milliohm
    

class ElectricalConductanceSetter(TypeSafeSetter):
    """ElectricalConductance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def emu_cgs(self):
        """Set value using emu cgs units."""
        unit_const = units.ElectricalConductanceUnits.emu_cgs
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def esu_cgs(self):
        """Set value using esu cgs units."""
        unit_const = units.ElectricalConductanceUnits.esu_cgs
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mho(self):
        """Set value using mho units."""
        unit_const = units.ElectricalConductanceUnits.mho
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def microsiemens(self):
        """Set value using microsiemens units."""
        unit_const = units.ElectricalConductanceUnits.microsiemens
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def siemens(self):
        """Set value using siemens units."""
        unit_const = units.ElectricalConductanceUnits.siemens
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def S(self):
        """Set value using S units (alias for siemens)."""
        return self.siemens
    
    @property
    def millisiemens(self):
        """Set value using millisiemens units."""
        unit_const = units.ElectricalConductanceUnits.millisiemens
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mS(self):
        """Set value using mS units (alias for millisiemens)."""
        return self.millisiemens
    

class ElectricalPermittivitySetter(TypeSafeSetter):
    """ElectricalPermittivity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def farad_per_meter(self):
        """Set value using farad per meter units."""
        unit_const = units.ElectricalPermittivityUnits.farad_per_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ElectricalResistivitySetter(TypeSafeSetter):
    """ElectricalResistivity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def circular_mil_ohm_per_foot(self):
        """Set value using circular mil-ohm per foot units."""
        unit_const = units.ElectricalResistivityUnits.circular_mil_ohm_per_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu cgs units."""
        unit_const = units.ElectricalResistivityUnits.emu_cgs
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def microhm_inch(self):
        """Set value using microhm-inch units."""
        unit_const = units.ElectricalResistivityUnits.microhm_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ohm_centimeter(self):
        """Set value using ohm-centimeter units."""
        unit_const = units.ElectricalResistivityUnits.ohm_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ohm_meter(self):
        """Set value using ohm-meter units."""
        unit_const = units.ElectricalResistivityUnits.ohm_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class EnergyFluxSetter(TypeSafeSetter):
    """EnergyFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Btu_per_square_foot_per_hour(self):
        """Set value using Btu per square foot per hour units."""
        unit_const = units.EnergyFluxUnits.Btu_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_per_square_centimeter_per_second(self):
        """Set value using calorie per square centimeter per second units."""
        unit_const = units.EnergyFluxUnits.calorie_per_square_centimeter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_cm_power_2_s(self):
        """Set value using cal / cm^{2 / s units (alias for calorie per square centimeter per second)."""
        return self.calorie_per_square_centimeter_per_second
    
    @property
    def cal_cm_power_2_tilde_s(self):
        """Set value using cal / ( cm^{2 ~s ) units (alias for calorie per square centimeter per second)."""
        return self.calorie_per_square_centimeter_per_second
    
    @property
    def Celsius_heat_units_Chu_per_square_foot_per_hour(self):
        """Set value using Celsius heat units (Chu) per square foot per hour units."""
        unit_const = units.EnergyFluxUnits.Celsius_heat_units_Chu_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilocalorie_per_square_foot_per_hour(self):
        """Set value using kilocalorie per square foot per hour units."""
        unit_const = units.EnergyFluxUnits.kilocalorie_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilocalorie_per_square_meter_per_hour(self):
        """Set value using kilocalorie per square meter per hour units."""
        unit_const = units.EnergyFluxUnits.kilocalorie_per_square_meter_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def watt_per_square_meter(self):
        """Set value using watt per square meter units."""
        unit_const = units.EnergyFluxUnits.watt_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class EnergyHeatWorkSetter(TypeSafeSetter):
    """EnergyHeatWork-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def barrel_oil_equivalent_or_equivalent_barrel(self):
        """Set value using barrel oil equivalent or equivalent barrel units."""
        unit_const = units.EnergyHeatWorkUnits.barrel_oil_equivalent_or_equivalent_barrel
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def bboe(self):
        """Set value using bboe units (alias for barrel oil equivalent or equivalent barrel)."""
        return self.barrel_oil_equivalent_or_equivalent_barrel
    
    @property
    def boe(self):
        """Set value using boe units (alias for barrel oil equivalent or equivalent barrel)."""
        return self.barrel_oil_equivalent_or_equivalent_barrel
    
    @property
    def billion_electronvolt(self):
        """Set value using billion electronvolt units."""
        unit_const = units.EnergyHeatWorkUnits.billion_electronvolt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def BeV(self):
        """Set value using BeV units (alias for billion electronvolt)."""
        return self.billion_electronvolt
    
    @property
    def British_thermal_unit_4_power_circ_mathrm_C(self):
        r"""Set value using British thermal unit ( $4^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.British_thermal_unit_4_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_60_power_circ_mathrm_F(self):
        r"""Set value using British thermal unit ( $60^{\circ} \mathrm{F}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.British_thermal_unit_60_power_circ_mathrm_F
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_international_steam_tables(self):
        """Set value using British thermal unit (international steam tables) units."""
        unit_const = units.EnergyHeatWorkUnits.British_thermal_unit_international_steam_tables
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_ISO_TC_12(self):
        """Set value using British thermal unit (ISO/TC 12) units."""
        unit_const = units.EnergyHeatWorkUnits.British_thermal_unit_ISO_TC_12
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_mean(self):
        """Set value using British thermal unit (mean) units."""
        unit_const = units.EnergyHeatWorkUnits.British_thermal_unit_mean
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_mean(self):
        """Set value using Btu (mean) units (alias for British thermal unit (mean))."""
        return self.British_thermal_unit_mean
    
    @property
    def Btu(self):
        """Set value using Btu units (alias for British thermal unit (mean))."""
        return self.British_thermal_unit_mean
    
    @property
    def British_thermal_unit_thermochemical(self):
        """Set value using British thermal unit (thermochemical) units."""
        unit_const = units.EnergyHeatWorkUnits.British_thermal_unit_thermochemical
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_20_power_circ_mathrm_C(self):
        r"""Set value using calorie ( $20^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_20_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_4_power_circ_mathrm_C(self):
        r"""Set value using calorie ( $4^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_4_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_international_steam_tables(self):
        """Set value using calorie (international steam tables) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_international_steam_tables
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_mean(self):
        """Set value using calorie (mean) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_mean
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Calorie_nutritional(self):
        """Set value using Calorie (nutritional) units."""
        unit_const = units.EnergyHeatWorkUnits.Calorie_nutritional
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_thermochemical(self):
        """Set value using calorie (thermochemical) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_thermochemical
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Celsius_heat_unit(self):
        """Set value using Celsius heat unit units."""
        unit_const = units.EnergyHeatWorkUnits.Celsius_heat_unit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu(self):
        """Set value using Chu units (alias for Celsius heat unit)."""
        return self.Celsius_heat_unit
    
    @property
    def Celsius_heat_unit_15_power_circ_mathrm_C(self):
        r"""Set value using Celsius heat unit ( $15{ }^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.Celsius_heat_unit_15_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def electron_volt(self):
        """Set value using electron volt units."""
        unit_const = units.EnergyHeatWorkUnits.electron_volt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def eV(self):
        """Set value using eV units (alias for electron volt)."""
        return self.electron_volt
    
    @property
    def erg(self):
        """Set value using erg units."""
        unit_const = units.EnergyHeatWorkUnits.erg
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pound_force_duty(self):
        """Set value using foot pound force (duty) units."""
        unit_const = units.EnergyHeatWorkUnits.foot_pound_force_duty
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_poundal(self):
        """Set value using foot-poundal units."""
        unit_const = units.EnergyHeatWorkUnits.foot_poundal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def frigorie(self):
        """Set value using frigorie units."""
        unit_const = units.EnergyHeatWorkUnits.frigorie
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def fg(self):
        """Set value using fg units (alias for frigorie)."""
        return self.frigorie
    
    @property
    def hartree_atomic_unit_of_energy(self):
        """Set value using hartree (atomic unit of energy) units."""
        unit_const = units.EnergyHeatWorkUnits.hartree_atomic_unit_of_energy
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule(self):
        """Set value using joule units."""
        unit_const = units.EnergyHeatWorkUnits.joule
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def J(self):
        """Set value using J units (alias for joule)."""
        return self.joule
    
    @property
    def joule_international(self):
        """Set value using joule (international) units."""
        unit_const = units.EnergyHeatWorkUnits.joule_international
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilocalorie_thermal(self):
        """Set value using kilocalorie (thermal) units."""
        unit_const = units.EnergyHeatWorkUnits.kilocalorie_thermal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force_meter(self):
        """Set value using kilogram force meter units."""
        unit_const = units.EnergyHeatWorkUnits.kilogram_force_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kiloton_TNT(self):
        """Set value using kiloton (TNT) units."""
        unit_const = units.EnergyHeatWorkUnits.kiloton_TNT
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilowatt_hour(self):
        """Set value using kilowatt hour units."""
        unit_const = units.EnergyHeatWorkUnits.kilowatt_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kWh(self):
        """Set value using kWh units (alias for kilowatt hour)."""
        return self.kilowatt_hour
    
    @property
    def liter_atmosphere(self):
        """Set value using liter atmosphere units."""
        unit_const = units.EnergyHeatWorkUnits.liter_atmosphere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def megaton_TNT(self):
        """Set value using megaton (TNT) units."""
        unit_const = units.EnergyHeatWorkUnits.megaton_TNT
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_centigrade_unit_15_power_circ_mathrm_C(self):
        r"""Set value using pound centigrade unit ( $15^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.pound_centigrade_unit_15_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def prout(self):
        """Set value using prout units."""
        unit_const = units.EnergyHeatWorkUnits.prout
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Q_unit(self):
        """Set value using Q unit units."""
        unit_const = units.EnergyHeatWorkUnits.Q_unit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Q(self):
        """Set value using Q units (alias for Q unit)."""
        return self.Q_unit
    
    @property
    def quad_quadrillion_Btu(self):
        """Set value using quad (quadrillion Btu) units."""
        unit_const = units.EnergyHeatWorkUnits.quad_quadrillion_Btu
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def quad(self):
        """Set value using quad units (alias for quad (quadrillion Btu))."""
        return self.quad_quadrillion_Btu
    
    @property
    def rydberg(self):
        """Set value using rydberg units."""
        unit_const = units.EnergyHeatWorkUnits.rydberg
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ry(self):
        """Set value using Ry units (alias for rydberg)."""
        return self.rydberg
    
    @property
    def therm_EEG(self):
        """Set value using therm (EEG) units."""
        unit_const = units.EnergyHeatWorkUnits.therm_EEG
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def therm_refineries(self):
        """Set value using therm (refineries) units."""
        unit_const = units.EnergyHeatWorkUnits.therm_refineries
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def therm_refy(self):
        """Set value using therm (refy) units (alias for therm (refineries))."""
        return self.therm_refineries
    
    @property
    def therm(self):
        """Set value using therm units (alias for therm (refineries))."""
        return self.therm_refineries
    
    @property
    def therm_US(self):
        """Set value using therm (US) units."""
        unit_const = units.EnergyHeatWorkUnits.therm_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_coal_equivalent(self):
        """Set value using ton coal equivalent units."""
        unit_const = units.EnergyHeatWorkUnits.ton_coal_equivalent
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_oil_equivalent(self):
        """Set value using ton oil equivalent units."""
        unit_const = units.EnergyHeatWorkUnits.ton_oil_equivalent
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilojoule(self):
        """Set value using kilojoule units."""
        unit_const = units.EnergyHeatWorkUnits.kilojoule
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kJ(self):
        """Set value using kJ units (alias for kilojoule)."""
        return self.kilojoule
    
    @property
    def megajoule(self):
        """Set value using megajoule units."""
        unit_const = units.EnergyHeatWorkUnits.megajoule
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MJ(self):
        """Set value using MJ units (alias for megajoule)."""
        return self.megajoule
    
    @property
    def gigajoule(self):
        """Set value using gigajoule units."""
        unit_const = units.EnergyHeatWorkUnits.gigajoule
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def GJ(self):
        """Set value using GJ units (alias for gigajoule)."""
        return self.gigajoule
    

class EnergyPerUnitAreaSetter(TypeSafeSetter):
    """EnergyPerUnitArea-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_per_square_foot(self):
        """Set value using British thermal unit per square foot units."""
        unit_const = units.EnergyPerUnitAreaUnits.British_thermal_unit_per_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_ft_power_2(self):
        """Set value using Btu / ft^{2 units (alias for British thermal unit per square foot)."""
        return self.British_thermal_unit_per_square_foot
    
    @property
    def Btu_sq_ft(self):
        """Set value using Btu/sq ft units (alias for British thermal unit per square foot)."""
        return self.British_thermal_unit_per_square_foot
    
    @property
    def joule_per_square_meter(self):
        """Set value using joule per square meter units."""
        unit_const = units.EnergyPerUnitAreaUnits.joule_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Langley(self):
        """Set value using Langley units."""
        unit_const = units.EnergyPerUnitAreaUnits.Langley
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ly(self):
        """Set value using Ly units (alias for Langley)."""
        return self.Langley
    

class ForceSetter(TypeSafeSetter):
    """Force-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def crinal(self):
        """Set value using crinal units."""
        unit_const = units.ForceUnits.crinal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyne(self):
        """Set value using dyne units."""
        unit_const = units.ForceUnits.dyne
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn(self):
        """Set value using dyn units (alias for dyne)."""
        return self.dyne
    
    @property
    def funal(self):
        """Set value using funal units."""
        unit_const = units.ForceUnits.funal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force(self):
        """Set value using kilogram force units."""
        unit_const = units.ForceUnits.kilogram_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kip_force(self):
        """Set value using kip force units."""
        unit_const = units.ForceUnits.kip_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton(self):
        """Set value using newton units."""
        unit_const = units.ForceUnits.newton
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def N(self):
        """Set value using N units (alias for newton)."""
        return self.newton
    
    @property
    def ounce_force(self):
        """Set value using ounce force units."""
        unit_const = units.ForceUnits.ounce_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def oz_f(self):
        """Set value using oz_{f units (alias for ounce force)."""
        return self.ounce_force
    
    @property
    def oz(self):
        """Set value using oz units (alias for ounce force)."""
        return self.ounce_force
    
    @property
    def pond(self):
        """Set value using pond units."""
        unit_const = units.ForceUnits.pond
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def p(self):
        """Set value using p units (alias for pond)."""
        return self.pond
    
    @property
    def pound_force(self):
        """Set value using pound force units."""
        unit_const = units.ForceUnits.pound_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_f(self):
        """Set value using lb_{f units (alias for pound force)."""
        return self.pound_force
    
    @property
    def lb(self):
        """Set value using lb units (alias for pound force)."""
        return self.pound_force
    
    @property
    def poundal(self):
        """Set value using poundal units."""
        unit_const = units.ForceUnits.poundal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pdl(self):
        """Set value using pdl units (alias for poundal)."""
        return self.poundal
    
    @property
    def slug_force(self):
        """Set value using slug force units."""
        unit_const = units.ForceUnits.slug_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sthène(self):
        """Set value using sthène units."""
        unit_const = units.ForceUnits.sthène
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sn(self):
        """Set value using sn units (alias for sthène)."""
        return self.sthène
    
    @property
    def ton_force_long(self):
        """Set value using ton (force, long) units."""
        unit_const = units.ForceUnits.ton_force_long
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def LT(self):
        """Set value using LT units (alias for ton (force, long))."""
        return self.ton_force_long
    
    @property
    def ton_force_metric(self):
        """Set value using ton (force, metric) units."""
        unit_const = units.ForceUnits.ton_force_metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT(self):
        """Set value using MT units (alias for ton (force, metric))."""
        return self.ton_force_metric
    
    @property
    def ton_force_short(self):
        """Set value using ton (force, short) units."""
        unit_const = units.ForceUnits.ton_force_short
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def T(self):
        """Set value using T units (alias for ton (force, short))."""
        return self.ton_force_short
    
    @property
    def kilonewton(self):
        """Set value using kilonewton units."""
        unit_const = units.ForceUnits.kilonewton
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kN(self):
        """Set value using kN units (alias for kilonewton)."""
        return self.kilonewton
    
    @property
    def millinewton(self):
        """Set value using millinewton units."""
        unit_const = units.ForceUnits.millinewton
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mN(self):
        """Set value using mN units (alias for millinewton)."""
        return self.millinewton
    

class ForceBodySetter(TypeSafeSetter):
    """ForceBody-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_cubic_centimeter(self):
        """Set value using dyne per cubic centimeter units."""
        unit_const = units.ForceBodyUnits.dyne_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_cc(self):
        """Set value using dyn/cc units (alias for dyne per cubic centimeter)."""
        return self.dyne_per_cubic_centimeter
    
    @property
    def dyn_cm_power_3(self):
        """Set value using dyn/ cm^{3 units (alias for dyne per cubic centimeter)."""
        return self.dyne_per_cubic_centimeter
    
    @property
    def kilogram_force_per_cubic_centimeter(self):
        """Set value using kilogram force per cubic centimeter units."""
        unit_const = units.ForceBodyUnits.kilogram_force_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force_per_cubic_meter(self):
        """Set value using kilogram force per cubic meter units."""
        unit_const = units.ForceBodyUnits.kilogram_force_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_per_cubic_meter(self):
        """Set value using newton per cubic meter units."""
        unit_const = units.ForceBodyUnits.newton_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_force_per_cubic_foot(self):
        """Set value using pound force per cubic foot units."""
        unit_const = units.ForceBodyUnits.pound_force_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_force_per_cubic_inch(self):
        """Set value using pound force per cubic inch units."""
        unit_const = units.ForceBodyUnits.pound_force_per_cubic_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_force_per_cubic_foot(self):
        """Set value using ton force per cubic foot units."""
        unit_const = units.ForceBodyUnits.ton_force_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ForcePerUnitMassSetter(TypeSafeSetter):
    """ForcePerUnitMass-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_gram(self):
        """Set value using dyne per gram units."""
        unit_const = units.ForcePerUnitMassUnits.dyne_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force_per_kilogram(self):
        """Set value using kilogram force per kilogram units."""
        unit_const = units.ForcePerUnitMassUnits.kilogram_force_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_per_kilogram(self):
        """Set value using newton per kilogram units."""
        unit_const = units.ForcePerUnitMassUnits.newton_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_force_per_pound_mass(self):
        """Set value using pound force per pound mass units."""
        unit_const = units.ForcePerUnitMassUnits.pound_force_per_pound_mass
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_f_lb(self):
        """Set value using lb_{f / lb units (alias for pound force per pound mass)."""
        return self.pound_force_per_pound_mass
    
    @property
    def lb_f_lb_m(self):
        """Set value using lb_{f / lb_{m units (alias for pound force per pound mass)."""
        return self.pound_force_per_pound_mass
    
    @property
    def pound_force_per_slug(self):
        """Set value using pound force per slug units."""
        unit_const = units.ForcePerUnitMassUnits.pound_force_per_slug
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class FrequencyVoltageRatioSetter(TypeSafeSetter):
    """FrequencyVoltageRatio-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cycles_per_second_per_volt(self):
        """Set value using cycles per second per volt units."""
        unit_const = units.FrequencyVoltageRatioUnits.cycles_per_second_per_volt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def hertz_per_volt(self):
        """Set value using hertz per volt units."""
        unit_const = units.FrequencyVoltageRatioUnits.hertz_per_volt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def terahertz_per_volt(self):
        """Set value using terahertz per volt units."""
        unit_const = units.FrequencyVoltageRatioUnits.terahertz_per_volt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class FuelConsumptionSetter(TypeSafeSetter):
    """FuelConsumption-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def unit_100_km_per_liter(self):
        """Set value using 100 km per liter units."""
        unit_const = units.FuelConsumptionUnits.unit_100_km_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallons_UK_per_100_miles(self):
        """Set value using gallons (UK) per 100 miles units."""
        unit_const = units.FuelConsumptionUnits.gallons_UK_per_100_miles
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallons_US_per_100_miles(self):
        """Set value using gallons (US) per 100 miles units."""
        unit_const = units.FuelConsumptionUnits.gallons_US_per_100_miles
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilometers_per_gallon_UK(self):
        """Set value using kilometers per gallon (UK) units."""
        unit_const = units.FuelConsumptionUnits.kilometers_per_gallon_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilometers_per_gallon_US(self):
        """Set value using kilometers per gallon (US) units."""
        unit_const = units.FuelConsumptionUnits.kilometers_per_gallon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilometers_per_liter(self):
        """Set value using kilometers per liter units."""
        unit_const = units.FuelConsumptionUnits.kilometers_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_100_km(self):
        """Set value using liters per 100 km units."""
        unit_const = units.FuelConsumptionUnits.liters_per_100_km
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_kilometer(self):
        """Set value using liters per kilometer units."""
        unit_const = units.FuelConsumptionUnits.liters_per_kilometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def meters_per_gallon_UK(self):
        """Set value using meters per gallon (UK) units."""
        unit_const = units.FuelConsumptionUnits.meters_per_gallon_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def meters_per_gallon_US(self):
        """Set value using meters per gallon (US) units."""
        unit_const = units.FuelConsumptionUnits.meters_per_gallon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def miles_per_gallon_UK(self):
        """Set value using miles per gallon (UK) units."""
        unit_const = units.FuelConsumptionUnits.miles_per_gallon_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_gal_UK(self):
        """Set value using mi/gal (UK) units (alias for miles per gallon (UK))."""
        return self.miles_per_gallon_UK
    
    @property
    def mpg_UK(self):
        """Set value using mpg (UK) units (alias for miles per gallon (UK))."""
        return self.miles_per_gallon_UK
    
    @property
    def miles_per_gallon_US(self):
        """Set value using miles per gallon (US) units."""
        unit_const = units.FuelConsumptionUnits.miles_per_gallon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_gal_US(self):
        """Set value using mi/gal (US) units (alias for miles per gallon (US))."""
        return self.miles_per_gallon_US
    
    @property
    def mpg_US(self):
        """Set value using mpg (US) units (alias for miles per gallon (US))."""
        return self.miles_per_gallon_US
    
    @property
    def miles_per_liter(self):
        """Set value using miles per liter units."""
        unit_const = units.FuelConsumptionUnits.miles_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class HeatOfCombustionSetter(TypeSafeSetter):
    """HeatOfCombustion-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.HeatOfCombustionUnits.British_thermal_unit_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.HeatOfCombustionUnits.calorie_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.HeatOfCombustionUnits.Chu_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.HeatOfCombustionUnits.joule_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class HeatOfFusionSetter(TypeSafeSetter):
    """HeatOfFusion-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_mean_per_pound(self):
        """Set value using British thermal unit (mean) per pound units."""
        unit_const = units.HeatOfFusionUnits.British_thermal_unit_mean_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.HeatOfFusionUnits.British_thermal_unit_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.HeatOfFusionUnits.calorie_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.HeatOfFusionUnits.Chu_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.HeatOfFusionUnits.joule_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class HeatOfVaporizationSetter(TypeSafeSetter):
    """HeatOfVaporization-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.HeatOfVaporizationUnits.British_thermal_unit_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.HeatOfVaporizationUnits.calorie_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.HeatOfVaporizationUnits.Chu_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.HeatOfVaporizationUnits.joule_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class HeatTransferCoefficientSetter(TypeSafeSetter):
    """HeatTransferCoefficient-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Btu_per_square_foot_per_hour_per_degree_Fahrenheit_or_Rankine(self):
        """Set value using Btu per square foot per hour per degree Fahrenheit (or Rankine) units."""
        unit_const = units.HeatTransferCoefficientUnits.Btu_per_square_foot_per_hour_per_degree_Fahrenheit_or_Rankine
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def watt_per_square_meter_per_degree_Celsius_or_kelvin(self):
        """Set value using watt per square meter per degree Celsius (or kelvin) units."""
        unit_const = units.HeatTransferCoefficientUnits.watt_per_square_meter_per_degree_Celsius_or_kelvin
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class IlluminanceSetter(TypeSafeSetter):
    """Illuminance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_candle(self):
        """Set value using foot-candle units."""
        unit_const = units.IlluminanceUnits.foot_candle
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_C(self):
        """Set value using ft-C units (alias for foot-candle)."""
        return self.foot_candle
    
    @property
    def ft_Cd(self):
        """Set value using ft-Cd units (alias for foot-candle)."""
        return self.foot_candle
    
    @property
    def lux(self):
        """Set value using lux units."""
        unit_const = units.IlluminanceUnits.lux
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lx(self):
        """Set value using lx units (alias for lux)."""
        return self.lux
    
    @property
    def nox(self):
        """Set value using nox units."""
        unit_const = units.IlluminanceUnits.nox
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def phot(self):
        """Set value using phot units."""
        unit_const = units.IlluminanceUnits.phot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ph(self):
        """Set value using ph units (alias for phot)."""
        return self.phot
    
    @property
    def skot(self):
        """Set value using skot units."""
        unit_const = units.IlluminanceUnits.skot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class KineticEnergyOfTurbulenceSetter(TypeSafeSetter):
    """KineticEnergyOfTurbulence-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_foot_per_second_squared(self):
        """Set value using square foot per second squared units."""
        unit_const = units.KineticEnergyOfTurbulenceUnits.square_foot_per_second_squared
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_2_s_power_2(self):
        """Set value using ft^{2 / s^{2 units (alias for square foot per second squared)."""
        return self.square_foot_per_second_squared
    
    @property
    def sqft_sec_power_2(self):
        """Set value using sqft/sec { ^{2 units (alias for square foot per second squared)."""
        return self.square_foot_per_second_squared
    
    @property
    def square_meters_per_second_squared(self):
        """Set value using square meters per second squared units."""
        unit_const = units.KineticEnergyOfTurbulenceUnits.square_meters_per_second_squared
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class LengthSetter(TypeSafeSetter):
    """Length-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def ångström(self):
        """Set value using ångström units."""
        unit_const = units.LengthUnits.ångström
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def AA(self):
        """Set value using AA units (alias for ångström)."""
        return self.ångström
    
    @property
    def arpent_Quebec(self):
        """Set value using arpent (Quebec) units."""
        unit_const = units.LengthUnits.arpent_Quebec
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def arp(self):
        """Set value using arp units (alias for arpent (Quebec))."""
        return self.arpent_Quebec
    
    @property
    def astronomic_unit(self):
        """Set value using astronomic unit units."""
        unit_const = units.LengthUnits.astronomic_unit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def AU(self):
        """Set value using AU units (alias for astronomic unit)."""
        return self.astronomic_unit
    
    @property
    def attometer(self):
        """Set value using attometer units."""
        unit_const = units.LengthUnits.attometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def am(self):
        """Set value using am units (alias for attometer)."""
        return self.attometer
    
    @property
    def calibre_centinch(self):
        """Set value using calibre (centinch) units."""
        unit_const = units.LengthUnits.calibre_centinch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cin(self):
        """Set value using cin units (alias for calibre (centinch))."""
        return self.calibre_centinch
    
    @property
    def centimeter(self):
        """Set value using centimeter units."""
        unit_const = units.LengthUnits.centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm(self):
        """Set value using cm units (alias for centimeter)."""
        return self.centimeter
    
    @property
    def chain_Engr_s_or_Ramsden(self):
        """Set value using chain (Engr's or Ramsden) units."""
        unit_const = units.LengthUnits.chain_Engr_s_or_Ramsden
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ch_eng(self):
        """Set value using ch (eng units (alias for chain (Engr's or Ramsden))."""
        return self.chain_Engr_s_or_Ramsden
    
    @property
    def Rams(self):
        """Set value using Rams) units (alias for chain (Engr's or Ramsden))."""
        return self.chain_Engr_s_or_Ramsden
    
    @property
    def chain_Gunter_s(self):
        """Set value using chain (Gunter's) units."""
        unit_const = units.LengthUnits.chain_Gunter_s
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def chain_surveyors(self):
        """Set value using chain (surveyors) units."""
        unit_const = units.LengthUnits.chain_surveyors
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubit_UK(self):
        """Set value using cubit (UK) units."""
        unit_const = units.LengthUnits.cubit_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ell(self):
        """Set value using ell units."""
        unit_const = units.LengthUnits.ell
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def fathom(self):
        """Set value using fathom units."""
        unit_const = units.LengthUnits.fathom
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def fath(self):
        """Set value using fath units (alias for fathom)."""
        return self.fathom
    
    @property
    def femtometre(self):
        """Set value using femtometre units."""
        unit_const = units.LengthUnits.femtometre
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def fm(self):
        """Set value using fm units (alias for femtometre)."""
        return self.femtometre
    
    @property
    def fermi(self):
        """Set value using fermi units."""
        unit_const = units.LengthUnits.fermi
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def F(self):
        """Set value using F units (alias for fermi)."""
        return self.fermi
    
    @property
    def foot(self):
        """Set value using foot units."""
        unit_const = units.LengthUnits.foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft(self):
        """Set value using ft units (alias for foot)."""
        return self.foot
    
    @property
    def furlong_UK_and_US(self):
        """Set value using furlong (UK and US) units."""
        unit_const = units.LengthUnits.furlong_UK_and_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def fur(self):
        """Set value using fur units (alias for furlong (UK and US))."""
        return self.furlong_UK_and_US
    
    @property
    def inch(self):
        """Set value using inch units."""
        unit_const = units.LengthUnits.inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_unit(self):
        """Set value using in units (alias for inch)."""
        return self.inch
    
    @property
    def kilometer(self):
        """Set value using kilometer units."""
        unit_const = units.LengthUnits.kilometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def km(self):
        """Set value using km units (alias for kilometer)."""
        return self.kilometer
    
    @property
    def league_US_statute(self):
        """Set value using league (US, statute) units."""
        unit_const = units.LengthUnits.league_US_statute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lieue_metric(self):
        """Set value using lieue (metric) units."""
        unit_const = units.LengthUnits.lieue_metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ligne_metric(self):
        """Set value using ligne (metric) units."""
        unit_const = units.LengthUnits.ligne_metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def line_US(self):
        """Set value using line (US) units."""
        unit_const = units.LengthUnits.line_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def link_surveyors(self):
        """Set value using link (surveyors) units."""
        unit_const = units.LengthUnits.link_surveyors
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def meter(self):
        """Set value using meter units."""
        unit_const = units.LengthUnits.meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def m(self):
        """Set value using m units (alias for meter)."""
        return self.meter
    
    @property
    def micrometer(self):
        """Set value using micrometer units."""
        unit_const = units.LengthUnits.micrometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def micron(self):
        """Set value using micron units."""
        unit_const = units.LengthUnits.micron
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu(self):
        """Set value using mu units (alias for micron)."""
        return self.micron
    
    @property
    def mil(self):
        """Set value using mil units."""
        unit_const = units.LengthUnits.mil
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mile_geographical(self):
        """Set value using mile (geographical) units."""
        unit_const = units.LengthUnits.mile_geographical
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi(self):
        """Set value using mi units (alias for mile (geographical))."""
        return self.mile_geographical
    
    @property
    def mile_US_nautical(self):
        """Set value using mile (US, nautical) units."""
        unit_const = units.LengthUnits.mile_US_nautical
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mile_US_statute(self):
        """Set value using mile (US, statute) units."""
        unit_const = units.LengthUnits.mile_US_statute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mile_US_survey(self):
        """Set value using mile (US, survey) units."""
        unit_const = units.LengthUnits.mile_US_survey
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millimeter(self):
        """Set value using millimeter units."""
        unit_const = units.LengthUnits.millimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mm(self):
        """Set value using mm units (alias for millimeter)."""
        return self.millimeter
    
    @property
    def millimicron(self):
        """Set value using millimicron units."""
        unit_const = units.LengthUnits.millimicron
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanometer_or_nanon(self):
        """Set value using nanometer or nanon units."""
        unit_const = units.LengthUnits.nanometer_or_nanon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nm(self):
        """Set value using nm units (alias for nanometer or nanon)."""
        return self.nanometer_or_nanon
    
    @property
    def parsec(self):
        """Set value using parsec units."""
        unit_const = units.LengthUnits.parsec
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pc(self):
        """Set value using pc units (alias for parsec)."""
        return self.parsec
    
    @property
    def perche(self):
        """Set value using perche units."""
        unit_const = units.LengthUnits.perche
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rod(self):
        """Set value using rod units (alias for perche)."""
        return self.perche
    
    @property
    def pica(self):
        """Set value using pica units."""
        unit_const = units.LengthUnits.pica
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def picometer(self):
        """Set value using picometer units."""
        unit_const = units.LengthUnits.picometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pm(self):
        """Set value using pm units (alias for picometer)."""
        return self.picometer
    
    @property
    def point_Didot(self):
        """Set value using point (Didot) units."""
        unit_const = units.LengthUnits.point_Didot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def point_US(self):
        """Set value using point (US) units."""
        unit_const = units.LengthUnits.point_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rod_or_pole(self):
        """Set value using rod or pole units."""
        unit_const = units.LengthUnits.rod_or_pole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def span(self):
        """Set value using span units."""
        unit_const = units.LengthUnits.span
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def thou_millinch(self):
        """Set value using thou (millinch) units."""
        unit_const = units.LengthUnits.thou_millinch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def thou(self):
        """Set value using thou units (alias for thou (millinch))."""
        return self.thou_millinch
    
    @property
    def toise_metric(self):
        """Set value using toise (metric) units."""
        unit_const = units.LengthUnits.toise_metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def yard(self):
        """Set value using yard units."""
        unit_const = units.LengthUnits.yard
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def yd(self):
        """Set value using yd units (alias for yard)."""
        return self.yard
    
    @property
    def nanometer(self):
        """Set value using nanometer units."""
        unit_const = units.LengthUnits.nanometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class LinearMassDensitySetter(TypeSafeSetter):
    """LinearMassDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def denier(self):
        """Set value using denier units."""
        unit_const = units.LinearMassDensityUnits.denier
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_centimeter(self):
        """Set value using kilogram per centimeter units."""
        unit_const = units.LinearMassDensityUnits.kilogram_per_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_meter(self):
        """Set value using kilogram per meter units."""
        unit_const = units.LinearMassDensityUnits.kilogram_per_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_per_foot(self):
        """Set value using pound per foot units."""
        unit_const = units.LinearMassDensityUnits.pound_per_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_per_inch(self):
        """Set value using pound per inch units."""
        unit_const = units.LinearMassDensityUnits.pound_per_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_per_yard(self):
        """Set value using pound per yard units."""
        unit_const = units.LinearMassDensityUnits.pound_per_yard
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_metric_per_kilometer(self):
        """Set value using ton (metric) per kilometer units."""
        unit_const = units.LinearMassDensityUnits.ton_metric_per_kilometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def t_km(self):
        """Set value using t/km units (alias for ton (metric) per kilometer)."""
        return self.ton_metric_per_kilometer
    
    @property
    def MT_km(self):
        """Set value using MT/km units (alias for ton (metric) per kilometer)."""
        return self.ton_metric_per_kilometer
    
    @property
    def ton_metric_per_meter(self):
        """Set value using ton (metric) per meter units."""
        unit_const = units.LinearMassDensityUnits.ton_metric_per_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def t_m(self):
        """Set value using t/m units (alias for ton (metric) per meter)."""
        return self.ton_metric_per_meter
    
    @property
    def MT_m(self):
        """Set value using MT/m units (alias for ton (metric) per meter)."""
        return self.ton_metric_per_meter
    

class LinearMomentumSetter(TypeSafeSetter):
    """LinearMomentum-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_pounds_force_per_hour(self):
        """Set value using foot pounds force per hour units."""
        unit_const = units.LinearMomentumUnits.foot_pounds_force_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_lb_f_power_h(self):
        """Set value using {ft lb_{f^{/ h units (alias for foot pounds force per hour)."""
        return self.foot_pounds_force_per_hour
    
    @property
    def ft_lb_hr(self):
        """Set value using ft-lb / hr units (alias for foot pounds force per hour)."""
        return self.foot_pounds_force_per_hour
    
    @property
    def foot_pounds_force_per_minute(self):
        """Set value using foot pounds force per minute units."""
        unit_const = units.LinearMomentumUnits.foot_pounds_force_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_lb_f_min(self):
        """Set value using ft lb_{f / min units (alias for foot pounds force per minute)."""
        return self.foot_pounds_force_per_minute
    
    @property
    def ft_lb_min(self):
        """Set value using ft-lb / min units (alias for foot pounds force per minute)."""
        return self.foot_pounds_force_per_minute
    
    @property
    def foot_pounds_force_per_second(self):
        """Set value using foot pounds force per second units."""
        unit_const = units.LinearMomentumUnits.foot_pounds_force_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_lb_f_s(self):
        """Set value using ft lb_{f / s units (alias for foot pounds force per second)."""
        return self.foot_pounds_force_per_second
    
    @property
    def ft_lb_sec(self):
        """Set value using ft-lb/sec units (alias for foot pounds force per second)."""
        return self.foot_pounds_force_per_second
    
    @property
    def gram_centimeters_per_second(self):
        """Set value using gram centimeters per second units."""
        unit_const = units.LinearMomentumUnits.gram_centimeters_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_meters_per_second(self):
        """Set value using kilogram meters per second units."""
        unit_const = units.LinearMomentumUnits.kilogram_meters_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class LuminanceSelfSetter(TypeSafeSetter):
    """LuminanceSelf-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def apostilb(self):
        """Set value using apostilb units."""
        unit_const = units.LuminanceSelfUnits.apostilb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def asb(self):
        """Set value using asb units (alias for apostilb)."""
        return self.apostilb
    
    @property
    def blondel(self):
        """Set value using blondel units."""
        unit_const = units.LuminanceSelfUnits.blondel
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def candela_per_square_meter(self):
        """Set value using candela per square meter units."""
        unit_const = units.LuminanceSelfUnits.candela_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_lambert(self):
        """Set value using foot-lambert units."""
        unit_const = units.LuminanceSelfUnits.foot_lambert
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lambert(self):
        """Set value using lambert units."""
        unit_const = units.LuminanceSelfUnits.lambert
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def L(self):
        """Set value using L units (alias for lambert)."""
        return self.lambert
    
    @property
    def luxon(self):
        """Set value using luxon units."""
        unit_const = units.LuminanceSelfUnits.luxon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nit(self):
        """Set value using nit units."""
        unit_const = units.LuminanceSelfUnits.nit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def stilb(self):
        """Set value using stilb units."""
        unit_const = units.LuminanceSelfUnits.stilb
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sb(self):
        """Set value using sb units (alias for stilb)."""
        return self.stilb
    
    @property
    def troland(self):
        """Set value using troland units."""
        unit_const = units.LuminanceSelfUnits.troland
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class LuminousFluxSetter(TypeSafeSetter):
    """LuminousFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def candela_steradian(self):
        """Set value using candela steradian units."""
        unit_const = units.LuminousFluxUnits.candela_steradian
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lumen(self):
        """Set value using lumen units."""
        unit_const = units.LuminousFluxUnits.lumen
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class LuminousIntensitySetter(TypeSafeSetter):
    """LuminousIntensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def candela(self):
        """Set value using candela units."""
        unit_const = units.LuminousIntensityUnits.candela
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cd(self):
        """Set value using cd units (alias for candela)."""
        return self.candela
    
    @property
    def candle_international(self):
        """Set value using candle (international) units."""
        unit_const = units.LuminousIntensityUnits.candle_international
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def carcel(self):
        """Set value using carcel units."""
        unit_const = units.LuminousIntensityUnits.carcel
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Hefner_unit(self):
        """Set value using Hefner unit units."""
        unit_const = units.LuminousIntensityUnits.Hefner_unit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def HK(self):
        """Set value using HK units (alias for Hefner unit)."""
        return self.Hefner_unit
    

class MagneticFieldSetter(TypeSafeSetter):
    """MagneticField-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def ampere_per_meter(self):
        """Set value using ampere per meter units."""
        unit_const = units.MagneticFieldUnits.ampere_per_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lenz(self):
        """Set value using lenz units."""
        unit_const = units.MagneticFieldUnits.lenz
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def oersted(self):
        """Set value using oersted units."""
        unit_const = units.MagneticFieldUnits.oersted
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Oe(self):
        """Set value using Oe units (alias for oersted)."""
        return self.oersted
    
    @property
    def praoersted(self):
        """Set value using praoersted units."""
        unit_const = units.MagneticFieldUnits.praoersted
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MagneticFluxSetter(TypeSafeSetter):
    """MagneticFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kapp_line(self):
        """Set value using kapp line units."""
        unit_const = units.MagneticFluxUnits.kapp_line
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def line(self):
        """Set value using line units."""
        unit_const = units.MagneticFluxUnits.line
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def maxwell(self):
        """Set value using maxwell units."""
        unit_const = units.MagneticFluxUnits.maxwell
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Mx(self):
        """Set value using Mx units (alias for maxwell)."""
        return self.maxwell
    
    @property
    def unit_pole(self):
        """Set value using unit pole units."""
        unit_const = units.MagneticFluxUnits.unit_pole
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def weber(self):
        """Set value using weber units."""
        unit_const = units.MagneticFluxUnits.weber
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Wb(self):
        """Set value using Wb units (alias for weber)."""
        return self.weber
    
    @property
    def milliweber(self):
        """Set value using milliweber units."""
        unit_const = units.MagneticFluxUnits.milliweber
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mWb(self):
        """Set value using mWb units (alias for milliweber)."""
        return self.milliweber
    
    @property
    def microweber(self):
        """Set value using microweber units."""
        unit_const = units.MagneticFluxUnits.microweber
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uWb(self):
        """Set value using μWb units (alias for microweber)."""
        return self.microweber
    

class MagneticInductionFieldStrengthSetter(TypeSafeSetter):
    """MagneticInductionFieldStrength-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gamma(self):
        """Set value using gamma units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.gamma
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gauss(self):
        """Set value using gauss units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.gauss
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def G(self):
        """Set value using G units (alias for gauss)."""
        return self.gauss
    
    @property
    def line_per_square_centimeter(self):
        """Set value using line per square centimeter units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.line_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def maxwell_per_square_centimeter(self):
        """Set value using maxwell per square centimeter units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.maxwell_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def tesla(self):
        """Set value using tesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.tesla
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def T(self):
        """Set value using T units (alias for tesla)."""
        return self.tesla
    
    @property
    def u_a(self):
        """Set value using u.a. units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.u_a
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def weber_per_square_meter(self):
        """Set value using weber per square meter units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.weber_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millitesla(self):
        """Set value using millitesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.millitesla
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mT(self):
        """Set value using mT units (alias for millitesla)."""
        return self.millitesla
    
    @property
    def microtesla(self):
        """Set value using microtesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.microtesla
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uT(self):
        """Set value using μT units (alias for microtesla)."""
        return self.microtesla
    
    @property
    def nanotesla(self):
        """Set value using nanotesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.nanotesla
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nT(self):
        """Set value using nT units (alias for nanotesla)."""
        return self.nanotesla
    

class MagneticMomentSetter(TypeSafeSetter):
    """MagneticMoment-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Bohr_magneton(self):
        """Set value using Bohr magneton units."""
        unit_const = units.MagneticMomentUnits.Bohr_magneton
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_tesla(self):
        """Set value using joule per tesla units."""
        unit_const = units.MagneticMomentUnits.joule_per_tesla
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nuclear_magneton(self):
        """Set value using nuclear magneton units."""
        unit_const = units.MagneticMomentUnits.nuclear_magneton
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MagneticPermeabilitySetter(TypeSafeSetter):
    """MagneticPermeability-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def henrys_per_meter(self):
        """Set value using henrys per meter units."""
        unit_const = units.MagneticPermeabilityUnits.henrys_per_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_per_square_ampere(self):
        """Set value using newton per square ampere units."""
        unit_const = units.MagneticPermeabilityUnits.newton_per_square_ampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MagnetomotiveForceSetter(TypeSafeSetter):
    """MagnetomotiveForce-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abampere_turn(self):
        """Set value using abampere-turn units."""
        unit_const = units.MagnetomotiveForceUnits.abampere_turn
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ampere(self):
        """Set value using ampere units."""
        unit_const = units.MagnetomotiveForceUnits.ampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def A(self):
        """Set value using A units (alias for ampere)."""
        return self.ampere
    
    @property
    def ampere_turn(self):
        """Set value using ampere-turn units."""
        unit_const = units.MagnetomotiveForceUnits.ampere_turn
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gilbert(self):
        """Set value using gilbert units."""
        unit_const = units.MagnetomotiveForceUnits.gilbert
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Gb(self):
        """Set value using Gb units (alias for gilbert)."""
        return self.gilbert
    
    @property
    def kiloampere(self):
        """Set value using kiloampere units."""
        unit_const = units.MagnetomotiveForceUnits.kiloampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kA(self):
        """Set value using kA units (alias for kiloampere)."""
        return self.kiloampere
    
    @property
    def milliampere(self):
        """Set value using milliampere units."""
        unit_const = units.MagnetomotiveForceUnits.milliampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mA(self):
        """Set value using mA units (alias for milliampere)."""
        return self.milliampere
    
    @property
    def microampere(self):
        """Set value using microampere units."""
        unit_const = units.MagnetomotiveForceUnits.microampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uA(self):
        """Set value using μA units (alias for microampere)."""
        return self.microampere
    
    @property
    def nanoampere(self):
        """Set value using nanoampere units."""
        unit_const = units.MagnetomotiveForceUnits.nanoampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def nA(self):
        """Set value using nA units (alias for nanoampere)."""
        return self.nanoampere
    
    @property
    def picoampere(self):
        """Set value using picoampere units."""
        unit_const = units.MagnetomotiveForceUnits.picoampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pA(self):
        """Set value using pA units (alias for picoampere)."""
        return self.picoampere
    

class MassSetter(TypeSafeSetter):
    """Mass-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def slug(self):
        """Set value using slug units."""
        unit_const = units.MassUnits.slug
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sl(self):
        """Set value using sl units (alias for slug)."""
        return self.slug
    
    @property
    def atomic_mass_unit_power_12_mathrm_C(self):
        r"""Set value using atomic mass unit ( ${ }^{12} \mathrm{C}$ ) units."""
        unit_const = units.MassUnits.atomic_mass_unit_power_12_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uleft_power_12_Cright(self):
        r"""Set value using uleft({ ^{12 Cright) units (alias for atomic mass unit ( ${ }^{12} \mathrm{C}$ ))."""
        return self.atomic_mass_unit_power_12_mathrm_C
    
    @property
    def amu(self):
        r"""Set value using amu units (alias for atomic mass unit ( ${ }^{12} \mathrm{C}$ ))."""
        return self.atomic_mass_unit_power_12_mathrm_C
    
    @property
    def carat_metric(self):
        """Set value using carat (metric) units."""
        unit_const = units.MassUnits.carat_metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ct(self):
        """Set value using ct units (alias for carat (metric))."""
        return self.carat_metric
    
    @property
    def cental(self):
        """Set value using cental units."""
        unit_const = units.MassUnits.cental
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def centigram(self):
        """Set value using centigram units."""
        unit_const = units.MassUnits.centigram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cg(self):
        """Set value using cg units (alias for centigram)."""
        return self.centigram
    
    @property
    def clove_UK(self):
        """Set value using clove (UK) units."""
        unit_const = units.MassUnits.clove_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cl(self):
        """Set value using cl units (alias for clove (UK))."""
        return self.clove_UK
    
    @property
    def drachm_apothecary(self):
        """Set value using drachm (apothecary) units."""
        unit_const = units.MassUnits.drachm_apothecary
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dram_avoirdupois(self):
        """Set value using dram (avoirdupois) units."""
        unit_const = units.MassUnits.dram_avoirdupois
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dram_troy(self):
        """Set value using dram (troy) units."""
        unit_const = units.MassUnits.dram_troy
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def grain(self):
        """Set value using grain units."""
        unit_const = units.MassUnits.grain
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gr(self):
        """Set value using gr units (alias for grain)."""
        return self.grain
    
    @property
    def gram(self):
        """Set value using gram units."""
        unit_const = units.MassUnits.gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def g(self):
        """Set value using g units (alias for gram)."""
        return self.gram
    
    @property
    def hundredweight_long_or_gross(self):
        """Set value using hundredweight, long or gross units."""
        unit_const = units.MassUnits.hundredweight_long_or_gross
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def hundredweight_short_or_net(self):
        """Set value using hundredweight, short or net units."""
        unit_const = units.MassUnits.hundredweight_short_or_net
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram(self):
        """Set value using kilogram units."""
        unit_const = units.MassUnits.kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg(self):
        """Set value using kg units (alias for kilogram)."""
        return self.kilogram
    
    @property
    def kip(self):
        """Set value using kip units."""
        unit_const = units.MassUnits.kip
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def microgram(self):
        """Set value using microgram units."""
        unit_const = units.MassUnits.microgram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def milligram(self):
        """Set value using milligram units."""
        unit_const = units.MassUnits.milligram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mg(self):
        """Set value using mg units (alias for milligram)."""
        return self.milligram
    
    @property
    def ounce_apothecary(self):
        """Set value using ounce (apothecary) units."""
        unit_const = units.MassUnits.ounce_apothecary
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ounce_avoirdupois(self):
        """Set value using ounce (avoirdupois) units."""
        unit_const = units.MassUnits.ounce_avoirdupois
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def oz(self):
        """Set value using oz units (alias for ounce (avoirdupois))."""
        return self.ounce_avoirdupois
    
    @property
    def ounce_troy(self):
        """Set value using ounce (troy) units."""
        unit_const = units.MassUnits.ounce_troy
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pennyweight_troy(self):
        """Set value using pennyweight (troy) units."""
        unit_const = units.MassUnits.pennyweight_troy
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pood_Russia(self):
        """Set value using pood, (Russia) units."""
        unit_const = units.MassUnits.pood_Russia
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pood(self):
        """Set value using pood units (alias for pood, (Russia))."""
        return self.pood_Russia
    
    @property
    def pound_apothecary(self):
        """Set value using pound (apothecary) units."""
        unit_const = units.MassUnits.pound_apothecary
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_avoirdupois(self):
        """Set value using pound (avoirdupois) units."""
        unit_const = units.MassUnits.pound_avoirdupois
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_troy(self):
        """Set value using pound (troy) units."""
        unit_const = units.MassUnits.pound_troy
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mass(self):
        """Set value using pound mass units."""
        unit_const = units.MassUnits.pound_mass
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def quarter_UK(self):
        """Set value using quarter (UK) units."""
        unit_const = units.MassUnits.quarter_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def qt(self):
        """Set value using qt units (alias for quarter (UK))."""
        return self.quarter_UK
    
    @property
    def quintal_metric(self):
        """Set value using quintal, metric units."""
        unit_const = units.MassUnits.quintal_metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def quital_US(self):
        """Set value using quital, US units."""
        unit_const = units.MassUnits.quital_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def scruple_avoirdupois(self):
        """Set value using scruple (avoirdupois) units."""
        unit_const = units.MassUnits.scruple_avoirdupois
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def scf(self):
        """Set value using scf units (alias for scruple (avoirdupois))."""
        return self.scruple_avoirdupois
    
    @property
    def stone_UK(self):
        """Set value using stone (UK) units."""
        unit_const = units.MassUnits.stone_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def st(self):
        """Set value using st units (alias for stone (UK))."""
        return self.stone_UK
    
    @property
    def ton_metric(self):
        """Set value using ton, metric units."""
        unit_const = units.MassUnits.ton_metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def t(self):
        """Set value using t units (alias for ton, metric)."""
        return self.ton_metric
    
    @property
    def ton_US_long(self):
        """Set value using ton, US, long units."""
        unit_const = units.MassUnits.ton_US_long
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_US_short(self):
        """Set value using ton, US, short units."""
        unit_const = units.MassUnits.ton_US_short
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MassDensitySetter(TypeSafeSetter):
    """MassDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_cubic_centimeter(self):
        """Set value using gram per cubic centimeter units."""
        unit_const = units.MassDensityUnits.gram_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_cc(self):
        """Set value using g/cc units (alias for gram per cubic centimeter)."""
        return self.gram_per_cubic_centimeter
    
    @property
    def g_ml(self):
        """Set value using g/ml units (alias for gram per cubic centimeter)."""
        return self.gram_per_cubic_centimeter
    
    @property
    def gram_per_cubic_decimeter(self):
        """Set value using gram per cubic decimeter units."""
        unit_const = units.MassDensityUnits.gram_per_cubic_decimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_per_cubic_meter(self):
        """Set value using gram per cubic meter units."""
        unit_const = units.MassDensityUnits.gram_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_per_liter(self):
        """Set value using gram per liter units."""
        unit_const = units.MassDensityUnits.gram_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_l(self):
        """Set value using g / l units (alias for gram per liter)."""
        return self.gram_per_liter
    
    @property
    def g_L(self):
        """Set value using g/L units (alias for gram per liter)."""
        return self.gram_per_liter
    
    @property
    def kilogram_per_cubic_meter(self):
        """Set value using kilogram per cubic meter units."""
        unit_const = units.MassDensityUnits.kilogram_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ounce_avdp_per_US_gallon(self):
        """Set value using ounce (avdp) per US gallon units."""
        unit_const = units.MassDensityUnits.ounce_avdp_per_US_gallon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_avdp_per_cubic_foot(self):
        """Set value using pound (avdp) per cubic foot units."""
        unit_const = units.MassDensityUnits.pound_avdp_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_cu_ft(self):
        """Set value using lb / cu ft units (alias for pound (avdp) per cubic foot)."""
        return self.pound_avdp_per_cubic_foot
    
    @property
    def lb_ft_power_3(self):
        """Set value using lb/ft { ^{3 units (alias for pound (avdp) per cubic foot)."""
        return self.pound_avdp_per_cubic_foot
    
    @property
    def pound_avdp_per_US_gallon(self):
        """Set value using pound (avdp) per US gallon units."""
        unit_const = units.MassDensityUnits.pound_avdp_per_US_gallon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mass_per_cubic_inch(self):
        """Set value using pound (mass) per cubic inch units."""
        unit_const = units.MassDensityUnits.pound_mass_per_cubic_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_cu_in(self):
        """Set value using lb / cu in units (alias for pound (mass) per cubic inch)."""
        return self.pound_mass_per_cubic_inch
    
    @property
    def lb_in_power_3(self):
        """Set value using lb / in^{3 units (alias for pound (mass) per cubic inch)."""
        return self.pound_mass_per_cubic_inch
    
    @property
    def ton_metric_per_cubic_meter(self):
        """Set value using ton (metric) per cubic meter units."""
        unit_const = units.MassDensityUnits.ton_metric_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def t_m_power_3(self):
        """Set value using t / m^{3 units (alias for ton (metric) per cubic meter)."""
        return self.ton_metric_per_cubic_meter
    
    @property
    def MT_m_power_3(self):
        """Set value using MT / m^{3 units (alias for ton (metric) per cubic meter)."""
        return self.ton_metric_per_cubic_meter
    

class MassFlowRateSetter(TypeSafeSetter):
    """MassFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kilograms_per_day(self):
        """Set value using kilograms per day units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilograms_per_hour(self):
        """Set value using kilograms per hour units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilograms_per_minute(self):
        """Set value using kilograms per minute units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilograms_per_second(self):
        """Set value using kilograms per second units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def metric_tons_per_day(self):
        """Set value using metric tons per day units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT_d(self):
        """Set value using MT/d units (alias for metric tons per day)."""
        return self.metric_tons_per_day
    
    @property
    def MTD(self):
        """Set value using MTD units (alias for metric tons per day)."""
        return self.metric_tons_per_day
    
    @property
    def metric_tons_per_hour(self):
        """Set value using metric tons per hour units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT_h(self):
        """Set value using MT/h units (alias for metric tons per hour)."""
        return self.metric_tons_per_hour
    
    @property
    def metric_tons_per_minute(self):
        """Set value using metric tons per minute units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def metric_tons_per_second(self):
        """Set value using metric tons per second units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def metric_tons_per_year_365_d(self):
        """Set value using metric tons per year (365 d) units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_year_365_d
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT_yr(self):
        """Set value using MT/yr units (alias for metric tons per year (365 d))."""
        return self.metric_tons_per_year_365_d
    
    @property
    def MTY(self):
        """Set value using MTY units (alias for metric tons per year (365 d))."""
        return self.metric_tons_per_year_365_d
    
    @property
    def pounds_per_day(self):
        """Set value using pounds per day units."""
        unit_const = units.MassFlowRateUnits.pounds_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_d(self):
        """Set value using lb / d units (alias for pounds per day)."""
        return self.pounds_per_day
    
    @property
    def lb_da(self):
        """Set value using lb / da units (alias for pounds per day)."""
        return self.pounds_per_day
    
    @property
    def PPD(self):
        """Set value using PPD units (alias for pounds per day)."""
        return self.pounds_per_day
    
    @property
    def pounds_per_hour(self):
        """Set value using pounds per hour units."""
        unit_const = units.MassFlowRateUnits.pounds_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_h(self):
        """Set value using lb / h units (alias for pounds per hour)."""
        return self.pounds_per_hour
    
    @property
    def lb_hr(self):
        """Set value using lb/hr units (alias for pounds per hour)."""
        return self.pounds_per_hour
    
    @property
    def PPH(self):
        """Set value using PPH units (alias for pounds per hour)."""
        return self.pounds_per_hour
    
    @property
    def pounds_per_minute(self):
        """Set value using pounds per minute units."""
        unit_const = units.MassFlowRateUnits.pounds_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_min(self):
        """Set value using lb / min units (alias for pounds per minute)."""
        return self.pounds_per_minute
    
    @property
    def PPM(self):
        """Set value using PPM units (alias for pounds per minute)."""
        return self.pounds_per_minute
    
    @property
    def pounds_per_second(self):
        """Set value using pounds per second units."""
        unit_const = units.MassFlowRateUnits.pounds_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_s(self):
        """Set value using lb / s units (alias for pounds per second)."""
        return self.pounds_per_second
    
    @property
    def lb_sec(self):
        """Set value using lb/sec units (alias for pounds per second)."""
        return self.pounds_per_second
    
    @property
    def PPS(self):
        """Set value using PPS units (alias for pounds per second)."""
        return self.pounds_per_second
    

class MassFluxSetter(TypeSafeSetter):
    """MassFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kilogram_per_square_meter_per_day(self):
        """Set value using kilogram per square meter per day units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_square_meter_per_hour(self):
        """Set value using kilogram per square meter per hour units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_square_meter_per_minute(self):
        """Set value using kilogram per square meter per minute units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_square_meter_per_second(self):
        """Set value using kilogram per square meter per second units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_per_square_foot_per_day(self):
        """Set value using pound per square foot per day units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_left_ft_power_2_tilde_dright(self):
        """Set value using lb /left(ft^{2 ~dright) units (alias for pound per square foot per day)."""
        return self.pound_per_square_foot_per_day
    
    @property
    def lb_sqft_da(self):
        """Set value using lb/sqft/ da units (alias for pound per square foot per day)."""
        return self.pound_per_square_foot_per_day
    
    @property
    def pound_per_square_foot_per_hour(self):
        """Set value using pound per square foot per hour units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_left_ft_power_2_tilde_hright(self):
        """Set value using lb /left(ft^{2 ~hright) units (alias for pound per square foot per hour)."""
        return self.pound_per_square_foot_per_hour
    
    @property
    def lb_sqft_hr(self):
        """Set value using lb/sqft/ hr units (alias for pound per square foot per hour)."""
        return self.pound_per_square_foot_per_hour
    
    @property
    def pound_per_square_foot_per_minute(self):
        """Set value using pound per square foot per minute units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_left_ft_power_2_min_right(self):
        """Set value using lb /left(ft^{2 min right) units (alias for pound per square foot per minute)."""
        return self.pound_per_square_foot_per_minute
    
    @property
    def lb_sqft_min(self):
        """Set value using lb/ sqft/min units (alias for pound per square foot per minute)."""
        return self.pound_per_square_foot_per_minute
    
    @property
    def pound_per_square_foot_per_second(self):
        """Set value using pound per square foot per second units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_left_ft_power_2_tilde_sright(self):
        """Set value using lb /left(ft^{2 ~sright) units (alias for pound per square foot per second)."""
        return self.pound_per_square_foot_per_second
    
    @property
    def lb_sqft_sec(self):
        """Set value using lb/sqft/ sec units (alias for pound per square foot per second)."""
        return self.pound_per_square_foot_per_second
    

class MassFractionOfISetter(TypeSafeSetter):
    """MassFractionOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def grains_of_i_per_pound_total(self):
        """Set value using grains of "i" per pound total units."""
        unit_const = units.MassFractionOfIUnits.grains_of_i_per_pound_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_of_i_per_kilogram_total(self):
        """Set value using gram of "i" per kilogram total units."""
        unit_const = units.MassFractionOfIUnits.gram_of_i_per_kilogram_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_of_i_per_kilogram_total(self):
        """Set value using kilogram of "i" per kilogram total units."""
        unit_const = units.MassFractionOfIUnits.kilogram_of_i_per_kilogram_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_of_i_per_pound_total(self):
        """Set value using pound of "i" per pound total units."""
        unit_const = units.MassFractionOfIUnits.pound_of_i_per_pound_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MassTransferCoefficientSetter(TypeSafeSetter):
    """MassTransferCoefficient-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_square_centimeter_per_second(self):
        """Set value using gram per square centimeter per second units."""
        unit_const = units.MassTransferCoefficientUnits.gram_per_square_centimeter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_square_meter_per_second(self):
        """Set value using kilogram per square meter per second units."""
        unit_const = units.MassTransferCoefficientUnits.kilogram_per_square_meter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pounds_force_per_cubic_foot_per_hour(self):
        """Set value using pounds force per cubic foot per hour units."""
        unit_const = units.MassTransferCoefficientUnits.pounds_force_per_cubic_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_f_ft_power_3_h(self):
        """Set value using lb_{f / ft^{3 / h units (alias for pounds force per cubic foot per hour)."""
        return self.pounds_force_per_cubic_foot_per_hour
    
    @property
    def lb_f_cft_hr(self):
        """Set value using lb_{f / cft / hr units (alias for pounds force per cubic foot per hour)."""
        return self.pounds_force_per_cubic_foot_per_hour
    
    @property
    def pounds_mass_per_square_foot_per_hour(self):
        """Set value using pounds mass per square foot per hour units."""
        unit_const = units.MassTransferCoefficientUnits.pounds_mass_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft_power_2_hr(self):
        """Set value using lb/(ft { ^{2 hr ) units (alias for pounds mass per square foot per hour)."""
        return self.pounds_mass_per_square_foot_per_hour
    
    @property
    def lb_sqft_hr(self):
        """Set value using lb/sqft/ hr units (alias for pounds mass per square foot per hour)."""
        return self.pounds_mass_per_square_foot_per_hour
    
    @property
    def pounds_mass_per_square_foot_per_second(self):
        """Set value using pounds mass per square foot per second units."""
        unit_const = units.MassTransferCoefficientUnits.pounds_mass_per_square_foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_left_ft_power_2_tilde_sright(self):
        """Set value using lb /left(ft^{2 ~sright) units (alias for pounds mass per square foot per second)."""
        return self.pounds_mass_per_square_foot_per_second
    
    @property
    def lb_sqft_sec(self):
        """Set value using lb/sqft/ sec units (alias for pounds mass per square foot per second)."""
        return self.pounds_mass_per_square_foot_per_second
    

class MolalityOfSoluteISetter(TypeSafeSetter):
    """MolalityOfSoluteI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_moles_of_i_per_kilogram(self):
        """Set value using gram moles of "i" per kilogram units."""
        unit_const = units.MolalityOfSoluteIUnits.gram_moles_of_i_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_mols_of_i_per_kilogram(self):
        """Set value using kilogram mols of "i" per kilogram units."""
        unit_const = units.MolalityOfSoluteIUnits.kilogram_mols_of_i_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmols_of_i_per_kilogram(self):
        """Set value using kmols of "i" per kilogram units."""
        unit_const = units.MolalityOfSoluteIUnits.kmols_of_i_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mols_of_i_per_gram(self):
        """Set value using mols of "i" per gram units."""
        unit_const = units.MolalityOfSoluteIUnits.mols_of_i_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_moles_of_i_per_pound_mass(self):
        """Set value using pound moles of "i" per pound mass units."""
        unit_const = units.MolalityOfSoluteIUnits.pound_moles_of_i_per_pound_mass
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MolarConcentrationByMassSetter(TypeSafeSetter):
    """MolarConcentrationByMass-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_mole_or_mole_per_gram(self):
        """Set value using gram mole or mole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.gram_mole_or_mole_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_mole_or_mole_per_kilogram(self):
        """Set value using gram mole or mole per kilogram units."""
        unit_const = units.MolarConcentrationByMassUnits.gram_mole_or_mole_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_mole_or_kmol_per_kilogram(self):
        """Set value using kilogram mole or kmol per kilogram units."""
        unit_const = units.MolarConcentrationByMassUnits.kilogram_mole_or_kmol_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def micromole_per_gram(self):
        """Set value using micromole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.micromole_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millimole_per_gram(self):
        """Set value using millimole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.millimole_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def picomole_per_gram(self):
        """Set value using picomole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.picomole_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mole_per_pound(self):
        """Set value using pound mole per pound units."""
        unit_const = units.MolarConcentrationByMassUnits.pound_mole_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_lb(self):
        """Set value using lb-mol / lb units (alias for pound mole per pound)."""
        return self.pound_mole_per_pound
    
    @property
    def mole_lb(self):
        """Set value using mole/lb units (alias for pound mole per pound)."""
        return self.pound_mole_per_pound
    

class MolarFlowRateSetter(TypeSafeSetter):
    """MolarFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_mole_per_day(self):
        """Set value using gram mole per day units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_mole_per_hour(self):
        """Set value using gram mole per hour units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_mole_per_minute(self):
        """Set value using gram mole per minute units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_mole_per_second(self):
        """Set value using gram mole per second units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_mole_or_kmol_per_day(self):
        """Set value using kilogram mole or kmol per day units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_mole_or_kmol_per_hour(self):
        """Set value using kilogram mole or kmol per hour units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_mole_or_kmol_per_minute(self):
        """Set value using kilogram mole or kmol per minute units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_mole_or_kmol_per_second(self):
        """Set value using kilogram mole or kmol per second units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mole_or_lb_mol_per_day(self):
        """Set value using pound mole or lb-mol per day units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_d(self):
        """Set value using lb-mol/d units (alias for pound mole or lb-mol per day)."""
        return self.pound_mole_or_lb_mol_per_day
    
    @property
    def mole_da(self):
        """Set value using mole/da units (alias for pound mole or lb-mol per day)."""
        return self.pound_mole_or_lb_mol_per_day
    
    @property
    def pound_mole_or_lb_mol_per_hour(self):
        """Set value using pound mole or lb-mol per hour units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_h(self):
        """Set value using lb-mol/h units (alias for pound mole or lb-mol per hour)."""
        return self.pound_mole_or_lb_mol_per_hour
    
    @property
    def mole_hr(self):
        """Set value using mole/hr units (alias for pound mole or lb-mol per hour)."""
        return self.pound_mole_or_lb_mol_per_hour
    
    @property
    def pound_mole_or_lb_mol_per_minute(self):
        """Set value using pound mole or lb-mol per minute units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_min(self):
        """Set value using lb-mol/min units (alias for pound mole or lb-mol per minute)."""
        return self.pound_mole_or_lb_mol_per_minute
    
    @property
    def mole_min(self):
        """Set value using mole/ min units (alias for pound mole or lb-mol per minute)."""
        return self.pound_mole_or_lb_mol_per_minute
    
    @property
    def pound_mole_or_lb_mol_per_second(self):
        """Set value using pound mole or lb-mol per second units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_s(self):
        """Set value using lb-mol / s units (alias for pound mole or lb-mol per second)."""
        return self.pound_mole_or_lb_mol_per_second
    
    @property
    def mole_sec(self):
        """Set value using mole/sec units (alias for pound mole or lb-mol per second)."""
        return self.pound_mole_or_lb_mol_per_second
    

class MolarFluxSetter(TypeSafeSetter):
    """MolarFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kmol_per_square_meter_per_day(self):
        """Set value using kmol per square meter per day units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_per_square_meter_per_hour(self):
        """Set value using kmol per square meter per hour units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_per_square_meter_per_minute(self):
        """Set value using kmol per square meter per minute units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_per_square_meter_per_second(self):
        """Set value using kmol per square meter per second units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mole_per_square_foot_per_day(self):
        """Set value using pound mole per square foot per day units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_left_ft_power_2_tilde_dright(self):
        """Set value using lb-mol /left(ft^{2 ~dright) units (alias for pound mole per square foot per day)."""
        return self.pound_mole_per_square_foot_per_day
    
    @property
    def mole_sqft_da(self):
        """Set value using mole/sqft/da units (alias for pound mole per square foot per day)."""
        return self.pound_mole_per_square_foot_per_day
    
    @property
    def pound_mole_per_square_foot_per_hour(self):
        """Set value using pound mole per square foot per hour units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_left_ft_power_2_tilde_hright(self):
        """Set value using lb-mol /left(ft^{2 ~hright) units (alias for pound mole per square foot per hour)."""
        return self.pound_mole_per_square_foot_per_hour
    
    @property
    def mole_sqft_hr(self):
        """Set value using mole/sqft/hr units (alias for pound mole per square foot per hour)."""
        return self.pound_mole_per_square_foot_per_hour
    
    @property
    def pound_mole_per_square_foot_per_minute(self):
        """Set value using pound mole per square foot per minute units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_left_ft_power_2_tilde_minright(self):
        """Set value using lb-mol /left(ft^{2 ~minright) units (alias for pound mole per square foot per minute)."""
        return self.pound_mole_per_square_foot_per_minute
    
    @property
    def mole_sqft_min(self):
        """Set value using mole/sqft/min units (alias for pound mole per square foot per minute)."""
        return self.pound_mole_per_square_foot_per_minute
    
    @property
    def pound_mole_per_square_foot_per_second(self):
        """Set value using pound mole per square foot per second units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_left_ft_power_2_tilde_sright(self):
        """Set value using lb-mol /left(ft^{2 ~sright) units (alias for pound mole per square foot per second)."""
        return self.pound_mole_per_square_foot_per_second
    
    @property
    def mole_sqft_sec(self):
        """Set value using mole/sqft/sec units (alias for pound mole per square foot per second)."""
        return self.pound_mole_per_square_foot_per_second
    

class MolarHeatCapacitySetter(TypeSafeSetter):
    """MolarHeatCapacity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Btu_per_pound_mole_per_degree_Fahrenheit_or_degree_Rankine(self):
        """Set value using Btu per pound mole per degree Fahrenheit (or degree Rankine) units."""
        unit_const = units.MolarHeatCapacityUnits.Btu_per_pound_mole_per_degree_Fahrenheit_or_degree_Rankine
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calories_per_gram_mole_per_kelvin_or_degree_Celsius(self):
        """Set value using calories per gram mole per kelvin (or degree Celsius) units."""
        unit_const = units.MolarHeatCapacityUnits.calories_per_gram_mole_per_kelvin_or_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_gram_mole_per_kelvin_or_degree_Celsius(self):
        """Set value using joule per gram mole per kelvin (or degree Celsius) units."""
        unit_const = units.MolarHeatCapacityUnits.joule_per_gram_mole_per_kelvin_or_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MolarityOfISetter(TypeSafeSetter):
    """MolarityOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_moles_of_i_per_cubic_meter(self):
        """Set value using gram moles of "i" per cubic meter units."""
        unit_const = units.MolarityOfIUnits.gram_moles_of_i_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol_i_m_power_3(self):
        """Set value using mol_{i / m^{3 units (alias for gram moles of "i" per cubic meter)."""
        return self.gram_moles_of_i_per_cubic_meter
    
    @property
    def c_i(self):
        """Set value using c_{i units (alias for gram moles of "i" per cubic meter)."""
        return self.gram_moles_of_i_per_cubic_meter
    
    @property
    def gram_moles_of_i_per_liter(self):
        """Set value using gram moles of "i" per liter units."""
        unit_const = units.MolarityOfIUnits.gram_moles_of_i_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_moles_of_i_per_cubic_meter(self):
        """Set value using kilogram moles of "i" per cubic meter units."""
        unit_const = units.MolarityOfIUnits.kilogram_moles_of_i_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_moles_of_i_per_liter(self):
        """Set value using kilogram moles of "i" per liter units."""
        unit_const = units.MolarityOfIUnits.kilogram_moles_of_i_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_moles_of_i_per_cubic_foot(self):
        """Set value using pound moles of "i" per cubic foot units."""
        unit_const = units.MolarityOfIUnits.pound_moles_of_i_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_i_ft_power_3(self):
        """Set value using lb mol_{i / ft^{3 units (alias for pound moles of "i" per cubic foot)."""
        return self.pound_moles_of_i_per_cubic_foot
    
    @property
    def mole_i_cft(self):
        """Set value using mole_{i / cft units (alias for pound moles of "i" per cubic foot)."""
        return self.pound_moles_of_i_per_cubic_foot
    
    @property
    def pound_moles_of_i_per_gallon_US(self):
        """Set value using pound moles of " $i$ " per gallon (US) units."""
        unit_const = units.MolarityOfIUnits.pound_moles_of_i_per_gallon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_i_gal(self):
        """Set value using lb mol_{i / gal units (alias for pound moles of " $i$ " per gallon (US))."""
        return self.pound_moles_of_i_per_gallon_US
    
    @property
    def mole_i_gal(self):
        """Set value using mole_{i / gal units (alias for pound moles of " $i$ " per gallon (US))."""
        return self.pound_moles_of_i_per_gallon_US
    

class MoleFractionOfISetter(TypeSafeSetter):
    """MoleFractionOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_mole_of_i_per_gram_mole_total(self):
        """Set value using gram mole of "i" per gram mole total units."""
        unit_const = units.MoleFractionOfIUnits.gram_mole_of_i_per_gram_mole_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_mole_of_i_per_kilogram_mole_total(self):
        """Set value using kilogram mole of "i" per kilogram mole total units."""
        unit_const = units.MoleFractionOfIUnits.kilogram_mole_of_i_per_kilogram_mole_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilomole_of_i_per_kilomole_total(self):
        """Set value using kilomole of "i" per kilomole total units."""
        unit_const = units.MoleFractionOfIUnits.kilomole_of_i_per_kilomole_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mole_of_i_per_pound_mole_total(self):
        """Set value using pound mole of "i" per pound mole total units."""
        unit_const = units.MoleFractionOfIUnits.pound_mole_of_i_per_pound_mole_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MomentOfInertiaSetter(TypeSafeSetter):
    """MomentOfInertia-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_force_centimeter_square_second(self):
        """Set value using gram force centimeter square second units."""
        unit_const = units.MomentOfInertiaUnits.gram_force_centimeter_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_square_centimeter(self):
        """Set value using gram square centimeter units."""
        unit_const = units.MomentOfInertiaUnits.gram_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force_centimeter_square_second(self):
        """Set value using kilogram force centimeter square second units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_force_centimeter_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force_meter_square_second(self):
        """Set value using kilogram force meter square second units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_force_meter_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_square_centimeter(self):
        """Set value using kilogram square centimeter units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_square_meter(self):
        """Set value using kilogram square meter units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ounce_force_inch_square_second(self):
        """Set value using ounce force inch square second units."""
        unit_const = units.MomentOfInertiaUnits.ounce_force_inch_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ounce_mass_square_inch(self):
        """Set value using ounce mass square inch units."""
        unit_const = units.MomentOfInertiaUnits.ounce_mass_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mass_square_foot(self):
        """Set value using pound mass square foot units."""
        unit_const = units.MomentOfInertiaUnits.pound_mass_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft_power_2(self):
        """Set value using lb ft { ^{2 units (alias for pound mass square foot)."""
        return self.pound_mass_square_foot
    
    @property
    def lb_sq_ft(self):
        """Set value using lb sq ft units (alias for pound mass square foot)."""
        return self.pound_mass_square_foot
    
    @property
    def pound_mass_square_inch(self):
        """Set value using pound mass square inch units."""
        unit_const = units.MomentOfInertiaUnits.pound_mass_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MomentumFlowRateSetter(TypeSafeSetter):
    """MomentumFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_pounds_per_square_hour(self):
        """Set value using foot pounds per square hour units."""
        unit_const = units.MomentumFlowRateUnits.foot_pounds_per_square_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_lb_h_power_2(self):
        """Set value using ft lb / h^{2 units (alias for foot pounds per square hour)."""
        return self.foot_pounds_per_square_hour
    
    @property
    def ft_lb_hr_power_2(self):
        """Set value using ft lb / hr^{2 units (alias for foot pounds per square hour)."""
        return self.foot_pounds_per_square_hour
    
    @property
    def foot_pounds_per_square_minute(self):
        """Set value using foot pounds per square minute units."""
        unit_const = units.MomentumFlowRateUnits.foot_pounds_per_square_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pounds_per_square_second(self):
        """Set value using foot pounds per square second units."""
        unit_const = units.MomentumFlowRateUnits.foot_pounds_per_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_lb_s_power_2(self):
        """Set value using ft lb / s^{2 units (alias for foot pounds per square second)."""
        return self.foot_pounds_per_square_second
    
    @property
    def ft_lb_sec_power_2(self):
        """Set value using ft lb/sec { ^{2 units (alias for foot pounds per square second)."""
        return self.foot_pounds_per_square_second
    
    @property
    def gram_centimeters_per_square_second(self):
        """Set value using gram centimeters per square second units."""
        unit_const = units.MomentumFlowRateUnits.gram_centimeters_per_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_meters_per_square_second(self):
        """Set value using kilogram meters per square second units."""
        unit_const = units.MomentumFlowRateUnits.kilogram_meters_per_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class MomentumFluxSetter(TypeSafeSetter):
    """MomentumFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_square_centimeter(self):
        """Set value using dyne per square centimeter units."""
        unit_const = units.MomentumFluxUnits.dyne_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_per_centimeter_per_square_second(self):
        """Set value using gram per centimeter per square second units."""
        unit_const = units.MomentumFluxUnits.gram_per_centimeter_per_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_per_square_meter(self):
        """Set value using newton per square meter units."""
        unit_const = units.MomentumFluxUnits.newton_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_force_per_square_foot(self):
        """Set value using pound force per square foot units."""
        unit_const = units.MomentumFluxUnits.pound_force_per_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mass_per_foot_per_square_second(self):
        """Set value using pound mass per foot per square second units."""
        unit_const = units.MomentumFluxUnits.pound_mass_per_foot_per_square_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_m_ft_s_power_2(self):
        """Set value using lb_{m / ft / s^{2 units (alias for pound mass per foot per square second)."""
        return self.pound_mass_per_foot_per_square_second
    
    @property
    def lb_ft_sec_power_2(self):
        """Set value using lb / ft / sec^{2 units (alias for pound mass per foot per square second)."""
        return self.pound_mass_per_foot_per_square_second
    

class NormalityOfSolutionSetter(TypeSafeSetter):
    """NormalityOfSolution-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_equivalents_per_cubic_meter(self):
        """Set value using gram equivalents per cubic meter units."""
        unit_const = units.NormalityOfSolutionUnits.gram_equivalents_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_equivalents_per_liter(self):
        """Set value using gram equivalents per liter units."""
        unit_const = units.NormalityOfSolutionUnits.gram_equivalents_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_equivalents_per_cubic_foot(self):
        """Set value using pound equivalents per cubic foot units."""
        unit_const = units.NormalityOfSolutionUnits.pound_equivalents_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_eq_ft_power_3(self):
        """Set value using lb eq / ft^{3 units (alias for pound equivalents per cubic foot)."""
        return self.pound_equivalents_per_cubic_foot
    
    @property
    def lb_eq_cft(self):
        """Set value using lb eq/cft units (alias for pound equivalents per cubic foot)."""
        return self.pound_equivalents_per_cubic_foot
    
    @property
    def pound_equivalents_per_gallon(self):
        """Set value using pound equivalents per gallon units."""
        unit_const = units.NormalityOfSolutionUnits.pound_equivalents_per_gallon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ParticleDensitySetter(TypeSafeSetter):
    """ParticleDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def particles_per_cubic_centimeter(self):
        """Set value using particles per cubic centimeter units."""
        unit_const = units.ParticleDensityUnits.particles_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_cm_power_3(self):
        """Set value using part/cm { ^{3 units (alias for particles per cubic centimeter)."""
        return self.particles_per_cubic_centimeter
    
    @property
    def part_cc(self):
        """Set value using part/cc units (alias for particles per cubic centimeter)."""
        return self.particles_per_cubic_centimeter
    
    @property
    def particles_per_cubic_foot(self):
        """Set value using particles per cubic foot units."""
        unit_const = units.ParticleDensityUnits.particles_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_ft_power_3(self):
        """Set value using part/ ft^{3 units (alias for particles per cubic foot)."""
        return self.particles_per_cubic_foot
    
    @property
    def part_cft(self):
        """Set value using part/cft units (alias for particles per cubic foot)."""
        return self.particles_per_cubic_foot
    
    @property
    def particles_per_cubic_meter(self):
        """Set value using particles per cubic meter units."""
        unit_const = units.ParticleDensityUnits.particles_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def particles_per_gallon_US(self):
        """Set value using particles per gallon (US) units."""
        unit_const = units.ParticleDensityUnits.particles_per_gallon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def particles_per_liter(self):
        """Set value using particles per liter units."""
        unit_const = units.ParticleDensityUnits.particles_per_liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def particles_per_milliliter(self):
        """Set value using particles per milliliter units."""
        unit_const = units.ParticleDensityUnits.particles_per_milliliter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class PercentSetter(TypeSafeSetter):
    """Percent-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def percent(self):
        """Set value using percent units."""
        unit_const = units.PercentUnits.percent
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def per_mille(self):
        """Set value using per mille units."""
        unit_const = units.PercentUnits.per_mille
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def basis_point(self):
        """Set value using basis point units."""
        unit_const = units.PercentUnits.basis_point
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def bp(self):
        """Set value using bp units (alias for basis point)."""
        return self.basis_point
    
    @property
    def bps(self):
        """Set value using bps units (alias for basis point)."""
        return self.basis_point
    

class PermeabilitySetter(TypeSafeSetter):
    """Permeability-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def darcy(self):
        """Set value using darcy units."""
        unit_const = units.PermeabilityUnits.darcy
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_feet(self):
        """Set value using square feet units."""
        unit_const = units.PermeabilityUnits.square_feet
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_2(self):
        """Set value using ft^{2 units (alias for square feet)."""
        return self.square_feet
    
    @property
    def sq_ft(self):
        """Set value using sq ft units (alias for square feet)."""
        return self.square_feet
    
    @property
    def square_meters(self):
        """Set value using square meters units."""
        unit_const = units.PermeabilityUnits.square_meters
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class PhotonEmissionRateSetter(TypeSafeSetter):
    """PhotonEmissionRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def rayleigh(self):
        """Set value using rayleigh units."""
        unit_const = units.PhotonEmissionRateUnits.rayleigh
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def R(self):
        """Set value using R units (alias for rayleigh)."""
        return self.rayleigh
    
    @property
    def reciprocal_square_meter_second(self):
        """Set value using reciprocal square meter second units."""
        unit_const = units.PhotonEmissionRateUnits.reciprocal_square_meter_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class PowerPerUnitMassSetter(TypeSafeSetter):
    """PowerPerUnitMass-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_per_hour_per_pound_mass(self):
        """Set value using British thermal unit per hour per pound mass units."""
        unit_const = units.PowerPerUnitMassUnits.British_thermal_unit_per_hour_per_pound_mass
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_h_lb(self):
        """Set value using Btu/h/lb units (alias for British thermal unit per hour per pound mass)."""
        return self.British_thermal_unit_per_hour_per_pound_mass
    
    @property
    def Btu_lb_hr(self):
        """Set value using Btu/ (lb hr) units (alias for British thermal unit per hour per pound mass)."""
        return self.British_thermal_unit_per_hour_per_pound_mass
    
    @property
    def calorie_per_second_per_gram(self):
        """Set value using calorie per second per gram units."""
        unit_const = units.PowerPerUnitMassUnits.calorie_per_second_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_s_g(self):
        """Set value using cal/s/g units (alias for calorie per second per gram)."""
        return self.calorie_per_second_per_gram
    
    @property
    def cal_g_sec(self):
        """Set value using cal/(g sec) units (alias for calorie per second per gram)."""
        return self.calorie_per_second_per_gram
    
    @property
    def kilocalorie_per_hour_per_kilogram(self):
        """Set value using kilocalorie per hour per kilogram units."""
        unit_const = units.PowerPerUnitMassUnits.kilocalorie_per_hour_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_h_kg(self):
        """Set value using kcal/h/kg units (alias for kilocalorie per hour per kilogram)."""
        return self.kilocalorie_per_hour_per_kilogram
    
    @property
    def kcal_kg_hr(self):
        """Set value using kcal/ (kg hr) units (alias for kilocalorie per hour per kilogram)."""
        return self.kilocalorie_per_hour_per_kilogram
    
    @property
    def watt_per_kilogram(self):
        """Set value using watt per kilogram units."""
        unit_const = units.PowerPerUnitMassUnits.watt_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class PowerPerUnitVolumeSetter(TypeSafeSetter):
    """PowerPerUnitVolume-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_per_hour_per_cubic_foot(self):
        """Set value using British thermal unit per hour per cubic foot units."""
        unit_const = units.PowerPerUnitVolumeUnits.British_thermal_unit_per_hour_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_h_ft_power_3(self):
        """Set value using Btu / h / ft^{3 units (alias for British thermal unit per hour per cubic foot)."""
        return self.British_thermal_unit_per_hour_per_cubic_foot
    
    @property
    def Btu_hr_cft(self):
        """Set value using Btu / hr / cft units (alias for British thermal unit per hour per cubic foot)."""
        return self.British_thermal_unit_per_hour_per_cubic_foot
    
    @property
    def calorie_per_second_per_cubic_centimeter(self):
        """Set value using calorie per second per cubic centimeter units."""
        unit_const = units.PowerPerUnitVolumeUnits.calorie_per_second_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_s_cm_power_3(self):
        """Set value using cal / s / cm^{3 units (alias for calorie per second per cubic centimeter)."""
        return self.calorie_per_second_per_cubic_centimeter
    
    @property
    def cal_s_cc(self):
        """Set value using cal / s / cc units (alias for calorie per second per cubic centimeter)."""
        return self.calorie_per_second_per_cubic_centimeter
    
    @property
    def Chu_per_hour_per_cubic_foot(self):
        """Set value using Chu per hour per cubic foot units."""
        unit_const = units.PowerPerUnitVolumeUnits.Chu_per_hour_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_h_ft3(self):
        """Set value using Chu/h/ft3 units (alias for Chu per hour per cubic foot)."""
        return self.Chu_per_hour_per_cubic_foot
    
    @property
    def Chu_hr_cft(self):
        """Set value using Chu/hr/ cft units (alias for Chu per hour per cubic foot)."""
        return self.Chu_per_hour_per_cubic_foot
    
    @property
    def kilocalorie_per_hour_per_cubic_centimeter(self):
        """Set value using kilocalorie per hour per cubic centimeter units."""
        unit_const = units.PowerPerUnitVolumeUnits.kilocalorie_per_hour_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_h_cm_power_3(self):
        """Set value using kcal / h / cm^{3 units (alias for kilocalorie per hour per cubic centimeter)."""
        return self.kilocalorie_per_hour_per_cubic_centimeter
    
    @property
    def kcal_hr_cc(self):
        """Set value using kcal / hr/cc units (alias for kilocalorie per hour per cubic centimeter)."""
        return self.kilocalorie_per_hour_per_cubic_centimeter
    
    @property
    def kilocalorie_per_hour_per_cubic_foot(self):
        """Set value using kilocalorie per hour per cubic foot units."""
        unit_const = units.PowerPerUnitVolumeUnits.kilocalorie_per_hour_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_h_ft_power_3(self):
        """Set value using kcal / h / ft^{3 units (alias for kilocalorie per hour per cubic foot)."""
        return self.kilocalorie_per_hour_per_cubic_foot
    
    @property
    def kcal_hr_cft(self):
        """Set value using kcal / hr / cft units (alias for kilocalorie per hour per cubic foot)."""
        return self.kilocalorie_per_hour_per_cubic_foot
    
    @property
    def kilocalorie_per_second_per_cubic_centimeter(self):
        """Set value using kilocalorie per second per cubic centimeter units."""
        unit_const = units.PowerPerUnitVolumeUnits.kilocalorie_per_second_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_s_cm_power_3(self):
        """Set value using kcal/s/cm { ^{3 units (alias for kilocalorie per second per cubic centimeter)."""
        return self.kilocalorie_per_second_per_cubic_centimeter
    
    @property
    def kcal_s_cc(self):
        """Set value using kcal/s/ cc units (alias for kilocalorie per second per cubic centimeter)."""
        return self.kilocalorie_per_second_per_cubic_centimeter
    
    @property
    def watt_per_cubic_meter(self):
        """Set value using watt per cubic meter units."""
        unit_const = units.PowerPerUnitVolumeUnits.watt_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class PowerThermalDutySetter(TypeSafeSetter):
    """PowerThermalDuty-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abwatt_emu_of_power(self):
        """Set value using abwatt (emu of power) units."""
        unit_const = units.PowerThermalDutyUnits.abwatt_emu_of_power
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu(self):
        """Set value using emu units (alias for abwatt (emu of power))."""
        return self.abwatt_emu_of_power
    
    @property
    def boiler_horsepower(self):
        """Set value using boiler horsepower units."""
        unit_const = units.PowerThermalDutyUnits.boiler_horsepower
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_mean_per_hour(self):
        """Set value using British thermal unit (mean) per hour units."""
        unit_const = units.PowerThermalDutyUnits.British_thermal_unit_mean_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_mean_hr(self):
        """Set value using Btu (mean)/hr units (alias for British thermal unit (mean) per hour)."""
        return self.British_thermal_unit_mean_per_hour
    
    @property
    def Btu_hr(self):
        """Set value using Btu/hr units (alias for British thermal unit (mean) per hour)."""
        return self.British_thermal_unit_mean_per_hour
    
    @property
    def British_thermal_unit_mean_per_minute(self):
        """Set value using British thermal unit (mean) per minute units."""
        unit_const = units.PowerThermalDutyUnits.British_thermal_unit_mean_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_min(self):
        """Set value using Btu/min units (alias for British thermal unit (mean) per minute)."""
        return self.British_thermal_unit_mean_per_minute
    
    @property
    def Btu_mean_min(self):
        """Set value using Btu (mean)/min units (alias for British thermal unit (mean) per minute)."""
        return self.British_thermal_unit_mean_per_minute
    
    @property
    def British_thermal_unit_thermochemical_per_hour(self):
        """Set value using British thermal unit (thermochemical) per hour units."""
        unit_const = units.PowerThermalDutyUnits.British_thermal_unit_thermochemical_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_therm_hr(self):
        """Set value using Btu (therm)/hr units (alias for British thermal unit (thermochemical) per hour)."""
        return self.British_thermal_unit_thermochemical_per_hour
    
    @property
    def British_thermal_unit_thermochemical_per_minute(self):
        """Set value using British thermal unit (thermochemical) per minute units."""
        unit_const = units.PowerThermalDutyUnits.British_thermal_unit_thermochemical_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_therm_min(self):
        """Set value using Btu (therm)/min units (alias for British thermal unit (thermochemical) per minute)."""
        return self.British_thermal_unit_thermochemical_per_minute
    
    @property
    def calorie_mean_per_hour(self):
        """Set value using calorie (mean) per hour units."""
        unit_const = units.PowerThermalDutyUnits.calorie_mean_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_thermochemical_per_hour(self):
        """Set value using calorie (thermochemical) per hour units."""
        unit_const = units.PowerThermalDutyUnits.calorie_thermochemical_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def donkey(self):
        """Set value using donkey units."""
        unit_const = units.PowerThermalDutyUnits.donkey
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def erg_per_second(self):
        """Set value using erg per second units."""
        unit_const = units.PowerThermalDutyUnits.erg_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pondal_per_second(self):
        """Set value using foot pondal per second units."""
        unit_const = units.PowerThermalDutyUnits.foot_pondal_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pound_force_per_hour(self):
        """Set value using foot pound force per hour units."""
        unit_const = units.PowerThermalDutyUnits.foot_pound_force_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pound_force_per_minute(self):
        """Set value using foot pound force per minute units."""
        unit_const = units.PowerThermalDutyUnits.foot_pound_force_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pound_force_per_second(self):
        """Set value using foot pound force per second units."""
        unit_const = units.PowerThermalDutyUnits.foot_pound_force_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def horsepower_550_mathrm_ft_mathrm_lb_mathrm_f_mathrm_s(self):
        r"""Set value using horsepower ( $550 \mathrm{ft} \mathrm{lb}_{\mathrm{f}} / \mathrm{s}$ ) units."""
        unit_const = units.PowerThermalDutyUnits.horsepower_550_mathrm_ft_mathrm_lb_mathrm_f_mathrm_s
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def HP(self):
        r"""Set value using HP units (alias for horsepower ( $550 \mathrm{ft} \mathrm{lb}_{\mathrm{f}} / \mathrm{s}$ ))."""
        return self.horsepower_550_mathrm_ft_mathrm_lb_mathrm_f_mathrm_s
    
    @property
    def horsepower_electric(self):
        """Set value using horsepower (electric) units."""
        unit_const = units.PowerThermalDutyUnits.horsepower_electric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def horsepower_UK(self):
        """Set value using horsepower (UK) units."""
        unit_const = units.PowerThermalDutyUnits.horsepower_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_per_hour(self):
        """Set value using kcal per hour units."""
        unit_const = units.PowerThermalDutyUnits.kcal_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force_meter_per_second(self):
        """Set value using kilogram force meter per second units."""
        unit_const = units.PowerThermalDutyUnits.kilogram_force_meter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilowatt(self):
        """Set value using kilowatt units."""
        unit_const = units.PowerThermalDutyUnits.kilowatt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kW(self):
        """Set value using kW units (alias for kilowatt)."""
        return self.kilowatt
    
    @property
    def megawatt(self):
        """Set value using megawatt units."""
        unit_const = units.PowerThermalDutyUnits.megawatt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MW(self):
        """Set value using MW units (alias for megawatt)."""
        return self.megawatt
    
    @property
    def metric_horsepower(self):
        """Set value using metric horsepower units."""
        unit_const = units.PowerThermalDutyUnits.metric_horsepower
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def million_British_thermal_units_per_hour_petroleum(self):
        """Set value using million British thermal units per hour (petroleum) units."""
        unit_const = units.PowerThermalDutyUnits.million_British_thermal_units_per_hour_petroleum
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def million_kilocalorie_per_hour(self):
        """Set value using million kilocalorie per hour units."""
        unit_const = units.PowerThermalDutyUnits.million_kilocalorie_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def prony(self):
        """Set value using prony units."""
        unit_const = units.PowerThermalDutyUnits.prony
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_of_refrigeration_US(self):
        """Set value using ton of refrigeration (US) units."""
        unit_const = units.PowerThermalDutyUnits.ton_of_refrigeration_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_or_refrigeration_UK(self):
        """Set value using ton or refrigeration (UK) units."""
        unit_const = units.PowerThermalDutyUnits.ton_or_refrigeration_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def volt_ampere(self):
        """Set value using volt-ampere units."""
        unit_const = units.PowerThermalDutyUnits.volt_ampere
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def VA(self):
        """Set value using VA units (alias for volt-ampere)."""
        return self.volt_ampere
    
    @property
    def water_horsepower(self):
        """Set value using water horsepower units."""
        unit_const = units.PowerThermalDutyUnits.water_horsepower
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def watt(self):
        """Set value using watt units."""
        unit_const = units.PowerThermalDutyUnits.watt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def W(self):
        """Set value using W units (alias for watt)."""
        return self.watt
    
    @property
    def watt_international_mean(self):
        """Set value using watt (international, mean) units."""
        unit_const = units.PowerThermalDutyUnits.watt_international_mean
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def watt_international_US(self):
        """Set value using watt (international, US) units."""
        unit_const = units.PowerThermalDutyUnits.watt_international_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gigawatt(self):
        """Set value using gigawatt units."""
        unit_const = units.PowerThermalDutyUnits.gigawatt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def GW(self):
        """Set value using GW units (alias for gigawatt)."""
        return self.gigawatt
    
    @property
    def milliwatt(self):
        """Set value using milliwatt units."""
        unit_const = units.PowerThermalDutyUnits.milliwatt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mW(self):
        """Set value using mW units (alias for milliwatt)."""
        return self.milliwatt
    
    @property
    def microwatt(self):
        """Set value using microwatt units."""
        unit_const = units.PowerThermalDutyUnits.microwatt
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uW(self):
        """Set value using μW units (alias for microwatt)."""
        return self.microwatt
    

class PressureSetter(TypeSafeSetter):
    """Pressure-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def atmosphere_standard(self):
        """Set value using atmosphere, standard units."""
        unit_const = units.PressureUnits.atmosphere_standard
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def atm(self):
        """Set value using atm units (alias for atmosphere, standard)."""
        return self.atmosphere_standard
    
    @property
    def bar(self):
        """Set value using bar units."""
        unit_const = units.PressureUnits.bar
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def barye(self):
        """Set value using barye units."""
        unit_const = units.PressureUnits.barye
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyne_per_square_centimeter(self):
        """Set value using dyne per square centimeter units."""
        unit_const = units.PressureUnits.dyne_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_of_mercury_60_power_circ_mathrm_F(self):
        r"""Set value using foot of mercury ( $60{ }^{\circ} \mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.foot_of_mercury_60_power_circ_mathrm_F
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_of_water_60_power_circ_mathrm_F(self):
        r"""Set value using foot of water ( $60{ }^{\circ} \mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.foot_of_water_60_power_circ_mathrm_F
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gigapascal(self):
        """Set value using gigapascal units."""
        unit_const = units.PressureUnits.gigapascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def GPa(self):
        """Set value using GPa units (alias for gigapascal)."""
        return self.gigapascal
    
    @property
    def hectopascal(self):
        """Set value using hectopascal units."""
        unit_const = units.PressureUnits.hectopascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def hPa(self):
        """Set value using hPa units (alias for hectopascal)."""
        return self.hectopascal
    
    @property
    def inch_of_mercury_60_power_circ_mathrm_F(self):
        r"""Set value using inch of mercury ( $60{ }^{\circ} \mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.inch_of_mercury_60_power_circ_mathrm_F
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def inch_of_water_60_power_circ_mathrm_F(self):
        r"""Set value using inch of water ( $60{ }^{\circ} \mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.inch_of_water_60_power_circ_mathrm_F
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force_per_square_centimeter(self):
        """Set value using kilogram force per square centimeter units."""
        unit_const = units.PressureUnits.kilogram_force_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def at(self):
        """Set value using at units (alias for kilogram force per square centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kg_f_cm_power_2(self):
        """Set value using kg_{f / cm^{2 units (alias for kilogram force per square centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kilogram_force_per_square_meter(self):
        """Set value using kilogram force per square meter units."""
        unit_const = units.PressureUnits.kilogram_force_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kip_force_per_square_inch(self):
        """Set value using kip force per square inch units."""
        unit_const = units.PressureUnits.kip_force_per_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def KSI(self):
        """Set value using KSI units (alias for kip force per square inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def ksi(self):
        """Set value using ksi units (alias for kip force per square inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def kip_f_in_power_2(self):
        """Set value using kip { _{f / in^{2 units (alias for kip force per square inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def megapascal(self):
        """Set value using megapascal units."""
        unit_const = units.PressureUnits.megapascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MPa(self):
        """Set value using MPa units (alias for megapascal)."""
        return self.megapascal
    
    @property
    def meter_of_water_4_power_circ_mathrm_C(self):
        r"""Set value using meter of water ( $4^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.PressureUnits.meter_of_water_4_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def microbar(self):
        """Set value using microbar units."""
        unit_const = units.PressureUnits.microbar
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millibar(self):
        """Set value using millibar units."""
        unit_const = units.PressureUnits.millibar
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mbar(self):
        """Set value using mbar units (alias for millibar)."""
        return self.millibar
    
    @property
    def millimeter_of_mercury_4_power_circ_mathrm_C(self):
        r"""Set value using millimeter of mercury ( $4^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.PressureUnits.millimeter_of_mercury_4_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millimeter_of_water_4_power_circ_mathrm_C(self):
        r"""Set value using millimeter of water ( $4^{\circ} \mathrm{C}$ ) units."""
        unit_const = units.PressureUnits.millimeter_of_water_4_power_circ_mathrm_C
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_per_square_meter(self):
        """Set value using newton per square meter units."""
        unit_const = units.PressureUnits.newton_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ounce_force_per_square_inch(self):
        """Set value using ounce force per square inch units."""
        unit_const = units.PressureUnits.ounce_force_per_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def OSI(self):
        """Set value using OSI units (alias for ounce force per square inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def osi(self):
        """Set value using osi units (alias for ounce force per square inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def pascal(self):
        """Set value using pascal units."""
        unit_const = units.PressureUnits.pascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Pa(self):
        """Set value using Pa units (alias for pascal)."""
        return self.pascal
    
    @property
    def pièze(self):
        """Set value using pièze units."""
        unit_const = units.PressureUnits.pièze
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pz(self):
        """Set value using pz units (alias for pièze)."""
        return self.pièze
    
    @property
    def pound_force_per_square_foot(self):
        """Set value using pound force per square foot units."""
        unit_const = units.PressureUnits.pound_force_per_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def psf(self):
        """Set value using psf units (alias for pound force per square foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def pound_force_per_square_inch(self):
        """Set value using pound force per square inch units."""
        unit_const = units.PressureUnits.pound_force_per_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def psi(self):
        """Set value using psi units (alias for pound force per square inch)."""
        return self.pound_force_per_square_inch
    
    @property
    def torr(self):
        """Set value using torr units."""
        unit_const = units.PressureUnits.torr
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mm_Hg_0_power_circ_C(self):
        """Set value using mm Hg ( 0{ ^{circ C) units (alias for torr)."""
        return self.torr
    
    @property
    def kilopascal(self):
        """Set value using kilopascal units."""
        unit_const = units.PressureUnits.kilopascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kPa(self):
        """Set value using kPa units (alias for kilopascal)."""
        return self.kilopascal
    

class RadiationDoseEquivalentSetter(TypeSafeSetter):
    """RadiationDoseEquivalent-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def rem(self):
        """Set value using rem units."""
        unit_const = units.RadiationDoseEquivalentUnits.rem
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sievert(self):
        """Set value using sievert units."""
        unit_const = units.RadiationDoseEquivalentUnits.sievert
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Sv(self):
        """Set value using Sv units (alias for sievert)."""
        return self.sievert
    
    @property
    def millisievert(self):
        """Set value using millisievert units."""
        unit_const = units.RadiationDoseEquivalentUnits.millisievert
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mSv(self):
        """Set value using mSv units (alias for millisievert)."""
        return self.millisievert
    
    @property
    def microsievert(self):
        """Set value using microsievert units."""
        unit_const = units.RadiationDoseEquivalentUnits.microsievert
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def uSv(self):
        """Set value using μSv units (alias for microsievert)."""
        return self.microsievert
    

class RadiationExposureSetter(TypeSafeSetter):
    """RadiationExposure-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def coulomb_per_kilogram(self):
        """Set value using coulomb per kilogram units."""
        unit_const = units.RadiationExposureUnits.coulomb_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def D_unit(self):
        """Set value using D unit units."""
        unit_const = units.RadiationExposureUnits.D_unit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pastille_dose_B_unit(self):
        """Set value using pastille dose (B unit) units."""
        unit_const = units.RadiationExposureUnits.pastille_dose_B_unit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def röentgen(self):
        """Set value using röentgen units."""
        unit_const = units.RadiationExposureUnits.röentgen
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def R(self):
        """Set value using R units (alias for röentgen)."""
        return self.röentgen
    

class RadioactivitySetter(TypeSafeSetter):
    """Radioactivity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def becquerel(self):
        """Set value using becquerel units."""
        unit_const = units.RadioactivityUnits.becquerel
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Bq(self):
        """Set value using Bq units (alias for becquerel)."""
        return self.becquerel
    
    @property
    def curie(self):
        """Set value using curie units."""
        unit_const = units.RadioactivityUnits.curie
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ci(self):
        """Set value using Ci units (alias for curie)."""
        return self.curie
    
    @property
    def Mache_unit(self):
        """Set value using Mache unit units."""
        unit_const = units.RadioactivityUnits.Mache_unit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rutherford(self):
        """Set value using rutherford units."""
        unit_const = units.RadioactivityUnits.rutherford
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Rd(self):
        """Set value using Rd units (alias for rutherford)."""
        return self.rutherford
    
    @property
    def stat(self):
        """Set value using stat units."""
        unit_const = units.RadioactivityUnits.stat
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilobecquerel(self):
        """Set value using kilobecquerel units."""
        unit_const = units.RadioactivityUnits.kilobecquerel
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kBq(self):
        """Set value using kBq units (alias for kilobecquerel)."""
        return self.kilobecquerel
    
    @property
    def megabecquerel(self):
        """Set value using megabecquerel units."""
        unit_const = units.RadioactivityUnits.megabecquerel
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MBq(self):
        """Set value using MBq units (alias for megabecquerel)."""
        return self.megabecquerel
    
    @property
    def gigabecquerel(self):
        """Set value using gigabecquerel units."""
        unit_const = units.RadioactivityUnits.gigabecquerel
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def GBq(self):
        """Set value using GBq units (alias for gigabecquerel)."""
        return self.gigabecquerel
    

class SecondMomentOfAreaSetter(TypeSafeSetter):
    """SecondMomentOfArea-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def inch_quadrupled(self):
        """Set value using inch quadrupled units."""
        unit_const = units.SecondMomentOfAreaUnits.inch_quadrupled
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def centimeter_quadrupled(self):
        """Set value using centimeter quadrupled units."""
        unit_const = units.SecondMomentOfAreaUnits.centimeter_quadrupled
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_quadrupled(self):
        """Set value using foot quadrupled units."""
        unit_const = units.SecondMomentOfAreaUnits.foot_quadrupled
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def meter_quadrupled(self):
        """Set value using meter quadrupled units."""
        unit_const = units.SecondMomentOfAreaUnits.meter_quadrupled
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class SecondRadiationConstantPlanckSetter(TypeSafeSetter):
    """SecondRadiationConstantPlanck-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def meter_kelvin(self):
        """Set value using meter kelvin units."""
        unit_const = units.SecondRadiationConstantPlanckUnits.meter_kelvin
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class SpecificEnthalpySetter(TypeSafeSetter):
    """SpecificEnthalpy-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_mean_per_pound(self):
        """Set value using British thermal unit (mean) per pound units."""
        unit_const = units.SpecificEnthalpyUnits.British_thermal_unit_mean_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.SpecificEnthalpyUnits.British_thermal_unit_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.SpecificEnthalpyUnits.calorie_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.SpecificEnthalpyUnits.Chu_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.SpecificEnthalpyUnits.joule_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilojoule_per_kilogram(self):
        """Set value using kilojoule per kilogram units."""
        unit_const = units.SpecificEnthalpyUnits.kilojoule_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class SpecificGravitySetter(TypeSafeSetter):
    """SpecificGravity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Dimensionless(self):
        """Set value using Dimensionless units."""
        unit_const = units.SpecificGravityUnits.Dimensionless
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Dmls(self):
        """Set value using Dmls units (alias for Dimensionless)."""
        return self.Dimensionless
    

class SpecificHeatCapacityConstantPressureSetter(TypeSafeSetter):
    """SpecificHeatCapacityConstantPressure-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Btu_per_pound_per_degree_Fahrenheit_or_degree_Rankine(self):
        """Set value using Btu per pound per degree Fahrenheit (or degree Rankine) units."""
        unit_const = units.SpecificHeatCapacityConstantPressureUnits.Btu_per_pound_per_degree_Fahrenheit_or_degree_Rankine
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calories_per_gram_per_kelvin_or_degree_Celsius(self):
        """Set value using calories per gram per kelvin (or degree Celsius) units."""
        unit_const = units.SpecificHeatCapacityConstantPressureUnits.calories_per_gram_per_kelvin_or_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joules_per_kilogram_per_kelvin_or_degree_Celsius(self):
        """Set value using joules per kilogram per kelvin (or degree Celsius) units."""
        unit_const = units.SpecificHeatCapacityConstantPressureUnits.joules_per_kilogram_per_kelvin_or_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class SpecificLengthSetter(TypeSafeSetter):
    """SpecificLength-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def centimeter_per_gram(self):
        """Set value using centimeter per gram units."""
        unit_const = units.SpecificLengthUnits.centimeter_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cotton_count(self):
        """Set value using cotton count units."""
        unit_const = units.SpecificLengthUnits.cotton_count
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cc(self):
        """Set value using cc units (alias for cotton count)."""
        return self.cotton_count
    
    @property
    def ft_per_pound(self):
        """Set value using ft per pound units."""
        unit_const = units.SpecificLengthUnits.ft_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def meters_per_kilogram(self):
        """Set value using meters per kilogram units."""
        unit_const = units.SpecificLengthUnits.meters_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_meter(self):
        """Set value using newton meter units."""
        unit_const = units.SpecificLengthUnits.newton_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Nm(self):
        """Set value using Nm units (alias for newton meter)."""
        return self.newton_meter
    
    @property
    def worsted(self):
        """Set value using worsted units."""
        unit_const = units.SpecificLengthUnits.worsted
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class SpecificSurfaceSetter(TypeSafeSetter):
    """SpecificSurface-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_centimeter_per_gram(self):
        """Set value using square centimeter per gram units."""
        unit_const = units.SpecificSurfaceUnits.square_centimeter_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_foot_per_kilogram(self):
        """Set value using square foot per kilogram units."""
        unit_const = units.SpecificSurfaceUnits.square_foot_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_2_kg(self):
        """Set value using ft^{2 / kg units (alias for square foot per kilogram)."""
        return self.square_foot_per_kilogram
    
    @property
    def sq_ft_kg(self):
        """Set value using sq ft/kg units (alias for square foot per kilogram)."""
        return self.square_foot_per_kilogram
    
    @property
    def square_foot_per_pound(self):
        """Set value using square foot per pound units."""
        unit_const = units.SpecificSurfaceUnits.square_foot_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_2_lb(self):
        """Set value using ft^{2 / lb units (alias for square foot per pound)."""
        return self.square_foot_per_pound
    
    @property
    def sq_ft_lb(self):
        """Set value using sq ft/lb units (alias for square foot per pound)."""
        return self.square_foot_per_pound
    
    @property
    def square_meter_per_gram(self):
        """Set value using square meter per gram units."""
        unit_const = units.SpecificSurfaceUnits.square_meter_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_meter_per_kilogram(self):
        """Set value using square meter per kilogram units."""
        unit_const = units.SpecificSurfaceUnits.square_meter_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class SpecificVolumeSetter(TypeSafeSetter):
    """SpecificVolume-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_centimeter_per_gram(self):
        """Set value using cubic centimeter per gram units."""
        unit_const = units.SpecificVolumeUnits.cubic_centimeter_per_gram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm_power_3_g(self):
        """Set value using cm^{3 / g units (alias for cubic centimeter per gram)."""
        return self.cubic_centimeter_per_gram
    
    @property
    def cc_g(self):
        """Set value using cc / g units (alias for cubic centimeter per gram)."""
        return self.cubic_centimeter_per_gram
    
    @property
    def cubic_foot_per_kilogram(self):
        """Set value using cubic foot per kilogram units."""
        unit_const = units.SpecificVolumeUnits.cubic_foot_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_kg(self):
        """Set value using ft^{3 / kg units (alias for cubic foot per kilogram)."""
        return self.cubic_foot_per_kilogram
    
    @property
    def cft_kg(self):
        """Set value using cft / kg units (alias for cubic foot per kilogram)."""
        return self.cubic_foot_per_kilogram
    
    @property
    def cubic_foot_per_pound(self):
        """Set value using cubic foot per pound units."""
        unit_const = units.SpecificVolumeUnits.cubic_foot_per_pound
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_lb(self):
        """Set value using ft^{3 / lb units (alias for cubic foot per pound)."""
        return self.cubic_foot_per_pound
    
    @property
    def cft_lb(self):
        """Set value using cft / lb units (alias for cubic foot per pound)."""
        return self.cubic_foot_per_pound
    
    @property
    def cubic_meter_per_kilogram(self):
        """Set value using cubic meter per kilogram units."""
        unit_const = units.SpecificVolumeUnits.cubic_meter_per_kilogram
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class StressSetter(TypeSafeSetter):
    """Stress-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_square_centimeter(self):
        """Set value using dyne per square centimeter units."""
        unit_const = units.StressUnits.dyne_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gigapascal(self):
        """Set value using gigapascal units."""
        unit_const = units.StressUnits.gigapascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def GPa(self):
        """Set value using GPa units (alias for gigapascal)."""
        return self.gigapascal
    
    @property
    def hectopascal(self):
        """Set value using hectopascal units."""
        unit_const = units.StressUnits.hectopascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def hPa(self):
        """Set value using hPa units (alias for hectopascal)."""
        return self.hectopascal
    
    @property
    def kilogram_force_per_square_centimeter(self):
        """Set value using kilogram force per square centimeter units."""
        unit_const = units.StressUnits.kilogram_force_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def at(self):
        """Set value using at units (alias for kilogram force per square centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kg_f_cm_power_2(self):
        """Set value using kg_{f / cm^{2 units (alias for kilogram force per square centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kilogram_force_per_square_meter(self):
        """Set value using kilogram force per square meter units."""
        unit_const = units.StressUnits.kilogram_force_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kip_force_per_square_inch(self):
        """Set value using kip force per square inch units."""
        unit_const = units.StressUnits.kip_force_per_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def KSI(self):
        """Set value using KSI units (alias for kip force per square inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def ksi(self):
        """Set value using ksi units (alias for kip force per square inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def kip_f_in_power_2(self):
        """Set value using kip { _{f / in^{2 units (alias for kip force per square inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def megapascal(self):
        """Set value using megapascal units."""
        unit_const = units.StressUnits.megapascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def MPa(self):
        """Set value using MPa units (alias for megapascal)."""
        return self.megapascal
    
    @property
    def newton_per_square_meter(self):
        """Set value using newton per square meter units."""
        unit_const = units.StressUnits.newton_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ounce_force_per_square_inch(self):
        """Set value using ounce force per square inch units."""
        unit_const = units.StressUnits.ounce_force_per_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def OSI(self):
        """Set value using OSI units (alias for ounce force per square inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def osi(self):
        """Set value using osi units (alias for ounce force per square inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def oz_f_in_power_2(self):
        """Set value using oz_{f / in^{2 units (alias for ounce force per square inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def pascal(self):
        """Set value using pascal units."""
        unit_const = units.StressUnits.pascal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Pa(self):
        """Set value using Pa units (alias for pascal)."""
        return self.pascal
    
    @property
    def pound_force_per_square_foot(self):
        """Set value using pound force per square foot units."""
        unit_const = units.StressUnits.pound_force_per_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def PSF(self):
        """Set value using PSF units (alias for pound force per square foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def psf(self):
        """Set value using psf units (alias for pound force per square foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def lb_f_ft_power_2(self):
        """Set value using lb_{f / ft^{2 units (alias for pound force per square foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def pound_force_per_square_inch(self):
        """Set value using pound force per square inch units."""
        unit_const = units.StressUnits.pound_force_per_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def psi(self):
        """Set value using psi units (alias for pound force per square inch)."""
        return self.pound_force_per_square_inch
    

class SurfaceMassDensitySetter(TypeSafeSetter):
    """SurfaceMassDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_square_centimeter(self):
        """Set value using gram per square centimeter units."""
        unit_const = units.SurfaceMassDensityUnits.gram_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_per_square_meter(self):
        """Set value using gram per square meter units."""
        unit_const = units.SurfaceMassDensityUnits.gram_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_square_meter(self):
        """Set value using kilogram per square meter units."""
        unit_const = units.SurfaceMassDensityUnits.kilogram_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mass_per_square_foot(self):
        """Set value using pound (mass) per square foot units."""
        unit_const = units.SurfaceMassDensityUnits.pound_mass_per_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mass_per_square_inch(self):
        """Set value using pound (mass) per square inch units."""
        unit_const = units.SurfaceMassDensityUnits.pound_mass_per_square_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class SurfaceTensionSetter(TypeSafeSetter):
    """SurfaceTension-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_centimeter(self):
        """Set value using dyne per centimeter units."""
        unit_const = units.SurfaceTensionUnits.dyne_per_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gram_force_per_centimeter(self):
        """Set value using gram force per centimeter units."""
        unit_const = units.SurfaceTensionUnits.gram_force_per_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_per_meter(self):
        """Set value using newton per meter units."""
        unit_const = units.SurfaceTensionUnits.newton_per_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_force_per_foot(self):
        """Set value using pound force per foot units."""
        unit_const = units.SurfaceTensionUnits.pound_force_per_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_force_per_inch(self):
        """Set value using pound force per inch units."""
        unit_const = units.SurfaceTensionUnits.pound_force_per_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class TemperatureSetter(TypeSafeSetter):
    """Temperature-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def degree_Celsius_unit_size(self):
        """Set value using degree Celsius (unit size) units."""
        unit_const = units.TemperatureUnits.degree_Celsius_unit_size
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def degree_Fahrenheit_unit_size(self):
        """Set value using degree Fahrenheit (unit size) units."""
        unit_const = units.TemperatureUnits.degree_Fahrenheit_unit_size
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def degree_Réaumur_unit_size(self):
        """Set value using degree Réaumur (unit size) units."""
        unit_const = units.TemperatureUnits.degree_Réaumur_unit_size
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kelvin_absolute_scale(self):
        """Set value using kelvin (absolute scale) units."""
        unit_const = units.TemperatureUnits.kelvin_absolute_scale
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def K(self):
        """Set value using K units (alias for kelvin (absolute scale))."""
        return self.kelvin_absolute_scale
    
    @property
    def Rankine_absolute_scale(self):
        """Set value using Rankine (absolute scale) units."""
        unit_const = units.TemperatureUnits.Rankine_absolute_scale
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class ThermalConductivitySetter(TypeSafeSetter):
    """ThermalConductivity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def Btu_IT_per_inch_per_hour_per_degree_Fahrenheit(self):
        """Set value using Btu (IT) per inch per hour per degree Fahrenheit units."""
        unit_const = units.ThermalConductivityUnits.Btu_IT_per_inch_per_hour_per_degree_Fahrenheit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_therm_per_foot_per_hour_per_degree_Fahrenheit(self):
        """Set value using Btu (therm) per foot per hour per degree Fahrenheit units."""
        unit_const = units.ThermalConductivityUnits.Btu_therm_per_foot_per_hour_per_degree_Fahrenheit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_therm_per_inch_per_hour_per_degree_Fahrenheit(self):
        """Set value using Btu (therm) per inch per hour per degree Fahrenheit units."""
        unit_const = units.ThermalConductivityUnits.Btu_therm_per_inch_per_hour_per_degree_Fahrenheit
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_therm_per_centimeter_per_second_per_degree_Celsius(self):
        """Set value using calorie (therm) per centimeter per second per degree Celsius units."""
        unit_const = units.ThermalConductivityUnits.calorie_therm_per_centimeter_per_second_per_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def joule_per_second_per_centimeter_per_kelvin(self):
        """Set value using joule per second per centimeter per kelvin units."""
        unit_const = units.ThermalConductivityUnits.joule_per_second_per_centimeter_per_kelvin
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def watt_per_centimeter_per_kelvin(self):
        """Set value using watt per centimeter per kelvin units."""
        unit_const = units.ThermalConductivityUnits.watt_per_centimeter_per_kelvin
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def watt_per_meter_per_kelvin(self):
        """Set value using watt per meter per kelvin units."""
        unit_const = units.ThermalConductivityUnits.watt_per_meter_per_kelvin
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class TimeSetter(TypeSafeSetter):
    """Time-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def blink(self):
        """Set value using blink units."""
        unit_const = units.TimeUnits.blink
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def century(self):
        """Set value using century units."""
        unit_const = units.TimeUnits.century
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def chronon_or_tempon(self):
        """Set value using chronon or tempon units."""
        unit_const = units.TimeUnits.chronon_or_tempon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gigan_or_eon(self):
        """Set value using gigan or eon units."""
        unit_const = units.TimeUnits.gigan_or_eon
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ga(self):
        """Set value using Ga units (alias for gigan or eon)."""
        return self.gigan_or_eon
    
    @property
    def eon(self):
        """Set value using eon units (alias for gigan or eon)."""
        return self.gigan_or_eon
    
    @property
    def hour(self):
        """Set value using hour units."""
        unit_const = units.TimeUnits.hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def h(self):
        """Set value using h units (alias for hour)."""
        return self.hour
    
    @property
    def hr(self):
        """Set value using hr units (alias for hour)."""
        return self.hour
    
    @property
    def Julian_year(self):
        """Set value using Julian year units."""
        unit_const = units.TimeUnits.Julian_year
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def a_jul(self):
        """Set value using a (jul) units (alias for Julian year)."""
        return self.Julian_year
    
    @property
    def yr(self):
        """Set value using yr units (alias for Julian year)."""
        return self.Julian_year
    
    @property
    def mean_solar_day(self):
        """Set value using mean solar day units."""
        unit_const = units.TimeUnits.mean_solar_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def da(self):
        """Set value using da units (alias for mean solar day)."""
        return self.mean_solar_day
    
    @property
    def d(self):
        """Set value using d units (alias for mean solar day)."""
        return self.mean_solar_day
    
    @property
    def millenium(self):
        """Set value using millenium units."""
        unit_const = units.TimeUnits.millenium
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def minute(self):
        """Set value using minute units."""
        unit_const = units.TimeUnits.minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def min(self):
        """Set value using min units (alias for minute)."""
        return self.minute
    
    @property
    def second(self):
        """Set value using second units."""
        unit_const = units.TimeUnits.second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def s(self):
        """Set value using s units (alias for second)."""
        return self.second
    
    @property
    def shake(self):
        """Set value using shake units."""
        unit_const = units.TimeUnits.shake
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def sidereal_year_1900_AD(self):
        """Set value using sidereal year (1900 AD) units."""
        unit_const = units.TimeUnits.sidereal_year_1900_AD
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def a_sider(self):
        """Set value using a (sider) units (alias for sidereal year (1900 AD))."""
        return self.sidereal_year_1900_AD
    
    @property
    def tropical_year(self):
        """Set value using tropical year units."""
        unit_const = units.TimeUnits.tropical_year
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def wink(self):
        """Set value using wink units."""
        unit_const = units.TimeUnits.wink
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def year(self):
        """Set value using year units."""
        unit_const = units.TimeUnits.year
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def a(self):
        """Set value using a units (alias for year)."""
        return self.year
    
    @property
    def y(self):
        """Set value using y units (alias for year)."""
        return self.year
    
    @property
    def millisecond(self):
        """Set value using millisecond units."""
        unit_const = units.TimeUnits.millisecond
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ms(self):
        """Set value using ms units (alias for millisecond)."""
        return self.millisecond
    
    @property
    def microsecond(self):
        """Set value using microsecond units."""
        unit_const = units.TimeUnits.microsecond
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def us(self):
        """Set value using μs units (alias for microsecond)."""
        return self.microsecond
    
    @property
    def nanosecond(self):
        """Set value using nanosecond units."""
        unit_const = units.TimeUnits.nanosecond
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ns(self):
        """Set value using ns units (alias for nanosecond)."""
        return self.nanosecond
    
    @property
    def picosecond(self):
        """Set value using picosecond units."""
        unit_const = units.TimeUnits.picosecond
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ps(self):
        """Set value using ps units (alias for picosecond)."""
        return self.picosecond
    

class TorqueSetter(TypeSafeSetter):
    """Torque-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def centimeter_kilogram_force(self):
        """Set value using centimeter kilogram force units."""
        unit_const = units.TorqueUnits.centimeter_kilogram_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyne_centimeter(self):
        """Set value using dyne centimeter units."""
        unit_const = units.TorqueUnits.dyne_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_kilogram_force(self):
        """Set value using foot kilogram force units."""
        unit_const = units.TorqueUnits.foot_kilogram_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pound_force(self):
        """Set value using foot pound force units."""
        unit_const = units.TorqueUnits.foot_pound_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_poundal(self):
        """Set value using foot poundal units."""
        unit_const = units.TorqueUnits.foot_poundal
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_pound_force(self):
        """Set value using in pound force units."""
        unit_const = units.TorqueUnits.in_pound_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def inch_ounce_force(self):
        """Set value using inch ounce force units."""
        unit_const = units.TorqueUnits.inch_ounce_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def meter_kilogram_force(self):
        """Set value using meter kilogram force units."""
        unit_const = units.TorqueUnits.meter_kilogram_force
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_centimeter(self):
        """Set value using newton centimeter units."""
        unit_const = units.TorqueUnits.newton_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def newton_meter(self):
        """Set value using newton meter units."""
        unit_const = units.TorqueUnits.newton_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class TurbulenceEnergyDissipationRateSetter(TypeSafeSetter):
    """TurbulenceEnergyDissipationRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_foot_per_cubic_second(self):
        """Set value using square foot per cubic second units."""
        unit_const = units.TurbulenceEnergyDissipationRateUnits.square_foot_per_cubic_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_2_s_power_3(self):
        """Set value using ft^{2 / s^{3 units (alias for square foot per cubic second)."""
        return self.square_foot_per_cubic_second
    
    @property
    def sq_ft_sec_power_3(self):
        """Set value using sq ft/sec { ^{3 units (alias for square foot per cubic second)."""
        return self.square_foot_per_cubic_second
    
    @property
    def square_meter_per_cubic_second(self):
        """Set value using square meter per cubic second units."""
        unit_const = units.TurbulenceEnergyDissipationRateUnits.square_meter_per_cubic_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class VelocityAngularSetter(TypeSafeSetter):
    """VelocityAngular-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def degree_per_minute(self):
        """Set value using degree per minute units."""
        unit_const = units.VelocityAngularUnits.degree_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def deg_min(self):
        """Set value using deg/min units (alias for degree per minute)."""
        return self.degree_per_minute
    
    @property
    def power_circ_min(self):
        """Set value using { ^{circ / min units (alias for degree per minute)."""
        return self.degree_per_minute
    
    @property
    def degree_per_second(self):
        """Set value using degree per second units."""
        unit_const = units.VelocityAngularUnits.degree_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def deg_s(self):
        """Set value using deg/s units (alias for degree per second)."""
        return self.degree_per_second
    
    @property
    def power_circ_s(self):
        """Set value using { ^{circ /s units (alias for degree per second)."""
        return self.degree_per_second
    
    @property
    def grade_per_minute(self):
        """Set value using grade per minute units."""
        unit_const = units.VelocityAngularUnits.grade_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gon_min(self):
        """Set value using gon/min units (alias for grade per minute)."""
        return self.grade_per_minute
    
    @property
    def grad_min(self):
        """Set value using grad/min units (alias for grade per minute)."""
        return self.grade_per_minute
    
    @property
    def radian_per_minute(self):
        """Set value using radian per minute units."""
        unit_const = units.VelocityAngularUnits.radian_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def radian_per_second(self):
        """Set value using radian per second units."""
        unit_const = units.VelocityAngularUnits.radian_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def revolution_per_minute(self):
        """Set value using revolution per minute units."""
        unit_const = units.VelocityAngularUnits.revolution_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rev_m(self):
        """Set value using rev/m units (alias for revolution per minute)."""
        return self.revolution_per_minute
    
    @property
    def rpm(self):
        """Set value using rpm units (alias for revolution per minute)."""
        return self.revolution_per_minute
    
    @property
    def revolution_per_second(self):
        """Set value using revolution per second units."""
        unit_const = units.VelocityAngularUnits.revolution_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def rev_s(self):
        """Set value using rev/s units (alias for revolution per second)."""
        return self.revolution_per_second
    
    @property
    def rps(self):
        """Set value using rps units (alias for revolution per second)."""
        return self.revolution_per_second
    
    @property
    def turn_per_minute(self):
        """Set value using turn per minute units."""
        unit_const = units.VelocityAngularUnits.turn_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class VelocityLinearSetter(TypeSafeSetter):
    """VelocityLinear-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_per_hour(self):
        """Set value using foot per hour units."""
        unit_const = units.VelocityLinearUnits.foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_h(self):
        """Set value using ft/h units (alias for foot per hour)."""
        return self.foot_per_hour
    
    @property
    def ft_hr(self):
        """Set value using ft/hr units (alias for foot per hour)."""
        return self.foot_per_hour
    
    @property
    def fph(self):
        """Set value using fph units (alias for foot per hour)."""
        return self.foot_per_hour
    
    @property
    def foot_per_minute(self):
        """Set value using foot per minute units."""
        unit_const = units.VelocityLinearUnits.foot_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_min(self):
        """Set value using ft/min units (alias for foot per minute)."""
        return self.foot_per_minute
    
    @property
    def fpm(self):
        """Set value using fpm units (alias for foot per minute)."""
        return self.foot_per_minute
    
    @property
    def foot_per_second(self):
        """Set value using foot per second units."""
        unit_const = units.VelocityLinearUnits.foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_s(self):
        """Set value using ft/s units (alias for foot per second)."""
        return self.foot_per_second
    
    @property
    def fps(self):
        """Set value using fps units (alias for foot per second)."""
        return self.foot_per_second
    
    @property
    def inch_per_second(self):
        """Set value using inch per second units."""
        unit_const = units.VelocityLinearUnits.inch_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_s(self):
        """Set value using in/s units (alias for inch per second)."""
        return self.inch_per_second
    
    @property
    def ips(self):
        """Set value using ips units (alias for inch per second)."""
        return self.inch_per_second
    
    @property
    def international_knot(self):
        """Set value using international knot units."""
        unit_const = units.VelocityLinearUnits.international_knot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def knot(self):
        """Set value using knot units (alias for international knot)."""
        return self.international_knot
    
    @property
    def kilometer_per_hour(self):
        """Set value using kilometer per hour units."""
        unit_const = units.VelocityLinearUnits.kilometer_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilometer_per_second(self):
        """Set value using kilometer per second units."""
        unit_const = units.VelocityLinearUnits.kilometer_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def meter_per_second(self):
        """Set value using meter per second units."""
        unit_const = units.VelocityLinearUnits.meter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mile_per_hour(self):
        """Set value using mile per hour units."""
        unit_const = units.VelocityLinearUnits.mile_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_h(self):
        """Set value using mi / h units (alias for mile per hour)."""
        return self.mile_per_hour
    
    @property
    def mi_hr(self):
        """Set value using mi / hr units (alias for mile per hour)."""
        return self.mile_per_hour
    
    @property
    def mph(self):
        """Set value using mph units (alias for mile per hour)."""
        return self.mile_per_hour
    

class ViscosityDynamicSetter(TypeSafeSetter):
    """ViscosityDynamic-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def centipoise(self):
        """Set value using centipoise units."""
        unit_const = units.ViscosityDynamicUnits.centipoise
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cP(self):
        """Set value using cP units (alias for centipoise)."""
        return self.centipoise
    
    @property
    def cPo(self):
        """Set value using cPo units (alias for centipoise)."""
        return self.centipoise
    
    @property
    def dyne_second_per_square_centimeter(self):
        """Set value using dyne second per square centimeter units."""
        unit_const = units.ViscosityDynamicUnits.dyne_second_per_square_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilopound_second_per_square_meter(self):
        """Set value using kilopound second per square meter units."""
        unit_const = units.ViscosityDynamicUnits.kilopound_second_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def millipoise(self):
        """Set value using millipoise units."""
        unit_const = units.ViscosityDynamicUnits.millipoise
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mP(self):
        """Set value using mP units (alias for millipoise)."""
        return self.millipoise
    
    @property
    def mPo(self):
        """Set value using mPo units (alias for millipoise)."""
        return self.millipoise
    
    @property
    def newton_second_per_square_meter(self):
        """Set value using newton second per square meter units."""
        unit_const = units.ViscosityDynamicUnits.newton_second_per_square_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pascal_second(self):
        """Set value using pascal second units."""
        unit_const = units.ViscosityDynamicUnits.pascal_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Pa_s(self):
        """Set value using Pa s units (alias for pascal second)."""
        return self.pascal_second
    
    @property
    def PI(self):
        """Set value using PI units (alias for pascal second)."""
        return self.pascal_second
    
    @property
    def poise(self):
        """Set value using poise units."""
        unit_const = units.ViscosityDynamicUnits.poise
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def P(self):
        """Set value using P units (alias for poise)."""
        return self.poise
    
    @property
    def Po(self):
        """Set value using Po units (alias for poise)."""
        return self.poise
    
    @property
    def pound_force_hour_per_square_foot(self):
        """Set value using pound force hour per square foot units."""
        unit_const = units.ViscosityDynamicUnits.pound_force_hour_per_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_f_h_ft_power_2(self):
        """Set value using lb_{f h / ft^{2 units (alias for pound force hour per square foot)."""
        return self.pound_force_hour_per_square_foot
    
    @property
    def lb_hr_sq_ft(self):
        """Set value using lb hr / sq ft units (alias for pound force hour per square foot)."""
        return self.pound_force_hour_per_square_foot
    
    @property
    def pound_force_second_per_square_foot(self):
        """Set value using pound force second per square foot units."""
        unit_const = units.ViscosityDynamicUnits.pound_force_second_per_square_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_f_s_ft_power_2(self):
        """Set value using lb_{f s / ft^{2 units (alias for pound force second per square foot)."""
        return self.pound_force_second_per_square_foot
    
    @property
    def lb_sec_sq_ft(self):
        """Set value using lb sec / sq ft units (alias for pound force second per square foot)."""
        return self.pound_force_second_per_square_foot
    

class ViscosityKinematicSetter(TypeSafeSetter):
    """ViscosityKinematic-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def centistokes(self):
        """Set value using centistokes units."""
        unit_const = units.ViscosityKinematicUnits.centistokes
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cSt(self):
        """Set value using cSt units (alias for centistokes)."""
        return self.centistokes
    
    @property
    def millistokes(self):
        """Set value using millistokes units."""
        unit_const = units.ViscosityKinematicUnits.millistokes
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mSt(self):
        """Set value using mSt units (alias for millistokes)."""
        return self.millistokes
    
    @property
    def square_centimeter_per_second(self):
        """Set value using square centimeter per second units."""
        unit_const = units.ViscosityKinematicUnits.square_centimeter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_foot_per_hour(self):
        """Set value using square foot per hour units."""
        unit_const = units.ViscosityKinematicUnits.square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_2_h(self):
        """Set value using ft^{2 / h units (alias for square foot per hour)."""
        return self.square_foot_per_hour
    
    @property
    def ft_power_2_hr(self):
        """Set value using ft^{2 / hr units (alias for square foot per hour)."""
        return self.square_foot_per_hour
    
    @property
    def square_foot_per_second(self):
        """Set value using square foot per second units."""
        unit_const = units.ViscosityKinematicUnits.square_foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_meters_per_second(self):
        """Set value using square meters per second units."""
        unit_const = units.ViscosityKinematicUnits.square_meters_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def stokes(self):
        """Set value using stokes units."""
        unit_const = units.ViscosityKinematicUnits.stokes
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def St(self):
        """Set value using St units (alias for stokes)."""
        return self.stokes
    

class VolumeSetter(TypeSafeSetter):
    """Volume-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def acre_foot(self):
        """Set value using acre foot units."""
        unit_const = units.VolumeUnits.acre_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def acre_inch(self):
        """Set value using acre inch units."""
        unit_const = units.VolumeUnits.acre_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def barrel_US_Liquid(self):
        """Set value using barrel (US Liquid) units."""
        unit_const = units.VolumeUnits.barrel_US_Liquid
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def barrel_US_Petro(self):
        """Set value using barrel (US, Petro) units."""
        unit_const = units.VolumeUnits.barrel_US_Petro
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def bbl(self):
        """Set value using bbl units (alias for barrel (US, Petro))."""
        return self.barrel_US_Petro
    
    @property
    def board_foot_measure(self):
        """Set value using board foot measure units."""
        unit_const = units.VolumeUnits.board_foot_measure
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def BM(self):
        """Set value using BM units (alias for board foot measure)."""
        return self.board_foot_measure
    
    @property
    def fbm(self):
        """Set value using fbm units (alias for board foot measure)."""
        return self.board_foot_measure
    
    @property
    def bushel_US_Dry(self):
        """Set value using bushel (US Dry) units."""
        unit_const = units.VolumeUnits.bushel_US_Dry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def centiliter(self):
        """Set value using centiliter units."""
        unit_const = units.VolumeUnits.centiliter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cl(self):
        """Set value using cl units (alias for centiliter)."""
        return self.centiliter
    
    @property
    def cL(self):
        """Set value using cL units (alias for centiliter)."""
        return self.centiliter
    
    @property
    def cord(self):
        """Set value using cord units."""
        unit_const = units.VolumeUnits.cord
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cd(self):
        """Set value using cd units (alias for cord)."""
        return self.cord
    
    @property
    def cord_foot(self):
        """Set value using cord foot units."""
        unit_const = units.VolumeUnits.cord_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_centimeter(self):
        """Set value using cubic centimeter units."""
        unit_const = units.VolumeUnits.cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm_power_3(self):
        """Set value using cm^{3 units (alias for cubic centimeter)."""
        return self.cubic_centimeter
    
    @property
    def cc(self):
        """Set value using cc units (alias for cubic centimeter)."""
        return self.cubic_centimeter
    
    @property
    def cubic_decameter(self):
        """Set value using cubic decameter units."""
        unit_const = units.VolumeUnits.cubic_decameter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_decimeter(self):
        """Set value using cubic decimeter units."""
        unit_const = units.VolumeUnits.cubic_decimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_foot(self):
        """Set value using cubic foot units."""
        unit_const = units.VolumeUnits.cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_ft(self):
        """Set value using cu ft units (alias for cubic foot)."""
        return self.cubic_foot
    
    @property
    def ft_power_3(self):
        """Set value using ft { ^{3 units (alias for cubic foot)."""
        return self.cubic_foot
    
    @property
    def cubic_inch(self):
        """Set value using cubic inch units."""
        unit_const = units.VolumeUnits.cubic_inch
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_in(self):
        """Set value using cu in units (alias for cubic inch)."""
        return self.cubic_inch
    
    @property
    def in_power_3(self):
        """Set value using in^{3 units (alias for cubic inch)."""
        return self.cubic_inch
    
    @property
    def cubic_kilometer(self):
        """Set value using cubic kilometer units."""
        unit_const = units.VolumeUnits.cubic_kilometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_meter(self):
        """Set value using cubic meter units."""
        unit_const = units.VolumeUnits.cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_micrometer(self):
        """Set value using cubic micrometer units."""
        unit_const = units.VolumeUnits.cubic_micrometer
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_mile_US_Intl(self):
        """Set value using cubic mile (US, Intl) units."""
        unit_const = units.VolumeUnits.cubic_mile_US_Intl
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_millimeter(self):
        """Set value using cubic millimeter units."""
        unit_const = units.VolumeUnits.cubic_millimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_yard(self):
        """Set value using cubic yard units."""
        unit_const = units.VolumeUnits.cubic_yard
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_yd(self):
        """Set value using cu yd units (alias for cubic yard)."""
        return self.cubic_yard
    
    @property
    def yd_power_3(self):
        """Set value using yd^{3 units (alias for cubic yard)."""
        return self.cubic_yard
    
    @property
    def decastére(self):
        """Set value using decastére units."""
        unit_const = units.VolumeUnits.decastére
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dast(self):
        """Set value using dast units (alias for decastére)."""
        return self.decastére
    
    @property
    def deciliter(self):
        """Set value using deciliter units."""
        unit_const = units.VolumeUnits.deciliter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def dl(self):
        """Set value using dl units (alias for deciliter)."""
        return self.deciliter
    
    @property
    def dL(self):
        """Set value using dL units (alias for deciliter)."""
        return self.deciliter
    
    @property
    def fluid_drachm_UK(self):
        """Set value using fluid drachm (UK) units."""
        unit_const = units.VolumeUnits.fluid_drachm_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def fluid_dram_US(self):
        """Set value using fluid dram (US) units."""
        unit_const = units.VolumeUnits.fluid_dram_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def fluid_ounce_US(self):
        """Set value using fluid ounce (US) units."""
        unit_const = units.VolumeUnits.fluid_ounce_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallon_Imperial_UK(self):
        """Set value using gallon (Imperial UK) units."""
        unit_const = units.VolumeUnits.gallon_Imperial_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_UK(self):
        """Set value using gal (UK) units (alias for gallon (Imperial UK))."""
        return self.gallon_Imperial_UK
    
    @property
    def Imp_gal(self):
        """Set value using Imp gal units (alias for gallon (Imperial UK))."""
        return self.gallon_Imperial_UK
    
    @property
    def gallon_US_Dry(self):
        """Set value using gallon (US Dry) units."""
        unit_const = units.VolumeUnits.gallon_US_Dry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallon_US_Liquid(self):
        """Set value using gallon (US Liquid) units."""
        unit_const = units.VolumeUnits.gallon_US_Liquid
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal(self):
        """Set value using gal units (alias for gallon (US Liquid))."""
        return self.gallon_US_Liquid
    
    @property
    def last(self):
        """Set value using last units."""
        unit_const = units.VolumeUnits.last
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liter(self):
        """Set value using liter units."""
        unit_const = units.VolumeUnits.liter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1(self):
        """Set value using 1 units (alias for liter)."""
        return self.liter
    
    @property
    def L(self):
        """Set value using L units (alias for liter)."""
        return self.liter
    
    @property
    def microliter(self):
        """Set value using microliter units."""
        unit_const = units.VolumeUnits.microliter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_l(self):
        """Set value using mu l units (alias for microliter)."""
        return self.microliter
    
    @property
    def mu_L(self):
        """Set value using mu L units (alias for microliter)."""
        return self.microliter
    
    @property
    def milliliter(self):
        """Set value using milliliter units."""
        unit_const = units.VolumeUnits.milliliter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ml(self):
        """Set value using ml units (alias for milliliter)."""
        return self.milliliter
    
    @property
    def Mohr_centicube(self):
        """Set value using Mohr centicube units."""
        unit_const = units.VolumeUnits.Mohr_centicube
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pint_UK(self):
        """Set value using pint (UK) units."""
        unit_const = units.VolumeUnits.pint_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pint_US_Dry(self):
        """Set value using pint (US Dry) units."""
        unit_const = units.VolumeUnits.pint_US_Dry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pint_US_Liquid(self):
        """Set value using pint (US Liquid) units."""
        unit_const = units.VolumeUnits.pint_US_Liquid
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def pt(self):
        """Set value using pt units (alias for pint (US Liquid))."""
        return self.pint_US_Liquid
    
    @property
    def quart_US_Dry(self):
        """Set value using quart (US Dry) units."""
        unit_const = units.VolumeUnits.quart_US_Dry
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def stére(self):
        """Set value using stére units."""
        unit_const = units.VolumeUnits.stére
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def st(self):
        """Set value using st units (alias for stére)."""
        return self.stére
    
    @property
    def tablespoon_Metric(self):
        """Set value using tablespoon (Metric) units."""
        unit_const = units.VolumeUnits.tablespoon_Metric
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def tablespoon_US(self):
        """Set value using tablespoon (US) units."""
        unit_const = units.VolumeUnits.tablespoon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def tbsp(self):
        """Set value using tbsp units (alias for tablespoon (US))."""
        return self.tablespoon_US
    
    @property
    def teaspoon_US(self):
        """Set value using teaspoon (US) units."""
        unit_const = units.VolumeUnits.teaspoon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def tsp(self):
        """Set value using tsp units (alias for teaspoon (US))."""
        return self.teaspoon_US
    

class VolumeFractionOfISetter(TypeSafeSetter):
    """VolumeFractionOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_centimeters_of_i_per_cubic_meter_total(self):
        """Set value using cubic centimeters of "i" per cubic meter total units."""
        unit_const = units.VolumeFractionOfIUnits.cubic_centimeters_of_i_per_cubic_meter_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm_i_power_3_m_power_3(self):
        """Set value using cm_{i^{3 / m^{3 units (alias for cubic centimeters of "i" per cubic meter total)."""
        return self.cubic_centimeters_of_i_per_cubic_meter_total
    
    @property
    def cc_i_m_power_3(self):
        """Set value using cc_{i / m^{3 units (alias for cubic centimeters of "i" per cubic meter total)."""
        return self.cubic_centimeters_of_i_per_cubic_meter_total
    
    @property
    def cubic_foot_of_i_per_cubic_foot_total(self):
        """Set value using cubic foot of "i" per cubic foot total units."""
        unit_const = units.VolumeFractionOfIUnits.cubic_foot_of_i_per_cubic_foot_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_i_power_3_ft_power_3(self):
        """Set value using ft_{i^{3 / ft^{3 units (alias for cubic foot of "i" per cubic foot total)."""
        return self.cubic_foot_of_i_per_cubic_foot_total
    
    @property
    def cft_i_cft(self):
        """Set value using cft_{i / cft units (alias for cubic foot of "i" per cubic foot total)."""
        return self.cubic_foot_of_i_per_cubic_foot_total
    
    @property
    def cubic_meters_of_i_per_cubic_meter_total(self):
        """Set value using cubic meters of " i " per cubic meter total units."""
        unit_const = units.VolumeFractionOfIUnits.cubic_meters_of_i_per_cubic_meter_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallons_of_i_per_gallon_total(self):
        """Set value using gallons of "i" per gallon total units."""
        unit_const = units.VolumeFractionOfIUnits.gallons_of_i_per_gallon_total
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class VolumetricCalorificHeatingValueSetter(TypeSafeSetter):
    """VolumetricCalorificHeatingValue-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def British_thermal_unit_per_cubic_foot(self):
        """Set value using British thermal unit per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.British_thermal_unit_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_ft_power_3(self):
        """Set value using Btu / ft^{3 units (alias for British thermal unit per cubic foot)."""
        return self.British_thermal_unit_per_cubic_foot
    
    @property
    def Btu_cft(self):
        """Set value using Btu/cft units (alias for British thermal unit per cubic foot)."""
        return self.British_thermal_unit_per_cubic_foot
    
    @property
    def British_thermal_unit_per_gallon_UK(self):
        """Set value using British thermal unit per gallon (UK) units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.British_thermal_unit_per_gallon_UK
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def British_thermal_unit_per_gallon_US(self):
        """Set value using British thermal unit per gallon (US) units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.British_thermal_unit_per_gallon_US
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def calorie_per_cubic_centimeter(self):
        """Set value using calorie per cubic centimeter units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.calorie_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_cm_power_3(self):
        """Set value using cal / cm^{3 units (alias for calorie per cubic centimeter)."""
        return self.calorie_per_cubic_centimeter
    
    @property
    def cal_cc(self):
        """Set value using cal / cc units (alias for calorie per cubic centimeter)."""
        return self.calorie_per_cubic_centimeter
    
    @property
    def Chu_per_cubic_foot(self):
        """Set value using Chu per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.Chu_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_ft_power_3(self):
        """Set value using Chu / ft^{3 units (alias for Chu per cubic foot)."""
        return self.Chu_per_cubic_foot
    
    @property
    def Chu_cft(self):
        """Set value using Chu / cft units (alias for Chu per cubic foot)."""
        return self.Chu_per_cubic_foot
    
    @property
    def joule_per_cubic_meter(self):
        """Set value using joule per cubic meter units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.joule_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilocalorie_per_cubic_foot(self):
        """Set value using kilocalorie per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.kilocalorie_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_ft_power_3(self):
        """Set value using kcal / ft^{3 units (alias for kilocalorie per cubic foot)."""
        return self.kilocalorie_per_cubic_foot
    
    @property
    def kcal_cft(self):
        """Set value using kcal / cft units (alias for kilocalorie per cubic foot)."""
        return self.kilocalorie_per_cubic_foot
    
    @property
    def kilocalorie_per_cubic_meter(self):
        """Set value using kilocalorie per cubic meter units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.kilocalorie_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def therm_100_K_Btu_per_cubic_foot(self):
        """Set value using therm ( 100 K Btu ) per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.therm_100_K_Btu_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class VolumetricCoefficientOfExpansionSetter(TypeSafeSetter):
    """VolumetricCoefficientOfExpansion-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius(self):
        """Set value using gram per cubic centimeter per kelvin (or degree Celsius) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_cm_power_3_K(self):
        """Set value using g / cm^{3 / K units (alias for gram per cubic centimeter per kelvin (or degree Celsius))."""
        return self.gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius
    
    @property
    def g_cc_power_circ_C(self):
        """Set value using g/cc/ { ^{circ C units (alias for gram per cubic centimeter per kelvin (or degree Celsius))."""
        return self.gram_per_cubic_centimeter_per_kelvin_or_degree_Celsius
    
    @property
    def kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius(self):
        """Set value using kilogram per cubic meter per kelvin (or degree Celsius) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_m_power_3_K(self):
        """Set value using kg / m^{3 / K units (alias for kilogram per cubic meter per kelvin (or degree Celsius))."""
        return self.kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius
    
    @property
    def kg_m_power_3_power_circ_C(self):
        """Set value using kg / m^{3 /{ ^{circ C units (alias for kilogram per cubic meter per kelvin (or degree Celsius))."""
        return self.kilogram_per_cubic_meter_per_kelvin_or_degree_Celsius
    
    @property
    def pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankine(self):
        """Set value using pound per cubic foot per degree Fahrenheit (or degree Rankine) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankine
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft_power_3_power_circ_R(self):
        """Set value using lb / ft^{3 /{ ^{circ R units (alias for pound per cubic foot per degree Fahrenheit (or degree Rankine))."""
        return self.pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankine
    
    @property
    def lb_cft_power_circ_F(self):
        """Set value using lb / cft /{ ^{circ F units (alias for pound per cubic foot per degree Fahrenheit (or degree Rankine))."""
        return self.pound_per_cubic_foot_per_degree_Fahrenheit_or_degree_Rankine
    
    @property
    def pound_per_cubic_foot_per_kelvin_or_degree_Celsius(self):
        """Set value using pound per cubic foot per kelvin (or degree Celsius) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.pound_per_cubic_foot_per_kelvin_or_degree_Celsius
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft_power_3_K(self):
        """Set value using lb / ft^{3 / K units (alias for pound per cubic foot per kelvin (or degree Celsius))."""
        return self.pound_per_cubic_foot_per_kelvin_or_degree_Celsius
    
    @property
    def lb_cft_power_circ_C(self):
        """Set value using lb / cft /{ ^{circ C units (alias for pound per cubic foot per kelvin (or degree Celsius))."""
        return self.pound_per_cubic_foot_per_kelvin_or_degree_Celsius
    

class VolumetricFlowRateSetter(TypeSafeSetter):
    """VolumetricFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_feet_per_day(self):
        """Set value using cubic feet per day units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_d(self):
        """Set value using ft^{3 / d units (alias for cubic feet per day)."""
        return self.cubic_feet_per_day
    
    @property
    def cft_da(self):
        """Set value using cft / da units (alias for cubic feet per day)."""
        return self.cubic_feet_per_day
    
    @property
    def cfd(self):
        """Set value using cfd units (alias for cubic feet per day)."""
        return self.cubic_feet_per_day
    
    @property
    def cubic_feet_per_hour(self):
        """Set value using cubic feet per hour units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_h(self):
        """Set value using ft^{3 / h units (alias for cubic feet per hour)."""
        return self.cubic_feet_per_hour
    
    @property
    def cft_hr(self):
        """Set value using cft / hr units (alias for cubic feet per hour)."""
        return self.cubic_feet_per_hour
    
    @property
    def cfh(self):
        """Set value using cfh units (alias for cubic feet per hour)."""
        return self.cubic_feet_per_hour
    
    @property
    def cubic_feet_per_minute(self):
        """Set value using cubic feet per minute units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_min(self):
        """Set value using ft^{3 / min units (alias for cubic feet per minute)."""
        return self.cubic_feet_per_minute
    
    @property
    def cft_min(self):
        """Set value using cft / min units (alias for cubic feet per minute)."""
        return self.cubic_feet_per_minute
    
    @property
    def cfm(self):
        """Set value using cfm units (alias for cubic feet per minute)."""
        return self.cubic_feet_per_minute
    
    @property
    def cubic_feet_per_second(self):
        """Set value using cubic feet per second units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_s(self):
        """Set value using ft^{3 / s units (alias for cubic feet per second)."""
        return self.cubic_feet_per_second
    
    @property
    def cft_sec(self):
        """Set value using cft/sec units (alias for cubic feet per second)."""
        return self.cubic_feet_per_second
    
    @property
    def cfs(self):
        """Set value using cfs units (alias for cubic feet per second)."""
        return self.cubic_feet_per_second
    
    @property
    def cubic_meters_per_day(self):
        """Set value using cubic meters per day units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_meters_per_hour(self):
        """Set value using cubic meters per hour units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_meters_per_minute(self):
        """Set value using cubic meters per minute units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_meters_per_second(self):
        """Set value using cubic meters per second units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallons_per_day(self):
        """Set value using gallons per day units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_d(self):
        """Set value using gal/d units (alias for gallons per day)."""
        return self.gallons_per_day
    
    @property
    def gpd(self):
        """Set value using gpd units (alias for gallons per day)."""
        return self.gallons_per_day
    
    @property
    def gal_da(self):
        """Set value using gal/ da units (alias for gallons per day)."""
        return self.gallons_per_day
    
    @property
    def gallons_per_hour(self):
        """Set value using gallons per hour units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_h(self):
        """Set value using gal/h units (alias for gallons per hour)."""
        return self.gallons_per_hour
    
    @property
    def gph(self):
        """Set value using gph units (alias for gallons per hour)."""
        return self.gallons_per_hour
    
    @property
    def gal_hr(self):
        """Set value using gal/ hr units (alias for gallons per hour)."""
        return self.gallons_per_hour
    
    @property
    def gallons_per_minute(self):
        """Set value using gallons per minute units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_min(self):
        """Set value using gal/min units (alias for gallons per minute)."""
        return self.gallons_per_minute
    
    @property
    def gpm(self):
        """Set value using gpm units (alias for gallons per minute)."""
        return self.gallons_per_minute
    
    @property
    def gallons_per_second(self):
        """Set value using gallons per second units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_s(self):
        """Set value using gal/s units (alias for gallons per second)."""
        return self.gallons_per_second
    
    @property
    def gps(self):
        """Set value using gps units (alias for gallons per second)."""
        return self.gallons_per_second
    
    @property
    def gal_sec(self):
        """Set value using gal/ sec units (alias for gallons per second)."""
        return self.gallons_per_second
    
    @property
    def liters_per_day(self):
        """Set value using liters per day units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_hour(self):
        """Set value using liters per hour units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_minute(self):
        """Set value using liters per minute units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_second(self):
        """Set value using liters per second units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class VolumetricFluxSetter(TypeSafeSetter):
    """VolumetricFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_feet_per_square_foot_per_day(self):
        """Set value using cubic feet per square foot per day units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_left_ft_power_2_tilde_dright(self):
        """Set value using ft^{3 /left(ft^{2 ~dright) units (alias for cubic feet per square foot per day)."""
        return self.cubic_feet_per_square_foot_per_day
    
    @property
    def cft_sqft_da(self):
        """Set value using cft / sqft / da units (alias for cubic feet per square foot per day)."""
        return self.cubic_feet_per_square_foot_per_day
    
    @property
    def cubic_feet_per_square_foot_per_hour(self):
        """Set value using cubic feet per square foot per hour units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_left_ft_power_2_tilde_hright(self):
        """Set value using ft^{3 /left(ft^{2 ~hright) units (alias for cubic feet per square foot per hour)."""
        return self.cubic_feet_per_square_foot_per_hour
    
    @property
    def cft_sqft_hr(self):
        """Set value using cft / sqft / hr units (alias for cubic feet per square foot per hour)."""
        return self.cubic_feet_per_square_foot_per_hour
    
    @property
    def cubic_feet_per_square_foot_per_minute(self):
        """Set value using cubic feet per square foot per minute units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_left_ft_power_2_min_right(self):
        """Set value using ft^{3 /left(ft^{2 min right) units (alias for cubic feet per square foot per minute)."""
        return self.cubic_feet_per_square_foot_per_minute
    
    @property
    def cft_sqft_min(self):
        """Set value using cft / sqft/min units (alias for cubic feet per square foot per minute)."""
        return self.cubic_feet_per_square_foot_per_minute
    
    @property
    def cubic_feet_per_square_foot_per_second(self):
        """Set value using cubic feet per square foot per second units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_power_3_left_ft_power_2_tilde_sright(self):
        """Set value using ft^{3 /left(ft^{2 ~sright) units (alias for cubic feet per square foot per second)."""
        return self.cubic_feet_per_square_foot_per_second
    
    @property
    def cft_sqft_sec(self):
        """Set value using cft/sqft/ sec units (alias for cubic feet per square foot per second)."""
        return self.cubic_feet_per_square_foot_per_second
    
    @property
    def cubic_meters_per_square_meter_per_day(self):
        """Set value using cubic meters per square meter per day units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_meters_per_square_meter_per_hour(self):
        """Set value using cubic meters per square meter per hour units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_meters_per_square_meter_per_minute(self):
        """Set value using cubic meters per square meter per minute units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def cubic_meters_per_square_meter_per_second(self):
        """Set value using cubic meters per square meter per second units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallons_per_square_foot_per_day(self):
        """Set value using gallons per square foot per day units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_left_ft_power_2_tilde_dright(self):
        """Set value using gal /left(ft^{2 ~dright) units (alias for gallons per square foot per day)."""
        return self.gallons_per_square_foot_per_day
    
    @property
    def gal_sqft_da(self):
        """Set value using gal/ sqft/da units (alias for gallons per square foot per day)."""
        return self.gallons_per_square_foot_per_day
    
    @property
    def gallons_per_square_foot_per_hour(self):
        """Set value using gallons per square foot per hour units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_left_ft_power_2_tilde_hright(self):
        """Set value using gal /left(ft^{2 ~hright) units (alias for gallons per square foot per hour)."""
        return self.gallons_per_square_foot_per_hour
    
    @property
    def gal_sqft_hr(self):
        """Set value using gal/ sqft/hr units (alias for gallons per square foot per hour)."""
        return self.gallons_per_square_foot_per_hour
    
    @property
    def gallons_per_square_foot_per_minute(self):
        """Set value using gallons per square foot per minute units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_left_ft_power_2_tilde_minright(self):
        """Set value using gal /left(ft^{2 ~minright) units (alias for gallons per square foot per minute)."""
        return self.gallons_per_square_foot_per_minute
    
    @property
    def gal_sqft_min(self):
        """Set value using gal/ sqft/min units (alias for gallons per square foot per minute)."""
        return self.gallons_per_square_foot_per_minute
    
    @property
    def gpm_sqft(self):
        """Set value using gpm/sqft units (alias for gallons per square foot per minute)."""
        return self.gallons_per_square_foot_per_minute
    
    @property
    def gallons_per_square_foot_per_second(self):
        """Set value using gallons per square foot per second units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_left_ft_power_2_tilde_sright(self):
        """Set value using gal /left(ft^{2 ~sright) units (alias for gallons per square foot per second)."""
        return self.gallons_per_square_foot_per_second
    
    @property
    def gal_sqft_sec(self):
        """Set value using gal/ sqft / sec units (alias for gallons per square foot per second)."""
        return self.gallons_per_square_foot_per_second
    
    @property
    def liters_per_square_meter_per_day(self):
        """Set value using liters per square meter per day units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_day
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_square_meter_per_hour(self):
        """Set value using liters per square meter per hour units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_hour
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_square_meter_per_minute(self):
        """Set value using liters per square meter per minute units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_minute
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_square_meter_per_second(self):
        """Set value using liters per square meter per second units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_second
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

class VolumetricMassFlowRateSetter(TypeSafeSetter):
    """VolumetricMassFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_second_per_cubic_centimeter(self):
        """Set value using gram per second per cubic centimeter units."""
        unit_const = units.VolumetricMassFlowRateUnits.gram_per_second_per_cubic_centimeter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_left_s_cm_power_3right(self):
        """Set value using g /left(s cm^{3right) units (alias for gram per second per cubic centimeter)."""
        return self.gram_per_second_per_cubic_centimeter
    
    @property
    def g_s_cc(self):
        """Set value using g/s/cc units (alias for gram per second per cubic centimeter)."""
        return self.gram_per_second_per_cubic_centimeter
    
    @property
    def g_cc_sec(self):
        """Set value using g / cc / sec units (alias for gram per second per cubic centimeter)."""
        return self.gram_per_second_per_cubic_centimeter
    
    @property
    def kilogram_per_hour_per_cubic_foot(self):
        """Set value using kilogram per hour per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.kilogram_per_hour_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_h_ft_power_3(self):
        """Set value using kg/(h ft { ^{3 ) units (alias for kilogram per hour per cubic foot)."""
        return self.kilogram_per_hour_per_cubic_foot
    
    @property
    def kg_hr_cft(self):
        """Set value using kg/hr/ cft units (alias for kilogram per hour per cubic foot)."""
        return self.kilogram_per_hour_per_cubic_foot
    
    @property
    def kilogram_per_hour_per_cubic_meter(self):
        """Set value using kilogram per hour per cubic meter units."""
        unit_const = units.VolumetricMassFlowRateUnits.kilogram_per_hour_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_h_m3(self):
        """Set value using kg/(h m3) units (alias for kilogram per hour per cubic meter)."""
        return self.kilogram_per_hour_per_cubic_meter
    
    @property
    def kg_hr_cu_m(self):
        """Set value using kg/hr/ cu.m units (alias for kilogram per hour per cubic meter)."""
        return self.kilogram_per_hour_per_cubic_meter
    
    @property
    def kilogram_per_second_per_cubic_meter(self):
        """Set value using kilogram per second per cubic meter units."""
        unit_const = units.VolumetricMassFlowRateUnits.kilogram_per_second_per_cubic_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_left_s_m_power_3right(self):
        """Set value using kg /left(s m^{3right) units (alias for kilogram per second per cubic meter)."""
        return self.kilogram_per_second_per_cubic_meter
    
    @property
    def kg_sec_cu_m(self):
        """Set value using kg/sec/ cu.m units (alias for kilogram per second per cubic meter)."""
        return self.kilogram_per_second_per_cubic_meter
    
    @property
    def pound_per_hour_per_cubic_foot(self):
        """Set value using pound per hour per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.pound_per_hour_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_left_h_ft_power_3right(self):
        """Set value using lb /left(h ft^{3right) units (alias for pound per hour per cubic foot)."""
        return self.pound_per_hour_per_cubic_foot
    
    @property
    def lb_hr_cft(self):
        """Set value using lb / hr / cft units (alias for pound per hour per cubic foot)."""
        return self.pound_per_hour_per_cubic_foot
    
    @property
    def PPH_cft(self):
        """Set value using PPH/cft units (alias for pound per hour per cubic foot)."""
        return self.pound_per_hour_per_cubic_foot
    
    @property
    def pound_per_minute_per_cubic_foot(self):
        """Set value using pound per minute per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.pound_per_minute_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_min_ft_power_3(self):
        """Set value using lb/(min ft^{3 ) units (alias for pound per minute per cubic foot)."""
        return self.pound_per_minute_per_cubic_foot
    
    @property
    def lb_min_cft(self):
        """Set value using lb/ min / cft units (alias for pound per minute per cubic foot)."""
        return self.pound_per_minute_per_cubic_foot
    
    @property
    def pound_per_second_per_cubic_foot(self):
        """Set value using pound per second per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.pound_per_second_per_cubic_foot
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def b_s_ft_power_3(self):
        """Set value using b/(s ft { ^{3 ) units (alias for pound per second per cubic foot)."""
        return self.pound_per_second_per_cubic_foot
    
    @property
    def lb_sec_cft(self):
        """Set value using lb/sec/cft units (alias for pound per second per cubic foot)."""
        return self.pound_per_second_per_cubic_foot
    

class WavenumberSetter(TypeSafeSetter):
    """Wavenumber-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def diopter(self):
        """Set value using diopter units."""
        unit_const = units.WavenumberUnits.diopter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def D(self):
        """Set value using D units (alias for diopter)."""
        return self.diopter
    
    @property
    def kayser(self):
        """Set value using kayser units."""
        unit_const = units.WavenumberUnits.kayser
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    
    @property
    def K(self):
        """Set value using K units (alias for kayser)."""
        return self.kayser
    
    @property
    def reciprocal_meter(self):
        """Set value using reciprocal meter units."""
        unit_const = units.WavenumberUnits.reciprocal_meter
        self.variable.quantity = FastQuantity(self.value, unit_const)
        return self.variable
    

# ===== VARIABLE CLASSES =====
# Static variable class definitions with __slots__ optimization

class AbsorbedDose(TypedVariable):
    """Type-safe absorbeddose variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AbsorbedDoseSetter
    _expected_dimension = ABSORBED_DOSE
    
    def set(self, value: float) -> AbsorbedDoseSetter:
        """Create a setter for this variable."""
        return AbsorbedDoseSetter(self, value)
    

class Acceleration(TypedVariable):
    """Type-safe acceleration variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AccelerationSetter
    _expected_dimension = ACCELERATION
    
    def set(self, value: float) -> AccelerationSetter:
        """Create a setter for this variable."""
        return AccelerationSetter(self, value)
    

class ActivationEnergy(TypedVariable):
    """Type-safe activationenergy variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ActivationEnergySetter
    _expected_dimension = ACTIVATION_ENERGY
    
    def set(self, value: float) -> ActivationEnergySetter:
        """Create a setter for this variable."""
        return ActivationEnergySetter(self, value)
    

class AmountOfSubstance(TypedVariable):
    """Type-safe amountofsubstance variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AmountOfSubstanceSetter
    _expected_dimension = AMOUNT_OF_SUBSTANCE
    
    def set(self, value: float) -> AmountOfSubstanceSetter:
        """Create a setter for this variable."""
        return AmountOfSubstanceSetter(self, value)
    

class AnglePlane(TypedVariable):
    """Type-safe angleplane variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AnglePlaneSetter
    _expected_dimension = ANGLE_PLANE
    
    def set(self, value: float) -> AnglePlaneSetter:
        """Create a setter for this variable."""
        return AnglePlaneSetter(self, value)
    

class AngleSolid(TypedVariable):
    """Type-safe anglesolid variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AngleSolidSetter
    _expected_dimension = ANGLE_SOLID
    
    def set(self, value: float) -> AngleSolidSetter:
        """Create a setter for this variable."""
        return AngleSolidSetter(self, value)
    

class AngularAcceleration(TypedVariable):
    """Type-safe angularacceleration variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AngularAccelerationSetter
    _expected_dimension = ANGULAR_ACCELERATION
    
    def set(self, value: float) -> AngularAccelerationSetter:
        """Create a setter for this variable."""
        return AngularAccelerationSetter(self, value)
    

class AngularMomentum(TypedVariable):
    """Type-safe angularmomentum variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AngularMomentumSetter
    _expected_dimension = ANGULAR_MOMENTUM
    
    def set(self, value: float) -> AngularMomentumSetter:
        """Create a setter for this variable."""
        return AngularMomentumSetter(self, value)
    

class Area(TypedVariable):
    """Type-safe area variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AreaSetter
    _expected_dimension = AREA
    
    def set(self, value: float) -> AreaSetter:
        """Create a setter for this variable."""
        return AreaSetter(self, value)
    

class AreaPerUnitVolume(TypedVariable):
    """Type-safe areaperunitvolume variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AreaPerUnitVolumeSetter
    _expected_dimension = AREA_PER_UNIT_VOLUME
    
    def set(self, value: float) -> AreaPerUnitVolumeSetter:
        """Create a setter for this variable."""
        return AreaPerUnitVolumeSetter(self, value)
    

class AtomicWeight(TypedVariable):
    """Type-safe atomicweight variable with expression capabilities."""
    __slots__ = ()
    _setter_class = AtomicWeightSetter
    _expected_dimension = ATOMIC_WEIGHT
    
    def set(self, value: float) -> AtomicWeightSetter:
        """Create a setter for this variable."""
        return AtomicWeightSetter(self, value)
    

class Concentration(TypedVariable):
    """Type-safe concentration variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ConcentrationSetter
    _expected_dimension = CONCENTRATION
    
    def set(self, value: float) -> ConcentrationSetter:
        """Create a setter for this variable."""
        return ConcentrationSetter(self, value)
    

class Dimensionless(TypedVariable):
    """Type-safe dimensionless variable with expression capabilities."""
    __slots__ = ()
    _setter_class = DimensionlessSetter
    _expected_dimension = DIMENSIONLESS
    
    def set(self, value: float) -> DimensionlessSetter:
        """Create a setter for this variable."""
        return DimensionlessSetter(self, value)
    

class DynamicFluidity(TypedVariable):
    """Type-safe dynamicfluidity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = DynamicFluiditySetter
    _expected_dimension = DYNAMIC_FLUIDITY
    
    def set(self, value: float) -> DynamicFluiditySetter:
        """Create a setter for this variable."""
        return DynamicFluiditySetter(self, value)
    

class ElectricCapacitance(TypedVariable):
    """Type-safe electriccapacitance variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricCapacitanceSetter
    _expected_dimension = ELECTRIC_CAPACITANCE
    
    def set(self, value: float) -> ElectricCapacitanceSetter:
        """Create a setter for this variable."""
        return ElectricCapacitanceSetter(self, value)
    

class ElectricCharge(TypedVariable):
    """Type-safe electriccharge variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricChargeSetter
    _expected_dimension = ELECTRIC_CHARGE
    
    def set(self, value: float) -> ElectricChargeSetter:
        """Create a setter for this variable."""
        return ElectricChargeSetter(self, value)
    

class ElectricCurrentIntensity(TypedVariable):
    """Type-safe electriccurrentintensity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricCurrentIntensitySetter
    _expected_dimension = ELECTRIC_CURRENT_INTENSITY
    
    def set(self, value: float) -> ElectricCurrentIntensitySetter:
        """Create a setter for this variable."""
        return ElectricCurrentIntensitySetter(self, value)
    

class ElectricDipoleMoment(TypedVariable):
    """Type-safe electricdipolemoment variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricDipoleMomentSetter
    _expected_dimension = ELECTRIC_DIPOLE_MOMENT
    
    def set(self, value: float) -> ElectricDipoleMomentSetter:
        """Create a setter for this variable."""
        return ElectricDipoleMomentSetter(self, value)
    

class ElectricFieldStrength(TypedVariable):
    """Type-safe electricfieldstrength variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricFieldStrengthSetter
    _expected_dimension = ELECTRIC_FIELD_STRENGTH
    
    def set(self, value: float) -> ElectricFieldStrengthSetter:
        """Create a setter for this variable."""
        return ElectricFieldStrengthSetter(self, value)
    

class ElectricInductance(TypedVariable):
    """Type-safe electricinductance variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricInductanceSetter
    _expected_dimension = ELECTRIC_INDUCTANCE
    
    def set(self, value: float) -> ElectricInductanceSetter:
        """Create a setter for this variable."""
        return ElectricInductanceSetter(self, value)
    

class ElectricPotential(TypedVariable):
    """Type-safe electricpotential variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricPotentialSetter
    _expected_dimension = ELECTRIC_POTENTIAL
    
    def set(self, value: float) -> ElectricPotentialSetter:
        """Create a setter for this variable."""
        return ElectricPotentialSetter(self, value)
    

class ElectricResistance(TypedVariable):
    """Type-safe electricresistance variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricResistanceSetter
    _expected_dimension = ELECTRIC_RESISTANCE
    
    def set(self, value: float) -> ElectricResistanceSetter:
        """Create a setter for this variable."""
        return ElectricResistanceSetter(self, value)
    

class ElectricalConductance(TypedVariable):
    """Type-safe electricalconductance variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricalConductanceSetter
    _expected_dimension = ELECTRICAL_CONDUCTANCE
    
    def set(self, value: float) -> ElectricalConductanceSetter:
        """Create a setter for this variable."""
        return ElectricalConductanceSetter(self, value)
    

class ElectricalPermittivity(TypedVariable):
    """Type-safe electricalpermittivity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricalPermittivitySetter
    _expected_dimension = ELECTRICAL_PERMITTIVITY
    
    def set(self, value: float) -> ElectricalPermittivitySetter:
        """Create a setter for this variable."""
        return ElectricalPermittivitySetter(self, value)
    

class ElectricalResistivity(TypedVariable):
    """Type-safe electricalresistivity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ElectricalResistivitySetter
    _expected_dimension = ELECTRICAL_RESISTIVITY
    
    def set(self, value: float) -> ElectricalResistivitySetter:
        """Create a setter for this variable."""
        return ElectricalResistivitySetter(self, value)
    

class EnergyFlux(TypedVariable):
    """Type-safe energyflux variable with expression capabilities."""
    __slots__ = ()
    _setter_class = EnergyFluxSetter
    _expected_dimension = ENERGY_FLUX
    
    def set(self, value: float) -> EnergyFluxSetter:
        """Create a setter for this variable."""
        return EnergyFluxSetter(self, value)
    

class EnergyHeatWork(TypedVariable):
    """Type-safe energyheatwork variable with expression capabilities."""
    __slots__ = ()
    _setter_class = EnergyHeatWorkSetter
    _expected_dimension = ENERGY_HEAT_WORK
    
    def set(self, value: float) -> EnergyHeatWorkSetter:
        """Create a setter for this variable."""
        return EnergyHeatWorkSetter(self, value)
    

class EnergyPerUnitArea(TypedVariable):
    """Type-safe energyperunitarea variable with expression capabilities."""
    __slots__ = ()
    _setter_class = EnergyPerUnitAreaSetter
    _expected_dimension = ENERGY_PER_UNIT_AREA
    
    def set(self, value: float) -> EnergyPerUnitAreaSetter:
        """Create a setter for this variable."""
        return EnergyPerUnitAreaSetter(self, value)
    

class Force(TypedVariable):
    """Type-safe force variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ForceSetter
    _expected_dimension = FORCE
    
    def set(self, value: float) -> ForceSetter:
        """Create a setter for this variable."""
        return ForceSetter(self, value)
    

class ForceBody(TypedVariable):
    """Type-safe forcebody variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ForceBodySetter
    _expected_dimension = FORCE_BODY
    
    def set(self, value: float) -> ForceBodySetter:
        """Create a setter for this variable."""
        return ForceBodySetter(self, value)
    

class ForcePerUnitMass(TypedVariable):
    """Type-safe forceperunitmass variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ForcePerUnitMassSetter
    _expected_dimension = FORCE_PER_UNIT_MASS
    
    def set(self, value: float) -> ForcePerUnitMassSetter:
        """Create a setter for this variable."""
        return ForcePerUnitMassSetter(self, value)
    

class FrequencyVoltageRatio(TypedVariable):
    """Type-safe frequencyvoltageratio variable with expression capabilities."""
    __slots__ = ()
    _setter_class = FrequencyVoltageRatioSetter
    _expected_dimension = FREQUENCY_VOLTAGE_RATIO
    
    def set(self, value: float) -> FrequencyVoltageRatioSetter:
        """Create a setter for this variable."""
        return FrequencyVoltageRatioSetter(self, value)
    

class FuelConsumption(TypedVariable):
    """Type-safe fuelconsumption variable with expression capabilities."""
    __slots__ = ()
    _setter_class = FuelConsumptionSetter
    _expected_dimension = FUEL_CONSUMPTION
    
    def set(self, value: float) -> FuelConsumptionSetter:
        """Create a setter for this variable."""
        return FuelConsumptionSetter(self, value)
    

class HeatOfCombustion(TypedVariable):
    """Type-safe heatofcombustion variable with expression capabilities."""
    __slots__ = ()
    _setter_class = HeatOfCombustionSetter
    _expected_dimension = HEAT_OF_COMBUSTION
    
    def set(self, value: float) -> HeatOfCombustionSetter:
        """Create a setter for this variable."""
        return HeatOfCombustionSetter(self, value)
    

class HeatOfFusion(TypedVariable):
    """Type-safe heatoffusion variable with expression capabilities."""
    __slots__ = ()
    _setter_class = HeatOfFusionSetter
    _expected_dimension = HEAT_OF_FUSION
    
    def set(self, value: float) -> HeatOfFusionSetter:
        """Create a setter for this variable."""
        return HeatOfFusionSetter(self, value)
    

class HeatOfVaporization(TypedVariable):
    """Type-safe heatofvaporization variable with expression capabilities."""
    __slots__ = ()
    _setter_class = HeatOfVaporizationSetter
    _expected_dimension = HEAT_OF_VAPORIZATION
    
    def set(self, value: float) -> HeatOfVaporizationSetter:
        """Create a setter for this variable."""
        return HeatOfVaporizationSetter(self, value)
    

class HeatTransferCoefficient(TypedVariable):
    """Type-safe heattransfercoefficient variable with expression capabilities."""
    __slots__ = ()
    _setter_class = HeatTransferCoefficientSetter
    _expected_dimension = HEAT_TRANSFER_COEFFICIENT
    
    def set(self, value: float) -> HeatTransferCoefficientSetter:
        """Create a setter for this variable."""
        return HeatTransferCoefficientSetter(self, value)
    

class Illuminance(TypedVariable):
    """Type-safe illuminance variable with expression capabilities."""
    __slots__ = ()
    _setter_class = IlluminanceSetter
    _expected_dimension = ILLUMINANCE
    
    def set(self, value: float) -> IlluminanceSetter:
        """Create a setter for this variable."""
        return IlluminanceSetter(self, value)
    

class KineticEnergyOfTurbulence(TypedVariable):
    """Type-safe kineticenergyofturbulence variable with expression capabilities."""
    __slots__ = ()
    _setter_class = KineticEnergyOfTurbulenceSetter
    _expected_dimension = KINETIC_ENERGY_OF_TURBULENCE
    
    def set(self, value: float) -> KineticEnergyOfTurbulenceSetter:
        """Create a setter for this variable."""
        return KineticEnergyOfTurbulenceSetter(self, value)
    

class Length(TypedVariable):
    """Type-safe length variable with expression capabilities."""
    __slots__ = ()
    _setter_class = LengthSetter
    _expected_dimension = LENGTH
    
    def set(self, value: float) -> LengthSetter:
        """Create a setter for this variable."""
        return LengthSetter(self, value)
    

class LinearMassDensity(TypedVariable):
    """Type-safe linearmassdensity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = LinearMassDensitySetter
    _expected_dimension = LINEAR_MASS_DENSITY
    
    def set(self, value: float) -> LinearMassDensitySetter:
        """Create a setter for this variable."""
        return LinearMassDensitySetter(self, value)
    

class LinearMomentum(TypedVariable):
    """Type-safe linearmomentum variable with expression capabilities."""
    __slots__ = ()
    _setter_class = LinearMomentumSetter
    _expected_dimension = LINEAR_MOMENTUM
    
    def set(self, value: float) -> LinearMomentumSetter:
        """Create a setter for this variable."""
        return LinearMomentumSetter(self, value)
    

class LuminanceSelf(TypedVariable):
    """Type-safe luminanceself variable with expression capabilities."""
    __slots__ = ()
    _setter_class = LuminanceSelfSetter
    _expected_dimension = LUMINANCE_SELF
    
    def set(self, value: float) -> LuminanceSelfSetter:
        """Create a setter for this variable."""
        return LuminanceSelfSetter(self, value)
    

class LuminousFlux(TypedVariable):
    """Type-safe luminousflux variable with expression capabilities."""
    __slots__ = ()
    _setter_class = LuminousFluxSetter
    _expected_dimension = LUMINOUS_FLUX
    
    def set(self, value: float) -> LuminousFluxSetter:
        """Create a setter for this variable."""
        return LuminousFluxSetter(self, value)
    

class LuminousIntensity(TypedVariable):
    """Type-safe luminousintensity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = LuminousIntensitySetter
    _expected_dimension = LUMINOUS_INTENSITY
    
    def set(self, value: float) -> LuminousIntensitySetter:
        """Create a setter for this variable."""
        return LuminousIntensitySetter(self, value)
    

class MagneticField(TypedVariable):
    """Type-safe magneticfield variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MagneticFieldSetter
    _expected_dimension = MAGNETIC_FIELD
    
    def set(self, value: float) -> MagneticFieldSetter:
        """Create a setter for this variable."""
        return MagneticFieldSetter(self, value)
    

class MagneticFlux(TypedVariable):
    """Type-safe magneticflux variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MagneticFluxSetter
    _expected_dimension = MAGNETIC_FLUX
    
    def set(self, value: float) -> MagneticFluxSetter:
        """Create a setter for this variable."""
        return MagneticFluxSetter(self, value)
    

class MagneticInductionFieldStrength(TypedVariable):
    """Type-safe magneticinductionfieldstrength variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MagneticInductionFieldStrengthSetter
    _expected_dimension = MAGNETIC_INDUCTION_FIELD_STRENGTH
    
    def set(self, value: float) -> MagneticInductionFieldStrengthSetter:
        """Create a setter for this variable."""
        return MagneticInductionFieldStrengthSetter(self, value)
    

class MagneticMoment(TypedVariable):
    """Type-safe magneticmoment variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MagneticMomentSetter
    _expected_dimension = MAGNETIC_MOMENT
    
    def set(self, value: float) -> MagneticMomentSetter:
        """Create a setter for this variable."""
        return MagneticMomentSetter(self, value)
    

class MagneticPermeability(TypedVariable):
    """Type-safe magneticpermeability variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MagneticPermeabilitySetter
    _expected_dimension = MAGNETIC_PERMEABILITY
    
    def set(self, value: float) -> MagneticPermeabilitySetter:
        """Create a setter for this variable."""
        return MagneticPermeabilitySetter(self, value)
    

class MagnetomotiveForce(TypedVariable):
    """Type-safe magnetomotiveforce variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MagnetomotiveForceSetter
    _expected_dimension = MAGNETOMOTIVE_FORCE
    
    def set(self, value: float) -> MagnetomotiveForceSetter:
        """Create a setter for this variable."""
        return MagnetomotiveForceSetter(self, value)
    

class Mass(TypedVariable):
    """Type-safe mass variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MassSetter
    _expected_dimension = MASS
    
    def set(self, value: float) -> MassSetter:
        """Create a setter for this variable."""
        return MassSetter(self, value)
    

class MassDensity(TypedVariable):
    """Type-safe massdensity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MassDensitySetter
    _expected_dimension = MASS_DENSITY
    
    def set(self, value: float) -> MassDensitySetter:
        """Create a setter for this variable."""
        return MassDensitySetter(self, value)
    

class MassFlowRate(TypedVariable):
    """Type-safe massflowrate variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MassFlowRateSetter
    _expected_dimension = MASS_FLOW_RATE
    
    def set(self, value: float) -> MassFlowRateSetter:
        """Create a setter for this variable."""
        return MassFlowRateSetter(self, value)
    

class MassFlux(TypedVariable):
    """Type-safe massflux variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MassFluxSetter
    _expected_dimension = MASS_FLUX
    
    def set(self, value: float) -> MassFluxSetter:
        """Create a setter for this variable."""
        return MassFluxSetter(self, value)
    

class MassFractionOfI(TypedVariable):
    """Type-safe massfractionofi variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MassFractionOfISetter
    _expected_dimension = MASS_FRACTION_OF_I
    
    def set(self, value: float) -> MassFractionOfISetter:
        """Create a setter for this variable."""
        return MassFractionOfISetter(self, value)
    

class MassTransferCoefficient(TypedVariable):
    """Type-safe masstransfercoefficient variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MassTransferCoefficientSetter
    _expected_dimension = MASS_TRANSFER_COEFFICIENT
    
    def set(self, value: float) -> MassTransferCoefficientSetter:
        """Create a setter for this variable."""
        return MassTransferCoefficientSetter(self, value)
    

class MolalityOfSoluteI(TypedVariable):
    """Type-safe molalityofsolutei variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MolalityOfSoluteISetter
    _expected_dimension = MOLALITY_OF_SOLUTE_I
    
    def set(self, value: float) -> MolalityOfSoluteISetter:
        """Create a setter for this variable."""
        return MolalityOfSoluteISetter(self, value)
    

class MolarConcentrationByMass(TypedVariable):
    """Type-safe molarconcentrationbymass variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MolarConcentrationByMassSetter
    _expected_dimension = MOLAR_CONCENTRATION_BY_MASS
    
    def set(self, value: float) -> MolarConcentrationByMassSetter:
        """Create a setter for this variable."""
        return MolarConcentrationByMassSetter(self, value)
    

class MolarFlowRate(TypedVariable):
    """Type-safe molarflowrate variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MolarFlowRateSetter
    _expected_dimension = MOLAR_FLOW_RATE
    
    def set(self, value: float) -> MolarFlowRateSetter:
        """Create a setter for this variable."""
        return MolarFlowRateSetter(self, value)
    

class MolarFlux(TypedVariable):
    """Type-safe molarflux variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MolarFluxSetter
    _expected_dimension = MOLAR_FLUX
    
    def set(self, value: float) -> MolarFluxSetter:
        """Create a setter for this variable."""
        return MolarFluxSetter(self, value)
    

class MolarHeatCapacity(TypedVariable):
    """Type-safe molarheatcapacity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MolarHeatCapacitySetter
    _expected_dimension = MOLAR_HEAT_CAPACITY
    
    def set(self, value: float) -> MolarHeatCapacitySetter:
        """Create a setter for this variable."""
        return MolarHeatCapacitySetter(self, value)
    

class MolarityOfI(TypedVariable):
    """Type-safe molarityofi variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MolarityOfISetter
    _expected_dimension = MOLARITY_OF_I
    
    def set(self, value: float) -> MolarityOfISetter:
        """Create a setter for this variable."""
        return MolarityOfISetter(self, value)
    

class MoleFractionOfI(TypedVariable):
    """Type-safe molefractionofi variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MoleFractionOfISetter
    _expected_dimension = MOLE_FRACTION_OF_I
    
    def set(self, value: float) -> MoleFractionOfISetter:
        """Create a setter for this variable."""
        return MoleFractionOfISetter(self, value)
    

class MomentOfInertia(TypedVariable):
    """Type-safe momentofinertia variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MomentOfInertiaSetter
    _expected_dimension = MOMENT_OF_INERTIA
    
    def set(self, value: float) -> MomentOfInertiaSetter:
        """Create a setter for this variable."""
        return MomentOfInertiaSetter(self, value)
    

class MomentumFlowRate(TypedVariable):
    """Type-safe momentumflowrate variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MomentumFlowRateSetter
    _expected_dimension = MOMENTUM_FLOW_RATE
    
    def set(self, value: float) -> MomentumFlowRateSetter:
        """Create a setter for this variable."""
        return MomentumFlowRateSetter(self, value)
    

class MomentumFlux(TypedVariable):
    """Type-safe momentumflux variable with expression capabilities."""
    __slots__ = ()
    _setter_class = MomentumFluxSetter
    _expected_dimension = MOMENTUM_FLUX
    
    def set(self, value: float) -> MomentumFluxSetter:
        """Create a setter for this variable."""
        return MomentumFluxSetter(self, value)
    

class NormalityOfSolution(TypedVariable):
    """Type-safe normalityofsolution variable with expression capabilities."""
    __slots__ = ()
    _setter_class = NormalityOfSolutionSetter
    _expected_dimension = NORMALITY_OF_SOLUTION
    
    def set(self, value: float) -> NormalityOfSolutionSetter:
        """Create a setter for this variable."""
        return NormalityOfSolutionSetter(self, value)
    

class ParticleDensity(TypedVariable):
    """Type-safe particledensity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ParticleDensitySetter
    _expected_dimension = PARTICLE_DENSITY
    
    def set(self, value: float) -> ParticleDensitySetter:
        """Create a setter for this variable."""
        return ParticleDensitySetter(self, value)
    

class Percent(TypedVariable):
    """Type-safe percent variable with expression capabilities."""
    __slots__ = ()
    _setter_class = PercentSetter
    _expected_dimension = PERCENT
    
    def set(self, value: float) -> PercentSetter:
        """Create a setter for this variable."""
        return PercentSetter(self, value)
    

class Permeability(TypedVariable):
    """Type-safe permeability variable with expression capabilities."""
    __slots__ = ()
    _setter_class = PermeabilitySetter
    _expected_dimension = PERMEABILITY
    
    def set(self, value: float) -> PermeabilitySetter:
        """Create a setter for this variable."""
        return PermeabilitySetter(self, value)
    

class PhotonEmissionRate(TypedVariable):
    """Type-safe photonemissionrate variable with expression capabilities."""
    __slots__ = ()
    _setter_class = PhotonEmissionRateSetter
    _expected_dimension = PHOTON_EMISSION_RATE
    
    def set(self, value: float) -> PhotonEmissionRateSetter:
        """Create a setter for this variable."""
        return PhotonEmissionRateSetter(self, value)
    

class PowerPerUnitMass(TypedVariable):
    """Type-safe powerperunitmass variable with expression capabilities."""
    __slots__ = ()
    _setter_class = PowerPerUnitMassSetter
    _expected_dimension = POWER_PER_UNIT_MASS
    
    def set(self, value: float) -> PowerPerUnitMassSetter:
        """Create a setter for this variable."""
        return PowerPerUnitMassSetter(self, value)
    

class PowerPerUnitVolume(TypedVariable):
    """Type-safe powerperunitvolume variable with expression capabilities."""
    __slots__ = ()
    _setter_class = PowerPerUnitVolumeSetter
    _expected_dimension = POWER_PER_UNIT_VOLUME
    
    def set(self, value: float) -> PowerPerUnitVolumeSetter:
        """Create a setter for this variable."""
        return PowerPerUnitVolumeSetter(self, value)
    

class PowerThermalDuty(TypedVariable):
    """Type-safe powerthermalduty variable with expression capabilities."""
    __slots__ = ()
    _setter_class = PowerThermalDutySetter
    _expected_dimension = POWER_THERMAL_DUTY
    
    def set(self, value: float) -> PowerThermalDutySetter:
        """Create a setter for this variable."""
        return PowerThermalDutySetter(self, value)
    

class Pressure(TypedVariable):
    """Type-safe pressure variable with expression capabilities."""
    __slots__ = ()
    _setter_class = PressureSetter
    _expected_dimension = PRESSURE
    
    def set(self, value: float) -> PressureSetter:
        """Create a setter for this variable."""
        return PressureSetter(self, value)
    

class RadiationDoseEquivalent(TypedVariable):
    """Type-safe radiationdoseequivalent variable with expression capabilities."""
    __slots__ = ()
    _setter_class = RadiationDoseEquivalentSetter
    _expected_dimension = RADIATION_DOSE_EQUIVALENT
    
    def set(self, value: float) -> RadiationDoseEquivalentSetter:
        """Create a setter for this variable."""
        return RadiationDoseEquivalentSetter(self, value)
    

class RadiationExposure(TypedVariable):
    """Type-safe radiationexposure variable with expression capabilities."""
    __slots__ = ()
    _setter_class = RadiationExposureSetter
    _expected_dimension = RADIATION_EXPOSURE
    
    def set(self, value: float) -> RadiationExposureSetter:
        """Create a setter for this variable."""
        return RadiationExposureSetter(self, value)
    

class Radioactivity(TypedVariable):
    """Type-safe radioactivity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = RadioactivitySetter
    _expected_dimension = RADIOACTIVITY
    
    def set(self, value: float) -> RadioactivitySetter:
        """Create a setter for this variable."""
        return RadioactivitySetter(self, value)
    

class SecondMomentOfArea(TypedVariable):
    """Type-safe secondmomentofarea variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SecondMomentOfAreaSetter
    _expected_dimension = SECOND_MOMENT_OF_AREA
    
    def set(self, value: float) -> SecondMomentOfAreaSetter:
        """Create a setter for this variable."""
        return SecondMomentOfAreaSetter(self, value)
    

class SecondRadiationConstantPlanck(TypedVariable):
    """Type-safe secondradiationconstantplanck variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SecondRadiationConstantPlanckSetter
    _expected_dimension = SECOND_RADIATION_CONSTANT_PLANCK
    
    def set(self, value: float) -> SecondRadiationConstantPlanckSetter:
        """Create a setter for this variable."""
        return SecondRadiationConstantPlanckSetter(self, value)
    

class SpecificEnthalpy(TypedVariable):
    """Type-safe specificenthalpy variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SpecificEnthalpySetter
    _expected_dimension = SPECIFIC_ENTHALPY
    
    def set(self, value: float) -> SpecificEnthalpySetter:
        """Create a setter for this variable."""
        return SpecificEnthalpySetter(self, value)
    

class SpecificGravity(TypedVariable):
    """Type-safe specificgravity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SpecificGravitySetter
    _expected_dimension = SPECIFIC_GRAVITY
    
    def set(self, value: float) -> SpecificGravitySetter:
        """Create a setter for this variable."""
        return SpecificGravitySetter(self, value)
    

class SpecificHeatCapacityConstantPressure(TypedVariable):
    """Type-safe specificheatcapacityconstantpressure variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SpecificHeatCapacityConstantPressureSetter
    _expected_dimension = SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE
    
    def set(self, value: float) -> SpecificHeatCapacityConstantPressureSetter:
        """Create a setter for this variable."""
        return SpecificHeatCapacityConstantPressureSetter(self, value)
    

class SpecificLength(TypedVariable):
    """Type-safe specificlength variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SpecificLengthSetter
    _expected_dimension = SPECIFIC_LENGTH
    
    def set(self, value: float) -> SpecificLengthSetter:
        """Create a setter for this variable."""
        return SpecificLengthSetter(self, value)
    

class SpecificSurface(TypedVariable):
    """Type-safe specificsurface variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SpecificSurfaceSetter
    _expected_dimension = SPECIFIC_SURFACE
    
    def set(self, value: float) -> SpecificSurfaceSetter:
        """Create a setter for this variable."""
        return SpecificSurfaceSetter(self, value)
    

class SpecificVolume(TypedVariable):
    """Type-safe specificvolume variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SpecificVolumeSetter
    _expected_dimension = SPECIFIC_VOLUME
    
    def set(self, value: float) -> SpecificVolumeSetter:
        """Create a setter for this variable."""
        return SpecificVolumeSetter(self, value)
    

class Stress(TypedVariable):
    """Type-safe stress variable with expression capabilities."""
    __slots__ = ()
    _setter_class = StressSetter
    _expected_dimension = STRESS
    
    def set(self, value: float) -> StressSetter:
        """Create a setter for this variable."""
        return StressSetter(self, value)
    

class SurfaceMassDensity(TypedVariable):
    """Type-safe surfacemassdensity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SurfaceMassDensitySetter
    _expected_dimension = SURFACE_MASS_DENSITY
    
    def set(self, value: float) -> SurfaceMassDensitySetter:
        """Create a setter for this variable."""
        return SurfaceMassDensitySetter(self, value)
    

class SurfaceTension(TypedVariable):
    """Type-safe surfacetension variable with expression capabilities."""
    __slots__ = ()
    _setter_class = SurfaceTensionSetter
    _expected_dimension = SURFACE_TENSION
    
    def set(self, value: float) -> SurfaceTensionSetter:
        """Create a setter for this variable."""
        return SurfaceTensionSetter(self, value)
    

class Temperature(TypedVariable):
    """Type-safe temperature variable with expression capabilities."""
    __slots__ = ()
    _setter_class = TemperatureSetter
    _expected_dimension = TEMPERATURE
    
    def set(self, value: float) -> TemperatureSetter:
        """Create a setter for this variable."""
        return TemperatureSetter(self, value)
    

class ThermalConductivity(TypedVariable):
    """Type-safe thermalconductivity variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ThermalConductivitySetter
    _expected_dimension = THERMAL_CONDUCTIVITY
    
    def set(self, value: float) -> ThermalConductivitySetter:
        """Create a setter for this variable."""
        return ThermalConductivitySetter(self, value)
    

class Time(TypedVariable):
    """Type-safe time variable with expression capabilities."""
    __slots__ = ()
    _setter_class = TimeSetter
    _expected_dimension = TIME
    
    def set(self, value: float) -> TimeSetter:
        """Create a setter for this variable."""
        return TimeSetter(self, value)
    

class Torque(TypedVariable):
    """Type-safe torque variable with expression capabilities."""
    __slots__ = ()
    _setter_class = TorqueSetter
    _expected_dimension = TORQUE
    
    def set(self, value: float) -> TorqueSetter:
        """Create a setter for this variable."""
        return TorqueSetter(self, value)
    

class TurbulenceEnergyDissipationRate(TypedVariable):
    """Type-safe turbulenceenergydissipationrate variable with expression capabilities."""
    __slots__ = ()
    _setter_class = TurbulenceEnergyDissipationRateSetter
    _expected_dimension = TURBULENCE_ENERGY_DISSIPATION_RATE
    
    def set(self, value: float) -> TurbulenceEnergyDissipationRateSetter:
        """Create a setter for this variable."""
        return TurbulenceEnergyDissipationRateSetter(self, value)
    

class VelocityAngular(TypedVariable):
    """Type-safe velocityangular variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VelocityAngularSetter
    _expected_dimension = VELOCITY_ANGULAR
    
    def set(self, value: float) -> VelocityAngularSetter:
        """Create a setter for this variable."""
        return VelocityAngularSetter(self, value)
    

class VelocityLinear(TypedVariable):
    """Type-safe velocitylinear variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VelocityLinearSetter
    _expected_dimension = VELOCITY_LINEAR
    
    def set(self, value: float) -> VelocityLinearSetter:
        """Create a setter for this variable."""
        return VelocityLinearSetter(self, value)
    

class ViscosityDynamic(TypedVariable):
    """Type-safe viscositydynamic variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ViscosityDynamicSetter
    _expected_dimension = VISCOSITY_DYNAMIC
    
    def set(self, value: float) -> ViscosityDynamicSetter:
        """Create a setter for this variable."""
        return ViscosityDynamicSetter(self, value)
    

class ViscosityKinematic(TypedVariable):
    """Type-safe viscositykinematic variable with expression capabilities."""
    __slots__ = ()
    _setter_class = ViscosityKinematicSetter
    _expected_dimension = VISCOSITY_KINEMATIC
    
    def set(self, value: float) -> ViscosityKinematicSetter:
        """Create a setter for this variable."""
        return ViscosityKinematicSetter(self, value)
    

class Volume(TypedVariable):
    """Type-safe volume variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VolumeSetter
    _expected_dimension = VOLUME
    
    def set(self, value: float) -> VolumeSetter:
        """Create a setter for this variable."""
        return VolumeSetter(self, value)
    

class VolumeFractionOfI(TypedVariable):
    """Type-safe volumefractionofi variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VolumeFractionOfISetter
    _expected_dimension = VOLUME_FRACTION_OF_I
    
    def set(self, value: float) -> VolumeFractionOfISetter:
        """Create a setter for this variable."""
        return VolumeFractionOfISetter(self, value)
    

class VolumetricCalorificHeatingValue(TypedVariable):
    """Type-safe volumetriccalorificheatingvalue variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VolumetricCalorificHeatingValueSetter
    _expected_dimension = VOLUMETRIC_CALORIFIC_HEATING_VALUE
    
    def set(self, value: float) -> VolumetricCalorificHeatingValueSetter:
        """Create a setter for this variable."""
        return VolumetricCalorificHeatingValueSetter(self, value)
    

class VolumetricCoefficientOfExpansion(TypedVariable):
    """Type-safe volumetriccoefficientofexpansion variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VolumetricCoefficientOfExpansionSetter
    _expected_dimension = VOLUMETRIC_COEFFICIENT_OF_EXPANSION
    
    def set(self, value: float) -> VolumetricCoefficientOfExpansionSetter:
        """Create a setter for this variable."""
        return VolumetricCoefficientOfExpansionSetter(self, value)
    

class VolumetricFlowRate(TypedVariable):
    """Type-safe volumetricflowrate variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VolumetricFlowRateSetter
    _expected_dimension = VOLUMETRIC_FLOW_RATE
    
    def set(self, value: float) -> VolumetricFlowRateSetter:
        """Create a setter for this variable."""
        return VolumetricFlowRateSetter(self, value)
    

class VolumetricFlux(TypedVariable):
    """Type-safe volumetricflux variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VolumetricFluxSetter
    _expected_dimension = VOLUMETRIC_FLUX
    
    def set(self, value: float) -> VolumetricFluxSetter:
        """Create a setter for this variable."""
        return VolumetricFluxSetter(self, value)
    

class VolumetricMassFlowRate(TypedVariable):
    """Type-safe volumetricmassflowrate variable with expression capabilities."""
    __slots__ = ()
    _setter_class = VolumetricMassFlowRateSetter
    _expected_dimension = VOLUMETRIC_MASS_FLOW_RATE
    
    def set(self, value: float) -> VolumetricMassFlowRateSetter:
        """Create a setter for this variable."""
        return VolumetricMassFlowRateSetter(self, value)
    

class Wavenumber(TypedVariable):
    """Type-safe wavenumber variable with expression capabilities."""
    __slots__ = ()
    _setter_class = WavenumberSetter
    _expected_dimension = WAVENUMBER
    
    def set(self, value: float) -> WavenumberSetter:
        """Create a setter for this variable."""
        return WavenumberSetter(self, value)
    

# Utility functions
def convert_unit_name_to_property(unit_name: str) -> str:
    """Convert unit name to property name without automatic pluralization."""
    import re
    property_name = (unit_name.replace("-", "_")
                              .replace(" ", "_")
                              .replace(".", "_")
                              .replace("(", "_")
                              .replace(")", "_")
                              .replace(",", "_")
                              .replace("'", "_")
                              .replace("\"", "_")
                              .replace("/", "_")
                              .replace("\\", "_")
                              .replace("°", "_degree_")
                              .replace("²", "_square_")
                              .replace("³", "_cubic_")
                              .replace("μ", "u")
                              .replace("Ω", "ohm")
                              .replace("$", "_")
                              .replace("{", "_")
                              .replace("}", "_")
                              .replace("[", "_")
                              .replace("]", "_")
                              .replace("=", "_eq_")
                              .replace("+", "_plus_")
                              .replace("*", "_star_")
                              .replace("&", "_and_")
                              .replace("%", "_percent_")
                              .replace("#", "_hash_")
                              .replace("@", "_at_")
                              .replace("!", "_excl_")
                              .replace("?", "_quest_")
                              .replace("<", "_lt_")
                              .replace(">", "_gt_")
                              .replace("^", "_power_")
                              .replace("~", "_tilde_")
                              .replace("`", "_backtick_")
                              .replace("|", "_pipe_"))
    property_name = re.sub(r"_+", "_", property_name).strip("_")
    reserved_words = {"class", "def", "if", "else", "for", "while", "import", "from", "as", "in", "or", "and", "not"}
    if property_name in reserved_words:
        property_name = f"{property_name}_unit"
    if property_name and not (property_name[0].isalpha() or property_name[0] == "_"):
        property_name = f"unit_{property_name}"
    return property_name

