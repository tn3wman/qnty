"""
Setter Classes Module - Static Edition
======================================

Static setter class definitions for maximum import performance.
Provides fluent API unit properties for all variable types.
Auto-generated from unit_data.json.
"""

from ..quantities.quantity import Quantity, TypeSafeSetter
from . import units

# ===== SETTER CLASSES =====
# Static setter class definitions with __slots__ optimization

class AbsorbedDoseSetter(TypeSafeSetter):
    """AbsorbedDose-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def erg_per_gram(self):
        """Set value using erg per gram units."""
        unit_const = units.AbsorbedDoseUnits.erg_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def erg_g(self):
        """Set value using erg_g units (alias for erg_per_gram)."""
        return self.erg_per_gram
    
    @property
    def erg_per_g(self):
        """Set value using erg_per_g units (alias for erg_per_gram)."""
        return self.erg_per_gram
    
    @property
    def gram_rad(self):
        """Set value using gram-rad units."""
        unit_const = units.AbsorbedDoseUnits.gram_rad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_rad(self):
        """Set value using g_rad units (alias for gram_rad)."""
        return self.gram_rad
    
    @property
    def gray(self):
        """Set value using gray units."""
        unit_const = units.AbsorbedDoseUnits.gray
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Gy(self):
        """Set value using Gy units (alias for gray)."""
        return self.gray
    
    @property
    def rad(self):
        """Set value using rad units."""
        unit_const = units.AbsorbedDoseUnits.rad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def milligray(self):
        """Set value using milligray units."""
        unit_const = units.AbsorbedDoseUnits.milligray
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mGy(self):
        """Set value using mGy units (alias for milligray)."""
        return self.milligray
    
    @property
    def microgray(self):
        """Set value using microgray units."""
        unit_const = units.AbsorbedDoseUnits.microgray
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class AccelerationSetter(TypeSafeSetter):
    """Acceleration-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def meter_per_second_squared(self):
        """Set value using meter per second squared units."""
        unit_const = units.AccelerationUnits.meter_per_second_squared
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_mathrm_s_2(self):
        """Set value using mathrm_m_mathrm_s_2 units (alias for meter_per_second_squared)."""
        return self.meter_per_second_squared
    
    @property
    def m_per_s2(self):
        """Set value using m_per_s2 units (alias for meter_per_second_squared)."""
        return self.meter_per_second_squared
    
    @property
    def foot_per_second_squared(self):
        """Set value using foot per second squared units."""
        unit_const = units.AccelerationUnits.foot_per_second_squared
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_s_2_or_mathrm_ft_mathrm_sec_2(self):
        """Set value using mathrm_ft_mathrm_s_2_or_mathrm_ft_mathrm_sec_2 units (alias for foot_per_second_squared)."""
        return self.foot_per_second_squared
    
    @property
    def ft_per_s2(self):
        """Set value using ft_per_s2 units (alias for foot_per_second_squared)."""
        return self.foot_per_second_squared
    
    @property
    def fps2(self):
        """Set value using fps2 units (alias for foot_per_second_squared)."""
        return self.foot_per_second_squared
    

class ActivationEnergySetter(TypeSafeSetter):
    """ActivationEnergy-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def btu_per_pound_mole(self):
        """Set value using Btu per pound mole units."""
        unit_const = units.ActivationEnergyUnits.btu_per_pound_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_lb_mol(self):
        """Set value using Btu_lb_mol units (alias for btu_per_pound_mole)."""
        return self.btu_per_pound_mole
    
    @property
    def btu_per_lbmol(self):
        """Set value using btu_per_lbmol units (alias for btu_per_pound_mole)."""
        return self.btu_per_pound_mole
    
    @property
    def calorie_mean_per_gram_mole(self):
        """Set value using calorie (mean) per gram mole units."""
        unit_const = units.ActivationEnergyUnits.calorie_mean_per_gram_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_mol(self):
        """Set value using cal_mol units (alias for calorie_mean_per_gram_mole)."""
        return self.calorie_mean_per_gram_mole
    
    @property
    def cal_mean_per_gmol(self):
        """Set value using cal_mean_per_gmol units (alias for calorie_mean_per_gram_mole)."""
        return self.calorie_mean_per_gram_mole
    
    @property
    def joule_per_gram_mole(self):
        """Set value using joule per gram mole units."""
        unit_const = units.ActivationEnergyUnits.joule_per_gram_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_mol(self):
        """Set value using J_mol units (alias for joule_per_gram_mole)."""
        return self.joule_per_gram_mole
    
    @property
    def joule_per_kilogram_mole(self):
        """Set value using joule per kilogram mole units."""
        unit_const = units.ActivationEnergyUnits.joule_per_kilogram_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_kmol(self):
        """Set value using J_kmol units (alias for joule_per_kilogram_mole)."""
        return self.joule_per_kilogram_mole
    
    @property
    def kilocalorie_per_kilogram_mole(self):
        """Set value using kilocalorie per kilogram mole units."""
        unit_const = units.ActivationEnergyUnits.kilocalorie_per_kilogram_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_kmol(self):
        """Set value using kcal_kmol units (alias for kilocalorie_per_kilogram_mole)."""
        return self.kilocalorie_per_kilogram_mole
    

class AmountOfSubstanceSetter(TypeSafeSetter):
    """AmountOfSubstance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kilogram_mol(self):
        """Set value using kilogram mol or kmol units."""
        unit_const = units.AmountOfSubstanceUnits.kilogram_mol
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol(self):
        """Set value using kmol units (alias for kilogram_mol)."""
        return self.kilogram_mol
    
    @property
    def mole(self):
        """Set value using mole (gram) units."""
        unit_const = units.AmountOfSubstanceUnits.mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol(self):
        """Set value using mol units (alias for mole)."""
        return self.mole
    
    @property
    def pound_mole(self):
        """Set value using pound-mole units."""
        unit_const = units.AmountOfSubstanceUnits.pound_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_or_mole(self):
        """Set value using lb_mol_or_mole units (alias for pound_mole)."""
        return self.pound_mole
    
    @property
    def lb_mol(self):
        """Set value using lb_mol units (alias for pound_mole)."""
        return self.pound_mole
    
    @property
    def millimole(self):
        """Set value using millimole (gram) units."""
        unit_const = units.AmountOfSubstanceUnits.millimole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mmol(self):
        """Set value using mmol units (alias for millimole)."""
        return self.millimole
    
    @property
    def micromole(self):
        """Set value using micromole (gram) units."""
        unit_const = units.AmountOfSubstanceUnits.micromole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class AnglePlaneSetter(TypeSafeSetter):
    """AnglePlane-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def degree(self):
        """Set value using degree units."""
        unit_const = units.AnglePlaneUnits.degree
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def circ(self):
        """Set value using circ units (alias for degree)."""
        return self.degree
    
    @property
    def gon(self):
        """Set value using gon units."""
        unit_const = units.AnglePlaneUnits.gon
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def grade(self):
        """Set value using grade units."""
        unit_const = units.AnglePlaneUnits.grade
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def minute_new(self):
        """Set value using minute (new) units."""
        unit_const = units.AnglePlaneUnits.minute_new
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def c(self):
        """Set value using c units (alias for minute_new)."""
        return self.minute_new
    
    @property
    def minute_of_angle(self):
        """Set value using minute of angle units."""
        unit_const = units.AnglePlaneUnits.minute_of_angle
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unnamed(self):
        """Set value using unnamed units (alias for minute_of_angle)."""
        return self.minute_of_angle
    
    @property
    def percent(self):
        """Set value using percent units."""
        unit_const = units.AnglePlaneUnits.percent
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def plane_angle(self):
        """Set value using plane angle units."""
        unit_const = units.AnglePlaneUnits.plane_angle
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def quadrant(self):
        """Set value using quadrant units."""
        unit_const = units.AnglePlaneUnits.quadrant
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def quadr(self):
        """Set value using quadr units (alias for quadrant)."""
        return self.quadrant
    
    @property
    def radian(self):
        """Set value using radian units."""
        unit_const = units.AnglePlaneUnits.radian
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def rad(self):
        """Set value using rad units (alias for radian)."""
        return self.radian
    
    @property
    def right_angle(self):
        """Set value using right angle units."""
        unit_const = units.AnglePlaneUnits.right_angle
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def perp(self):
        """Set value using perp units (alias for right_angle)."""
        return self.right_angle
    
    @property
    def round(self):
        """Set value using round units."""
        unit_const = units.AnglePlaneUnits.round
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def tr_or_r(self):
        """Set value using tr_or_r units (alias for round)."""
        return self.round
    
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cc(self):
        """Set value using cc units (alias for second_new)."""
        return self.second_new
    
    @property
    def second_of_angle(self):
        """Set value using second of angle units."""
        unit_const = units.AnglePlaneUnits.second_of_angle
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def thousandth_us(self):
        """Set value using thousandth (US) units."""
        unit_const = units.AnglePlaneUnits.thousandth_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def US(self):
        """Set value using US units (alias for thousandth_us)."""
        return self.thousandth_us
    
    @property
    def turn(self):
        """Set value using turn units."""
        unit_const = units.AnglePlaneUnits.turn
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def turn_or_rev(self):
        """Set value using turn_or_rev units (alias for turn)."""
        return self.turn
    
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_degree(self):
        """Set value using square degree units."""
        unit_const = units.AngleSolidUnits.square_degree
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def left_circ_right_2(self):
        """Set value using left_circ_right_2 units (alias for square_degree)."""
        return self.square_degree
    
    @property
    def square_gon(self):
        """Set value using square gon units."""
        unit_const = units.AngleSolidUnits.square_gon
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_2(self):
        """Set value using g_2 units (alias for square_gon)."""
        return self.square_gon
    
    @property
    def steradian(self):
        """Set value using steradian units."""
        unit_const = units.AngleSolidUnits.steradian
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_rad_mathrm_s_2(self):
        """Set value using mathrm_rad_mathrm_s_2 units (alias for radian_per_second_squared)."""
        return self.radian_per_second_squared
    
    @property
    def revolution_per_second_squared(self):
        """Set value using revolution per second squared units."""
        unit_const = units.AngularAccelerationUnits.revolution_per_second_squared
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_rev_mathrm_sec_2(self):
        """Set value using mathrm_rev_mathrm_sec_2 units (alias for revolution_per_second_squared)."""
        return self.revolution_per_second_squared
    
    @property
    def rpm_or_revolution_per_minute(self):
        """Set value using rpm (or revolution per minute) per minute units."""
        unit_const = units.AngularAccelerationUnits.rpm_or_revolution_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_rev_mathrm_min_2_or_rpm_min(self):
        """Set value using mathrm_rev_mathrm_min_2_or_rpm_min units (alias for rpm_or_revolution_per_minute)."""
        return self.rpm_or_revolution_per_minute
    
    @property
    def rev_min_2(self):
        """Set value using rev_min_2 units (alias for rpm_or_revolution_per_minute)."""
        return self.rpm_or_revolution_per_minute
    
    @property
    def rpm_min(self):
        """Set value using rpm_min units (alias for rpm_or_revolution_per_minute)."""
        return self.rpm_or_revolution_per_minute
    

class AngularMomentumSetter(TypeSafeSetter):
    """AngularMomentum-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_centimeter_squared_per_second(self):
        """Set value using gram centimeter squared per second units."""
        unit_const = units.AngularMomentumUnits.gram_centimeter_squared_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_cm_2_mathrm_s(self):
        """Set value using mathrm_g_mathrm_cm_2_mathrm_s units (alias for gram_centimeter_squared_per_second)."""
        return self.gram_centimeter_squared_per_second
    
    @property
    def kilogram_meter_squared_per_second(self):
        """Set value using kilogram meter squared per second units."""
        unit_const = units.AngularMomentumUnits.kilogram_meter_squared_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_2_mathrm_s(self):
        """Set value using mathrm_kg_mathrm_m_2_mathrm_s units (alias for kilogram_meter_squared_per_second)."""
        return self.kilogram_meter_squared_per_second
    
    @property
    def pound_force_square_foot_per_second(self):
        """Set value using pound force square foot per second units."""
        unit_const = units.AngularMomentumUnits.pound_force_square_foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft_2_mathrm_sec(self):
        """Set value using lb_ft_2_mathrm_sec units (alias for pound_force_square_foot_per_second)."""
        return self.pound_force_square_foot_per_second
    

class AreaSetter(TypeSafeSetter):
    """Area-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def acre_general(self):
        """Set value using acre (general) units."""
        unit_const = units.AreaUnits.acre_general
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ac(self):
        """Set value using ac units (alias for acre_general)."""
        return self.acre_general
    
    @property
    def are(self):
        """Set value using are units."""
        unit_const = units.AreaUnits.are
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def a(self):
        """Set value using a units (alias for are)."""
        return self.are
    
    @property
    def arpent_quebec(self):
        """Set value using arpent (Quebec) units."""
        unit_const = units.AreaUnits.arpent_quebec
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def arp(self):
        """Set value using arp units (alias for arpent_quebec)."""
        return self.arpent_quebec
    
    @property
    def barn(self):
        """Set value using barn units."""
        unit_const = units.AreaUnits.barn
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def b(self):
        """Set value using b units (alias for barn)."""
        return self.barn
    
    @property
    def circular_inch(self):
        """Set value using circular inch units."""
        unit_const = units.AreaUnits.circular_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cin(self):
        """Set value using cin units (alias for circular_inch)."""
        return self.circular_inch
    
    @property
    def circular_mil(self):
        """Set value using circular mil units."""
        unit_const = units.AreaUnits.circular_mil
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cmil(self):
        """Set value using cmil units (alias for circular_mil)."""
        return self.circular_mil
    
    @property
    def hectare(self):
        """Set value using hectare units."""
        unit_const = units.AreaUnits.hectare
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ha(self):
        """Set value using ha units (alias for hectare)."""
        return self.hectare
    
    @property
    def shed(self):
        """Set value using shed units."""
        unit_const = units.AreaUnits.shed
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_centimeter(self):
        """Set value using square centimeter units."""
        unit_const = units.AreaUnits.square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_2(self):
        """Set value using mathrm_cm_2 units (alias for square_centimeter)."""
        return self.square_centimeter
    
    @property
    def square_chain_ramsden(self):
        """Set value using square chain (Ramsden) units."""
        unit_const = units.AreaUnits.square_chain_ramsden
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_ch_Rams(self):
        """Set value using sq_ch_Rams units (alias for square_chain_ramsden)."""
        return self.square_chain_ramsden
    
    @property
    def square_chain_survey_gunters(self):
        """Set value using square chain (Survey, Gunter's) units."""
        unit_const = units.AreaUnits.square_chain_survey_gunters
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_ch_surv(self):
        """Set value using sq_ch_surv units (alias for square_chain_survey_gunters)."""
        return self.square_chain_survey_gunters
    
    @property
    def square_decimeter(self):
        """Set value using square decimeter units."""
        unit_const = units.AreaUnits.square_decimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_dm_2(self):
        """Set value using mathrm_dm_2 units (alias for square_decimeter)."""
        return self.square_decimeter
    
    @property
    def square_fermi(self):
        """Set value using square fermi units."""
        unit_const = units.AreaUnits.square_fermi
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_F_2(self):
        """Set value using mathrm_F_2 units (alias for square_fermi)."""
        return self.square_fermi
    
    @property
    def square_foot(self):
        """Set value using square foot units."""
        unit_const = units.AreaUnits.square_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_ft_or_ft_2(self):
        """Set value using sq_ft_or_ft_2 units (alias for square_foot)."""
        return self.square_foot
    
    @property
    def sq_ft(self):
        """Set value using sq_ft units (alias for square_foot)."""
        return self.square_foot
    
    @property
    def ft_2(self):
        """Set value using ft_2 units (alias for square_foot)."""
        return self.square_foot
    
    @property
    def square_hectometer(self):
        """Set value using square hectometer units."""
        unit_const = units.AreaUnits.square_hectometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_hm_2(self):
        """Set value using mathrm_hm_2 units (alias for square_hectometer)."""
        return self.square_hectometer
    
    @property
    def square_inch(self):
        """Set value using square inch units."""
        unit_const = units.AreaUnits.square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_in_or_in_2(self):
        """Set value using sq_in_or_in_2 units (alias for square_inch)."""
        return self.square_inch
    
    @property
    def sq_in(self):
        """Set value using sq_in units (alias for square_inch)."""
        return self.square_inch
    
    @property
    def in_2(self):
        """Set value using in_2 units (alias for square_inch)."""
        return self.square_inch
    
    @property
    def square_kilometer(self):
        """Set value using square kilometer units."""
        unit_const = units.AreaUnits.square_kilometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_km_2(self):
        """Set value using mathrm_km_2 units (alias for square_kilometer)."""
        return self.square_kilometer
    
    @property
    def square_league_statute(self):
        """Set value using square league (statute) units."""
        unit_const = units.AreaUnits.square_league_statute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_lg_stat(self):
        """Set value using sq_lg_stat units (alias for square_league_statute)."""
        return self.square_league_statute
    
    @property
    def square_meter(self):
        """Set value using square meter units."""
        unit_const = units.AreaUnits.square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2(self):
        """Set value using mathrm_m_2 units (alias for square_meter)."""
        return self.square_meter
    
    @property
    def square_micron(self):
        """Set value using square micron units."""
        unit_const = units.AreaUnits.square_micron
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_m_2_or_mu_2(self):
        """Set value using mu_mathrm_m_2_or_mu_2 units (alias for square_micron)."""
        return self.square_micron
    
    @property
    def mu_m_2(self):
        """Set value using mu_m_2 units (alias for square_micron)."""
        return self.square_micron
    
    @property
    def mu_2(self):
        """Set value using mu_2 units (alias for square_micron)."""
        return self.square_micron
    
    @property
    def square_mile_statute(self):
        """Set value using square mile (statute) units."""
        unit_const = units.AreaUnits.square_mile_statute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_mi_stat(self):
        """Set value using sq_mi_stat units (alias for square_mile_statute)."""
        return self.square_mile_statute
    
    @property
    def square_mile_us_survey(self):
        """Set value using square mile (US survey) units."""
        unit_const = units.AreaUnits.square_mile_us_survey
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_mi_US_Surv(self):
        """Set value using sq_mi_US_Surv units (alias for square_mile_us_survey)."""
        return self.square_mile_us_survey
    
    @property
    def square_millimeter(self):
        """Set value using square millimeter units."""
        unit_const = units.AreaUnits.square_millimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mm_2(self):
        """Set value using mathrm_mm_2 units (alias for square_millimeter)."""
        return self.square_millimeter
    
    @property
    def square_nanometer(self):
        """Set value using square nanometer units."""
        unit_const = units.AreaUnits.square_nanometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_nm_2(self):
        """Set value using mathrm_nm_2 units (alias for square_nanometer)."""
        return self.square_nanometer
    
    @property
    def square_yard(self):
        """Set value using square yard units."""
        unit_const = units.AreaUnits.square_yard
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sq_yd(self):
        """Set value using sq_yd units (alias for square_yard)."""
        return self.square_yard
    
    @property
    def township_us(self):
        """Set value using township (US) units."""
        unit_const = units.AreaUnits.township_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def twshp(self):
        """Set value using twshp units (alias for township_us)."""
        return self.township_us
    

class AreaPerUnitVolumeSetter(TypeSafeSetter):
    """AreaPerUnitVolume-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_centimeter_per_cubic_centimeter(self):
        """Set value using square centimeter per cubic centimeter units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_centimeter_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_2_mathrm_cc(self):
        """Set value using mathrm_cm_2_mathrm_cc units (alias for square_centimeter_per_cubic_centimeter)."""
        return self.square_centimeter_per_cubic_centimeter
    
    @property
    def square_foot_per_cubic_foot(self):
        """Set value using square foot per cubic foot units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_foot_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_mathrm_ft_3_or_sqft_cft(self):
        """Set value using mathrm_ft_2_mathrm_ft_3_or_sqft_cft units (alias for square_foot_per_cubic_foot)."""
        return self.square_foot_per_cubic_foot
    
    @property
    def ft_2_ft_3(self):
        """Set value using ft_2_ft_3 units (alias for square_foot_per_cubic_foot)."""
        return self.square_foot_per_cubic_foot
    
    @property
    def sqft_cft(self):
        """Set value using sqft_cft units (alias for square_foot_per_cubic_foot)."""
        return self.square_foot_per_cubic_foot
    
    @property
    def square_inch_per_cubic_inch(self):
        """Set value using square inch per cubic inch units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_inch_per_cubic_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_in_2_mathrm_in_3_or_sq_in_cu_in(self):
        """Set value using mathrm_in_2_mathrm_in_3_or_sq_in_cu_in units (alias for square_inch_per_cubic_inch)."""
        return self.square_inch_per_cubic_inch
    
    @property
    def in_2_in_3(self):
        """Set value using in_2_in_3 units (alias for square_inch_per_cubic_inch)."""
        return self.square_inch_per_cubic_inch
    
    @property
    def sq_in_cu_in(self):
        """Set value using sq_in_cu_in units (alias for square_inch_per_cubic_inch)."""
        return self.square_inch_per_cubic_inch
    
    @property
    def square_meter_per_cubic_meter(self):
        """Set value using square meter per cubic meter units."""
        unit_const = units.AreaPerUnitVolumeUnits.square_meter_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2_mathrm_m_3_or_1_mathrm_m_3(self):
        """Set value using mathrm_m_2_mathrm_m_3_or_1_mathrm_m_3 units (alias for square_meter_per_cubic_meter)."""
        return self.square_meter_per_cubic_meter
    
    @property
    def m_2_m_3(self):
        """Set value using m_2_m_3 units (alias for square_meter_per_cubic_meter)."""
        return self.square_meter_per_cubic_meter
    
    @property
    def unit_1_m_3(self):
        """Set value using unit_1_m_3 units (alias for square_meter_per_cubic_meter)."""
        return self.square_meter_per_cubic_meter
    

class AtomicWeightSetter(TypeSafeSetter):
    """AtomicWeight-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def atomic_mass_unit_12c(self):
        """Set value using atomic mass unit (12C) units."""
        unit_const = units.AtomicWeightUnits.atomic_mass_unit_12c
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def amu(self):
        """Set value using amu units (alias for atomic_mass_unit_12c)."""
        return self.atomic_mass_unit_12c
    
    @property
    def grams_per_mole(self):
        """Set value using grams per mole units."""
        unit_const = units.AtomicWeightUnits.grams_per_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_mol(self):
        """Set value using g_mol units (alias for grams_per_mole)."""
        return self.grams_per_mole
    
    @property
    def kilograms_per_kilomole(self):
        """Set value using kilograms per kilomole units."""
        unit_const = units.AtomicWeightUnits.kilograms_per_kilomole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_kmol(self):
        """Set value using kg_kmol units (alias for kilograms_per_kilomole)."""
        return self.kilograms_per_kilomole
    
    @property
    def pounds_per_pound_mole(self):
        """Set value using pounds per pound mole units."""
        unit_const = units.AtomicWeightUnits.pounds_per_pound_mole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_lb_mol_or_mathrm_lb_mole(self):
        """Set value using mathrm_lb_mathrm_lb_mol_or_mathrm_lb_mole units (alias for pounds_per_pound_mole)."""
        return self.pounds_per_pound_mole
    
    @property
    def lb_lb_mol(self):
        """Set value using lb_lb_mol units (alias for pounds_per_pound_mole)."""
        return self.pounds_per_pound_mole
    
    @property
    def lb_mole(self):
        """Set value using lb_mole units (alias for pounds_per_pound_mole)."""
        return self.pounds_per_pound_mole
    

class ConcentrationSetter(TypeSafeSetter):
    """Concentration-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def grains_of_i_per_cubic_foot(self):
        """Set value using grains of "i" per cubic foot units."""
        unit_const = units.ConcentrationUnits.grains_of_i_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_gr_mathrm_ft_3_or_gr_cft(self):
        """Set value using mathrm_gr_mathrm_ft_3_or_gr_cft units (alias for grains_of_i_per_cubic_foot)."""
        return self.grains_of_i_per_cubic_foot
    
    @property
    def gr_ft_3(self):
        """Set value using gr_ft_3 units (alias for grains_of_i_per_cubic_foot)."""
        return self.grains_of_i_per_cubic_foot
    
    @property
    def gr_cft(self):
        """Set value using gr_cft units (alias for grains_of_i_per_cubic_foot)."""
        return self.grains_of_i_per_cubic_foot
    
    @property
    def grains_of_i_per_gallon_us(self):
        """Set value using grains of "i" per gallon (US) units."""
        unit_const = units.ConcentrationUnits.grains_of_i_per_gallon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gr_gal(self):
        """Set value using gr_gal units (alias for grains_of_i_per_gallon_us)."""
        return self.grains_of_i_per_gallon_us
    

class DimensionlessSetter(TypeSafeSetter):
    """Dimensionless-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dimensionless(self):
        """Set value using dimensionless units."""
        unit_const = units.DimensionlessUnits.dimensionless
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ratio(self):
        """Set value using ratio units."""
        unit_const = units.DimensionlessUnits.ratio
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def parts_per_million(self):
        """Set value using parts per million units."""
        unit_const = units.DimensionlessUnits.parts_per_million
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ppm(self):
        """Set value using ppm units (alias for parts_per_million)."""
        return self.parts_per_million
    
    @property
    def parts_per_billion(self):
        """Set value using parts per billion units."""
        unit_const = units.DimensionlessUnits.parts_per_billion
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ppb(self):
        """Set value using ppb units (alias for parts_per_billion)."""
        return self.parts_per_billion
    

class DynamicFluiditySetter(TypeSafeSetter):
    """DynamicFluidity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def meter_seconds_per_kilogram(self):
        """Set value using meter-seconds per kilogram units."""
        unit_const = units.DynamicFluidityUnits.meter_seconds_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_s_kg(self):
        """Set value using m_s_kg units (alias for meter_seconds_per_kilogram)."""
        return self.meter_seconds_per_kilogram
    
    @property
    def rhe(self):
        """Set value using rhe units."""
        unit_const = units.DynamicFluidityUnits.rhe
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_foot_per_pound_second(self):
        """Set value using square foot per pound second units."""
        unit_const = units.DynamicFluidityUnits.square_foot_per_pound_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_lb_sec(self):
        """Set value using mathrm_ft_2_lb_sec units (alias for square_foot_per_pound_second)."""
        return self.square_foot_per_pound_second
    
    @property
    def square_meters_per_newton_per_second(self):
        """Set value using square meters per newton per second units."""
        unit_const = units.DynamicFluidityUnits.square_meters_per_newton_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2_mathrm_N_mathrm_s(self):
        """Set value using mathrm_m_2_mathrm_N_mathrm_s units (alias for square_meters_per_newton_per_second)."""
        return self.square_meters_per_newton_per_second
    

class ElectricCapacitanceSetter(TypeSafeSetter):
    """ElectricCapacitance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cm(self):
        """Set value using "cm" units."""
        unit_const = units.ElectricCapacitanceUnits.cm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def abfarad(self):
        """Set value using abfarad units."""
        unit_const = units.ElectricCapacitanceUnits.abfarad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu_cgs units (alias for abfarad)."""
        return self.abfarad
    
    @property
    def farad(self):
        """Set value using farad units."""
        unit_const = units.ElectricCapacitanceUnits.farad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def F(self):
        """Set value using F units (alias for farad)."""
        return self.farad
    
    @property
    def farad_intl(self):
        """Set value using farad (intl) units."""
        unit_const = units.ElectricCapacitanceUnits.farad_intl
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def F_int(self):
        """Set value using F_int units (alias for farad_intl)."""
        return self.farad_intl
    
    @property
    def jar(self):
        """Set value using jar units."""
        unit_const = units.ElectricCapacitanceUnits.jar
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def puff(self):
        """Set value using puff units."""
        unit_const = units.ElectricCapacitanceUnits.puff
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def statfarad(self):
        """Set value using statfarad units."""
        unit_const = units.ElectricCapacitanceUnits.statfarad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def esu_cgs(self):
        """Set value using esu_cgs units (alias for statfarad)."""
        return self.statfarad
    
    @property
    def millifarad(self):
        """Set value using millifarad units."""
        unit_const = units.ElectricCapacitanceUnits.millifarad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mF(self):
        """Set value using mF units (alias for millifarad)."""
        return self.millifarad
    
    @property
    def microfarad(self):
        """Set value using microfarad units."""
        unit_const = units.ElectricCapacitanceUnits.microfarad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanofarad(self):
        """Set value using nanofarad units."""
        unit_const = units.ElectricCapacitanceUnits.nanofarad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nF(self):
        """Set value using nF units (alias for nanofarad)."""
        return self.nanofarad
    
    @property
    def picofarad(self):
        """Set value using picofarad units."""
        unit_const = units.ElectricCapacitanceUnits.picofarad
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu_cgs units (alias for abcoulomb)."""
        return self.abcoulomb
    
    @property
    def ampere_hour(self):
        """Set value using ampere-hour units."""
        unit_const = units.ElectricChargeUnits.ampere_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ah(self):
        """Set value using Ah units (alias for ampere_hour)."""
        return self.ampere_hour
    
    @property
    def coulomb(self):
        """Set value using coulomb units."""
        unit_const = units.ElectricChargeUnits.coulomb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def C(self):
        """Set value using C units (alias for coulomb)."""
        return self.coulomb
    
    @property
    def faraday_c12(self):
        """Set value using faraday (C12) units."""
        unit_const = units.ElectricChargeUnits.faraday_c12
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def F(self):
        """Set value using F units (alias for faraday_c12)."""
        return self.faraday_c12
    
    @property
    def franklin(self):
        """Set value using franklin units."""
        unit_const = units.ElectricChargeUnits.franklin
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Fr(self):
        """Set value using Fr units (alias for franklin)."""
        return self.franklin
    
    @property
    def statcoulomb(self):
        """Set value using statcoulomb units."""
        unit_const = units.ElectricChargeUnits.statcoulomb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def esu_cgs(self):
        """Set value using esu_cgs units (alias for statcoulomb)."""
        return self.statcoulomb
    
    @property
    def u_a_charge(self):
        """Set value using u.a. charge units."""
        unit_const = units.ElectricChargeUnits.u_a_charge
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def u_a(self):
        """Set value using u_a units (alias for u_a_charge)."""
        return self.u_a_charge
    
    @property
    def kilocoulomb(self):
        """Set value using kilocoulomb units."""
        unit_const = units.ElectricChargeUnits.kilocoulomb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kC(self):
        """Set value using kC units (alias for kilocoulomb)."""
        return self.kilocoulomb
    
    @property
    def millicoulomb(self):
        """Set value using millicoulomb units."""
        unit_const = units.ElectricChargeUnits.millicoulomb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mC(self):
        """Set value using mC units (alias for millicoulomb)."""
        return self.millicoulomb
    
    @property
    def microcoulomb(self):
        """Set value using microcoulomb units."""
        unit_const = units.ElectricChargeUnits.microcoulomb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanocoulomb(self):
        """Set value using nanocoulomb units."""
        unit_const = units.ElectricChargeUnits.nanocoulomb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nC(self):
        """Set value using nC units (alias for nanocoulomb)."""
        return self.nanocoulomb
    
    @property
    def picocoulomb(self):
        """Set value using picocoulomb units."""
        unit_const = units.ElectricChargeUnits.picocoulomb
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu_cgs units (alias for abampere)."""
        return self.abampere
    
    @property
    def ampere_intl_mean(self):
        """Set value using ampere (intl mean) units."""
        unit_const = units.ElectricCurrentIntensityUnits.ampere_intl_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def A_int_mean(self):
        """Set value using A_int_mean units (alias for ampere_intl_mean)."""
        return self.ampere_intl_mean
    
    @property
    def ampere_intl_us(self):
        """Set value using ampere (intl US) units."""
        unit_const = units.ElectricCurrentIntensityUnits.ampere_intl_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def A_int_US(self):
        """Set value using A_int_US units (alias for ampere_intl_us)."""
        return self.ampere_intl_us
    
    @property
    def ampere_or_amp(self):
        """Set value using ampere or amp units."""
        unit_const = units.ElectricCurrentIntensityUnits.ampere_or_amp
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def A(self):
        """Set value using A units (alias for ampere_or_amp)."""
        return self.ampere_or_amp
    
    @property
    def biot(self):
        """Set value using biot units."""
        unit_const = units.ElectricCurrentIntensityUnits.biot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def statampere(self):
        """Set value using statampere units."""
        unit_const = units.ElectricCurrentIntensityUnits.statampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def esu_cgs(self):
        """Set value using esu_cgs units (alias for statampere)."""
        return self.statampere
    
    @property
    def u_a_or_current(self):
        """Set value using u.a. or current units."""
        unit_const = units.ElectricCurrentIntensityUnits.u_a_or_current
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def u_a(self):
        """Set value using u_a units (alias for u_a_or_current)."""
        return self.u_a_or_current
    

class ElectricDipoleMomentSetter(TypeSafeSetter):
    """ElectricDipoleMoment-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def ampere_meter_second(self):
        """Set value using ampere meter second units."""
        unit_const = units.ElectricDipoleMomentUnits.ampere_meter_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def A_m_s(self):
        """Set value using A_m_s units (alias for ampere_meter_second)."""
        return self.ampere_meter_second
    
    @property
    def coulomb_meter(self):
        """Set value using coulomb meter units."""
        unit_const = units.ElectricDipoleMomentUnits.coulomb_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def C_m(self):
        """Set value using C_m units (alias for coulomb_meter)."""
        return self.coulomb_meter
    
    @property
    def debye(self):
        """Set value using debye units."""
        unit_const = units.ElectricDipoleMomentUnits.debye
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def D(self):
        """Set value using D units (alias for debye)."""
        return self.debye
    
    @property
    def electron_meter(self):
        """Set value using electron meter units."""
        unit_const = units.ElectricDipoleMomentUnits.electron_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def e_m(self):
        """Set value using e_m units (alias for electron_meter)."""
        return self.electron_meter
    

class ElectricFieldStrengthSetter(TypeSafeSetter):
    """ElectricFieldStrength-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def volt_per_centimeter(self):
        """Set value using volt per centimeter units."""
        unit_const = units.ElectricFieldStrengthUnits.volt_per_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def V_cm(self):
        """Set value using V_cm units (alias for volt_per_centimeter)."""
        return self.volt_per_centimeter
    
    @property
    def volt_per_meter(self):
        """Set value using volt per meter units."""
        unit_const = units.ElectricFieldStrengthUnits.volt_per_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def V_m(self):
        """Set value using V_m units (alias for volt_per_meter)."""
        return self.volt_per_meter
    

class ElectricInductanceSetter(TypeSafeSetter):
    """ElectricInductance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abhenry(self):
        """Set value using abhenry units."""
        unit_const = units.ElectricInductanceUnits.abhenry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu_cgs units (alias for abhenry)."""
        return self.abhenry
    
    @property
    def cm(self):
        """Set value using cm units."""
        unit_const = units.ElectricInductanceUnits.cm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def henry(self):
        """Set value using henry units."""
        unit_const = units.ElectricInductanceUnits.henry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def H(self):
        """Set value using H units (alias for henry)."""
        return self.henry
    
    @property
    def henry_intl_mean(self):
        """Set value using henry (intl mean) units."""
        unit_const = units.ElectricInductanceUnits.henry_intl_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def H_int_mean(self):
        """Set value using H_int_mean units (alias for henry_intl_mean)."""
        return self.henry_intl_mean
    
    @property
    def henry_intl_us(self):
        """Set value using henry (intl US) units."""
        unit_const = units.ElectricInductanceUnits.henry_intl_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def H_int_US(self):
        """Set value using H_int_US units (alias for henry_intl_us)."""
        return self.henry_intl_us
    
    @property
    def mic(self):
        """Set value using mic units."""
        unit_const = units.ElectricInductanceUnits.mic
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def stathenry(self):
        """Set value using stathenry units."""
        unit_const = units.ElectricInductanceUnits.stathenry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def esu_cgs(self):
        """Set value using esu_cgs units (alias for stathenry)."""
        return self.stathenry
    
    @property
    def millihenry(self):
        """Set value using millihenry units."""
        unit_const = units.ElectricInductanceUnits.millihenry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mH(self):
        """Set value using mH units (alias for millihenry)."""
        return self.millihenry
    
    @property
    def microhenry(self):
        """Set value using microhenry units."""
        unit_const = units.ElectricInductanceUnits.microhenry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanohenry(self):
        """Set value using nanohenry units."""
        unit_const = units.ElectricInductanceUnits.nanohenry
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu_cgs units (alias for abvolt)."""
        return self.abvolt
    
    @property
    def statvolt(self):
        """Set value using statvolt units."""
        unit_const = units.ElectricPotentialUnits.statvolt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def esu_cgs(self):
        """Set value using esu_cgs units (alias for statvolt)."""
        return self.statvolt
    
    @property
    def u_a_potential(self):
        """Set value using u.a. potential units."""
        unit_const = units.ElectricPotentialUnits.u_a_potential
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def u_a(self):
        """Set value using u_a units (alias for u_a_potential)."""
        return self.u_a_potential
    
    @property
    def volt(self):
        """Set value using volt units."""
        unit_const = units.ElectricPotentialUnits.volt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def V(self):
        """Set value using V units (alias for volt)."""
        return self.volt
    
    @property
    def volt_intl_mean(self):
        """Set value using volt (intl mean) units."""
        unit_const = units.ElectricPotentialUnits.volt_intl_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def V_int_mean(self):
        """Set value using V_int_mean units (alias for volt_intl_mean)."""
        return self.volt_intl_mean
    
    @property
    def volt_us(self):
        """Set value using volt (US) units."""
        unit_const = units.ElectricPotentialUnits.volt_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def V_int_US(self):
        """Set value using V_int_US units (alias for volt_us)."""
        return self.volt_us
    
    @property
    def kilovolt(self):
        """Set value using kilovolt units."""
        unit_const = units.ElectricPotentialUnits.kilovolt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kV(self):
        """Set value using kV units (alias for kilovolt)."""
        return self.kilovolt
    
    @property
    def millivolt(self):
        """Set value using millivolt units."""
        unit_const = units.ElectricPotentialUnits.millivolt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mV(self):
        """Set value using mV units (alias for millivolt)."""
        return self.millivolt
    
    @property
    def microvolt(self):
        """Set value using microvolt units."""
        unit_const = units.ElectricPotentialUnits.microvolt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanovolt(self):
        """Set value using nanovolt units."""
        unit_const = units.ElectricPotentialUnits.nanovolt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nV(self):
        """Set value using nV units (alias for nanovolt)."""
        return self.nanovolt
    
    @property
    def picovolt(self):
        """Set value using picovolt units."""
        unit_const = units.ElectricPotentialUnits.picovolt
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu_cgs units (alias for abohm)."""
        return self.abohm
    
    @property
    def jacobi(self):
        """Set value using jacobi units."""
        unit_const = units.ElectricResistanceUnits.jacobi
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unnamed(self):
        """Set value using unnamed units (alias for jacobi)."""
        return self.jacobi
    
    @property
    def lenz(self):
        """Set value using lenz units."""
        unit_const = units.ElectricResistanceUnits.lenz
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Metric(self):
        """Set value using Metric units (alias for lenz)."""
        return self.lenz
    
    @property
    def ohm(self):
        """Set value using ohm units."""
        unit_const = units.ElectricResistanceUnits.ohm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Omega(self):
        """Set value using Omega units (alias for ohm)."""
        return self.ohm
    
    @property
    def ohm_intl_mean(self):
        """Set value using ohm (intl mean) units."""
        unit_const = units.ElectricResistanceUnits.ohm_intl_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Omega_int_mean(self):
        """Set value using Omega_int_mean units (alias for ohm_intl_mean)."""
        return self.ohm_intl_mean
    
    @property
    def ohm_intl_us(self):
        """Set value using ohm (intl US) units."""
        unit_const = units.ElectricResistanceUnits.ohm_intl_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Omega_int_US(self):
        """Set value using Omega_int_US units (alias for ohm_intl_us)."""
        return self.ohm_intl_us
    
    @property
    def ohm_legal(self):
        """Set value using ohm (legal) units."""
        unit_const = units.ElectricResistanceUnits.ohm_legal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Omega_legal(self):
        """Set value using Omega_legal units (alias for ohm_legal)."""
        return self.ohm_legal
    
    @property
    def preece(self):
        """Set value using preece units."""
        unit_const = units.ElectricResistanceUnits.preece
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def statohm(self):
        """Set value using statohm units."""
        unit_const = units.ElectricResistanceUnits.statohm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def csu_cgs(self):
        """Set value using csu_cgs units (alias for statohm)."""
        return self.statohm
    
    @property
    def wheatstone(self):
        """Set value using wheatstone units."""
        unit_const = units.ElectricResistanceUnits.wheatstone
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kiloohm(self):
        """Set value using kiloohm units."""
        unit_const = units.ElectricResistanceUnits.kiloohm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def k_Omega(self):
        """Set value using k_Omega units (alias for kiloohm)."""
        return self.kiloohm
    
    @property
    def megaohm(self):
        """Set value using megaohm units."""
        unit_const = units.ElectricResistanceUnits.megaohm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def M_Omega(self):
        """Set value using M_Omega units (alias for megaohm)."""
        return self.megaohm
    
    @property
    def milliohm(self):
        """Set value using milliohm units."""
        unit_const = units.ElectricResistanceUnits.milliohm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_Omega(self):
        """Set value using m_Omega units (alias for milliohm)."""
        return self.milliohm
    

class ElectricalConductanceSetter(TypeSafeSetter):
    """ElectricalConductance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def emu_cgs(self):
        """Set value using emu cgs units."""
        unit_const = units.ElectricalConductanceUnits.emu_cgs
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def abmho(self):
        """Set value using abmho units (alias for emu_cgs)."""
        return self.emu_cgs
    
    @property
    def esu_cgs(self):
        """Set value using esu cgs units."""
        unit_const = units.ElectricalConductanceUnits.esu_cgs
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def statmho(self):
        """Set value using statmho units (alias for esu_cgs)."""
        return self.esu_cgs
    
    @property
    def mho(self):
        """Set value using mho units."""
        unit_const = units.ElectricalConductanceUnits.mho
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def microsiemens(self):
        """Set value using microsiemens units."""
        unit_const = units.ElectricalConductanceUnits.microsiemens
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_S(self):
        """Set value using mu_mathrm_S units (alias for microsiemens)."""
        return self.microsiemens
    
    @property
    def siemens(self):
        """Set value using siemens units."""
        unit_const = units.ElectricalConductanceUnits.siemens
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def S(self):
        """Set value using S units (alias for siemens)."""
        return self.siemens
    
    @property
    def millisiemens(self):
        """Set value using millisiemens units."""
        unit_const = units.ElectricalConductanceUnits.millisiemens
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def F_m(self):
        """Set value using F_m units (alias for farad_per_meter)."""
        return self.farad_per_meter
    

class ElectricalResistivitySetter(TypeSafeSetter):
    """ElectricalResistivity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def circular_mil_ohm_per_foot(self):
        """Set value using circular mil-ohm per foot units."""
        unit_const = units.ElectricalResistivityUnits.circular_mil_ohm_per_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def circmil_Omega_mathrm_ft(self):
        """Set value using circmil_Omega_mathrm_ft units (alias for circular_mil_ohm_per_foot)."""
        return self.circular_mil_ohm_per_foot
    
    @property
    def emu_cgs(self):
        """Set value using emu cgs units."""
        unit_const = units.ElectricalResistivityUnits.emu_cgs
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def abohm_cm(self):
        """Set value using abohm_cm units (alias for emu_cgs)."""
        return self.emu_cgs
    
    @property
    def microhm_inch(self):
        """Set value using microhm-inch units."""
        unit_const = units.ElectricalResistivityUnits.microhm_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_Omega_in(self):
        """Set value using mu_Omega_in units (alias for microhm_inch)."""
        return self.microhm_inch
    
    @property
    def ohm_centimeter(self):
        """Set value using ohm-centimeter units."""
        unit_const = units.ElectricalResistivityUnits.ohm_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def boldsymbol_Omega_mathbf_c_m(self):
        """Set value using boldsymbol_Omega_mathbf_c_m units (alias for ohm_centimeter)."""
        return self.ohm_centimeter
    
    @property
    def ohm_meter(self):
        """Set value using ohm-meter units."""
        unit_const = units.ElectricalResistivityUnits.ohm_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Omega_mathrm_m(self):
        """Set value using Omega_mathrm_m units (alias for ohm_meter)."""
        return self.ohm_meter
    

class EnergyFluxSetter(TypeSafeSetter):
    """EnergyFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def btu_per_square_foot_per_hour(self):
        """Set value using Btu per square foot per hour units."""
        unit_const = units.EnergyFluxUnits.btu_per_square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Btu_mathrm_ft_2_mathrm_hr(self):
        """Set value using mathrm_Btu_mathrm_ft_2_mathrm_hr units (alias for btu_per_square_foot_per_hour)."""
        return self.btu_per_square_foot_per_hour
    
    @property
    def calorie_per_square_centimeter_per_second(self):
        """Set value using calorie per square centimeter per second units."""
        unit_const = units.EnergyFluxUnits.calorie_per_square_centimeter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cal_mathrm_cm_2_mathrm_s_or_mathrm_cal_mathrm_cm_2_mathrm_s(self):
        """Set value using mathrm_cal_mathrm_cm_2_mathrm_s_or_mathrm_cal_mathrm_cm_2_mathrm_s units (alias for calorie_per_square_centimeter_per_second)."""
        return self.calorie_per_square_centimeter_per_second
    
    @property
    def cal_cm_2_s(self):
        """Set value using cal_cm_2_s units (alias for calorie_per_square_centimeter_per_second)."""
        return self.calorie_per_square_centimeter_per_second
    
    @property
    def celsius_heat_units_chu(self):
        """Set value using Celsius heat units (Chu) per square foot per hour units."""
        unit_const = units.EnergyFluxUnits.celsius_heat_units_chu
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Chu_mathrm_ft_2_mathrm_hr(self):
        """Set value using mathrm_Chu_mathrm_ft_2_mathrm_hr units (alias for celsius_heat_units_chu)."""
        return self.celsius_heat_units_chu
    
    @property
    def kilocalorie_per_square_foot_per_hour(self):
        """Set value using kilocalorie per square foot per hour units."""
        unit_const = units.EnergyFluxUnits.kilocalorie_per_square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kcal_left_mathrm_ft_2_mathrm_hr_right(self):
        """Set value using mathrm_kcal_left_mathrm_ft_2_mathrm_hr_right units (alias for kilocalorie_per_square_foot_per_hour)."""
        return self.kilocalorie_per_square_foot_per_hour
    
    @property
    def kilocalorie_per_square_meter_per_hour(self):
        """Set value using kilocalorie per square meter per hour units."""
        unit_const = units.EnergyFluxUnits.kilocalorie_per_square_meter_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kcal_left_mathrm_m_2_mathrm_hr_right(self):
        """Set value using mathrm_kcal_left_mathrm_m_2_mathrm_hr_right units (alias for kilocalorie_per_square_meter_per_hour)."""
        return self.kilocalorie_per_square_meter_per_hour
    
    @property
    def watt_per_square_meter(self):
        """Set value using watt per square meter units."""
        unit_const = units.EnergyFluxUnits.watt_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_W_mathrm_m_2(self):
        """Set value using mathrm_W_mathrm_m_2 units (alias for watt_per_square_meter)."""
        return self.watt_per_square_meter
    

class EnergyHeatWorkSetter(TypeSafeSetter):
    """EnergyHeatWork-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def barrel_oil_equivalent_or_equivalent_barrel(self):
        """Set value using barrel oil equivalent or equivalent barrel units."""
        unit_const = units.EnergyHeatWorkUnits.barrel_oil_equivalent_or_equivalent_barrel
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def bboe_or_boe(self):
        """Set value using bboe_or_boe units (alias for barrel_oil_equivalent_or_equivalent_barrel)."""
        return self.barrel_oil_equivalent_or_equivalent_barrel
    
    @property
    def bboe(self):
        """Set value using bboe units (alias for barrel_oil_equivalent_or_equivalent_barrel)."""
        return self.barrel_oil_equivalent_or_equivalent_barrel
    
    @property
    def boe(self):
        """Set value using boe units (alias for barrel_oil_equivalent_or_equivalent_barrel)."""
        return self.barrel_oil_equivalent_or_equivalent_barrel
    
    @property
    def billion_electronvolt(self):
        """Set value using billion electronvolt units."""
        unit_const = units.EnergyHeatWorkUnits.billion_electronvolt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def BeV(self):
        """Set value using BeV units (alias for billion_electronvolt)."""
        return self.billion_electronvolt
    
    @property
    def british_thermal_unit_4circ_mathrmc(self):
        """Set value using British thermal unit ( $4^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.british_thermal_unit_4circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_39_2_circ_mathrm_F(self):
        """Set value using Btu_39_2_circ_mathrm_F units (alias for british_thermal_unit_4circ_mathrmc)."""
        return self.british_thermal_unit_4circ_mathrmc
    
    @property
    def british_thermal_unit_60circ_mathrmf(self):
        """Set value using British thermal unit ( $60^{\\circ} \\mathrm{F}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.british_thermal_unit_60circ_mathrmf
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_60_circ_mathrm_F(self):
        """Set value using Btu_60_circ_mathrm_F units (alias for british_thermal_unit_60circ_mathrmf)."""
        return self.british_thermal_unit_60circ_mathrmf
    
    @property
    def british_thermal_unit_international_steam_tables(self):
        """Set value using British thermal unit (international steam tables) units."""
        unit_const = units.EnergyHeatWorkUnits.british_thermal_unit_international_steam_tables
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_IT(self):
        """Set value using Btu_IT units (alias for british_thermal_unit_international_steam_tables)."""
        return self.british_thermal_unit_international_steam_tables
    
    @property
    def british_thermal_unit_isotc_12(self):
        """Set value using British thermal unit (ISO/TC 12) units."""
        unit_const = units.EnergyHeatWorkUnits.british_thermal_unit_isotc_12
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_ISO(self):
        """Set value using Btu_ISO units (alias for british_thermal_unit_isotc_12)."""
        return self.british_thermal_unit_isotc_12
    
    @property
    def british_thermal_unit_mean(self):
        """Set value using British thermal unit (mean) units."""
        unit_const = units.EnergyHeatWorkUnits.british_thermal_unit_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_mean_or_Btu(self):
        """Set value using Btu_mean_or_Btu units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def Btu_mean(self):
        """Set value using Btu_mean units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def Btu(self):
        """Set value using Btu units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def british_thermal_unit_thermochemical(self):
        """Set value using British thermal unit (thermochemical) units."""
        unit_const = units.EnergyHeatWorkUnits.british_thermal_unit_thermochemical
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_therm(self):
        """Set value using Btu_therm units (alias for british_thermal_unit_thermochemical)."""
        return self.british_thermal_unit_thermochemical
    
    @property
    def calorie_20circ_mathrmc(self):
        """Set value using calorie ( $20^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_20circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_20_circ_mathrm_C(self):
        """Set value using cal_20_circ_mathrm_C units (alias for calorie_20circ_mathrmc)."""
        return self.calorie_20circ_mathrmc
    
    @property
    def calorie_4circ_mathrmc(self):
        """Set value using calorie ( $4^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_4circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_4_circ_mathrm_C(self):
        """Set value using cal_4_circ_mathrm_C units (alias for calorie_4circ_mathrmc)."""
        return self.calorie_4circ_mathrmc
    
    @property
    def calorie_international_steam_tables(self):
        """Set value using calorie (international steam tables) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_international_steam_tables
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_IT(self):
        """Set value using cal_IT units (alias for calorie_international_steam_tables)."""
        return self.calorie_international_steam_tables
    
    @property
    def calorie_mean(self):
        """Set value using calorie (mean) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_mean(self):
        """Set value using cal_mean units (alias for calorie_mean)."""
        return self.calorie_mean
    
    @property
    def calorie_nutritional(self):
        """Set value using Calorie (nutritional) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_nutritional
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Cal_nutr(self):
        """Set value using Cal_nutr units (alias for calorie_nutritional)."""
        return self.calorie_nutritional
    
    @property
    def calorie_thermochemical(self):
        """Set value using calorie (thermochemical) units."""
        unit_const = units.EnergyHeatWorkUnits.calorie_thermochemical
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_therm(self):
        """Set value using cal_therm units (alias for calorie_thermochemical)."""
        return self.calorie_thermochemical
    
    @property
    def celsius_heat_unit(self):
        """Set value using Celsius heat unit units."""
        unit_const = units.EnergyHeatWorkUnits.celsius_heat_unit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu(self):
        """Set value using Chu units (alias for celsius_heat_unit)."""
        return self.celsius_heat_unit
    
    @property
    def celsius_heat_unit_15_circ_mathrmc(self):
        """Set value using Celsius heat unit ( $15{ }^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.celsius_heat_unit_15_circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_15_circ_mathrm_C(self):
        """Set value using Chu_15_circ_mathrm_C units (alias for celsius_heat_unit_15_circ_mathrmc)."""
        return self.celsius_heat_unit_15_circ_mathrmc
    
    @property
    def electron_volt(self):
        """Set value using electron volt units."""
        unit_const = units.EnergyHeatWorkUnits.electron_volt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def eV(self):
        """Set value using eV units (alias for electron_volt)."""
        return self.electron_volt
    
    @property
    def erg(self):
        """Set value using erg units."""
        unit_const = units.EnergyHeatWorkUnits.erg
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def foot_pound_force_duty(self):
        """Set value using foot pound force (duty) units."""
        unit_const = units.EnergyHeatWorkUnits.foot_pound_force_duty
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_mathrm_lb_mathrm_f(self):
        """Set value using ft_mathrm_lb_mathrm_f units (alias for foot_pound_force_duty)."""
        return self.foot_pound_force_duty
    
    @property
    def foot_poundal(self):
        """Set value using foot-poundal units."""
        unit_const = units.EnergyHeatWorkUnits.foot_poundal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_pdl(self):
        """Set value using ft_pdl units (alias for foot_poundal)."""
        return self.foot_poundal
    
    @property
    def frigorie(self):
        """Set value using frigorie units."""
        unit_const = units.EnergyHeatWorkUnits.frigorie
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fg(self):
        """Set value using fg units (alias for frigorie)."""
        return self.frigorie
    
    @property
    def hartree_atomic_unit_of_energy(self):
        """Set value using hartree (atomic unit of energy) units."""
        unit_const = units.EnergyHeatWorkUnits.hartree_atomic_unit_of_energy
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_E_mathrm_H_a_u(self):
        """Set value using mathrm_E_mathrm_H_a_u units (alias for hartree_atomic_unit_of_energy)."""
        return self.hartree_atomic_unit_of_energy
    
    @property
    def joule(self):
        """Set value using joule units."""
        unit_const = units.EnergyHeatWorkUnits.joule
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J(self):
        """Set value using J units (alias for joule)."""
        return self.joule
    
    @property
    def joule_international(self):
        """Set value using joule (international) units."""
        unit_const = units.EnergyHeatWorkUnits.joule_international
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_intl(self):
        """Set value using J_intl units (alias for joule_international)."""
        return self.joule_international
    
    @property
    def kilocalorie_thermal(self):
        """Set value using kilocalorie (thermal) units."""
        unit_const = units.EnergyHeatWorkUnits.kilocalorie_thermal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_therm(self):
        """Set value using kcal_therm units (alias for kilocalorie_thermal)."""
        return self.kilocalorie_thermal
    
    @property
    def kilogram_force_meter(self):
        """Set value using kilogram force meter units."""
        unit_const = units.EnergyHeatWorkUnits.kilogram_force_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_m(self):
        """Set value using mathrm_kg_mathrm_f_m units (alias for kilogram_force_meter)."""
        return self.kilogram_force_meter
    
    @property
    def kiloton_tnt(self):
        """Set value using kiloton (TNT) units."""
        unit_const = units.EnergyHeatWorkUnits.kiloton_tnt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kt_TNT(self):
        """Set value using kt_TNT units (alias for kiloton_tnt)."""
        return self.kiloton_tnt
    
    @property
    def kilowatt_hour(self):
        """Set value using kilowatt hour units."""
        unit_const = units.EnergyHeatWorkUnits.kilowatt_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kWh(self):
        """Set value using kWh units (alias for kilowatt_hour)."""
        return self.kilowatt_hour
    
    @property
    def liter_atmosphere(self):
        """Set value using liter atmosphere units."""
        unit_const = units.EnergyHeatWorkUnits.liter_atmosphere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def L_atm(self):
        """Set value using L_atm units (alias for liter_atmosphere)."""
        return self.liter_atmosphere
    
    @property
    def megaton_tnt(self):
        """Set value using megaton (TNT) units."""
        unit_const = units.EnergyHeatWorkUnits.megaton_tnt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Mt_TNT(self):
        """Set value using Mt_TNT units (alias for megaton_tnt)."""
        return self.megaton_tnt
    
    @property
    def pound_centigrade_unit_15circ_mathrmc(self):
        """Set value using pound centigrade unit ( $15^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.EnergyHeatWorkUnits.pound_centigrade_unit_15circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pcu_15_circ_mathrm_C(self):
        """Set value using pcu_15_circ_mathrm_C units (alias for pound_centigrade_unit_15circ_mathrmc)."""
        return self.pound_centigrade_unit_15circ_mathrmc
    
    @property
    def prout(self):
        """Set value using prout units."""
        unit_const = units.EnergyHeatWorkUnits.prout
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def q_unit(self):
        """Set value using Q unit units."""
        unit_const = units.EnergyHeatWorkUnits.q_unit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Q(self):
        """Set value using Q units (alias for q_unit)."""
        return self.q_unit
    
    @property
    def quad_quadrillion_btu(self):
        """Set value using quad (quadrillion Btu) units."""
        unit_const = units.EnergyHeatWorkUnits.quad_quadrillion_btu
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def quad(self):
        """Set value using quad units (alias for quad_quadrillion_btu)."""
        return self.quad_quadrillion_btu
    
    @property
    def rydberg(self):
        """Set value using rydberg units."""
        unit_const = units.EnergyHeatWorkUnits.rydberg
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ry(self):
        """Set value using Ry units (alias for rydberg)."""
        return self.rydberg
    
    @property
    def therm_eeg(self):
        """Set value using therm (EEG) units."""
        unit_const = units.EnergyHeatWorkUnits.therm_eeg
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def therm_EEG(self):
        """Set value using therm_EEG units (alias for therm_eeg)."""
        return self.therm_eeg
    
    @property
    def therm_refineries(self):
        """Set value using therm (refineries) units."""
        unit_const = units.EnergyHeatWorkUnits.therm_refineries
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def therm_refy_or_therm(self):
        """Set value using therm_refy_or_therm units (alias for therm_refineries)."""
        return self.therm_refineries
    
    @property
    def therm_refy(self):
        """Set value using therm_refy units (alias for therm_refineries)."""
        return self.therm_refineries
    
    @property
    def therm(self):
        """Set value using therm units (alias for therm_refineries)."""
        return self.therm_refineries
    
    @property
    def therm_us(self):
        """Set value using therm (US) units."""
        unit_const = units.EnergyHeatWorkUnits.therm_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def therm_US_or_therm(self):
        """Set value using therm_US_or_therm units (alias for therm_us)."""
        return self.therm_us
    
    @property
    def ton_coal_equivalent(self):
        """Set value using ton coal equivalent units."""
        unit_const = units.EnergyHeatWorkUnits.ton_coal_equivalent
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def tce_tec(self):
        """Set value using tce_tec units (alias for ton_coal_equivalent)."""
        return self.ton_coal_equivalent
    
    @property
    def ton_oil_equivalent(self):
        """Set value using ton oil equivalent units."""
        unit_const = units.EnergyHeatWorkUnits.ton_oil_equivalent
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def toe_tep(self):
        """Set value using toe_tep units (alias for ton_oil_equivalent)."""
        return self.ton_oil_equivalent
    
    @property
    def kilojoule(self):
        """Set value using kilojoule units."""
        unit_const = units.EnergyHeatWorkUnits.kilojoule
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kJ(self):
        """Set value using kJ units (alias for kilojoule)."""
        return self.kilojoule
    
    @property
    def megajoule(self):
        """Set value using megajoule units."""
        unit_const = units.EnergyHeatWorkUnits.megajoule
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MJ(self):
        """Set value using MJ units (alias for megajoule)."""
        return self.megajoule
    
    @property
    def gigajoule(self):
        """Set value using gigajoule units."""
        unit_const = units.EnergyHeatWorkUnits.gigajoule
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def GJ(self):
        """Set value using GJ units (alias for gigajoule)."""
        return self.gigajoule
    

class EnergyPerUnitAreaSetter(TypeSafeSetter):
    """EnergyPerUnitArea-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_per_square_foot(self):
        """Set value using British thermal unit per square foot units."""
        unit_const = units.EnergyPerUnitAreaUnits.british_thermal_unit_per_square_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Btu_mathrm_ft_2_or_Btu_sq_ft(self):
        """Set value using mathrm_Btu_mathrm_ft_2_or_Btu_sq_ft units (alias for british_thermal_unit_per_square_foot)."""
        return self.british_thermal_unit_per_square_foot
    
    @property
    def Btu_ft_2(self):
        """Set value using Btu_ft_2 units (alias for british_thermal_unit_per_square_foot)."""
        return self.british_thermal_unit_per_square_foot
    
    @property
    def Btu_sq_ft(self):
        """Set value using Btu_sq_ft units (alias for british_thermal_unit_per_square_foot)."""
        return self.british_thermal_unit_per_square_foot
    
    @property
    def joule_per_square_meter(self):
        """Set value using joule per square meter units."""
        unit_const = units.EnergyPerUnitAreaUnits.joule_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_J_mathrm_m_2(self):
        """Set value using mathrm_J_mathrm_m_2 units (alias for joule_per_square_meter)."""
        return self.joule_per_square_meter
    
    @property
    def langley(self):
        """Set value using Langley units."""
        unit_const = units.EnergyPerUnitAreaUnits.langley
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ly(self):
        """Set value using Ly units (alias for langley)."""
        return self.langley
    

class ForceSetter(TypeSafeSetter):
    """Force-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def crinal(self):
        """Set value using crinal units."""
        unit_const = units.ForceUnits.crinal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyne(self):
        """Set value using dyne units."""
        unit_const = units.ForceUnits.dyne
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn(self):
        """Set value using dyn units (alias for dyne)."""
        return self.dyne
    
    @property
    def funal(self):
        """Set value using funal units."""
        unit_const = units.ForceUnits.funal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_force(self):
        """Set value using kilogram force units."""
        unit_const = units.ForceUnits.kilogram_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f(self):
        """Set value using mathrm_kg_mathrm_f units (alias for kilogram_force)."""
        return self.kilogram_force
    
    @property
    def kip_force(self):
        """Set value using kip force units."""
        unit_const = units.ForceUnits.kip_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def operatorname_kip_mathrm_f(self):
        """Set value using operatorname_kip_mathrm_f units (alias for kip_force)."""
        return self.kip_force
    
    @property
    def newton(self):
        """Set value using newton units."""
        unit_const = units.ForceUnits.newton
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def N(self):
        """Set value using N units (alias for newton)."""
        return self.newton
    
    @property
    def ounce_force(self):
        """Set value using ounce force units."""
        unit_const = units.ForceUnits.ounce_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_oz_mathrm_f_or_oz(self):
        """Set value using mathrm_oz_mathrm_f_or_oz units (alias for ounce_force)."""
        return self.ounce_force
    
    @property
    def oz_f(self):
        """Set value using oz_f units (alias for ounce_force)."""
        return self.ounce_force
    
    @property
    def oz(self):
        """Set value using oz units (alias for ounce_force)."""
        return self.ounce_force
    
    @property
    def pond(self):
        """Set value using pond units."""
        unit_const = units.ForceUnits.pond
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def p(self):
        """Set value using p units (alias for pond)."""
        return self.pond
    
    @property
    def pound_force(self):
        """Set value using pound force units."""
        unit_const = units.ForceUnits.pound_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_or_lb(self):
        """Set value using mathrm_lb_mathrm_f_or_lb units (alias for pound_force)."""
        return self.pound_force
    
    @property
    def lb_f(self):
        """Set value using lb_f units (alias for pound_force)."""
        return self.pound_force
    
    @property
    def lb(self):
        """Set value using lb units (alias for pound_force)."""
        return self.pound_force
    
    @property
    def poundal(self):
        """Set value using poundal units."""
        unit_const = units.ForceUnits.poundal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pdl(self):
        """Set value using pdl units (alias for poundal)."""
        return self.poundal
    
    @property
    def slug_force(self):
        """Set value using slug force units."""
        unit_const = units.ForceUnits.slug_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def operatorname_slug_f(self):
        """Set value using operatorname_slug_f units (alias for slug_force)."""
        return self.slug_force
    
    @property
    def sth_ne(self):
        """Set value using sthène units."""
        unit_const = units.ForceUnits.sth_ne
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sn(self):
        """Set value using sn units (alias for sth_ne)."""
        return self.sth_ne
    
    @property
    def ton_force_long(self):
        """Set value using ton (force, long) units."""
        unit_const = units.ForceUnits.ton_force_long
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def LT(self):
        """Set value using LT units (alias for ton_force_long)."""
        return self.ton_force_long
    
    @property
    def ton_force_metric(self):
        """Set value using ton (force, metric) units."""
        unit_const = units.ForceUnits.ton_force_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT(self):
        """Set value using MT units (alias for ton_force_metric)."""
        return self.ton_force_metric
    
    @property
    def ton_force_short(self):
        """Set value using ton (force, short) units."""
        unit_const = units.ForceUnits.ton_force_short
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def T(self):
        """Set value using T units (alias for ton_force_short)."""
        return self.ton_force_short
    
    @property
    def kilonewton(self):
        """Set value using kilonewton units."""
        unit_const = units.ForceUnits.kilonewton
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kN(self):
        """Set value using kN units (alias for kilonewton)."""
        return self.kilonewton
    
    @property
    def millinewton(self):
        """Set value using millinewton units."""
        unit_const = units.ForceUnits.millinewton
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_cc_or_dyn_mathrm_cm_3(self):
        """Set value using dyn_cc_or_dyn_mathrm_cm_3 units (alias for dyne_per_cubic_centimeter)."""
        return self.dyne_per_cubic_centimeter
    
    @property
    def dyn_cc(self):
        """Set value using dyn_cc units (alias for dyne_per_cubic_centimeter)."""
        return self.dyne_per_cubic_centimeter
    
    @property
    def dyn_cm_3(self):
        """Set value using dyn_cm_3 units (alias for dyne_per_cubic_centimeter)."""
        return self.dyne_per_cubic_centimeter
    
    @property
    def kilogram_force_per_cubic_centimeter(self):
        """Set value using kilogram force per cubic centimeter units."""
        unit_const = units.ForceBodyUnits.kilogram_force_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_cm_3(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_cm_3 units (alias for kilogram_force_per_cubic_centimeter)."""
        return self.kilogram_force_per_cubic_centimeter
    
    @property
    def kilogram_force_per_cubic_meter(self):
        """Set value using kilogram force per cubic meter units."""
        unit_const = units.ForceBodyUnits.kilogram_force_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_m_3(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_m_3 units (alias for kilogram_force_per_cubic_meter)."""
        return self.kilogram_force_per_cubic_meter
    
    @property
    def newton_per_cubic_meter(self):
        """Set value using newton per cubic meter units."""
        unit_const = units.ForceBodyUnits.newton_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_N_mathrm_m_3(self):
        """Set value using mathrm_N_mathrm_m_3 units (alias for newton_per_cubic_meter)."""
        return self.newton_per_cubic_meter
    
    @property
    def pound_force_per_cubic_foot(self):
        """Set value using pound force per cubic foot units."""
        unit_const = units.ForceBodyUnits.pound_force_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_cft(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_cft units (alias for pound_force_per_cubic_foot)."""
        return self.pound_force_per_cubic_foot
    
    @property
    def pound_force_per_cubic_inch(self):
        """Set value using pound force per cubic inch units."""
        unit_const = units.ForceBodyUnits.pound_force_per_cubic_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_cu_mathrm_in(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_cu_mathrm_in units (alias for pound_force_per_cubic_inch)."""
        return self.pound_force_per_cubic_inch
    
    @property
    def ton_force_per_cubic_foot(self):
        """Set value using ton force per cubic foot units."""
        unit_const = units.ForceBodyUnits.ton_force_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_mathrm_f_mathrm_cft(self):
        """Set value using ton_mathrm_f_mathrm_cft units (alias for ton_force_per_cubic_foot)."""
        return self.ton_force_per_cubic_foot
    

class ForcePerUnitMassSetter(TypeSafeSetter):
    """ForcePerUnitMass-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_gram(self):
        """Set value using dyne per gram units."""
        unit_const = units.ForcePerUnitMassUnits.dyne_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_g(self):
        """Set value using dyn_g units (alias for dyne_per_gram)."""
        return self.dyne_per_gram
    
    @property
    def kilogram_force_per_kilogram(self):
        """Set value using kilogram force per kilogram units."""
        unit_const = units.ForcePerUnitMassUnits.kilogram_force_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_kg(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_kg units (alias for kilogram_force_per_kilogram)."""
        return self.kilogram_force_per_kilogram
    
    @property
    def newton_per_kilogram(self):
        """Set value using newton per kilogram units."""
        unit_const = units.ForcePerUnitMassUnits.newton_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def N_kg(self):
        """Set value using N_kg units (alias for newton_per_kilogram)."""
        return self.newton_per_kilogram
    
    @property
    def pound_force_per_pound_mass(self):
        """Set value using pound force per pound mass units."""
        unit_const = units.ForcePerUnitMassUnits.pound_force_per_pound_mass
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_lb_or_mathrm_lb_mathrm_f_mathrm_lb_mathrm_m(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_lb_or_mathrm_lb_mathrm_f_mathrm_lb_mathrm_m units (alias for pound_force_per_pound_mass)."""
        return self.pound_force_per_pound_mass
    
    @property
    def lb_f_lb(self):
        """Set value using lb_f_lb units (alias for pound_force_per_pound_mass)."""
        return self.pound_force_per_pound_mass
    
    @property
    def lb_f_lb_m(self):
        """Set value using lb_f_lb_m units (alias for pound_force_per_pound_mass)."""
        return self.pound_force_per_pound_mass
    
    @property
    def pound_force_per_slug(self):
        """Set value using pound force per slug units."""
        unit_const = units.ForcePerUnitMassUnits.pound_force_per_slug
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_slug(self):
        """Set value using mathrm_lb_mathrm_f_slug units (alias for pound_force_per_slug)."""
        return self.pound_force_per_slug
    

class FrequencyVoltageRatioSetter(TypeSafeSetter):
    """FrequencyVoltageRatio-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cycles_per_second_per_volt(self):
        """Set value using cycles per second per volt units."""
        unit_const = units.FrequencyVoltageRatioUnits.cycles_per_second_per_volt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cycle_sec_V(self):
        """Set value using cycle_sec_V units (alias for cycles_per_second_per_volt)."""
        return self.cycles_per_second_per_volt
    
    @property
    def hertz_per_volt(self):
        """Set value using hertz per volt units."""
        unit_const = units.FrequencyVoltageRatioUnits.hertz_per_volt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Hz_V(self):
        """Set value using Hz_V units (alias for hertz_per_volt)."""
        return self.hertz_per_volt
    
    @property
    def terahertz_per_volt(self):
        """Set value using terahertz per volt units."""
        unit_const = units.FrequencyVoltageRatioUnits.terahertz_per_volt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def THz_V(self):
        """Set value using THz_V units (alias for terahertz_per_volt)."""
        return self.terahertz_per_volt
    

class FuelConsumptionSetter(TypeSafeSetter):
    """FuelConsumption-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def unit_100_km_per_liter(self):
        """Set value using 100 km per liter units."""
        unit_const = units.FuelConsumptionUnits.unit_100_km_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gallons_uk(self):
        """Set value using gallons (UK) per 100 miles units."""
        unit_const = units.FuelConsumptionUnits.gallons_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_UK_100_mi(self):
        """Set value using gal_UK_100_mi units (alias for gallons_uk)."""
        return self.gallons_uk
    
    @property
    def gallons_us(self):
        """Set value using gallons (US) per 100 miles units."""
        unit_const = units.FuelConsumptionUnits.gallons_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_US_100_mi(self):
        """Set value using gal_US_100_mi units (alias for gallons_us)."""
        return self.gallons_us
    
    @property
    def kilometers_per_gallon_uk(self):
        """Set value using kilometers per gallon (UK) units."""
        unit_const = units.FuelConsumptionUnits.kilometers_per_gallon_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def km_gal_UK(self):
        """Set value using km_gal_UK units (alias for kilometers_per_gallon_uk)."""
        return self.kilometers_per_gallon_uk
    
    @property
    def kilometers_per_gallon_us(self):
        """Set value using kilometers per gallon (US) units."""
        unit_const = units.FuelConsumptionUnits.kilometers_per_gallon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def km_gal_US(self):
        """Set value using km_gal_US units (alias for kilometers_per_gallon_us)."""
        return self.kilometers_per_gallon_us
    
    @property
    def kilometers_per_liter(self):
        """Set value using kilometers per liter units."""
        unit_const = units.FuelConsumptionUnits.kilometers_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def km_l(self):
        """Set value using km_l units (alias for kilometers_per_liter)."""
        return self.kilometers_per_liter
    
    @property
    def liters_per_100_km(self):
        """Set value using liters per 100 km units."""
        unit_const = units.FuelConsumptionUnits.liters_per_100_km
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_kilometer(self):
        """Set value using liters per kilometer units."""
        unit_const = units.FuelConsumptionUnits.liters_per_kilometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1_km(self):
        """Set value using unit_1_km units (alias for liters_per_kilometer)."""
        return self.liters_per_kilometer
    
    @property
    def meters_per_gallon_uk(self):
        """Set value using meters per gallon (UK) units."""
        unit_const = units.FuelConsumptionUnits.meters_per_gallon_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_gal_UK(self):
        """Set value using m_gal_UK units (alias for meters_per_gallon_uk)."""
        return self.meters_per_gallon_uk
    
    @property
    def meters_per_gallon_us(self):
        """Set value using meters per gallon (US) units."""
        unit_const = units.FuelConsumptionUnits.meters_per_gallon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1_gal_US(self):
        """Set value using unit_1_gal_US units (alias for meters_per_gallon_us)."""
        return self.meters_per_gallon_us
    
    @property
    def miles_per_gallon_uk(self):
        """Set value using miles per gallon (UK) units."""
        unit_const = units.FuelConsumptionUnits.miles_per_gallon_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_gal_UK_or_mpg_UK(self):
        """Set value using mi_gal_UK_or_mpg_UK units (alias for miles_per_gallon_uk)."""
        return self.miles_per_gallon_uk
    
    @property
    def mi_gal_UK(self):
        """Set value using mi_gal_UK units (alias for miles_per_gallon_uk)."""
        return self.miles_per_gallon_uk
    
    @property
    def mpg_UK(self):
        """Set value using mpg_UK units (alias for miles_per_gallon_uk)."""
        return self.miles_per_gallon_uk
    
    @property
    def miles_per_gallon_us(self):
        """Set value using miles per gallon (US) units."""
        unit_const = units.FuelConsumptionUnits.miles_per_gallon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_gal_US_or_mpg_US(self):
        """Set value using mi_gal_US_or_mpg_US units (alias for miles_per_gallon_us)."""
        return self.miles_per_gallon_us
    
    @property
    def mi_gal_US(self):
        """Set value using mi_gal_US units (alias for miles_per_gallon_us)."""
        return self.miles_per_gallon_us
    
    @property
    def mpg_US(self):
        """Set value using mpg_US units (alias for miles_per_gallon_us)."""
        return self.miles_per_gallon_us
    
    @property
    def miles_per_liter(self):
        """Set value using miles per liter units."""
        unit_const = units.FuelConsumptionUnits.miles_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_l(self):
        """Set value using mi_l units (alias for miles_per_liter)."""
        return self.miles_per_liter
    

class HeatOfCombustionSetter(TypeSafeSetter):
    """HeatOfCombustion-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.HeatOfCombustionUnits.british_thermal_unit_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_lb(self):
        """Set value using Btu_lb units (alias for british_thermal_unit_per_pound)."""
        return self.british_thermal_unit_per_pound
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.HeatOfCombustionUnits.calorie_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cal_mathrm_g(self):
        """Set value using mathrm_cal_mathrm_g units (alias for calorie_per_gram)."""
        return self.calorie_per_gram
    
    @property
    def chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.HeatOfCombustionUnits.chu_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_lb(self):
        """Set value using Chu_lb units (alias for chu_per_pound)."""
        return self.chu_per_pound
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.HeatOfCombustionUnits.joule_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_kg(self):
        """Set value using J_kg units (alias for joule_per_kilogram)."""
        return self.joule_per_kilogram
    

class HeatOfFusionSetter(TypeSafeSetter):
    """HeatOfFusion-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_mean(self):
        """Set value using British thermal unit (mean) per pound units."""
        unit_const = units.HeatOfFusionUnits.british_thermal_unit_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_mean_lb(self):
        """Set value using Btu_mean_lb units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def british_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.HeatOfFusionUnits.british_thermal_unit_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_lb(self):
        """Set value using Btu_lb units (alias for british_thermal_unit_per_pound)."""
        return self.british_thermal_unit_per_pound
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.HeatOfFusionUnits.calorie_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cal_mathrm_g(self):
        """Set value using mathrm_cal_mathrm_g units (alias for calorie_per_gram)."""
        return self.calorie_per_gram
    
    @property
    def chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.HeatOfFusionUnits.chu_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_lb(self):
        """Set value using Chu_lb units (alias for chu_per_pound)."""
        return self.chu_per_pound
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.HeatOfFusionUnits.joule_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_kg(self):
        """Set value using J_kg units (alias for joule_per_kilogram)."""
        return self.joule_per_kilogram
    

class HeatOfVaporizationSetter(TypeSafeSetter):
    """HeatOfVaporization-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.HeatOfVaporizationUnits.british_thermal_unit_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_lb(self):
        """Set value using Btu_lb units (alias for british_thermal_unit_per_pound)."""
        return self.british_thermal_unit_per_pound
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.HeatOfVaporizationUnits.calorie_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cal_mathrm_g(self):
        """Set value using mathrm_cal_mathrm_g units (alias for calorie_per_gram)."""
        return self.calorie_per_gram
    
    @property
    def chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.HeatOfVaporizationUnits.chu_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_lb(self):
        """Set value using Chu_lb units (alias for chu_per_pound)."""
        return self.chu_per_pound
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.HeatOfVaporizationUnits.joule_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_kg(self):
        """Set value using J_kg units (alias for joule_per_kilogram)."""
        return self.joule_per_kilogram
    

class HeatTransferCoefficientSetter(TypeSafeSetter):
    """HeatTransferCoefficient-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def btu_per_square_foot_per_hour_per_degree_fahrenheit_or_rankine(self):
        """Set value using Btu per square foot per hour per degree Fahrenheit (or Rankine) units."""
        unit_const = units.HeatTransferCoefficientUnits.btu_per_square_foot_per_hour_per_degree_fahrenheit_or_rankine
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Btu_left_mathrm_ft_2_mathrm_h_circ_mathrm_F_right(self):
        """Set value using mathrm_Btu_left_mathrm_ft_2_mathrm_h_circ_mathrm_F_right units (alias for btu_per_square_foot_per_hour_per_degree_fahrenheit_or_rankine)."""
        return self.btu_per_square_foot_per_hour_per_degree_fahrenheit_or_rankine
    
    @property
    def watt_per_square_meter_per_degree_celsius_or_kelvin(self):
        """Set value using watt per square meter per degree Celsius (or kelvin) units."""
        unit_const = units.HeatTransferCoefficientUnits.watt_per_square_meter_per_degree_celsius_or_kelvin
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_W_left_mathrm_m_2_circ_mathrm_C_right(self):
        """Set value using mathrm_W_left_mathrm_m_2_circ_mathrm_C_right units (alias for watt_per_square_meter_per_degree_celsius_or_kelvin)."""
        return self.watt_per_square_meter_per_degree_celsius_or_kelvin
    

class IlluminanceSetter(TypeSafeSetter):
    """Illuminance-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_candle(self):
        """Set value using foot-candle units."""
        unit_const = units.IlluminanceUnits.foot_candle
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_C_or_mathrm_ft_mathrm_Cd(self):
        """Set value using mathrm_ft_mathrm_C_or_mathrm_ft_mathrm_Cd units (alias for foot_candle)."""
        return self.foot_candle
    
    @property
    def ft_C(self):
        """Set value using ft_C units (alias for foot_candle)."""
        return self.foot_candle
    
    @property
    def ft_Cd(self):
        """Set value using ft_Cd units (alias for foot_candle)."""
        return self.foot_candle
    
    @property
    def lux(self):
        """Set value using lux units."""
        unit_const = units.IlluminanceUnits.lux
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lx(self):
        """Set value using lx units (alias for lux)."""
        return self.lux
    
    @property
    def nox(self):
        """Set value using nox units."""
        unit_const = units.IlluminanceUnits.nox
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def phot(self):
        """Set value using phot units."""
        unit_const = units.IlluminanceUnits.phot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ph(self):
        """Set value using ph units (alias for phot)."""
        return self.phot
    
    @property
    def skot(self):
        """Set value using skot units."""
        unit_const = units.IlluminanceUnits.skot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class KineticEnergyOfTurbulenceSetter(TypeSafeSetter):
    """KineticEnergyOfTurbulence-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_foot_per_second_squared(self):
        """Set value using square foot per second squared units."""
        unit_const = units.KineticEnergyOfTurbulenceUnits.square_foot_per_second_squared
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_mathrm_s_2_or_sqft_sec_2(self):
        """Set value using mathrm_ft_2_mathrm_s_2_or_sqft_sec_2 units (alias for square_foot_per_second_squared)."""
        return self.square_foot_per_second_squared
    
    @property
    def ft_2_s_2(self):
        """Set value using ft_2_s_2 units (alias for square_foot_per_second_squared)."""
        return self.square_foot_per_second_squared
    
    @property
    def sqft_sec_2(self):
        """Set value using sqft_sec_2 units (alias for square_foot_per_second_squared)."""
        return self.square_foot_per_second_squared
    
    @property
    def square_meters_per_second_squared(self):
        """Set value using square meters per second squared units."""
        unit_const = units.KineticEnergyOfTurbulenceUnits.square_meters_per_second_squared
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2_mathrm_s_2(self):
        """Set value using mathrm_m_2_mathrm_s_2 units (alias for square_meters_per_second_squared)."""
        return self.square_meters_per_second_squared
    

class LengthSetter(TypeSafeSetter):
    """Length-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def ngstr_m(self):
        """Set value using ångström units."""
        unit_const = units.LengthUnits.ngstr_m
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def AA(self):
        """Set value using AA units (alias for ngstr_m)."""
        return self.ngstr_m
    
    @property
    def arpent_quebec(self):
        """Set value using arpent (Quebec) units."""
        unit_const = units.LengthUnits.arpent_quebec
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def arp(self):
        """Set value using arp units (alias for arpent_quebec)."""
        return self.arpent_quebec
    
    @property
    def astronomic_unit(self):
        """Set value using astronomic unit units."""
        unit_const = units.LengthUnits.astronomic_unit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def AU(self):
        """Set value using AU units (alias for astronomic_unit)."""
        return self.astronomic_unit
    
    @property
    def attometer(self):
        """Set value using attometer units."""
        unit_const = units.LengthUnits.attometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def am(self):
        """Set value using am units (alias for attometer)."""
        return self.attometer
    
    @property
    def calibre_centinch(self):
        """Set value using calibre (centinch) units."""
        unit_const = units.LengthUnits.calibre_centinch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cin(self):
        """Set value using cin units (alias for calibre_centinch)."""
        return self.calibre_centinch
    
    @property
    def centimeter(self):
        """Set value using centimeter units."""
        unit_const = units.LengthUnits.centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm(self):
        """Set value using cm units (alias for centimeter)."""
        return self.centimeter
    
    @property
    def chain_engrs_or_ramsden(self):
        """Set value using chain (Engr's or Ramsden) units."""
        unit_const = units.LengthUnits.chain_engrs_or_ramsden
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ch_eng_or_Rams(self):
        """Set value using ch_eng_or_Rams units (alias for chain_engrs_or_ramsden)."""
        return self.chain_engrs_or_ramsden
    
    @property
    def ch_eng(self):
        """Set value using ch_eng units (alias for chain_engrs_or_ramsden)."""
        return self.chain_engrs_or_ramsden
    
    @property
    def Rams(self):
        """Set value using Rams units (alias for chain_engrs_or_ramsden)."""
        return self.chain_engrs_or_ramsden
    
    @property
    def chain_gunters(self):
        """Set value using chain (Gunter's) units."""
        unit_const = units.LengthUnits.chain_gunters
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ch_Gunt(self):
        """Set value using ch_Gunt units (alias for chain_gunters)."""
        return self.chain_gunters
    
    @property
    def chain_surveyors(self):
        """Set value using chain (surveyors) units."""
        unit_const = units.LengthUnits.chain_surveyors
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ch_surv(self):
        """Set value using ch_surv units (alias for chain_surveyors)."""
        return self.chain_surveyors
    
    @property
    def cubit_uk(self):
        """Set value using cubit (UK) units."""
        unit_const = units.LengthUnits.cubit_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_UK(self):
        """Set value using cu_UK units (alias for cubit_uk)."""
        return self.cubit_uk
    
    @property
    def ell(self):
        """Set value using ell units."""
        unit_const = units.LengthUnits.ell
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fathom(self):
        """Set value using fathom units."""
        unit_const = units.LengthUnits.fathom
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fath(self):
        """Set value using fath units (alias for fathom)."""
        return self.fathom
    
    @property
    def femtometre(self):
        """Set value using femtometre units."""
        unit_const = units.LengthUnits.femtometre
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fm(self):
        """Set value using fm units (alias for femtometre)."""
        return self.femtometre
    
    @property
    def fermi(self):
        """Set value using fermi units."""
        unit_const = units.LengthUnits.fermi
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def F(self):
        """Set value using F units (alias for fermi)."""
        return self.fermi
    
    @property
    def foot(self):
        """Set value using foot units."""
        unit_const = units.LengthUnits.foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft(self):
        """Set value using ft units (alias for foot)."""
        return self.foot
    
    @property
    def furlong_uk_and_us(self):
        """Set value using furlong (UK and US) units."""
        unit_const = units.LengthUnits.furlong_uk_and_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fur(self):
        """Set value using fur units (alias for furlong_uk_and_us)."""
        return self.furlong_uk_and_us
    
    @property
    def inch(self):
        """Set value using inch units."""
        unit_const = units.LengthUnits.inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_unit(self):
        """Set value using in_unit units (alias for inch)."""
        return self.inch
    
    @property
    def kilometer(self):
        """Set value using kilometer units."""
        unit_const = units.LengthUnits.kilometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def km(self):
        """Set value using km units (alias for kilometer)."""
        return self.kilometer
    
    @property
    def league_us_statute(self):
        """Set value using league (US, statute) units."""
        unit_const = units.LengthUnits.league_us_statute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lg_US_stat(self):
        """Set value using lg_US_stat units (alias for league_us_statute)."""
        return self.league_us_statute
    
    @property
    def lieue_metric(self):
        """Set value using lieue (metric) units."""
        unit_const = units.LengthUnits.lieue_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ligne_metric(self):
        """Set value using ligne (metric) units."""
        unit_const = units.LengthUnits.ligne_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def line_us(self):
        """Set value using line (US) units."""
        unit_const = units.LengthUnits.line_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def li_US(self):
        """Set value using li_US units (alias for line_us)."""
        return self.line_us
    
    @property
    def link_surveyors(self):
        """Set value using link (surveyors) units."""
        unit_const = units.LengthUnits.link_surveyors
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def li_surv(self):
        """Set value using li_surv units (alias for link_surveyors)."""
        return self.link_surveyors
    
    @property
    def meter(self):
        """Set value using meter units."""
        unit_const = units.LengthUnits.meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def m(self):
        """Set value using m units (alias for meter)."""
        return self.meter
    
    @property
    def micrometer(self):
        """Set value using micrometer units."""
        unit_const = units.LengthUnits.micrometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_m(self):
        """Set value using mu_mathrm_m units (alias for micrometer)."""
        return self.micrometer
    
    @property
    def micron(self):
        """Set value using micron units."""
        unit_const = units.LengthUnits.micron
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu(self):
        """Set value using mu units (alias for micron)."""
        return self.micron
    
    @property
    def mil(self):
        """Set value using mil units."""
        unit_const = units.LengthUnits.mil
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mile_geographical(self):
        """Set value using mile (geographical) units."""
        unit_const = units.LengthUnits.mile_geographical
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi(self):
        """Set value using mi units (alias for mile_geographical)."""
        return self.mile_geographical
    
    @property
    def mile_us_nautical(self):
        """Set value using mile (US, nautical) units."""
        unit_const = units.LengthUnits.mile_us_nautical
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_US_naut(self):
        """Set value using mi_US_naut units (alias for mile_us_nautical)."""
        return self.mile_us_nautical
    
    @property
    def mile_us_statute(self):
        """Set value using mile (US, statute) units."""
        unit_const = units.LengthUnits.mile_us_statute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mile_us_survey(self):
        """Set value using mile (US, survey) units."""
        unit_const = units.LengthUnits.mile_us_survey
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mi_US_surv(self):
        """Set value using mi_US_surv units (alias for mile_us_survey)."""
        return self.mile_us_survey
    
    @property
    def millimeter(self):
        """Set value using millimeter units."""
        unit_const = units.LengthUnits.millimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mm(self):
        """Set value using mm units (alias for millimeter)."""
        return self.millimeter
    
    @property
    def millimicron(self):
        """Set value using millimicron units."""
        unit_const = units.LengthUnits.millimicron
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_mu(self):
        """Set value using mathrm_m_mu units (alias for millimicron)."""
        return self.millimicron
    
    @property
    def nanometer_or_nanon(self):
        """Set value using nanometer or nanon units."""
        unit_const = units.LengthUnits.nanometer_or_nanon
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nm(self):
        """Set value using nm units (alias for nanometer_or_nanon)."""
        return self.nanometer_or_nanon
    
    @property
    def parsec(self):
        """Set value using parsec units."""
        unit_const = units.LengthUnits.parsec
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pc(self):
        """Set value using pc units (alias for parsec)."""
        return self.parsec
    
    @property
    def perche(self):
        """Set value using perche units."""
        unit_const = units.LengthUnits.perche
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def rod(self):
        """Set value using rod units (alias for perche)."""
        return self.perche
    
    @property
    def pica(self):
        """Set value using pica units."""
        unit_const = units.LengthUnits.pica
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def picometer(self):
        """Set value using picometer units."""
        unit_const = units.LengthUnits.picometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pm(self):
        """Set value using pm units (alias for picometer)."""
        return self.picometer
    
    @property
    def point_didot(self):
        """Set value using point (Didot) units."""
        unit_const = units.LengthUnits.point_didot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pt_Didot(self):
        """Set value using pt_Didot units (alias for point_didot)."""
        return self.point_didot
    
    @property
    def point_us(self):
        """Set value using point (US) units."""
        unit_const = units.LengthUnits.point_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pt_US(self):
        """Set value using pt_US units (alias for point_us)."""
        return self.point_us
    
    @property
    def rod_or_pole(self):
        """Set value using rod or pole units."""
        unit_const = units.LengthUnits.rod_or_pole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def span(self):
        """Set value using span units."""
        unit_const = units.LengthUnits.span
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def thou_millinch(self):
        """Set value using thou (millinch) units."""
        unit_const = units.LengthUnits.thou_millinch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def thou(self):
        """Set value using thou units (alias for thou_millinch)."""
        return self.thou_millinch
    
    @property
    def toise_metric(self):
        """Set value using toise (metric) units."""
        unit_const = units.LengthUnits.toise_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def yard(self):
        """Set value using yard units."""
        unit_const = units.LengthUnits.yard
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def yd(self):
        """Set value using yd units (alias for yard)."""
        return self.yard
    
    @property
    def nanometer(self):
        """Set value using nanometer units."""
        unit_const = units.LengthUnits.nanometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class LinearMassDensitySetter(TypeSafeSetter):
    """LinearMassDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def denier(self):
        """Set value using denier units."""
        unit_const = units.LinearMassDensityUnits.denier
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilogram_per_centimeter(self):
        """Set value using kilogram per centimeter units."""
        unit_const = units.LinearMassDensityUnits.kilogram_per_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_cm(self):
        """Set value using kg_cm units (alias for kilogram_per_centimeter)."""
        return self.kilogram_per_centimeter
    
    @property
    def kilogram_per_meter(self):
        """Set value using kilogram per meter units."""
        unit_const = units.LinearMassDensityUnits.kilogram_per_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_m(self):
        """Set value using kg_m units (alias for kilogram_per_meter)."""
        return self.kilogram_per_meter
    
    @property
    def pound_per_foot(self):
        """Set value using pound per foot units."""
        unit_const = units.LinearMassDensityUnits.pound_per_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft(self):
        """Set value using lb_ft units (alias for pound_per_foot)."""
        return self.pound_per_foot
    
    @property
    def pound_per_inch(self):
        """Set value using pound per inch units."""
        unit_const = units.LinearMassDensityUnits.pound_per_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_in(self):
        """Set value using lb_in units (alias for pound_per_inch)."""
        return self.pound_per_inch
    
    @property
    def pound_per_yard(self):
        """Set value using pound per yard units."""
        unit_const = units.LinearMassDensityUnits.pound_per_yard
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_yd(self):
        """Set value using lb_yd units (alias for pound_per_yard)."""
        return self.pound_per_yard
    
    @property
    def ton_metric(self):
        """Set value using ton (metric) per kilometer units."""
        unit_const = units.LinearMassDensityUnits.ton_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def t_km_or_MT_km(self):
        """Set value using t_km_or_MT_km units (alias for ton_metric)."""
        return self.ton_metric
    
    @property
    def t_km(self):
        """Set value using t_km units (alias for ton_metric)."""
        return self.ton_metric
    
    @property
    def MT_km(self):
        """Set value using MT_km units (alias for ton_metric)."""
        return self.ton_metric
    

class LinearMomentumSetter(TypeSafeSetter):
    """LinearMomentum-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_pounds_force_per_hour(self):
        """Set value using foot pounds force per hour units."""
        unit_const = units.LinearMomentumUnits.foot_pounds_force_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_f_mathrm_h_or_mathrm_ft_mathrm_lb_mathrm_hr(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_f_mathrm_h_or_mathrm_ft_mathrm_lb_mathrm_hr units (alias for foot_pounds_force_per_hour)."""
        return self.foot_pounds_force_per_hour
    
    @property
    def ft_lb_f_h(self):
        """Set value using ft_lb_f_h units (alias for foot_pounds_force_per_hour)."""
        return self.foot_pounds_force_per_hour
    
    @property
    def ft_lb_hr(self):
        """Set value using ft_lb_hr units (alias for foot_pounds_force_per_hour)."""
        return self.foot_pounds_force_per_hour
    
    @property
    def foot_pounds_force_per_minute(self):
        """Set value using foot pounds force per minute units."""
        unit_const = units.LinearMomentumUnits.foot_pounds_force_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_f_min_or_mathrm_ft_mathrm_lb_min(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_f_min_or_mathrm_ft_mathrm_lb_min units (alias for foot_pounds_force_per_minute)."""
        return self.foot_pounds_force_per_minute
    
    @property
    def ft_lb_f_min(self):
        """Set value using ft_lb_f_min units (alias for foot_pounds_force_per_minute)."""
        return self.foot_pounds_force_per_minute
    
    @property
    def ft_lb_min(self):
        """Set value using ft_lb_min units (alias for foot_pounds_force_per_minute)."""
        return self.foot_pounds_force_per_minute
    
    @property
    def foot_pounds_force_per_second(self):
        """Set value using foot pounds force per second units."""
        unit_const = units.LinearMomentumUnits.foot_pounds_force_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_f_mathrm_s_or_ft_lb_sec(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_f_mathrm_s_or_ft_lb_sec units (alias for foot_pounds_force_per_second)."""
        return self.foot_pounds_force_per_second
    
    @property
    def ft_lb_f_s(self):
        """Set value using ft_lb_f_s units (alias for foot_pounds_force_per_second)."""
        return self.foot_pounds_force_per_second
    
    @property
    def ft_lb_sec(self):
        """Set value using ft_lb_sec units (alias for foot_pounds_force_per_second)."""
        return self.foot_pounds_force_per_second
    
    @property
    def gram_centimeters_per_second(self):
        """Set value using gram centimeters per second units."""
        unit_const = units.LinearMomentumUnits.gram_centimeters_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_cm_mathrm_s(self):
        """Set value using mathrm_g_mathrm_cm_mathrm_s units (alias for gram_centimeters_per_second)."""
        return self.gram_centimeters_per_second
    
    @property
    def kilogram_meters_per_second(self):
        """Set value using kilogram meters per second units."""
        unit_const = units.LinearMomentumUnits.kilogram_meters_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_mathrm_s(self):
        """Set value using mathrm_kg_mathrm_m_mathrm_s units (alias for kilogram_meters_per_second)."""
        return self.kilogram_meters_per_second
    

class LuminanceSelfSetter(TypeSafeSetter):
    """LuminanceSelf-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def apostilb(self):
        """Set value using apostilb units."""
        unit_const = units.LuminanceSelfUnits.apostilb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def asb(self):
        """Set value using asb units (alias for apostilb)."""
        return self.apostilb
    
    @property
    def blondel(self):
        """Set value using blondel units."""
        unit_const = units.LuminanceSelfUnits.blondel
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def B1(self):
        """Set value using B1 units (alias for blondel)."""
        return self.blondel
    
    @property
    def candela_per_square_meter(self):
        """Set value using candela per square meter units."""
        unit_const = units.LuminanceSelfUnits.candela_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cd_mathrm_m_2(self):
        """Set value using mathrm_cd_mathrm_m_2 units (alias for candela_per_square_meter)."""
        return self.candela_per_square_meter
    
    @property
    def foot_lambert(self):
        """Set value using foot-lambert units."""
        unit_const = units.LuminanceSelfUnits.foot_lambert
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_L(self):
        """Set value using ft_L units (alias for foot_lambert)."""
        return self.foot_lambert
    
    @property
    def lambert(self):
        """Set value using lambert units."""
        unit_const = units.LuminanceSelfUnits.lambert
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def L(self):
        """Set value using L units (alias for lambert)."""
        return self.lambert
    
    @property
    def luxon(self):
        """Set value using luxon units."""
        unit_const = units.LuminanceSelfUnits.luxon
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nit(self):
        """Set value using nit units."""
        unit_const = units.LuminanceSelfUnits.nit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def stilb(self):
        """Set value using stilb units."""
        unit_const = units.LuminanceSelfUnits.stilb
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sb(self):
        """Set value using sb units (alias for stilb)."""
        return self.stilb
    
    @property
    def troland(self):
        """Set value using troland units."""
        unit_const = units.LuminanceSelfUnits.troland
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class LuminousFluxSetter(TypeSafeSetter):
    """LuminousFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def candela_steradian(self):
        """Set value using candela steradian units."""
        unit_const = units.LuminousFluxUnits.candela_steradian
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cd_sr(self):
        """Set value using cd_sr units (alias for candela_steradian)."""
        return self.candela_steradian
    
    @property
    def lumen(self):
        """Set value using lumen units."""
        unit_const = units.LuminousFluxUnits.lumen
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class LuminousIntensitySetter(TypeSafeSetter):
    """LuminousIntensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def candela(self):
        """Set value using candela units."""
        unit_const = units.LuminousIntensityUnits.candela
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cd(self):
        """Set value using cd units (alias for candela)."""
        return self.candela
    
    @property
    def candle_international(self):
        """Set value using candle (international) units."""
        unit_const = units.LuminousIntensityUnits.candle_international
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Cd_int(self):
        """Set value using Cd_int units (alias for candle_international)."""
        return self.candle_international
    
    @property
    def carcel(self):
        """Set value using carcel units."""
        unit_const = units.LuminousIntensityUnits.carcel
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def hefner_unit(self):
        """Set value using Hefner unit units."""
        unit_const = units.LuminousIntensityUnits.hefner_unit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def HK(self):
        """Set value using HK units (alias for hefner_unit)."""
        return self.hefner_unit
    

class MagneticFieldSetter(TypeSafeSetter):
    """MagneticField-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def ampere_per_meter(self):
        """Set value using ampere per meter units."""
        unit_const = units.MagneticFieldUnits.ampere_per_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def A_m(self):
        """Set value using A_m units (alias for ampere_per_meter)."""
        return self.ampere_per_meter
    
    @property
    def lenz(self):
        """Set value using lenz units."""
        unit_const = units.MagneticFieldUnits.lenz
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def oersted(self):
        """Set value using oersted units."""
        unit_const = units.MagneticFieldUnits.oersted
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Oe(self):
        """Set value using Oe units (alias for oersted)."""
        return self.oersted
    
    @property
    def praoersted(self):
        """Set value using praoersted units."""
        unit_const = units.MagneticFieldUnits.praoersted
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unnamed(self):
        """Set value using unnamed units (alias for praoersted)."""
        return self.praoersted
    

class MagneticFluxSetter(TypeSafeSetter):
    """MagneticFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kapp_line(self):
        """Set value using kapp line units."""
        unit_const = units.MagneticFluxUnits.kapp_line
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unnamed(self):
        """Set value using unnamed units (alias for kapp_line)."""
        return self.kapp_line
    
    @property
    def line(self):
        """Set value using line units."""
        unit_const = units.MagneticFluxUnits.line
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def maxwell(self):
        """Set value using maxwell units."""
        unit_const = units.MagneticFluxUnits.maxwell
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Mx(self):
        """Set value using Mx units (alias for maxwell)."""
        return self.maxwell
    
    @property
    def unit_pole(self):
        """Set value using unit pole units."""
        unit_const = units.MagneticFluxUnits.unit_pole
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def weber(self):
        """Set value using weber units."""
        unit_const = units.MagneticFluxUnits.weber
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Wb(self):
        """Set value using Wb units (alias for weber)."""
        return self.weber
    
    @property
    def milliweber(self):
        """Set value using milliweber units."""
        unit_const = units.MagneticFluxUnits.milliweber
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mWb(self):
        """Set value using mWb units (alias for milliweber)."""
        return self.milliweber
    
    @property
    def microweber(self):
        """Set value using microweber units."""
        unit_const = units.MagneticFluxUnits.microweber
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class MagneticInductionFieldStrengthSetter(TypeSafeSetter):
    """MagneticInductionFieldStrength-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gamma(self):
        """Set value using gamma units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.gamma
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gauss(self):
        """Set value using gauss units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.gauss
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def G(self):
        """Set value using G units (alias for gauss)."""
        return self.gauss
    
    @property
    def line_per_square_centimeter(self):
        """Set value using line per square centimeter units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.line_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def line_mathrm_cm_2(self):
        """Set value using line_mathrm_cm_2 units (alias for line_per_square_centimeter)."""
        return self.line_per_square_centimeter
    
    @property
    def maxwell_per_square_centimeter(self):
        """Set value using maxwell per square centimeter units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.maxwell_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Mx_mathrm_cm_2(self):
        """Set value using mathrm_Mx_mathrm_cm_2 units (alias for maxwell_per_square_centimeter)."""
        return self.maxwell_per_square_centimeter
    
    @property
    def tesla(self):
        """Set value using tesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.tesla
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def T(self):
        """Set value using T units (alias for tesla)."""
        return self.tesla
    
    @property
    def u_a(self):
        """Set value using u.a. units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.u_a
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def weber_per_square_meter(self):
        """Set value using weber per square meter units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.weber_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Wb_mathrm_m_2(self):
        """Set value using mathrm_Wb_mathrm_m_2 units (alias for weber_per_square_meter)."""
        return self.weber_per_square_meter
    
    @property
    def millitesla(self):
        """Set value using millitesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.millitesla
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mT(self):
        """Set value using mT units (alias for millitesla)."""
        return self.millitesla
    
    @property
    def microtesla(self):
        """Set value using microtesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.microtesla
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanotesla(self):
        """Set value using nanotesla units."""
        unit_const = units.MagneticInductionFieldStrengthUnits.nanotesla
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nT(self):
        """Set value using nT units (alias for nanotesla)."""
        return self.nanotesla
    

class MagneticMomentSetter(TypeSafeSetter):
    """MagneticMoment-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def bohr_magneton(self):
        """Set value using Bohr magneton units."""
        unit_const = units.MagneticMomentUnits.bohr_magneton
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Bohr_magneton(self):
        """Set value using Bohr_magneton units (alias for bohr_magneton)."""
        return self.bohr_magneton
    
    @property
    def joule_per_tesla(self):
        """Set value using joule per tesla units."""
        unit_const = units.MagneticMomentUnits.joule_per_tesla
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_T(self):
        """Set value using J_T units (alias for joule_per_tesla)."""
        return self.joule_per_tesla
    
    @property
    def nuclear_magneton(self):
        """Set value using nuclear magneton units."""
        unit_const = units.MagneticMomentUnits.nuclear_magneton
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nucl_Magneton(self):
        """Set value using nucl_Magneton units (alias for nuclear_magneton)."""
        return self.nuclear_magneton
    

class MagneticPermeabilitySetter(TypeSafeSetter):
    """MagneticPermeability-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def henrys_per_meter(self):
        """Set value using henrys per meter units."""
        unit_const = units.MagneticPermeabilityUnits.henrys_per_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def H_m(self):
        """Set value using H_m units (alias for henrys_per_meter)."""
        return self.henrys_per_meter
    
    @property
    def newton_per_square_ampere(self):
        """Set value using newton per square ampere units."""
        unit_const = units.MagneticPermeabilityUnits.newton_per_square_ampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def N_A_2(self):
        """Set value using N_A_2 units (alias for newton_per_square_ampere)."""
        return self.newton_per_square_ampere
    

class MagnetomotiveForceSetter(TypeSafeSetter):
    """MagnetomotiveForce-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abampere_turn(self):
        """Set value using abampere-turn units."""
        unit_const = units.MagnetomotiveForceUnits.abampere_turn
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu_cgs(self):
        """Set value using emu_cgs units (alias for abampere_turn)."""
        return self.abampere_turn
    
    @property
    def ampere(self):
        """Set value using ampere units."""
        unit_const = units.MagnetomotiveForceUnits.ampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def A(self):
        """Set value using A units (alias for ampere)."""
        return self.ampere
    
    @property
    def ampere_turn(self):
        """Set value using ampere-turn units."""
        unit_const = units.MagnetomotiveForceUnits.ampere_turn
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def A_turn(self):
        """Set value using A_turn units (alias for ampere_turn)."""
        return self.ampere_turn
    
    @property
    def gilbert(self):
        """Set value using gilbert units."""
        unit_const = units.MagnetomotiveForceUnits.gilbert
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Gb(self):
        """Set value using Gb units (alias for gilbert)."""
        return self.gilbert
    
    @property
    def kiloampere(self):
        """Set value using kiloampere units."""
        unit_const = units.MagnetomotiveForceUnits.kiloampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kA(self):
        """Set value using kA units (alias for kiloampere)."""
        return self.kiloampere
    
    @property
    def milliampere(self):
        """Set value using milliampere units."""
        unit_const = units.MagnetomotiveForceUnits.milliampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mA(self):
        """Set value using mA units (alias for milliampere)."""
        return self.milliampere
    
    @property
    def microampere(self):
        """Set value using microampere units."""
        unit_const = units.MagnetomotiveForceUnits.microampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanoampere(self):
        """Set value using nanoampere units."""
        unit_const = units.MagnetomotiveForceUnits.nanoampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nA(self):
        """Set value using nA units (alias for nanoampere)."""
        return self.nanoampere
    
    @property
    def picoampere(self):
        """Set value using picoampere units."""
        unit_const = units.MagnetomotiveForceUnits.picoampere
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sl(self):
        """Set value using sl units (alias for slug)."""
        return self.slug
    
    @property
    def atomic_mass_unit_12_mathrmc(self):
        """Set value using atomic mass unit ( ${ }^{12} \\mathrm{C}$ ) units."""
        unit_const = units.MassUnits.atomic_mass_unit_12_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_u_left_12_mathrm_C_right_or_amu(self):
        """Set value using mathrm_u_left_12_mathrm_C_right_or_amu units (alias for atomic_mass_unit_12_mathrmc)."""
        return self.atomic_mass_unit_12_mathrmc
    
    @property
    def uleft_12_Cright(self):
        """Set value using uleft_12_Cright units (alias for atomic_mass_unit_12_mathrmc)."""
        return self.atomic_mass_unit_12_mathrmc
    
    @property
    def amu(self):
        """Set value using amu units (alias for atomic_mass_unit_12_mathrmc)."""
        return self.atomic_mass_unit_12_mathrmc
    
    @property
    def carat_metric(self):
        """Set value using carat (metric) units."""
        unit_const = units.MassUnits.carat_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ct(self):
        """Set value using ct units (alias for carat_metric)."""
        return self.carat_metric
    
    @property
    def cental(self):
        """Set value using cental units."""
        unit_const = units.MassUnits.cental
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sh_cwt_cH(self):
        """Set value using sh_cwt_cH units (alias for cental)."""
        return self.cental
    
    @property
    def centigram(self):
        """Set value using centigram units."""
        unit_const = units.MassUnits.centigram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cg(self):
        """Set value using cg units (alias for centigram)."""
        return self.centigram
    
    @property
    def clove_uk(self):
        """Set value using clove (UK) units."""
        unit_const = units.MassUnits.clove_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cl(self):
        """Set value using cl units (alias for clove_uk)."""
        return self.clove_uk
    
    @property
    def drachm_apothecary(self):
        """Set value using drachm (apothecary) units."""
        unit_const = units.MassUnits.drachm_apothecary
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dr_ap(self):
        """Set value using dr_ap units (alias for drachm_apothecary)."""
        return self.drachm_apothecary
    
    @property
    def dram_avoirdupois(self):
        """Set value using dram (avoirdupois) units."""
        unit_const = units.MassUnits.dram_avoirdupois
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dr_av(self):
        """Set value using dr_av units (alias for dram_avoirdupois)."""
        return self.dram_avoirdupois
    
    @property
    def dram_troy(self):
        """Set value using dram (troy) units."""
        unit_const = units.MassUnits.dram_troy
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dr_troy(self):
        """Set value using dr_troy units (alias for dram_troy)."""
        return self.dram_troy
    
    @property
    def grain(self):
        """Set value using grain units."""
        unit_const = units.MassUnits.grain
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gr(self):
        """Set value using gr units (alias for grain)."""
        return self.grain
    
    @property
    def gram(self):
        """Set value using gram units."""
        unit_const = units.MassUnits.gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def g(self):
        """Set value using g units (alias for gram)."""
        return self.gram
    
    @property
    def hundredweight_long_or_gross(self):
        """Set value using hundredweight, long or gross units."""
        unit_const = units.MassUnits.hundredweight_long_or_gross
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cwt_lg_cwt(self):
        """Set value using cwt_lg_cwt units (alias for hundredweight_long_or_gross)."""
        return self.hundredweight_long_or_gross
    
    @property
    def hundredweight_short_or_net(self):
        """Set value using hundredweight, short or net units."""
        unit_const = units.MassUnits.hundredweight_short_or_net
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sh_cwt(self):
        """Set value using sh_cwt units (alias for hundredweight_short_or_net)."""
        return self.hundredweight_short_or_net
    
    @property
    def kilogram(self):
        """Set value using kilogram units."""
        unit_const = units.MassUnits.kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg(self):
        """Set value using kg units (alias for kilogram)."""
        return self.kilogram
    
    @property
    def kip(self):
        """Set value using kip units."""
        unit_const = units.MassUnits.kip
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def microgram(self):
        """Set value using microgram units."""
        unit_const = units.MassUnits.microgram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_g(self):
        """Set value using mu_mathrm_g units (alias for microgram)."""
        return self.microgram
    
    @property
    def milligram(self):
        """Set value using milligram units."""
        unit_const = units.MassUnits.milligram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mg(self):
        """Set value using mg units (alias for milligram)."""
        return self.milligram
    
    @property
    def ounce_apothecary(self):
        """Set value using ounce (apothecary) units."""
        unit_const = units.MassUnits.ounce_apothecary
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def oz_ap(self):
        """Set value using oz_ap units (alias for ounce_apothecary)."""
        return self.ounce_apothecary
    
    @property
    def ounce_avoirdupois(self):
        """Set value using ounce (avoirdupois) units."""
        unit_const = units.MassUnits.ounce_avoirdupois
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def oz(self):
        """Set value using oz units (alias for ounce_avoirdupois)."""
        return self.ounce_avoirdupois
    
    @property
    def ounce_troy(self):
        """Set value using ounce (troy) units."""
        unit_const = units.MassUnits.ounce_troy
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def oz_troy(self):
        """Set value using oz_troy units (alias for ounce_troy)."""
        return self.ounce_troy
    
    @property
    def pennyweight_troy(self):
        """Set value using pennyweight (troy) units."""
        unit_const = units.MassUnits.pennyweight_troy
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dwt_troy(self):
        """Set value using dwt_troy units (alias for pennyweight_troy)."""
        return self.pennyweight_troy
    
    @property
    def pood_russia(self):
        """Set value using pood, (Russia) units."""
        unit_const = units.MassUnits.pood_russia
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pood(self):
        """Set value using pood units (alias for pood_russia)."""
        return self.pood_russia
    
    @property
    def pound_apothecary(self):
        """Set value using pound (apothecary) units."""
        unit_const = units.MassUnits.pound_apothecary
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ap(self):
        """Set value using lb_ap units (alias for pound_apothecary)."""
        return self.pound_apothecary
    
    @property
    def pound_avoirdupois(self):
        """Set value using pound (avoirdupois) units."""
        unit_const = units.MassUnits.pound_avoirdupois
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_av(self):
        """Set value using lb_av units (alias for pound_avoirdupois)."""
        return self.pound_avoirdupois
    
    @property
    def pound_troy(self):
        """Set value using pound (troy) units."""
        unit_const = units.MassUnits.pound_troy
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_troy(self):
        """Set value using lb_troy units (alias for pound_troy)."""
        return self.pound_troy
    
    @property
    def pound_mass(self):
        """Set value using pound mass units."""
        unit_const = units.MassUnits.pound_mass
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_m(self):
        """Set value using mathrm_lb_mathrm_m units (alias for pound_mass)."""
        return self.pound_mass
    
    @property
    def quarter_uk(self):
        """Set value using quarter (UK) units."""
        unit_const = units.MassUnits.quarter_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def qt(self):
        """Set value using qt units (alias for quarter_uk)."""
        return self.quarter_uk
    
    @property
    def quintal_metric(self):
        """Set value using quintal, metric units."""
        unit_const = units.MassUnits.quintal_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def q_dt(self):
        """Set value using q_dt units (alias for quintal_metric)."""
        return self.quintal_metric
    
    @property
    def quital_us(self):
        """Set value using quital, US units."""
        unit_const = units.MassUnits.quital_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def quint_US(self):
        """Set value using quint_US units (alias for quital_us)."""
        return self.quital_us
    
    @property
    def scruple_avoirdupois(self):
        """Set value using scruple (avoirdupois) units."""
        unit_const = units.MassUnits.scruple_avoirdupois
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def scf(self):
        """Set value using scf units (alias for scruple_avoirdupois)."""
        return self.scruple_avoirdupois
    
    @property
    def stone_uk(self):
        """Set value using stone (UK) units."""
        unit_const = units.MassUnits.stone_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def st(self):
        """Set value using st units (alias for stone_uk)."""
        return self.stone_uk
    
    @property
    def ton_metric(self):
        """Set value using ton, metric units."""
        unit_const = units.MassUnits.ton_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def t(self):
        """Set value using t units (alias for ton_metric)."""
        return self.ton_metric
    
    @property
    def ton_us_long(self):
        """Set value using ton, US, long units."""
        unit_const = units.MassUnits.ton_us_long
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lg_ton(self):
        """Set value using lg_ton units (alias for ton_us_long)."""
        return self.ton_us_long
    
    @property
    def ton_us_short(self):
        """Set value using ton, US, short units."""
        unit_const = units.MassUnits.ton_us_short
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sh_ton(self):
        """Set value using sh_ton units (alias for ton_us_short)."""
        return self.ton_us_short
    

class MassDensitySetter(TypeSafeSetter):
    """MassDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_cubic_centimeter(self):
        """Set value using gram per cubic centimeter units."""
        unit_const = units.MassDensityUnits.gram_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def g_cc_or_g_ml(self):
        """Set value using g_cc_or_g_ml units (alias for gram_per_cubic_centimeter)."""
        return self.gram_per_cubic_centimeter
    
    @property
    def g_cc(self):
        """Set value using g_cc units (alias for gram_per_cubic_centimeter)."""
        return self.gram_per_cubic_centimeter
    
    @property
    def g_ml(self):
        """Set value using g_ml units (alias for gram_per_cubic_centimeter)."""
        return self.gram_per_cubic_centimeter
    
    @property
    def gram_per_cubic_decimeter(self):
        """Set value using gram per cubic decimeter units."""
        unit_const = units.MassDensityUnits.gram_per_cubic_decimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_dm_3(self):
        """Set value using mathrm_g_mathrm_dm_3 units (alias for gram_per_cubic_decimeter)."""
        return self.gram_per_cubic_decimeter
    
    @property
    def gram_per_cubic_meter(self):
        """Set value using gram per cubic meter units."""
        unit_const = units.MassDensityUnits.gram_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_m_3(self):
        """Set value using mathrm_g_mathrm_m_3 units (alias for gram_per_cubic_meter)."""
        return self.gram_per_cubic_meter
    
    @property
    def gram_per_liter(self):
        """Set value using gram per liter units."""
        unit_const = units.MassDensityUnits.gram_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_l_or_g_L(self):
        """Set value using mathrm_g_mathrm_l_or_g_L units (alias for gram_per_liter)."""
        return self.gram_per_liter
    
    @property
    def g_l(self):
        """Set value using g_l units (alias for gram_per_liter)."""
        return self.gram_per_liter
    
    @property
    def g_L(self):
        """Set value using g_L units (alias for gram_per_liter)."""
        return self.gram_per_liter
    
    @property
    def kilogram_per_cubic_meter(self):
        """Set value using kilogram per cubic meter units."""
        unit_const = units.MassDensityUnits.kilogram_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_3(self):
        """Set value using mathrm_kg_mathrm_m_3 units (alias for kilogram_per_cubic_meter)."""
        return self.kilogram_per_cubic_meter
    
    @property
    def ounce_avdp(self):
        """Set value using ounce (avdp) per US gallon units."""
        unit_const = units.MassDensityUnits.ounce_avdp
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def oz_gal(self):
        """Set value using oz_gal units (alias for ounce_avdp)."""
        return self.ounce_avdp
    
    @property
    def pound_avdp(self):
        """Set value using pound (avdp) per cubic foot units."""
        unit_const = units.MassDensityUnits.pound_avdp
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_cu_mathrm_ft_or_lb_ft_3(self):
        """Set value using mathrm_lb_mathrm_cu_mathrm_ft_or_lb_ft_3 units (alias for pound_avdp)."""
        return self.pound_avdp
    
    @property
    def lb_cu_ft(self):
        """Set value using lb_cu_ft units (alias for pound_avdp)."""
        return self.pound_avdp
    
    @property
    def lb_ft_3(self):
        """Set value using lb_ft_3 units (alias for pound_avdp)."""
        return self.pound_avdp
    
    @property
    def pound_mass(self):
        """Set value using pound (mass) per cubic inch units."""
        unit_const = units.MassDensityUnits.pound_mass
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_cu_in_or_mathrm_lb_mathrm_in_3(self):
        """Set value using mathrm_lb_mathrm_cu_in_or_mathrm_lb_mathrm_in_3 units (alias for pound_mass)."""
        return self.pound_mass
    
    @property
    def lb_cu_in(self):
        """Set value using lb_cu_in units (alias for pound_mass)."""
        return self.pound_mass
    
    @property
    def lb_in_3(self):
        """Set value using lb_in_3 units (alias for pound_mass)."""
        return self.pound_mass
    
    @property
    def ton_metric(self):
        """Set value using ton (metric) per cubic meter units."""
        unit_const = units.MassDensityUnits.ton_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_t_mathrm_m_3_or_MT_mathrm_m_3(self):
        """Set value using mathrm_t_mathrm_m_3_or_MT_mathrm_m_3 units (alias for ton_metric)."""
        return self.ton_metric
    
    @property
    def t_m_3(self):
        """Set value using t_m_3 units (alias for ton_metric)."""
        return self.ton_metric
    
    @property
    def MT_m_3(self):
        """Set value using MT_m_3 units (alias for ton_metric)."""
        return self.ton_metric
    

class MassFlowRateSetter(TypeSafeSetter):
    """MassFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kilograms_per_day(self):
        """Set value using kilograms per day units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_d(self):
        """Set value using kg_d units (alias for kilograms_per_day)."""
        return self.kilograms_per_day
    
    @property
    def kilograms_per_hour(self):
        """Set value using kilograms per hour units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_h(self):
        """Set value using kg_h units (alias for kilograms_per_hour)."""
        return self.kilograms_per_hour
    
    @property
    def kilograms_per_minute(self):
        """Set value using kilograms per minute units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_min(self):
        """Set value using kg_min units (alias for kilograms_per_minute)."""
        return self.kilograms_per_minute
    
    @property
    def kilograms_per_second(self):
        """Set value using kilograms per second units."""
        unit_const = units.MassFlowRateUnits.kilograms_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_s(self):
        """Set value using kg_s units (alias for kilograms_per_second)."""
        return self.kilograms_per_second
    
    @property
    def metric_tons_per_day(self):
        """Set value using metric tons per day units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT_d_or_MTD(self):
        """Set value using MT_d_or_MTD units (alias for metric_tons_per_day)."""
        return self.metric_tons_per_day
    
    @property
    def MT_d(self):
        """Set value using MT_d units (alias for metric_tons_per_day)."""
        return self.metric_tons_per_day
    
    @property
    def MTD(self):
        """Set value using MTD units (alias for metric_tons_per_day)."""
        return self.metric_tons_per_day
    
    @property
    def metric_tons_per_hour(self):
        """Set value using metric tons per hour units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT_h_or_MTD(self):
        """Set value using MT_h_or_MTD units (alias for metric_tons_per_hour)."""
        return self.metric_tons_per_hour
    
    @property
    def MT_h(self):
        """Set value using MT_h units (alias for metric_tons_per_hour)."""
        return self.metric_tons_per_hour
    
    @property
    def metric_tons_per_minute(self):
        """Set value using metric tons per minute units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def metric_tons_per_second(self):
        """Set value using metric tons per second units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT_s(self):
        """Set value using MT_s units (alias for metric_tons_per_second)."""
        return self.metric_tons_per_second
    
    @property
    def metric_tons_per_year_365_d(self):
        """Set value using metric tons per year (365 d) units."""
        unit_const = units.MassFlowRateUnits.metric_tons_per_year_365_d
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MT_yr_or_MTY(self):
        """Set value using MT_yr_or_MTY units (alias for metric_tons_per_year_365_d)."""
        return self.metric_tons_per_year_365_d
    
    @property
    def MT_yr(self):
        """Set value using MT_yr units (alias for metric_tons_per_year_365_d)."""
        return self.metric_tons_per_year_365_d
    
    @property
    def MTY(self):
        """Set value using MTY units (alias for metric_tons_per_year_365_d)."""
        return self.metric_tons_per_year_365_d
    
    @property
    def pounds_per_day(self):
        """Set value using pounds per day units."""
        unit_const = units.MassFlowRateUnits.pounds_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_d_or_mathrm_lb_mathrm_da_or_PPD(self):
        """Set value using mathrm_lb_mathrm_d_or_mathrm_lb_mathrm_da_or_PPD units (alias for pounds_per_day)."""
        return self.pounds_per_day
    
    @property
    def lb_d(self):
        """Set value using lb_d units (alias for pounds_per_day)."""
        return self.pounds_per_day
    
    @property
    def lb_da(self):
        """Set value using lb_da units (alias for pounds_per_day)."""
        return self.pounds_per_day
    
    @property
    def PPD(self):
        """Set value using PPD units (alias for pounds_per_day)."""
        return self.pounds_per_day
    
    @property
    def pounds_per_hour(self):
        """Set value using pounds per hour units."""
        unit_const = units.MassFlowRateUnits.pounds_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_h_or_lb_hr_or_PPH(self):
        """Set value using mathrm_lb_mathrm_h_or_lb_hr_or_PPH units (alias for pounds_per_hour)."""
        return self.pounds_per_hour
    
    @property
    def lb_h(self):
        """Set value using lb_h units (alias for pounds_per_hour)."""
        return self.pounds_per_hour
    
    @property
    def lb_hr(self):
        """Set value using lb_hr units (alias for pounds_per_hour)."""
        return self.pounds_per_hour
    
    @property
    def PPH(self):
        """Set value using PPH units (alias for pounds_per_hour)."""
        return self.pounds_per_hour
    
    @property
    def pounds_per_minute(self):
        """Set value using pounds per minute units."""
        unit_const = units.MassFlowRateUnits.pounds_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_min_or_PPM(self):
        """Set value using mathrm_lb_mathrm_min_or_PPM units (alias for pounds_per_minute)."""
        return self.pounds_per_minute
    
    @property
    def lb_min(self):
        """Set value using lb_min units (alias for pounds_per_minute)."""
        return self.pounds_per_minute
    
    @property
    def PPM(self):
        """Set value using PPM units (alias for pounds_per_minute)."""
        return self.pounds_per_minute
    
    @property
    def pounds_per_second(self):
        """Set value using pounds per second units."""
        unit_const = units.MassFlowRateUnits.pounds_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_s_or_lb_sec_or_PPS(self):
        """Set value using mathrm_lb_mathrm_s_or_lb_sec_or_PPS units (alias for pounds_per_second)."""
        return self.pounds_per_second
    
    @property
    def lb_s(self):
        """Set value using lb_s units (alias for pounds_per_second)."""
        return self.pounds_per_second
    
    @property
    def lb_sec(self):
        """Set value using lb_sec units (alias for pounds_per_second)."""
        return self.pounds_per_second
    
    @property
    def PPS(self):
        """Set value using PPS units (alias for pounds_per_second)."""
        return self.pounds_per_second
    

class MassFluxSetter(TypeSafeSetter):
    """MassFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kilogram_per_square_meter_per_day(self):
        """Set value using kilogram per square meter per day units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_left_mathrm_m_2_mathrm_d_right(self):
        """Set value using mathrm_kg_left_mathrm_m_2_mathrm_d_right units (alias for kilogram_per_square_meter_per_day)."""
        return self.kilogram_per_square_meter_per_day
    
    @property
    def kilogram_per_square_meter_per_hour(self):
        """Set value using kilogram per square meter per hour units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_left_mathrm_m_2_mathrm_h_right(self):
        """Set value using mathrm_kg_left_mathrm_m_2_mathrm_h_right units (alias for kilogram_per_square_meter_per_hour)."""
        return self.kilogram_per_square_meter_per_hour
    
    @property
    def kilogram_per_square_meter_per_minute(self):
        """Set value using kilogram per square meter per minute units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_left_mathrm_m_2_mathrm_min_right(self):
        """Set value using mathrm_kg_left_mathrm_m_2_mathrm_min_right units (alias for kilogram_per_square_meter_per_minute)."""
        return self.kilogram_per_square_meter_per_minute
    
    @property
    def kilogram_per_square_meter_per_second(self):
        """Set value using kilogram per square meter per second units."""
        unit_const = units.MassFluxUnits.kilogram_per_square_meter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_left_mathrm_m_2_mathrm_s_right(self):
        """Set value using mathrm_kg_left_mathrm_m_2_mathrm_s_right units (alias for kilogram_per_square_meter_per_second)."""
        return self.kilogram_per_square_meter_per_second
    
    @property
    def pound_per_square_foot_per_day(self):
        """Set value using pound per square foot per day units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_left_mathrm_ft_2_mathrm_d_right_or_lb_sqft_da(self):
        """Set value using mathrm_lb_left_mathrm_ft_2_mathrm_d_right_or_lb_sqft_da units (alias for pound_per_square_foot_per_day)."""
        return self.pound_per_square_foot_per_day
    
    @property
    def lb_left_ft_2_dright(self):
        """Set value using lb_left_ft_2_dright units (alias for pound_per_square_foot_per_day)."""
        return self.pound_per_square_foot_per_day
    
    @property
    def lb_sqft_da(self):
        """Set value using lb_sqft_da units (alias for pound_per_square_foot_per_day)."""
        return self.pound_per_square_foot_per_day
    
    @property
    def pound_per_square_foot_per_hour(self):
        """Set value using pound per square foot per hour units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_left_mathrm_ft_2_mathrm_h_right_or_lb_sqft_hr(self):
        """Set value using mathrm_lb_left_mathrm_ft_2_mathrm_h_right_or_lb_sqft_hr units (alias for pound_per_square_foot_per_hour)."""
        return self.pound_per_square_foot_per_hour
    
    @property
    def lb_left_ft_2_hright(self):
        """Set value using lb_left_ft_2_hright units (alias for pound_per_square_foot_per_hour)."""
        return self.pound_per_square_foot_per_hour
    
    @property
    def lb_sqft_hr(self):
        """Set value using lb_sqft_hr units (alias for pound_per_square_foot_per_hour)."""
        return self.pound_per_square_foot_per_hour
    
    @property
    def pound_per_square_foot_per_minute(self):
        """Set value using pound per square foot per minute units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_left_mathrm_ft_2_min_right_or_lb_sqft_min(self):
        """Set value using mathrm_lb_left_mathrm_ft_2_min_right_or_lb_sqft_min units (alias for pound_per_square_foot_per_minute)."""
        return self.pound_per_square_foot_per_minute
    
    @property
    def lb_left_ft_2_min_right(self):
        """Set value using lb_left_ft_2_min_right units (alias for pound_per_square_foot_per_minute)."""
        return self.pound_per_square_foot_per_minute
    
    @property
    def lb_sqft_min(self):
        """Set value using lb_sqft_min units (alias for pound_per_square_foot_per_minute)."""
        return self.pound_per_square_foot_per_minute
    
    @property
    def pound_per_square_foot_per_second(self):
        """Set value using pound per square foot per second units."""
        unit_const = units.MassFluxUnits.pound_per_square_foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_left_mathrm_ft_2_mathrm_s_right_or_lb_sqft_sec(self):
        """Set value using mathrm_lb_left_mathrm_ft_2_mathrm_s_right_or_lb_sqft_sec units (alias for pound_per_square_foot_per_second)."""
        return self.pound_per_square_foot_per_second
    
    @property
    def lb_left_ft_2_sright(self):
        """Set value using lb_left_ft_2_sright units (alias for pound_per_square_foot_per_second)."""
        return self.pound_per_square_foot_per_second
    
    @property
    def lb_sqft_sec(self):
        """Set value using lb_sqft_sec units (alias for pound_per_square_foot_per_second)."""
        return self.pound_per_square_foot_per_second
    

class MassFractionOfISetter(TypeSafeSetter):
    """MassFractionOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def grains_of_i_per_pound_total(self):
        """Set value using grains of "i" per pound total units."""
        unit_const = units.MassFractionOfIUnits.grains_of_i_per_pound_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_gr_mathrm_i_mathrm_lb(self):
        """Set value using mathrm_gr_mathrm_i_mathrm_lb units (alias for grains_of_i_per_pound_total)."""
        return self.grains_of_i_per_pound_total
    
    @property
    def gram_of_i_per_kilogram_total(self):
        """Set value using gram of "i" per kilogram total units."""
        unit_const = units.MassFractionOfIUnits.gram_of_i_per_kilogram_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_i_mathrm_kg(self):
        """Set value using mathrm_g_mathrm_i_mathrm_kg units (alias for gram_of_i_per_kilogram_total)."""
        return self.gram_of_i_per_kilogram_total
    
    @property
    def kilogram_of_i_per_kilogram_total(self):
        """Set value using kilogram of "i" per kilogram total units."""
        unit_const = units.MassFractionOfIUnits.kilogram_of_i_per_kilogram_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_i_mathrm_kg(self):
        """Set value using mathrm_kg_mathrm_i_mathrm_kg units (alias for kilogram_of_i_per_kilogram_total)."""
        return self.kilogram_of_i_per_kilogram_total
    
    @property
    def pound_of_i_per_pound_total(self):
        """Set value using pound of "i" per pound total units."""
        unit_const = units.MassFractionOfIUnits.pound_of_i_per_pound_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_i_mathrm_lb(self):
        """Set value using mathrm_lb_mathrm_i_mathrm_lb units (alias for pound_of_i_per_pound_total)."""
        return self.pound_of_i_per_pound_total
    

class MassTransferCoefficientSetter(TypeSafeSetter):
    """MassTransferCoefficient-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_square_centimeter_per_second(self):
        """Set value using gram per square centimeter per second units."""
        unit_const = units.MassTransferCoefficientUnits.gram_per_square_centimeter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_cm_2_mathrm_s(self):
        """Set value using mathrm_g_mathrm_cm_2_mathrm_s units (alias for gram_per_square_centimeter_per_second)."""
        return self.gram_per_square_centimeter_per_second
    
    @property
    def kilogram_per_square_meter_per_second(self):
        """Set value using kilogram per square meter per second units."""
        unit_const = units.MassTransferCoefficientUnits.kilogram_per_square_meter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_2_mathrm_s(self):
        """Set value using mathrm_kg_mathrm_m_2_mathrm_s units (alias for kilogram_per_square_meter_per_second)."""
        return self.kilogram_per_square_meter_per_second
    
    @property
    def pounds_force_per_cubic_foot_per_hour(self):
        """Set value using pounds force per cubic foot per hour units."""
        unit_const = units.MassTransferCoefficientUnits.pounds_force_per_cubic_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_ft_3_mathrm_h_or_mathrm_lb_mathrm_f_mathrm_cft_mathrm_hr(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_ft_3_mathrm_h_or_mathrm_lb_mathrm_f_mathrm_cft_mathrm_hr units (alias for pounds_force_per_cubic_foot_per_hour)."""
        return self.pounds_force_per_cubic_foot_per_hour
    
    @property
    def lb_f_ft_3_h(self):
        """Set value using lb_f_ft_3_h units (alias for pounds_force_per_cubic_foot_per_hour)."""
        return self.pounds_force_per_cubic_foot_per_hour
    
    @property
    def lb_f_cft_hr(self):
        """Set value using lb_f_cft_hr units (alias for pounds_force_per_cubic_foot_per_hour)."""
        return self.pounds_force_per_cubic_foot_per_hour
    
    @property
    def pounds_mass_per_square_foot_per_hour(self):
        """Set value using pounds mass per square foot per hour units."""
        unit_const = units.MassTransferCoefficientUnits.pounds_mass_per_square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft_2_mathrm_hr_or_lb_sqft_hr(self):
        """Set value using lb_ft_2_mathrm_hr_or_lb_sqft_hr units (alias for pounds_mass_per_square_foot_per_hour)."""
        return self.pounds_mass_per_square_foot_per_hour
    
    @property
    def lb_ft_2_hr(self):
        """Set value using lb_ft_2_hr units (alias for pounds_mass_per_square_foot_per_hour)."""
        return self.pounds_mass_per_square_foot_per_hour
    
    @property
    def lb_sqft_hr(self):
        """Set value using lb_sqft_hr units (alias for pounds_mass_per_square_foot_per_hour)."""
        return self.pounds_mass_per_square_foot_per_hour
    
    @property
    def pounds_mass_per_square_foot_per_second(self):
        """Set value using pounds mass per square foot per second units."""
        unit_const = units.MassTransferCoefficientUnits.pounds_mass_per_square_foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_left_mathrm_ft_2_mathrm_s_right_or_lb_sqft_sec(self):
        """Set value using mathrm_lb_left_mathrm_ft_2_mathrm_s_right_or_lb_sqft_sec units (alias for pounds_mass_per_square_foot_per_second)."""
        return self.pounds_mass_per_square_foot_per_second
    
    @property
    def lb_left_ft_2_sright(self):
        """Set value using lb_left_ft_2_sright units (alias for pounds_mass_per_square_foot_per_second)."""
        return self.pounds_mass_per_square_foot_per_second
    
    @property
    def lb_sqft_sec(self):
        """Set value using lb_sqft_sec units (alias for pounds_mass_per_square_foot_per_second)."""
        return self.pounds_mass_per_square_foot_per_second
    

class MolalityOfSoluteISetter(TypeSafeSetter):
    """MolalityOfSoluteI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_moles_of_i_per_kilogram(self):
        """Set value using gram moles of "i" per kilogram units."""
        unit_const = units.MolalityOfSoluteIUnits.gram_moles_of_i_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mol_mathrm_i_mathrm_kg(self):
        """Set value using mathrm_mol_mathrm_i_mathrm_kg units (alias for gram_moles_of_i_per_kilogram)."""
        return self.gram_moles_of_i_per_kilogram
    
    @property
    def kilogram_mols_of_i_per_kilogram(self):
        """Set value using kilogram mols of "i" per kilogram units."""
        unit_const = units.MolalityOfSoluteIUnits.kilogram_mols_of_i_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_mathrm_i_mathrm_kg(self):
        """Set value using mathrm_kmol_mathrm_i_mathrm_kg units (alias for kilogram_mols_of_i_per_kilogram)."""
        return self.kilogram_mols_of_i_per_kilogram
    
    @property
    def kmols_of_i_per_kilogram(self):
        """Set value using kmols of "i" per kilogram units."""
        unit_const = units.MolalityOfSoluteIUnits.kmols_of_i_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mols_of_i_per_gram(self):
        """Set value using mols of "i" per gram units."""
        unit_const = units.MolalityOfSoluteIUnits.mols_of_i_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mol_mathrm_i_mathrm_g(self):
        """Set value using mathrm_mol_mathrm_i_mathrm_g units (alias for mols_of_i_per_gram)."""
        return self.mols_of_i_per_gram
    
    @property
    def pound_moles_of_i_per_pound_mass(self):
        """Set value using pound moles of "i" per pound mass units."""
        unit_const = units.MolalityOfSoluteIUnits.pound_moles_of_i_per_pound_mass
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mole_mathrm_i_mathrm_lb_mass(self):
        """Set value using mole_mathrm_i_mathrm_lb_mass units (alias for pound_moles_of_i_per_pound_mass)."""
        return self.pound_moles_of_i_per_pound_mass
    

class MolarConcentrationByMassSetter(TypeSafeSetter):
    """MolarConcentrationByMass-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_mole_or_mole_per_gram(self):
        """Set value using gram mole or mole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.gram_mole_or_mole_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol_g(self):
        """Set value using mol_g units (alias for gram_mole_or_mole_per_gram)."""
        return self.gram_mole_or_mole_per_gram
    
    @property
    def gram_mole_or_mole_per_kilogram(self):
        """Set value using gram mole or mole per kilogram units."""
        unit_const = units.MolarConcentrationByMassUnits.gram_mole_or_mole_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol_kg(self):
        """Set value using mol_kg units (alias for gram_mole_or_mole_per_kilogram)."""
        return self.gram_mole_or_mole_per_kilogram
    
    @property
    def kilogram_mole_or_kmol_per_kilogram(self):
        """Set value using kilogram mole or kmol per kilogram units."""
        unit_const = units.MolarConcentrationByMassUnits.kilogram_mole_or_kmol_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_kg(self):
        """Set value using kmol_kg units (alias for kilogram_mole_or_kmol_per_kilogram)."""
        return self.kilogram_mole_or_kmol_per_kilogram
    
    @property
    def micromole_per_gram(self):
        """Set value using micromole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.micromole_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_mol_mathrm_g(self):
        """Set value using mu_mathrm_mol_mathrm_g units (alias for micromole_per_gram)."""
        return self.micromole_per_gram
    
    @property
    def millimole_per_gram(self):
        """Set value using millimole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.millimole_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mmol_g(self):
        """Set value using mmol_g units (alias for millimole_per_gram)."""
        return self.millimole_per_gram
    
    @property
    def picomole_per_gram(self):
        """Set value using picomole per gram units."""
        unit_const = units.MolarConcentrationByMassUnits.picomole_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pmol_g(self):
        """Set value using pmol_g units (alias for picomole_per_gram)."""
        return self.picomole_per_gram
    
    @property
    def pound_mole_per_pound(self):
        """Set value using pound mole per pound units."""
        unit_const = units.MolarConcentrationByMassUnits.pound_mole_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_mol_mathrm_lb_or_mole_lb(self):
        """Set value using mathrm_lb_mathrm_mol_mathrm_lb_or_mole_lb units (alias for pound_mole_per_pound)."""
        return self.pound_mole_per_pound
    
    @property
    def lb_mol_lb(self):
        """Set value using lb_mol_lb units (alias for pound_mole_per_pound)."""
        return self.pound_mole_per_pound
    
    @property
    def mole_lb(self):
        """Set value using mole_lb units (alias for pound_mole_per_pound)."""
        return self.pound_mole_per_pound
    

class MolarFlowRateSetter(TypeSafeSetter):
    """MolarFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_mole_per_day(self):
        """Set value using gram mole per day units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol_d(self):
        """Set value using mol_d units (alias for gram_mole_per_day)."""
        return self.gram_mole_per_day
    
    @property
    def gram_mole_per_hour(self):
        """Set value using gram mole per hour units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol_h(self):
        """Set value using mol_h units (alias for gram_mole_per_hour)."""
        return self.gram_mole_per_hour
    
    @property
    def gram_mole_per_minute(self):
        """Set value using gram mole per minute units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol_min(self):
        """Set value using mol_min units (alias for gram_mole_per_minute)."""
        return self.gram_mole_per_minute
    
    @property
    def gram_mole_per_second(self):
        """Set value using gram mole per second units."""
        unit_const = units.MolarFlowRateUnits.gram_mole_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mol_s(self):
        """Set value using mol_s units (alias for gram_mole_per_second)."""
        return self.gram_mole_per_second
    
    @property
    def kilogram_mole_or_kmol_per_day(self):
        """Set value using kilogram mole or kmol per day units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_d(self):
        """Set value using kmol_d units (alias for kilogram_mole_or_kmol_per_day)."""
        return self.kilogram_mole_or_kmol_per_day
    
    @property
    def kilogram_mole_or_kmol_per_hour(self):
        """Set value using kilogram mole or kmol per hour units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_h(self):
        """Set value using kmol_h units (alias for kilogram_mole_or_kmol_per_hour)."""
        return self.kilogram_mole_or_kmol_per_hour
    
    @property
    def kilogram_mole_or_kmol_per_minute(self):
        """Set value using kilogram mole or kmol per minute units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_min(self):
        """Set value using kmol_min units (alias for kilogram_mole_or_kmol_per_minute)."""
        return self.kilogram_mole_or_kmol_per_minute
    
    @property
    def kilogram_mole_or_kmol_per_second(self):
        """Set value using kilogram mole or kmol per second units."""
        unit_const = units.MolarFlowRateUnits.kilogram_mole_or_kmol_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kmol_s(self):
        """Set value using kmol_s units (alias for kilogram_mole_or_kmol_per_second)."""
        return self.kilogram_mole_or_kmol_per_second
    
    @property
    def pound_mole_or_lb_mol_per_day(self):
        """Set value using pound mole or lb-mol per day units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_d_or_mole_da(self):
        """Set value using lb_mol_d_or_mole_da units (alias for pound_mole_or_lb_mol_per_day)."""
        return self.pound_mole_or_lb_mol_per_day
    
    @property
    def lb_mol_d(self):
        """Set value using lb_mol_d units (alias for pound_mole_or_lb_mol_per_day)."""
        return self.pound_mole_or_lb_mol_per_day
    
    @property
    def mole_da(self):
        """Set value using mole_da units (alias for pound_mole_or_lb_mol_per_day)."""
        return self.pound_mole_or_lb_mol_per_day
    
    @property
    def pound_mole_or_lb_mol_per_hour(self):
        """Set value using pound mole or lb-mol per hour units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_h_or_mole_hr(self):
        """Set value using lb_mol_h_or_mole_hr units (alias for pound_mole_or_lb_mol_per_hour)."""
        return self.pound_mole_or_lb_mol_per_hour
    
    @property
    def lb_mol_h(self):
        """Set value using lb_mol_h units (alias for pound_mole_or_lb_mol_per_hour)."""
        return self.pound_mole_or_lb_mol_per_hour
    
    @property
    def mole_hr(self):
        """Set value using mole_hr units (alias for pound_mole_or_lb_mol_per_hour)."""
        return self.pound_mole_or_lb_mol_per_hour
    
    @property
    def pound_mole_or_lb_mol_per_minute(self):
        """Set value using pound mole or lb-mol per minute units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mol_min_or_mole_min(self):
        """Set value using lb_mol_min_or_mole_min units (alias for pound_mole_or_lb_mol_per_minute)."""
        return self.pound_mole_or_lb_mol_per_minute
    
    @property
    def lb_mol_min(self):
        """Set value using lb_mol_min units (alias for pound_mole_or_lb_mol_per_minute)."""
        return self.pound_mole_or_lb_mol_per_minute
    
    @property
    def mole_min(self):
        """Set value using mole_min units (alias for pound_mole_or_lb_mol_per_minute)."""
        return self.pound_mole_or_lb_mol_per_minute
    
    @property
    def pound_mole_or_lb_mol_per_second(self):
        """Set value using pound mole or lb-mol per second units."""
        unit_const = units.MolarFlowRateUnits.pound_mole_or_lb_mol_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_mol_mathrm_s_or_mole_sec(self):
        """Set value using mathrm_lb_mathrm_mol_mathrm_s_or_mole_sec units (alias for pound_mole_or_lb_mol_per_second)."""
        return self.pound_mole_or_lb_mol_per_second
    
    @property
    def lb_mol_s(self):
        """Set value using lb_mol_s units (alias for pound_mole_or_lb_mol_per_second)."""
        return self.pound_mole_or_lb_mol_per_second
    
    @property
    def mole_sec(self):
        """Set value using mole_sec units (alias for pound_mole_or_lb_mol_per_second)."""
        return self.pound_mole_or_lb_mol_per_second
    

class MolarFluxSetter(TypeSafeSetter):
    """MolarFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def kmol_per_square_meter_per_day(self):
        """Set value using kmol per square meter per day units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_left_mathrm_m_2_mathrm_d_right(self):
        """Set value using mathrm_kmol_left_mathrm_m_2_mathrm_d_right units (alias for kmol_per_square_meter_per_day)."""
        return self.kmol_per_square_meter_per_day
    
    @property
    def kmol_per_square_meter_per_hour(self):
        """Set value using kmol per square meter per hour units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_left_mathrm_m_2_mathrm_h_right(self):
        """Set value using mathrm_kmol_left_mathrm_m_2_mathrm_h_right units (alias for kmol_per_square_meter_per_hour)."""
        return self.kmol_per_square_meter_per_hour
    
    @property
    def kmol_per_square_meter_per_minute(self):
        """Set value using kmol per square meter per minute units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_left_mathrm_m_2_right_amin(self):
        """Set value using mathrm_kmol_left_mathrm_m_2_right_amin units (alias for kmol_per_square_meter_per_minute)."""
        return self.kmol_per_square_meter_per_minute
    
    @property
    def kmol_per_square_meter_per_second(self):
        """Set value using kmol per square meter per second units."""
        unit_const = units.MolarFluxUnits.kmol_per_square_meter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_left_mathrm_m_2_mathrm_s_right(self):
        """Set value using mathrm_kmol_left_mathrm_m_2_mathrm_s_right units (alias for kmol_per_square_meter_per_second)."""
        return self.kmol_per_square_meter_per_second
    
    @property
    def pound_mole_per_square_foot_per_day(self):
        """Set value using pound mole per square foot per day units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_d_right_or_mole_sqft_da(self):
        """Set value using mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_d_right_or_mole_sqft_da units (alias for pound_mole_per_square_foot_per_day)."""
        return self.pound_mole_per_square_foot_per_day
    
    @property
    def lb_mol_left_ft_2_dright(self):
        """Set value using lb_mol_left_ft_2_dright units (alias for pound_mole_per_square_foot_per_day)."""
        return self.pound_mole_per_square_foot_per_day
    
    @property
    def mole_sqft_da(self):
        """Set value using mole_sqft_da units (alias for pound_mole_per_square_foot_per_day)."""
        return self.pound_mole_per_square_foot_per_day
    
    @property
    def pound_mole_per_square_foot_per_hour(self):
        """Set value using pound mole per square foot per hour units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_h_right_or_mole_sqft_hr(self):
        """Set value using mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_h_right_or_mole_sqft_hr units (alias for pound_mole_per_square_foot_per_hour)."""
        return self.pound_mole_per_square_foot_per_hour
    
    @property
    def lb_mol_left_ft_2_hright(self):
        """Set value using lb_mol_left_ft_2_hright units (alias for pound_mole_per_square_foot_per_hour)."""
        return self.pound_mole_per_square_foot_per_hour
    
    @property
    def mole_sqft_hr(self):
        """Set value using mole_sqft_hr units (alias for pound_mole_per_square_foot_per_hour)."""
        return self.pound_mole_per_square_foot_per_hour
    
    @property
    def pound_mole_per_square_foot_per_minute(self):
        """Set value using pound mole per square foot per minute units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_min_right_or_mole_sqft_min(self):
        """Set value using mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_min_right_or_mole_sqft_min units (alias for pound_mole_per_square_foot_per_minute)."""
        return self.pound_mole_per_square_foot_per_minute
    
    @property
    def lb_mol_left_ft_2_minright(self):
        """Set value using lb_mol_left_ft_2_minright units (alias for pound_mole_per_square_foot_per_minute)."""
        return self.pound_mole_per_square_foot_per_minute
    
    @property
    def mole_sqft_min(self):
        """Set value using mole_sqft_min units (alias for pound_mole_per_square_foot_per_minute)."""
        return self.pound_mole_per_square_foot_per_minute
    
    @property
    def pound_mole_per_square_foot_per_second(self):
        """Set value using pound mole per square foot per second units."""
        unit_const = units.MolarFluxUnits.pound_mole_per_square_foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_s_right_or_mole_sqft_sec(self):
        """Set value using mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_s_right_or_mole_sqft_sec units (alias for pound_mole_per_square_foot_per_second)."""
        return self.pound_mole_per_square_foot_per_second
    
    @property
    def lb_mol_left_ft_2_sright(self):
        """Set value using lb_mol_left_ft_2_sright units (alias for pound_mole_per_square_foot_per_second)."""
        return self.pound_mole_per_square_foot_per_second
    
    @property
    def mole_sqft_sec(self):
        """Set value using mole_sqft_sec units (alias for pound_mole_per_square_foot_per_second)."""
        return self.pound_mole_per_square_foot_per_second
    

class MolarHeatCapacitySetter(TypeSafeSetter):
    """MolarHeatCapacity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def btu_per_pound_mole_per_degree_fahrenheit_or_degree_rankine(self):
        """Set value using Btu per pound mole per degree Fahrenheit (or degree Rankine) units."""
        unit_const = units.MolarHeatCapacityUnits.btu_per_pound_mole_per_degree_fahrenheit_or_degree_rankine
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_lb_mol_circ_mathrm_F(self):
        """Set value using Btu_lb_mol_circ_mathrm_F units (alias for btu_per_pound_mole_per_degree_fahrenheit_or_degree_rankine)."""
        return self.btu_per_pound_mole_per_degree_fahrenheit_or_degree_rankine
    
    @property
    def calories_per_gram_mole_per_kelvin_or_degree_celsius(self):
        """Set value using calories per gram mole per kelvin (or degree Celsius) units."""
        unit_const = units.MolarHeatCapacityUnits.calories_per_gram_mole_per_kelvin_or_degree_celsius
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_mol_K(self):
        """Set value using cal_mol_K units (alias for calories_per_gram_mole_per_kelvin_or_degree_celsius)."""
        return self.calories_per_gram_mole_per_kelvin_or_degree_celsius
    
    @property
    def joule_per_gram_mole_per_kelvin_or_degree_celsius(self):
        """Set value using joule per gram mole per kelvin (or degree Celsius) units."""
        unit_const = units.MolarHeatCapacityUnits.joule_per_gram_mole_per_kelvin_or_degree_celsius
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_mol_K(self):
        """Set value using J_mol_K units (alias for joule_per_gram_mole_per_kelvin_or_degree_celsius)."""
        return self.joule_per_gram_mole_per_kelvin_or_degree_celsius
    

class MolarityOfISetter(TypeSafeSetter):
    """MolarityOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_moles_of_i_per_cubic_meter(self):
        """Set value using gram moles of "i" per cubic meter units."""
        unit_const = units.MolarityOfIUnits.gram_moles_of_i_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mol_mathrm_i_mathrm_m_3_or_mathrm_c_mathrm_i(self):
        """Set value using mathrm_mol_mathrm_i_mathrm_m_3_or_mathrm_c_mathrm_i units (alias for gram_moles_of_i_per_cubic_meter)."""
        return self.gram_moles_of_i_per_cubic_meter
    
    @property
    def mol_i_m_3(self):
        """Set value using mol_i_m_3 units (alias for gram_moles_of_i_per_cubic_meter)."""
        return self.gram_moles_of_i_per_cubic_meter
    
    @property
    def c_i(self):
        """Set value using c_i units (alias for gram_moles_of_i_per_cubic_meter)."""
        return self.gram_moles_of_i_per_cubic_meter
    
    @property
    def gram_moles_of_i_per_liter(self):
        """Set value using gram moles of "i" per liter units."""
        unit_const = units.MolarityOfIUnits.gram_moles_of_i_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mol_mathrm_i_mathrm_l(self):
        """Set value using mathrm_mol_mathrm_i_mathrm_l units (alias for gram_moles_of_i_per_liter)."""
        return self.gram_moles_of_i_per_liter
    
    @property
    def kilogram_moles_of_i_per_cubic_meter(self):
        """Set value using kilogram moles of "i" per cubic meter units."""
        unit_const = units.MolarityOfIUnits.kilogram_moles_of_i_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_mathrm_i_mathrm_m_3(self):
        """Set value using mathrm_kmol_mathrm_i_mathrm_m_3 units (alias for kilogram_moles_of_i_per_cubic_meter)."""
        return self.kilogram_moles_of_i_per_cubic_meter
    
    @property
    def kilogram_moles_of_i_per_liter(self):
        """Set value using kilogram moles of "i" per liter units."""
        unit_const = units.MolarityOfIUnits.kilogram_moles_of_i_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_mathrm_i_mathrm_l(self):
        """Set value using mathrm_kmol_mathrm_i_mathrm_l units (alias for kilogram_moles_of_i_per_liter)."""
        return self.kilogram_moles_of_i_per_liter
    
    @property
    def pound_moles_of_i_per_cubic_foot(self):
        """Set value using pound moles of "i" per cubic foot units."""
        unit_const = units.MolarityOfIUnits.pound_moles_of_i_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mathrm_mol_mathrm_i_mathrm_ft_3_or_mathrm_mole_mathrm_i_cft(self):
        """Set value using lb_mathrm_mol_mathrm_i_mathrm_ft_3_or_mathrm_mole_mathrm_i_cft units (alias for pound_moles_of_i_per_cubic_foot)."""
        return self.pound_moles_of_i_per_cubic_foot
    
    @property
    def lb_mol_i_ft_3(self):
        """Set value using lb_mol_i_ft_3 units (alias for pound_moles_of_i_per_cubic_foot)."""
        return self.pound_moles_of_i_per_cubic_foot
    
    @property
    def mole_i_cft(self):
        """Set value using mole_i_cft units (alias for pound_moles_of_i_per_cubic_foot)."""
        return self.pound_moles_of_i_per_cubic_foot
    
    @property
    def pound_moles_of_i_per_gallon_us(self):
        """Set value using pound moles of " $i$ " per gallon (US) units."""
        unit_const = units.MolarityOfIUnits.pound_moles_of_i_per_gallon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mathrm_mol_mathrm_i_mathrm_gal_or_mathrm_mole_mathrm_i_gal(self):
        """Set value using lb_mathrm_mol_mathrm_i_mathrm_gal_or_mathrm_mole_mathrm_i_gal units (alias for pound_moles_of_i_per_gallon_us)."""
        return self.pound_moles_of_i_per_gallon_us
    
    @property
    def lb_mol_i_gal(self):
        """Set value using lb_mol_i_gal units (alias for pound_moles_of_i_per_gallon_us)."""
        return self.pound_moles_of_i_per_gallon_us
    
    @property
    def mole_i_gal(self):
        """Set value using mole_i_gal units (alias for pound_moles_of_i_per_gallon_us)."""
        return self.pound_moles_of_i_per_gallon_us
    

class MoleFractionOfISetter(TypeSafeSetter):
    """MoleFractionOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_mole_of_i_per_gram_mole_total(self):
        """Set value using gram mole of "i" per gram mole total units."""
        unit_const = units.MoleFractionOfIUnits.gram_mole_of_i_per_gram_mole_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mol_mathrm_i_mathrm_mol(self):
        """Set value using mathrm_mol_mathrm_i_mathrm_mol units (alias for gram_mole_of_i_per_gram_mole_total)."""
        return self.gram_mole_of_i_per_gram_mole_total
    
    @property
    def kilogram_mole_of_i_per_kilogram_mole_total(self):
        """Set value using kilogram mole of "i" per kilogram mole total units."""
        unit_const = units.MoleFractionOfIUnits.kilogram_mole_of_i_per_kilogram_mole_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kmol_mathrm_i_mathrm_kmol(self):
        """Set value using mathrm_kmol_mathrm_i_mathrm_kmol units (alias for kilogram_mole_of_i_per_kilogram_mole_total)."""
        return self.kilogram_mole_of_i_per_kilogram_mole_total
    
    @property
    def kilomole_of_i_per_kilomole_total(self):
        """Set value using kilomole of "i" per kilomole total units."""
        unit_const = units.MoleFractionOfIUnits.kilomole_of_i_per_kilomole_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pound_mole_of_i_per_pound_mole_total(self):
        """Set value using pound mole of "i" per pound mole total units."""
        unit_const = units.MoleFractionOfIUnits.pound_mole_of_i_per_pound_mole_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_mathrm_mol_mathrm_i_mathrm_lb_mathrm_mol(self):
        """Set value using lb_mathrm_mol_mathrm_i_mathrm_lb_mathrm_mol units (alias for pound_mole_of_i_per_pound_mole_total)."""
        return self.pound_mole_of_i_per_pound_mole_total
    

class MomentOfInertiaSetter(TypeSafeSetter):
    """MomentOfInertia-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_force_centimeter_square_second(self):
        """Set value using gram force centimeter square second units."""
        unit_const = units.MomentOfInertiaUnits.gram_force_centimeter_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_f_mathrm_cm_mathrm_s_2(self):
        """Set value using mathrm_g_mathrm_f_mathrm_cm_mathrm_s_2 units (alias for gram_force_centimeter_square_second)."""
        return self.gram_force_centimeter_square_second
    
    @property
    def gram_square_centimeter(self):
        """Set value using gram square centimeter units."""
        unit_const = units.MomentOfInertiaUnits.gram_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_cm_2(self):
        """Set value using mathrm_g_mathrm_cm_2 units (alias for gram_square_centimeter)."""
        return self.gram_square_centimeter
    
    @property
    def kilogram_force_centimeter_square_second(self):
        """Set value using kilogram force centimeter square second units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_force_centimeter_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_cm_mathrm_s_2(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_cm_mathrm_s_2 units (alias for kilogram_force_centimeter_square_second)."""
        return self.kilogram_force_centimeter_square_second
    
    @property
    def kilogram_force_meter_square_second(self):
        """Set value using kilogram force meter square second units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_force_meter_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_m_mathrm_s_2(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_m_mathrm_s_2 units (alias for kilogram_force_meter_square_second)."""
        return self.kilogram_force_meter_square_second
    
    @property
    def kilogram_square_centimeter(self):
        """Set value using kilogram square centimeter units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_cm_2(self):
        """Set value using mathrm_kg_mathrm_cm_2 units (alias for kilogram_square_centimeter)."""
        return self.kilogram_square_centimeter
    
    @property
    def kilogram_square_meter(self):
        """Set value using kilogram square meter units."""
        unit_const = units.MomentOfInertiaUnits.kilogram_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_2(self):
        """Set value using mathrm_kg_mathrm_m_2 units (alias for kilogram_square_meter)."""
        return self.kilogram_square_meter
    
    @property
    def ounce_force_inch_square_second(self):
        """Set value using ounce force inch square second units."""
        unit_const = units.MomentOfInertiaUnits.ounce_force_inch_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_oz_mathrm_f_in_mathrm_s_2(self):
        """Set value using mathrm_oz_mathrm_f_in_mathrm_s_2 units (alias for ounce_force_inch_square_second)."""
        return self.ounce_force_inch_square_second
    
    @property
    def ounce_mass_square_inch(self):
        """Set value using ounce mass square inch units."""
        unit_const = units.MomentOfInertiaUnits.ounce_mass_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def oz_in_2(self):
        """Set value using oz_in_2 units (alias for ounce_mass_square_inch)."""
        return self.ounce_mass_square_inch
    
    @property
    def pound_mass_square_foot(self):
        """Set value using pound mass square foot units."""
        unit_const = units.MomentOfInertiaUnits.pound_mass_square_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_ft_2_or_lb_sq_ft(self):
        """Set value using lb_ft_2_or_lb_sq_ft units (alias for pound_mass_square_foot)."""
        return self.pound_mass_square_foot
    
    @property
    def lb_ft_2(self):
        """Set value using lb_ft_2 units (alias for pound_mass_square_foot)."""
        return self.pound_mass_square_foot
    
    @property
    def lb_sq_ft(self):
        """Set value using lb_sq_ft units (alias for pound_mass_square_foot)."""
        return self.pound_mass_square_foot
    
    @property
    def pound_mass_square_inch(self):
        """Set value using pound mass square inch units."""
        unit_const = units.MomentOfInertiaUnits.pound_mass_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_in_2(self):
        """Set value using mathrm_lb_mathrm_in_2 units (alias for pound_mass_square_inch)."""
        return self.pound_mass_square_inch
    

class MomentumFlowRateSetter(TypeSafeSetter):
    """MomentumFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_pounds_per_square_hour(self):
        """Set value using foot pounds per square hour units."""
        unit_const = units.MomentumFlowRateUnits.foot_pounds_per_square_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_h_2_or_mathrm_ft_mathrm_lb_mathrm_hr_2(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_h_2_or_mathrm_ft_mathrm_lb_mathrm_hr_2 units (alias for foot_pounds_per_square_hour)."""
        return self.foot_pounds_per_square_hour
    
    @property
    def ft_lb_h_2(self):
        """Set value using ft_lb_h_2 units (alias for foot_pounds_per_square_hour)."""
        return self.foot_pounds_per_square_hour
    
    @property
    def ft_lb_hr_2(self):
        """Set value using ft_lb_hr_2 units (alias for foot_pounds_per_square_hour)."""
        return self.foot_pounds_per_square_hour
    
    @property
    def foot_pounds_per_square_minute(self):
        """Set value using foot pounds per square minute units."""
        unit_const = units.MomentumFlowRateUnits.foot_pounds_per_square_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_min_2(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_min_2 units (alias for foot_pounds_per_square_minute)."""
        return self.foot_pounds_per_square_minute
    
    @property
    def foot_pounds_per_square_second(self):
        """Set value using foot pounds per square second units."""
        unit_const = units.MomentumFlowRateUnits.foot_pounds_per_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_s_2_or_ft_lb_sec_2(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_s_2_or_ft_lb_sec_2 units (alias for foot_pounds_per_square_second)."""
        return self.foot_pounds_per_square_second
    
    @property
    def ft_lb_s_2(self):
        """Set value using ft_lb_s_2 units (alias for foot_pounds_per_square_second)."""
        return self.foot_pounds_per_square_second
    
    @property
    def ft_lb_sec_2(self):
        """Set value using ft_lb_sec_2 units (alias for foot_pounds_per_square_second)."""
        return self.foot_pounds_per_square_second
    
    @property
    def gram_centimeters_per_square_second(self):
        """Set value using gram centimeters per square second units."""
        unit_const = units.MomentumFlowRateUnits.gram_centimeters_per_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_cm_mathrm_s_2(self):
        """Set value using mathrm_g_mathrm_cm_mathrm_s_2 units (alias for gram_centimeters_per_square_second)."""
        return self.gram_centimeters_per_square_second
    
    @property
    def kilogram_meters_per_square_second(self):
        """Set value using kilogram meters per square second units."""
        unit_const = units.MomentumFlowRateUnits.kilogram_meters_per_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_mathrm_s_2(self):
        """Set value using mathrm_kg_mathrm_m_mathrm_s_2 units (alias for kilogram_meters_per_square_second)."""
        return self.kilogram_meters_per_square_second
    

class MomentumFluxSetter(TypeSafeSetter):
    """MomentumFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_square_centimeter(self):
        """Set value using dyne per square centimeter units."""
        unit_const = units.MomentumFluxUnits.dyne_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_mathrm_cm_2(self):
        """Set value using dyn_mathrm_cm_2 units (alias for dyne_per_square_centimeter)."""
        return self.dyne_per_square_centimeter
    
    @property
    def gram_per_centimeter_per_square_second(self):
        """Set value using gram per centimeter per square second units."""
        unit_const = units.MomentumFluxUnits.gram_per_centimeter_per_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_cm_mathrm_s_2(self):
        """Set value using mathrm_g_mathrm_cm_mathrm_s_2 units (alias for gram_per_centimeter_per_square_second)."""
        return self.gram_per_centimeter_per_square_second
    
    @property
    def newton_per_square_meter(self):
        """Set value using newton per square meter units."""
        unit_const = units.MomentumFluxUnits.newton_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_N_mathrm_m_2(self):
        """Set value using mathrm_N_mathrm_m_2 units (alias for newton_per_square_meter)."""
        return self.newton_per_square_meter
    
    @property
    def pound_force_per_square_foot(self):
        """Set value using pound force per square foot units."""
        unit_const = units.MomentumFluxUnits.pound_force_per_square_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_sq_mathrm_ft(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_sq_mathrm_ft units (alias for pound_force_per_square_foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def pound_mass_per_foot_per_square_second(self):
        """Set value using pound mass per foot per square second units."""
        unit_const = units.MomentumFluxUnits.pound_mass_per_foot_per_square_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_m_mathrm_ft_mathrm_s_2_or_mathrm_lb_mathrm_ft_mathrm_sec_2(self):
        """Set value using mathrm_lb_mathrm_m_mathrm_ft_mathrm_s_2_or_mathrm_lb_mathrm_ft_mathrm_sec_2 units (alias for pound_mass_per_foot_per_square_second)."""
        return self.pound_mass_per_foot_per_square_second
    
    @property
    def lb_m_ft_s_2(self):
        """Set value using lb_m_ft_s_2 units (alias for pound_mass_per_foot_per_square_second)."""
        return self.pound_mass_per_foot_per_square_second
    
    @property
    def lb_ft_sec_2(self):
        """Set value using lb_ft_sec_2 units (alias for pound_mass_per_foot_per_square_second)."""
        return self.pound_mass_per_foot_per_square_second
    

class NormalityOfSolutionSetter(TypeSafeSetter):
    """NormalityOfSolution-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_equivalents_per_cubic_meter(self):
        """Set value using gram equivalents per cubic meter units."""
        unit_const = units.NormalityOfSolutionUnits.gram_equivalents_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_eq_mathrm_m_3(self):
        """Set value using mathrm_eq_mathrm_m_3 units (alias for gram_equivalents_per_cubic_meter)."""
        return self.gram_equivalents_per_cubic_meter
    
    @property
    def gram_equivalents_per_liter(self):
        """Set value using gram equivalents per liter units."""
        unit_const = units.NormalityOfSolutionUnits.gram_equivalents_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def eq_l(self):
        """Set value using eq_l units (alias for gram_equivalents_per_liter)."""
        return self.gram_equivalents_per_liter
    
    @property
    def pound_equivalents_per_cubic_foot(self):
        """Set value using pound equivalents per cubic foot units."""
        unit_const = units.NormalityOfSolutionUnits.pound_equivalents_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_eq_mathrm_ft_3_or_lb_eq_cft(self):
        """Set value using mathrm_lb_mathrm_eq_mathrm_ft_3_or_lb_eq_cft units (alias for pound_equivalents_per_cubic_foot)."""
        return self.pound_equivalents_per_cubic_foot
    
    @property
    def lb_eq_ft_3(self):
        """Set value using lb_eq_ft_3 units (alias for pound_equivalents_per_cubic_foot)."""
        return self.pound_equivalents_per_cubic_foot
    
    @property
    def lb_eq_cft(self):
        """Set value using lb_eq_cft units (alias for pound_equivalents_per_cubic_foot)."""
        return self.pound_equivalents_per_cubic_foot
    
    @property
    def pound_equivalents_per_gallon(self):
        """Set value using pound equivalents per gallon units."""
        unit_const = units.NormalityOfSolutionUnits.pound_equivalents_per_gallon
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_eq_gal_US(self):
        """Set value using lb_eq_gal_US units (alias for pound_equivalents_per_gallon)."""
        return self.pound_equivalents_per_gallon
    

class ParticleDensitySetter(TypeSafeSetter):
    """ParticleDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def particles_per_cubic_centimeter(self):
        """Set value using particles per cubic centimeter units."""
        unit_const = units.ParticleDensityUnits.particles_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_cm_3_or_part_cc(self):
        """Set value using part_cm_3_or_part_cc units (alias for particles_per_cubic_centimeter)."""
        return self.particles_per_cubic_centimeter
    
    @property
    def part_cm_3(self):
        """Set value using part_cm_3 units (alias for particles_per_cubic_centimeter)."""
        return self.particles_per_cubic_centimeter
    
    @property
    def part_cc(self):
        """Set value using part_cc units (alias for particles_per_cubic_centimeter)."""
        return self.particles_per_cubic_centimeter
    
    @property
    def particles_per_cubic_foot(self):
        """Set value using particles per cubic foot units."""
        unit_const = units.ParticleDensityUnits.particles_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_mathrm_ft_3_or_part_cft(self):
        """Set value using part_mathrm_ft_3_or_part_cft units (alias for particles_per_cubic_foot)."""
        return self.particles_per_cubic_foot
    
    @property
    def part_ft_3(self):
        """Set value using part_ft_3 units (alias for particles_per_cubic_foot)."""
        return self.particles_per_cubic_foot
    
    @property
    def part_cft(self):
        """Set value using part_cft units (alias for particles_per_cubic_foot)."""
        return self.particles_per_cubic_foot
    
    @property
    def particles_per_cubic_meter(self):
        """Set value using particles per cubic meter units."""
        unit_const = units.ParticleDensityUnits.particles_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_mathrm_m_3(self):
        """Set value using part_mathrm_m_3 units (alias for particles_per_cubic_meter)."""
        return self.particles_per_cubic_meter
    
    @property
    def particles_per_gallon_us(self):
        """Set value using particles per gallon (US) units."""
        unit_const = units.ParticleDensityUnits.particles_per_gallon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_gal(self):
        """Set value using part_gal units (alias for particles_per_gallon_us)."""
        return self.particles_per_gallon_us
    
    @property
    def particles_per_liter(self):
        """Set value using particles per liter units."""
        unit_const = units.ParticleDensityUnits.particles_per_liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_l(self):
        """Set value using part_l units (alias for particles_per_liter)."""
        return self.particles_per_liter
    
    @property
    def particles_per_milliliter(self):
        """Set value using particles per milliliter units."""
        unit_const = units.ParticleDensityUnits.particles_per_milliliter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def part_ml(self):
        """Set value using part_ml units (alias for particles_per_milliliter)."""
        return self.particles_per_milliliter
    

class PercentSetter(TypeSafeSetter):
    """Percent-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def percent(self):
        """Set value using percent units."""
        unit_const = units.PercentUnits.percent
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unnamed(self):
        """Set value using unnamed units (alias for percent)."""
        return self.percent
    
    @property
    def per_mille(self):
        """Set value using per mille units."""
        unit_const = units.PercentUnits.per_mille
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def basis_point(self):
        """Set value using basis point units."""
        unit_const = units.PercentUnits.basis_point
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def bp(self):
        """Set value using bp units (alias for basis_point)."""
        return self.basis_point
    
    @property
    def bps(self):
        """Set value using bps units (alias for basis_point)."""
        return self.basis_point
    

class PermeabilitySetter(TypeSafeSetter):
    """Permeability-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def darcy(self):
        """Set value using darcy units."""
        unit_const = units.PermeabilityUnits.darcy
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def square_feet(self):
        """Set value using square feet units."""
        unit_const = units.PermeabilityUnits.square_feet
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_or_sq_ft(self):
        """Set value using mathrm_ft_2_or_sq_ft units (alias for square_feet)."""
        return self.square_feet
    
    @property
    def ft_2(self):
        """Set value using ft_2 units (alias for square_feet)."""
        return self.square_feet
    
    @property
    def sq_ft(self):
        """Set value using sq_ft units (alias for square_feet)."""
        return self.square_feet
    
    @property
    def square_meters(self):
        """Set value using square meters units."""
        unit_const = units.PermeabilityUnits.square_meters
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2(self):
        """Set value using mathrm_m_2 units (alias for square_meters)."""
        return self.square_meters
    

class PhotonEmissionRateSetter(TypeSafeSetter):
    """PhotonEmissionRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def rayleigh(self):
        """Set value using rayleigh units."""
        unit_const = units.PhotonEmissionRateUnits.rayleigh
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def R(self):
        """Set value using R units (alias for rayleigh)."""
        return self.rayleigh
    
    @property
    def reciprocal_square_meter_second(self):
        """Set value using reciprocal square meter second units."""
        unit_const = units.PhotonEmissionRateUnits.reciprocal_square_meter_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class PowerPerUnitMassSetter(TypeSafeSetter):
    """PowerPerUnitMass-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_per_hour_per_pound_mass(self):
        """Set value using British thermal unit per hour per pound mass units."""
        unit_const = units.PowerPerUnitMassUnits.british_thermal_unit_per_hour_per_pound_mass
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_h_lb_or_Btu_lb_hr(self):
        """Set value using Btu_h_lb_or_Btu_lb_hr units (alias for british_thermal_unit_per_hour_per_pound_mass)."""
        return self.british_thermal_unit_per_hour_per_pound_mass
    
    @property
    def Btu_h_lb(self):
        """Set value using Btu_h_lb units (alias for british_thermal_unit_per_hour_per_pound_mass)."""
        return self.british_thermal_unit_per_hour_per_pound_mass
    
    @property
    def Btu_lb_hr(self):
        """Set value using Btu_lb_hr units (alias for british_thermal_unit_per_hour_per_pound_mass)."""
        return self.british_thermal_unit_per_hour_per_pound_mass
    
    @property
    def calorie_per_second_per_gram(self):
        """Set value using calorie per second per gram units."""
        unit_const = units.PowerPerUnitMassUnits.calorie_per_second_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_s_g_or_cal_g_sec(self):
        """Set value using cal_s_g_or_cal_g_sec units (alias for calorie_per_second_per_gram)."""
        return self.calorie_per_second_per_gram
    
    @property
    def cal_s_g(self):
        """Set value using cal_s_g units (alias for calorie_per_second_per_gram)."""
        return self.calorie_per_second_per_gram
    
    @property
    def cal_g_sec(self):
        """Set value using cal_g_sec units (alias for calorie_per_second_per_gram)."""
        return self.calorie_per_second_per_gram
    
    @property
    def kilocalorie_per_hour_per_kilogram(self):
        """Set value using kilocalorie per hour per kilogram units."""
        unit_const = units.PowerPerUnitMassUnits.kilocalorie_per_hour_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_h_kg_or_kcal_kg_hr(self):
        """Set value using kcal_h_kg_or_kcal_kg_hr units (alias for kilocalorie_per_hour_per_kilogram)."""
        return self.kilocalorie_per_hour_per_kilogram
    
    @property
    def kcal_h_kg(self):
        """Set value using kcal_h_kg units (alias for kilocalorie_per_hour_per_kilogram)."""
        return self.kilocalorie_per_hour_per_kilogram
    
    @property
    def kcal_kg_hr(self):
        """Set value using kcal_kg_hr units (alias for kilocalorie_per_hour_per_kilogram)."""
        return self.kilocalorie_per_hour_per_kilogram
    
    @property
    def watt_per_kilogram(self):
        """Set value using watt per kilogram units."""
        unit_const = units.PowerPerUnitMassUnits.watt_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def W_kg(self):
        """Set value using W_kg units (alias for watt_per_kilogram)."""
        return self.watt_per_kilogram
    

class PowerPerUnitVolumeSetter(TypeSafeSetter):
    """PowerPerUnitVolume-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_per_hour_per_cubic_foot(self):
        """Set value using British thermal unit per hour per cubic foot units."""
        unit_const = units.PowerPerUnitVolumeUnits.british_thermal_unit_per_hour_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Btu_mathrm_h_mathrm_ft_3_or_mathrm_Btu_mathrm_hr_cft(self):
        """Set value using mathrm_Btu_mathrm_h_mathrm_ft_3_or_mathrm_Btu_mathrm_hr_cft units (alias for british_thermal_unit_per_hour_per_cubic_foot)."""
        return self.british_thermal_unit_per_hour_per_cubic_foot
    
    @property
    def Btu_h_ft_3(self):
        """Set value using Btu_h_ft_3 units (alias for british_thermal_unit_per_hour_per_cubic_foot)."""
        return self.british_thermal_unit_per_hour_per_cubic_foot
    
    @property
    def Btu_hr_cft(self):
        """Set value using Btu_hr_cft units (alias for british_thermal_unit_per_hour_per_cubic_foot)."""
        return self.british_thermal_unit_per_hour_per_cubic_foot
    
    @property
    def calorie_per_second_per_cubic_centimeter(self):
        """Set value using calorie per second per cubic centimeter units."""
        unit_const = units.PowerPerUnitVolumeUnits.calorie_per_second_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cal_mathrm_s_mathrm_cm_3_or_mathrm_cal_mathrm_s_mathrm_cc(self):
        """Set value using mathrm_cal_mathrm_s_mathrm_cm_3_or_mathrm_cal_mathrm_s_mathrm_cc units (alias for calorie_per_second_per_cubic_centimeter)."""
        return self.calorie_per_second_per_cubic_centimeter
    
    @property
    def cal_s_cm_3(self):
        """Set value using cal_s_cm_3 units (alias for calorie_per_second_per_cubic_centimeter)."""
        return self.calorie_per_second_per_cubic_centimeter
    
    @property
    def cal_s_cc(self):
        """Set value using cal_s_cc units (alias for calorie_per_second_per_cubic_centimeter)."""
        return self.calorie_per_second_per_cubic_centimeter
    
    @property
    def chu_per_hour_per_cubic_foot(self):
        """Set value using Chu per hour per cubic foot units."""
        unit_const = units.PowerPerUnitVolumeUnits.chu_per_hour_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_h_ft3_or_Chu_hr_cft(self):
        """Set value using Chu_h_ft3_or_Chu_hr_cft units (alias for chu_per_hour_per_cubic_foot)."""
        return self.chu_per_hour_per_cubic_foot
    
    @property
    def Chu_h_ft3(self):
        """Set value using Chu_h_ft3 units (alias for chu_per_hour_per_cubic_foot)."""
        return self.chu_per_hour_per_cubic_foot
    
    @property
    def Chu_hr_cft(self):
        """Set value using Chu_hr_cft units (alias for chu_per_hour_per_cubic_foot)."""
        return self.chu_per_hour_per_cubic_foot
    
    @property
    def kilocalorie_per_hour_per_cubic_centimeter(self):
        """Set value using kilocalorie per hour per cubic centimeter units."""
        unit_const = units.PowerPerUnitVolumeUnits.kilocalorie_per_hour_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kcal_mathrm_h_mathrm_cm_3_or_mathrm_kcal_hr_cc(self):
        """Set value using mathrm_kcal_mathrm_h_mathrm_cm_3_or_mathrm_kcal_hr_cc units (alias for kilocalorie_per_hour_per_cubic_centimeter)."""
        return self.kilocalorie_per_hour_per_cubic_centimeter
    
    @property
    def kcal_h_cm_3(self):
        """Set value using kcal_h_cm_3 units (alias for kilocalorie_per_hour_per_cubic_centimeter)."""
        return self.kilocalorie_per_hour_per_cubic_centimeter
    
    @property
    def kcal_hr_cc(self):
        """Set value using kcal_hr_cc units (alias for kilocalorie_per_hour_per_cubic_centimeter)."""
        return self.kilocalorie_per_hour_per_cubic_centimeter
    
    @property
    def kilocalorie_per_hour_per_cubic_foot(self):
        """Set value using kilocalorie per hour per cubic foot units."""
        unit_const = units.PowerPerUnitVolumeUnits.kilocalorie_per_hour_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kcal_mathrm_h_mathrm_ft_3_or_mathrm_kcal_mathrm_hr_cft(self):
        """Set value using mathrm_kcal_mathrm_h_mathrm_ft_3_or_mathrm_kcal_mathrm_hr_cft units (alias for kilocalorie_per_hour_per_cubic_foot)."""
        return self.kilocalorie_per_hour_per_cubic_foot
    
    @property
    def kcal_h_ft_3(self):
        """Set value using kcal_h_ft_3 units (alias for kilocalorie_per_hour_per_cubic_foot)."""
        return self.kilocalorie_per_hour_per_cubic_foot
    
    @property
    def kcal_hr_cft(self):
        """Set value using kcal_hr_cft units (alias for kilocalorie_per_hour_per_cubic_foot)."""
        return self.kilocalorie_per_hour_per_cubic_foot
    
    @property
    def kilocalorie_per_second_per_cubic_centimeter(self):
        """Set value using kilocalorie per second per cubic centimeter units."""
        unit_const = units.PowerPerUnitVolumeUnits.kilocalorie_per_second_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_s_cm_3_or_kcal_s_cc(self):
        """Set value using kcal_s_cm_3_or_kcal_s_cc units (alias for kilocalorie_per_second_per_cubic_centimeter)."""
        return self.kilocalorie_per_second_per_cubic_centimeter
    
    @property
    def kcal_s_cm_3(self):
        """Set value using kcal_s_cm_3 units (alias for kilocalorie_per_second_per_cubic_centimeter)."""
        return self.kilocalorie_per_second_per_cubic_centimeter
    
    @property
    def kcal_s_cc(self):
        """Set value using kcal_s_cc units (alias for kilocalorie_per_second_per_cubic_centimeter)."""
        return self.kilocalorie_per_second_per_cubic_centimeter
    
    @property
    def watt_per_cubic_meter(self):
        """Set value using watt per cubic meter units."""
        unit_const = units.PowerPerUnitVolumeUnits.watt_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_W_mathrm_m_3(self):
        """Set value using mathrm_W_mathrm_m_3 units (alias for watt_per_cubic_meter)."""
        return self.watt_per_cubic_meter
    

class PowerThermalDutySetter(TypeSafeSetter):
    """PowerThermalDuty-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def abwatt_emu_of_power(self):
        """Set value using abwatt (emu of power) units."""
        unit_const = units.PowerThermalDutyUnits.abwatt_emu_of_power
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def emu(self):
        """Set value using emu units (alias for abwatt_emu_of_power)."""
        return self.abwatt_emu_of_power
    
    @property
    def boiler_horsepower(self):
        """Set value using boiler horsepower units."""
        unit_const = units.PowerThermalDutyUnits.boiler_horsepower
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def HP_boiler(self):
        """Set value using HP_boiler units (alias for boiler_horsepower)."""
        return self.boiler_horsepower
    
    @property
    def british_thermal_unit_mean(self):
        """Set value using British thermal unit (mean) per hour units."""
        unit_const = units.PowerThermalDutyUnits.british_thermal_unit_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_mean_hr_or_Btu_hr(self):
        """Set value using Btu_mean_hr_or_Btu_hr units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def Btu_mean_hr(self):
        """Set value using Btu_mean_hr units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def Btu_hr(self):
        """Set value using Btu_hr units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def british_thermal_unit_thermochemical(self):
        """Set value using British thermal unit (thermochemical) per hour units."""
        unit_const = units.PowerThermalDutyUnits.british_thermal_unit_thermochemical
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_therm_hr_or_Btu_hr(self):
        """Set value using Btu_therm_hr_or_Btu_hr units (alias for british_thermal_unit_thermochemical)."""
        return self.british_thermal_unit_thermochemical
    
    @property
    def Btu_therm_hr(self):
        """Set value using Btu_therm_hr units (alias for british_thermal_unit_thermochemical)."""
        return self.british_thermal_unit_thermochemical
    
    @property
    def calorie_mean(self):
        """Set value using calorie (mean) per hour units."""
        unit_const = units.PowerThermalDutyUnits.calorie_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_mean_hr(self):
        """Set value using cal_mean_hr units (alias for calorie_mean)."""
        return self.calorie_mean
    
    @property
    def calorie_thermochemical(self):
        """Set value using calorie (thermochemical) per hour units."""
        unit_const = units.PowerThermalDutyUnits.calorie_thermochemical
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_therm_hr(self):
        """Set value using cal_therm_hr units (alias for calorie_thermochemical)."""
        return self.calorie_thermochemical
    
    @property
    def donkey(self):
        """Set value using donkey units."""
        unit_const = units.PowerThermalDutyUnits.donkey
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def erg_per_second(self):
        """Set value using erg per second units."""
        unit_const = units.PowerThermalDutyUnits.erg_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def erg_s(self):
        """Set value using erg_s units (alias for erg_per_second)."""
        return self.erg_per_second
    
    @property
    def foot_pondal_per_second(self):
        """Set value using foot pondal per second units."""
        unit_const = units.PowerThermalDutyUnits.foot_pondal_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_pdl_s(self):
        """Set value using ft_pdl_s units (alias for foot_pondal_per_second)."""
        return self.foot_pondal_per_second
    
    @property
    def foot_pound_force_per_hour(self):
        """Set value using foot pound force per hour units."""
        unit_const = units.PowerThermalDutyUnits.foot_pound_force_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_f_mathrm_hr(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_f_mathrm_hr units (alias for foot_pound_force_per_hour)."""
        return self.foot_pound_force_per_hour
    
    @property
    def foot_pound_force_per_minute(self):
        """Set value using foot pound force per minute units."""
        unit_const = units.PowerThermalDutyUnits.foot_pound_force_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_f_min(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_f_min units (alias for foot_pound_force_per_minute)."""
        return self.foot_pound_force_per_minute
    
    @property
    def foot_pound_force_per_second(self):
        """Set value using foot pound force per second units."""
        unit_const = units.PowerThermalDutyUnits.foot_pound_force_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_f_mathrm_s(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_f_mathrm_s units (alias for foot_pound_force_per_second)."""
        return self.foot_pound_force_per_second
    
    @property
    def horsepower_550_mathrmft_mathrmlb_mathrmf_mathrms(self):
        """Set value using horsepower ( $550 \\mathrm{ft} \\mathrm{lb}_{\\mathrm{f}} / \\mathrm{s}$ ) units."""
        unit_const = units.PowerThermalDutyUnits.horsepower_550_mathrmft_mathrmlb_mathrmf_mathrms
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def HP(self):
        """Set value using HP units (alias for horsepower_550_mathrmft_mathrmlb_mathrmf_mathrms)."""
        return self.horsepower_550_mathrmft_mathrmlb_mathrmf_mathrms
    
    @property
    def horsepower_electric(self):
        """Set value using horsepower (electric) units."""
        unit_const = units.PowerThermalDutyUnits.horsepower_electric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def HP_elect(self):
        """Set value using HP_elect units (alias for horsepower_electric)."""
        return self.horsepower_electric
    
    @property
    def horsepower_uk(self):
        """Set value using horsepower (UK) units."""
        unit_const = units.PowerThermalDutyUnits.horsepower_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def HP_UK(self):
        """Set value using HP_UK units (alias for horsepower_uk)."""
        return self.horsepower_uk
    
    @property
    def kcal_per_hour(self):
        """Set value using kcal per hour units."""
        unit_const = units.PowerThermalDutyUnits.kcal_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kcal_hr(self):
        """Set value using kcal_hr units (alias for kcal_per_hour)."""
        return self.kcal_per_hour
    
    @property
    def kilogram_force_meter_per_second(self):
        """Set value using kilogram force meter per second units."""
        unit_const = units.PowerThermalDutyUnits.kilogram_force_meter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_m_mathrm_s(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_m_mathrm_s units (alias for kilogram_force_meter_per_second)."""
        return self.kilogram_force_meter_per_second
    
    @property
    def kilowatt(self):
        """Set value using kilowatt units."""
        unit_const = units.PowerThermalDutyUnits.kilowatt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kW(self):
        """Set value using kW units (alias for kilowatt)."""
        return self.kilowatt
    
    @property
    def megawatt(self):
        """Set value using megawatt units."""
        unit_const = units.PowerThermalDutyUnits.megawatt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MW(self):
        """Set value using MW units (alias for megawatt)."""
        return self.megawatt
    
    @property
    def metric_horsepower(self):
        """Set value using metric horsepower units."""
        unit_const = units.PowerThermalDutyUnits.metric_horsepower
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def HP_metric(self):
        """Set value using HP_metric units (alias for metric_horsepower)."""
        return self.metric_horsepower
    
    @property
    def million_british_thermal_units_per_hour_petroleum(self):
        """Set value using million British thermal units per hour (petroleum) units."""
        unit_const = units.PowerThermalDutyUnits.million_british_thermal_units_per_hour_petroleum
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MMBtu_hr(self):
        """Set value using MMBtu_hr units (alias for million_british_thermal_units_per_hour_petroleum)."""
        return self.million_british_thermal_units_per_hour_petroleum
    
    @property
    def million_kilocalorie_per_hour(self):
        """Set value using million kilocalorie per hour units."""
        unit_const = units.PowerThermalDutyUnits.million_kilocalorie_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MM_kcal_hr(self):
        """Set value using MM_kcal_hr units (alias for million_kilocalorie_per_hour)."""
        return self.million_kilocalorie_per_hour
    
    @property
    def prony(self):
        """Set value using prony units."""
        unit_const = units.PowerThermalDutyUnits.prony
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ton_of_refrigeration_us(self):
        """Set value using ton of refrigeration (US) units."""
        unit_const = units.PowerThermalDutyUnits.ton_of_refrigeration_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def CTR_US(self):
        """Set value using CTR_US units (alias for ton_of_refrigeration_us)."""
        return self.ton_of_refrigeration_us
    
    @property
    def ton_or_refrigeration_uk(self):
        """Set value using ton or refrigeration (UK) units."""
        unit_const = units.PowerThermalDutyUnits.ton_or_refrigeration_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def CTR_UK(self):
        """Set value using CTR_UK units (alias for ton_or_refrigeration_uk)."""
        return self.ton_or_refrigeration_uk
    
    @property
    def volt_ampere(self):
        """Set value using volt-ampere units."""
        unit_const = units.PowerThermalDutyUnits.volt_ampere
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def VA(self):
        """Set value using VA units (alias for volt_ampere)."""
        return self.volt_ampere
    
    @property
    def water_horsepower(self):
        """Set value using water horsepower units."""
        unit_const = units.PowerThermalDutyUnits.water_horsepower
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def HP_water(self):
        """Set value using HP_water units (alias for water_horsepower)."""
        return self.water_horsepower
    
    @property
    def watt(self):
        """Set value using watt units."""
        unit_const = units.PowerThermalDutyUnits.watt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def W(self):
        """Set value using W units (alias for watt)."""
        return self.watt
    
    @property
    def watt_international_mean(self):
        """Set value using watt (international, mean) units."""
        unit_const = units.PowerThermalDutyUnits.watt_international_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def W_int_mean(self):
        """Set value using W_int_mean units (alias for watt_international_mean)."""
        return self.watt_international_mean
    
    @property
    def watt_international_us(self):
        """Set value using watt (international, US) units."""
        unit_const = units.PowerThermalDutyUnits.watt_international_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def watt_int_US(self):
        """Set value using watt_int_US units (alias for watt_international_us)."""
        return self.watt_international_us
    
    @property
    def gigawatt(self):
        """Set value using gigawatt units."""
        unit_const = units.PowerThermalDutyUnits.gigawatt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def GW(self):
        """Set value using GW units (alias for gigawatt)."""
        return self.gigawatt
    
    @property
    def milliwatt(self):
        """Set value using milliwatt units."""
        unit_const = units.PowerThermalDutyUnits.milliwatt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mW(self):
        """Set value using mW units (alias for milliwatt)."""
        return self.milliwatt
    
    @property
    def microwatt(self):
        """Set value using microwatt units."""
        unit_const = units.PowerThermalDutyUnits.microwatt
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class PressureSetter(TypeSafeSetter):
    """Pressure-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def atmosphere_standard(self):
        """Set value using atmosphere, standard units."""
        unit_const = units.PressureUnits.atmosphere_standard
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def atm(self):
        """Set value using atm units (alias for atmosphere_standard)."""
        return self.atmosphere_standard
    
    @property
    def bar(self):
        """Set value using bar units."""
        unit_const = units.PressureUnits.bar
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def barye(self):
        """Set value using barye units."""
        unit_const = units.PressureUnits.barye
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyne_per_square_centimeter(self):
        """Set value using dyne per square centimeter units."""
        unit_const = units.PressureUnits.dyne_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_mathrm_cm_2(self):
        """Set value using dyn_mathrm_cm_2 units (alias for dyne_per_square_centimeter)."""
        return self.dyne_per_square_centimeter
    
    @property
    def foot_of_mercury_60_circ_mathrmf(self):
        """Set value using foot of mercury ( $60{ }^{\\circ} \\mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.foot_of_mercury_60_circ_mathrmf
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_Hg_60_circ_mathrm_F(self):
        """Set value using ft_Hg_60_circ_mathrm_F units (alias for foot_of_mercury_60_circ_mathrmf)."""
        return self.foot_of_mercury_60_circ_mathrmf
    
    @property
    def foot_of_water_60_circ_mathrmf(self):
        """Set value using foot of water ( $60{ }^{\\circ} \\mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.foot_of_water_60_circ_mathrmf
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_mathrm_H_2_mathrm_O_left_60_circ_mathrm_F_right(self):
        """Set value using ft_mathrm_H_2_mathrm_O_left_60_circ_mathrm_F_right units (alias for foot_of_water_60_circ_mathrmf)."""
        return self.foot_of_water_60_circ_mathrmf
    
    @property
    def gigapascal(self):
        """Set value using gigapascal units."""
        unit_const = units.PressureUnits.gigapascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def GPa(self):
        """Set value using GPa units (alias for gigapascal)."""
        return self.gigapascal
    
    @property
    def hectopascal(self):
        """Set value using hectopascal units."""
        unit_const = units.PressureUnits.hectopascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def hPa(self):
        """Set value using hPa units (alias for hectopascal)."""
        return self.hectopascal
    
    @property
    def inch_of_mercury_60_circ_mathrmf(self):
        """Set value using inch of mercury ( $60{ }^{\\circ} \\mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.inch_of_mercury_60_circ_mathrmf
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_mathrm_Hg_left_60_circ_mathrm_F_right(self):
        """Set value using in_mathrm_Hg_left_60_circ_mathrm_F_right units (alias for inch_of_mercury_60_circ_mathrmf)."""
        return self.inch_of_mercury_60_circ_mathrmf
    
    @property
    def inch_of_water_60_circ_mathrmf(self):
        """Set value using inch of water ( $60{ }^{\\circ} \\mathrm{F}$ ) units."""
        unit_const = units.PressureUnits.inch_of_water_60_circ_mathrmf
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_mathrm_H_2_mathrm_O_left_60_circ_mathrm_F_right(self):
        """Set value using in_mathrm_H_2_mathrm_O_left_60_circ_mathrm_F_right units (alias for inch_of_water_60_circ_mathrmf)."""
        return self.inch_of_water_60_circ_mathrmf
    
    @property
    def kilogram_force_per_square_centimeter(self):
        """Set value using kilogram force per square centimeter units."""
        unit_const = units.PressureUnits.kilogram_force_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def at_or_mathrm_kg_mathrm_f_mathrm_cm_2(self):
        """Set value using at_or_mathrm_kg_mathrm_f_mathrm_cm_2 units (alias for kilogram_force_per_square_centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def at(self):
        """Set value using at units (alias for kilogram_force_per_square_centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kg_f_cm_2(self):
        """Set value using kg_f_cm_2 units (alias for kilogram_force_per_square_centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kilogram_force_per_square_meter(self):
        """Set value using kilogram force per square meter units."""
        unit_const = units.PressureUnits.kilogram_force_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_m_2(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_m_2 units (alias for kilogram_force_per_square_meter)."""
        return self.kilogram_force_per_square_meter
    
    @property
    def kip_force_per_square_inch(self):
        """Set value using kip force per square inch units."""
        unit_const = units.PressureUnits.kip_force_per_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def KSI_or_ksi_or_kip_f_mathrm_in_2(self):
        """Set value using KSI_or_ksi_or_kip_f_mathrm_in_2 units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def KSI(self):
        """Set value using KSI units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def ksi(self):
        """Set value using ksi units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def kip_f_in_2(self):
        """Set value using kip_f_in_2 units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def megapascal(self):
        """Set value using megapascal units."""
        unit_const = units.PressureUnits.megapascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MPa(self):
        """Set value using MPa units (alias for megapascal)."""
        return self.megapascal
    
    @property
    def meter_of_water_4circ_mathrmc(self):
        """Set value using meter of water ( $4^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.PressureUnits.meter_of_water_4circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_mathrm_H_2_mathrm_O_left_4_circ_mathrm_C_right(self):
        """Set value using mathrm_m_mathrm_H_2_mathrm_O_left_4_circ_mathrm_C_right units (alias for meter_of_water_4circ_mathrmc)."""
        return self.meter_of_water_4circ_mathrmc
    
    @property
    def microbar(self):
        """Set value using microbar units."""
        unit_const = units.PressureUnits.microbar
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_bar(self):
        """Set value using mu_mathrm_bar units (alias for microbar)."""
        return self.microbar
    
    @property
    def millibar(self):
        """Set value using millibar units."""
        unit_const = units.PressureUnits.millibar
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mbar(self):
        """Set value using mbar units (alias for millibar)."""
        return self.millibar
    
    @property
    def millimeter_of_mercury_4circ_mathrmc(self):
        """Set value using millimeter of mercury ( $4^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.PressureUnits.millimeter_of_mercury_4circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mm_mathrm_Hg_left_4_circ_mathrm_C_right(self):
        """Set value using mathrm_mm_mathrm_Hg_left_4_circ_mathrm_C_right units (alias for millimeter_of_mercury_4circ_mathrmc)."""
        return self.millimeter_of_mercury_4circ_mathrmc
    
    @property
    def millimeter_of_water_4circ_mathrmc(self):
        """Set value using millimeter of water ( $4^{\\circ} \\mathrm{C}$ ) units."""
        unit_const = units.PressureUnits.millimeter_of_water_4circ_mathrmc
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mm_mathrm_H_2_mathrm_O_left_4_circ_mathrm_C_right(self):
        """Set value using mathrm_mm_mathrm_H_2_mathrm_O_left_4_circ_mathrm_C_right units (alias for millimeter_of_water_4circ_mathrmc)."""
        return self.millimeter_of_water_4circ_mathrmc
    
    @property
    def newton_per_square_meter(self):
        """Set value using newton per square meter units."""
        unit_const = units.PressureUnits.newton_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_N_mathrm_m_2(self):
        """Set value using mathrm_N_mathrm_m_2 units (alias for newton_per_square_meter)."""
        return self.newton_per_square_meter
    
    @property
    def ounce_force_per_square_inch(self):
        """Set value using ounce force per square inch units."""
        unit_const = units.PressureUnits.ounce_force_per_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def OSI_or_osi_or_mathrm_oz_mathrm_f_mathrm_in_2(self):
        """Set value using OSI_or_osi_or_mathrm_oz_mathrm_f_mathrm_in_2 units (alias for ounce_force_per_square_inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def OSI(self):
        """Set value using OSI units (alias for ounce_force_per_square_inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def osi(self):
        """Set value using osi units (alias for ounce_force_per_square_inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def pascal(self):
        """Set value using pascal units."""
        unit_const = units.PressureUnits.pascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Pa(self):
        """Set value using Pa units (alias for pascal)."""
        return self.pascal
    
    @property
    def pi_ze(self):
        """Set value using pièze units."""
        unit_const = units.PressureUnits.pi_ze
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pz(self):
        """Set value using pz units (alias for pi_ze)."""
        return self.pi_ze
    
    @property
    def pound_force_per_square_foot(self):
        """Set value using pound force per square foot units."""
        unit_const = units.PressureUnits.pound_force_per_square_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def PSF_or_psf_or_mathrm_lb_mathrm_f_mathrm_ft_2(self):
        """Set value using PSF_or_psf_or_mathrm_lb_mathrm_f_mathrm_ft_2 units (alias for pound_force_per_square_foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def psf(self):
        """Set value using psf units (alias for pound_force_per_square_foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def pound_force_per_square_inch(self):
        """Set value using pound force per square inch units."""
        unit_const = units.PressureUnits.pound_force_per_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def psi(self):
        """Set value using psi units (alias for pound_force_per_square_inch)."""
        return self.pound_force_per_square_inch
    
    @property
    def torr(self):
        """Set value using torr units."""
        unit_const = units.PressureUnits.torr
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def torr_or_mm_Hg_0_circ_C(self):
        """Set value using torr_or_mm_Hg_0_circ_C units (alias for torr)."""
        return self.torr
    
    @property
    def mm_Hg_0_circ_C(self):
        """Set value using mm_Hg_0_circ_C units (alias for torr)."""
        return self.torr
    
    @property
    def kilopascal(self):
        """Set value using kilopascal units."""
        unit_const = units.PressureUnits.kilopascal
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sievert(self):
        """Set value using sievert units."""
        unit_const = units.RadiationDoseEquivalentUnits.sievert
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Sv(self):
        """Set value using Sv units (alias for sievert)."""
        return self.sievert
    
    @property
    def millisievert(self):
        """Set value using millisievert units."""
        unit_const = units.RadiationDoseEquivalentUnits.millisievert
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mSv(self):
        """Set value using mSv units (alias for millisievert)."""
        return self.millisievert
    
    @property
    def microsievert(self):
        """Set value using microsievert units."""
        unit_const = units.RadiationDoseEquivalentUnits.microsievert
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class RadiationExposureSetter(TypeSafeSetter):
    """RadiationExposure-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def coulomb_per_kilogram(self):
        """Set value using coulomb per kilogram units."""
        unit_const = units.RadiationExposureUnits.coulomb_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def C_kg(self):
        """Set value using C_kg units (alias for coulomb_per_kilogram)."""
        return self.coulomb_per_kilogram
    
    @property
    def d_unit(self):
        """Set value using D unit units."""
        unit_const = units.RadiationExposureUnits.d_unit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def D_unit(self):
        """Set value using D_unit units (alias for d_unit)."""
        return self.d_unit
    
    @property
    def pastille_dose_b_unit(self):
        """Set value using pastille dose (B unit) units."""
        unit_const = units.RadiationExposureUnits.pastille_dose_b_unit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def B_unit(self):
        """Set value using B_unit units (alias for pastille_dose_b_unit)."""
        return self.pastille_dose_b_unit
    
    @property
    def r_entgen(self):
        """Set value using röentgen units."""
        unit_const = units.RadiationExposureUnits.r_entgen
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def R(self):
        """Set value using R units (alias for r_entgen)."""
        return self.r_entgen
    

class RadioactivitySetter(TypeSafeSetter):
    """Radioactivity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def becquerel(self):
        """Set value using becquerel units."""
        unit_const = units.RadioactivityUnits.becquerel
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Bq(self):
        """Set value using Bq units (alias for becquerel)."""
        return self.becquerel
    
    @property
    def curie(self):
        """Set value using curie units."""
        unit_const = units.RadioactivityUnits.curie
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ci(self):
        """Set value using Ci units (alias for curie)."""
        return self.curie
    
    @property
    def mache_unit(self):
        """Set value using Mache unit units."""
        unit_const = units.RadioactivityUnits.mache_unit
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Mache(self):
        """Set value using Mache units (alias for mache_unit)."""
        return self.mache_unit
    
    @property
    def rutherford(self):
        """Set value using rutherford units."""
        unit_const = units.RadioactivityUnits.rutherford
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Rd(self):
        """Set value using Rd units (alias for rutherford)."""
        return self.rutherford
    
    @property
    def stat(self):
        """Set value using stat units."""
        unit_const = units.RadioactivityUnits.stat
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kilobecquerel(self):
        """Set value using kilobecquerel units."""
        unit_const = units.RadioactivityUnits.kilobecquerel
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kBq(self):
        """Set value using kBq units (alias for kilobecquerel)."""
        return self.kilobecquerel
    
    @property
    def megabecquerel(self):
        """Set value using megabecquerel units."""
        unit_const = units.RadioactivityUnits.megabecquerel
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MBq(self):
        """Set value using MBq units (alias for megabecquerel)."""
        return self.megabecquerel
    
    @property
    def gigabecquerel(self):
        """Set value using gigabecquerel units."""
        unit_const = units.RadioactivityUnits.gigabecquerel
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_4(self):
        """Set value using in_4 units (alias for inch_quadrupled)."""
        return self.inch_quadrupled
    
    @property
    def centimeter_quadrupled(self):
        """Set value using centimeter quadrupled units."""
        unit_const = units.SecondMomentOfAreaUnits.centimeter_quadrupled
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_4(self):
        """Set value using mathrm_cm_4 units (alias for centimeter_quadrupled)."""
        return self.centimeter_quadrupled
    
    @property
    def foot_quadrupled(self):
        """Set value using foot quadrupled units."""
        unit_const = units.SecondMomentOfAreaUnits.foot_quadrupled
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_4(self):
        """Set value using mathrm_ft_4 units (alias for foot_quadrupled)."""
        return self.foot_quadrupled
    
    @property
    def meter_quadrupled(self):
        """Set value using meter quadrupled units."""
        unit_const = units.SecondMomentOfAreaUnits.meter_quadrupled
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_4(self):
        """Set value using mathrm_m_4 units (alias for meter_quadrupled)."""
        return self.meter_quadrupled
    

class SecondRadiationConstantPlanckSetter(TypeSafeSetter):
    """SecondRadiationConstantPlanck-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def meter_kelvin(self):
        """Set value using meter kelvin units."""
        unit_const = units.SecondRadiationConstantPlanckUnits.meter_kelvin
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_K(self):
        """Set value using m_K units (alias for meter_kelvin)."""
        return self.meter_kelvin
    

class SpecificEnthalpySetter(TypeSafeSetter):
    """SpecificEnthalpy-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_mean(self):
        """Set value using British thermal unit (mean) per pound units."""
        unit_const = units.SpecificEnthalpyUnits.british_thermal_unit_mean
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_mean_lb(self):
        """Set value using Btu_mean_lb units (alias for british_thermal_unit_mean)."""
        return self.british_thermal_unit_mean
    
    @property
    def british_thermal_unit_per_pound(self):
        """Set value using British thermal unit per pound units."""
        unit_const = units.SpecificEnthalpyUnits.british_thermal_unit_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_lb(self):
        """Set value using Btu_lb units (alias for british_thermal_unit_per_pound)."""
        return self.british_thermal_unit_per_pound
    
    @property
    def calorie_per_gram(self):
        """Set value using calorie per gram units."""
        unit_const = units.SpecificEnthalpyUnits.calorie_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cal_mathrm_g(self):
        """Set value using mathrm_cal_mathrm_g units (alias for calorie_per_gram)."""
        return self.calorie_per_gram
    
    @property
    def chu_per_pound(self):
        """Set value using Chu per pound units."""
        unit_const = units.SpecificEnthalpyUnits.chu_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Chu_lb(self):
        """Set value using Chu_lb units (alias for chu_per_pound)."""
        return self.chu_per_pound
    
    @property
    def joule_per_kilogram(self):
        """Set value using joule per kilogram units."""
        unit_const = units.SpecificEnthalpyUnits.joule_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_kg(self):
        """Set value using J_kg units (alias for joule_per_kilogram)."""
        return self.joule_per_kilogram
    
    @property
    def kilojoule_per_kilogram(self):
        """Set value using kilojoule per kilogram units."""
        unit_const = units.SpecificEnthalpyUnits.kilojoule_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kJ_kg(self):
        """Set value using kJ_kg units (alias for kilojoule_per_kilogram)."""
        return self.kilojoule_per_kilogram
    

class SpecificGravitySetter(TypeSafeSetter):
    """SpecificGravity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dimensionless(self):
        """Set value using Dimensionless units."""
        unit_const = units.SpecificGravityUnits.dimensionless
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Dmls(self):
        """Set value using Dmls units (alias for dimensionless)."""
        return self.dimensionless
    

class SpecificHeatCapacityConstantPressureSetter(TypeSafeSetter):
    """SpecificHeatCapacityConstantPressure-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def btu_per_pound_per_degree_fahrenheit_or_degree_rankine(self):
        """Set value using Btu per pound per degree Fahrenheit (or degree Rankine) units."""
        unit_const = units.SpecificHeatCapacityConstantPressureUnits.btu_per_pound_per_degree_fahrenheit_or_degree_rankine
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_lb_circ_mathrm_F(self):
        """Set value using Btu_lb_circ_mathrm_F units (alias for btu_per_pound_per_degree_fahrenheit_or_degree_rankine)."""
        return self.btu_per_pound_per_degree_fahrenheit_or_degree_rankine
    
    @property
    def calories_per_gram_per_kelvin_or_degree_celsius(self):
        """Set value using calories per gram per kelvin (or degree Celsius) units."""
        unit_const = units.SpecificHeatCapacityConstantPressureUnits.calories_per_gram_per_kelvin_or_degree_celsius
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cal_g_K(self):
        """Set value using cal_g_K units (alias for calories_per_gram_per_kelvin_or_degree_celsius)."""
        return self.calories_per_gram_per_kelvin_or_degree_celsius
    
    @property
    def joules_per_kilogram_per_kelvin_or_degree_celsius(self):
        """Set value using joules per kilogram per kelvin (or degree Celsius) units."""
        unit_const = units.SpecificHeatCapacityConstantPressureUnits.joules_per_kilogram_per_kelvin_or_degree_celsius
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_kg_K(self):
        """Set value using J_kg_K units (alias for joules_per_kilogram_per_kelvin_or_degree_celsius)."""
        return self.joules_per_kilogram_per_kelvin_or_degree_celsius
    

class SpecificLengthSetter(TypeSafeSetter):
    """SpecificLength-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def centimeter_per_gram(self):
        """Set value using centimeter per gram units."""
        unit_const = units.SpecificLengthUnits.centimeter_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm_g(self):
        """Set value using cm_g units (alias for centimeter_per_gram)."""
        return self.centimeter_per_gram
    
    @property
    def cotton_count(self):
        """Set value using cotton count units."""
        unit_const = units.SpecificLengthUnits.cotton_count
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cc(self):
        """Set value using cc units (alias for cotton_count)."""
        return self.cotton_count
    
    @property
    def ft_per_pound(self):
        """Set value using ft per pound units."""
        unit_const = units.SpecificLengthUnits.ft_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_lb(self):
        """Set value using ft_lb units (alias for ft_per_pound)."""
        return self.ft_per_pound
    
    @property
    def meters_per_kilogram(self):
        """Set value using meters per kilogram units."""
        unit_const = units.SpecificLengthUnits.meters_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def m_kg(self):
        """Set value using m_kg units (alias for meters_per_kilogram)."""
        return self.meters_per_kilogram
    
    @property
    def newton_meter(self):
        """Set value using newton meter units."""
        unit_const = units.SpecificLengthUnits.newton_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Nm(self):
        """Set value using Nm units (alias for newton_meter)."""
        return self.newton_meter
    
    @property
    def worsted(self):
        """Set value using worsted units."""
        unit_const = units.SpecificLengthUnits.worsted
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class SpecificSurfaceSetter(TypeSafeSetter):
    """SpecificSurface-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_centimeter_per_gram(self):
        """Set value using square centimeter per gram units."""
        unit_const = units.SpecificSurfaceUnits.square_centimeter_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_2_mathrm_g(self):
        """Set value using mathrm_cm_2_mathrm_g units (alias for square_centimeter_per_gram)."""
        return self.square_centimeter_per_gram
    
    @property
    def square_foot_per_kilogram(self):
        """Set value using square foot per kilogram units."""
        unit_const = units.SpecificSurfaceUnits.square_foot_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_mathrm_kg_or_sq_ft_kg(self):
        """Set value using mathrm_ft_2_mathrm_kg_or_sq_ft_kg units (alias for square_foot_per_kilogram)."""
        return self.square_foot_per_kilogram
    
    @property
    def ft_2_kg(self):
        """Set value using ft_2_kg units (alias for square_foot_per_kilogram)."""
        return self.square_foot_per_kilogram
    
    @property
    def sq_ft_kg(self):
        """Set value using sq_ft_kg units (alias for square_foot_per_kilogram)."""
        return self.square_foot_per_kilogram
    
    @property
    def square_foot_per_pound(self):
        """Set value using square foot per pound units."""
        unit_const = units.SpecificSurfaceUnits.square_foot_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_mathrm_lb_or_sq_ft_lb(self):
        """Set value using mathrm_ft_2_mathrm_lb_or_sq_ft_lb units (alias for square_foot_per_pound)."""
        return self.square_foot_per_pound
    
    @property
    def ft_2_lb(self):
        """Set value using ft_2_lb units (alias for square_foot_per_pound)."""
        return self.square_foot_per_pound
    
    @property
    def sq_ft_lb(self):
        """Set value using sq_ft_lb units (alias for square_foot_per_pound)."""
        return self.square_foot_per_pound
    
    @property
    def square_meter_per_gram(self):
        """Set value using square meter per gram units."""
        unit_const = units.SpecificSurfaceUnits.square_meter_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2_mathrm_g(self):
        """Set value using mathrm_m_2_mathrm_g units (alias for square_meter_per_gram)."""
        return self.square_meter_per_gram
    
    @property
    def square_meter_per_kilogram(self):
        """Set value using square meter per kilogram units."""
        unit_const = units.SpecificSurfaceUnits.square_meter_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2_mathrm_kg(self):
        """Set value using mathrm_m_2_mathrm_kg units (alias for square_meter_per_kilogram)."""
        return self.square_meter_per_kilogram
    

class SpecificVolumeSetter(TypeSafeSetter):
    """SpecificVolume-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_centimeter_per_gram(self):
        """Set value using cubic centimeter per gram units."""
        unit_const = units.SpecificVolumeUnits.cubic_centimeter_per_gram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_3_mathrm_g_or_mathrm_cc_mathrm_g(self):
        """Set value using mathrm_cm_3_mathrm_g_or_mathrm_cc_mathrm_g units (alias for cubic_centimeter_per_gram)."""
        return self.cubic_centimeter_per_gram
    
    @property
    def cm_3_g(self):
        """Set value using cm_3_g units (alias for cubic_centimeter_per_gram)."""
        return self.cubic_centimeter_per_gram
    
    @property
    def cc_g(self):
        """Set value using cc_g units (alias for cubic_centimeter_per_gram)."""
        return self.cubic_centimeter_per_gram
    
    @property
    def cubic_foot_per_kilogram(self):
        """Set value using cubic foot per kilogram units."""
        unit_const = units.SpecificVolumeUnits.cubic_foot_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_mathrm_kg_or_mathrm_cft_mathrm_kg(self):
        """Set value using mathrm_ft_3_mathrm_kg_or_mathrm_cft_mathrm_kg units (alias for cubic_foot_per_kilogram)."""
        return self.cubic_foot_per_kilogram
    
    @property
    def ft_3_kg(self):
        """Set value using ft_3_kg units (alias for cubic_foot_per_kilogram)."""
        return self.cubic_foot_per_kilogram
    
    @property
    def cft_kg(self):
        """Set value using cft_kg units (alias for cubic_foot_per_kilogram)."""
        return self.cubic_foot_per_kilogram
    
    @property
    def cubic_foot_per_pound(self):
        """Set value using cubic foot per pound units."""
        unit_const = units.SpecificVolumeUnits.cubic_foot_per_pound
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_mathrm_lb_or_mathrm_cft_mathrm_lb(self):
        """Set value using mathrm_ft_3_mathrm_lb_or_mathrm_cft_mathrm_lb units (alias for cubic_foot_per_pound)."""
        return self.cubic_foot_per_pound
    
    @property
    def ft_3_lb(self):
        """Set value using ft_3_lb units (alias for cubic_foot_per_pound)."""
        return self.cubic_foot_per_pound
    
    @property
    def cft_lb(self):
        """Set value using cft_lb units (alias for cubic_foot_per_pound)."""
        return self.cubic_foot_per_pound
    
    @property
    def cubic_meter_per_kilogram(self):
        """Set value using cubic meter per kilogram units."""
        unit_const = units.SpecificVolumeUnits.cubic_meter_per_kilogram
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_mathrm_kg(self):
        """Set value using mathrm_m_3_mathrm_kg units (alias for cubic_meter_per_kilogram)."""
        return self.cubic_meter_per_kilogram
    

class StressSetter(TypeSafeSetter):
    """Stress-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_square_centimeter(self):
        """Set value using dyne per square centimeter units."""
        unit_const = units.StressUnits.dyne_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_mathrm_cm_2(self):
        """Set value using dyn_mathrm_cm_2 units (alias for dyne_per_square_centimeter)."""
        return self.dyne_per_square_centimeter
    
    @property
    def gigapascal(self):
        """Set value using gigapascal units."""
        unit_const = units.StressUnits.gigapascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def GPa(self):
        """Set value using GPa units (alias for gigapascal)."""
        return self.gigapascal
    
    @property
    def hectopascal(self):
        """Set value using hectopascal units."""
        unit_const = units.StressUnits.hectopascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def hPa(self):
        """Set value using hPa units (alias for hectopascal)."""
        return self.hectopascal
    
    @property
    def kilogram_force_per_square_centimeter(self):
        """Set value using kilogram force per square centimeter units."""
        unit_const = units.StressUnits.kilogram_force_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def at_or_mathrm_kg_mathrm_f_mathrm_cm_2(self):
        """Set value using at_or_mathrm_kg_mathrm_f_mathrm_cm_2 units (alias for kilogram_force_per_square_centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def at(self):
        """Set value using at units (alias for kilogram_force_per_square_centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kg_f_cm_2(self):
        """Set value using kg_f_cm_2 units (alias for kilogram_force_per_square_centimeter)."""
        return self.kilogram_force_per_square_centimeter
    
    @property
    def kilogram_force_per_square_meter(self):
        """Set value using kilogram force per square meter units."""
        unit_const = units.StressUnits.kilogram_force_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_f_mathrm_m_2(self):
        """Set value using mathrm_kg_mathrm_f_mathrm_m_2 units (alias for kilogram_force_per_square_meter)."""
        return self.kilogram_force_per_square_meter
    
    @property
    def kip_force_per_square_inch(self):
        """Set value using kip force per square inch units."""
        unit_const = units.StressUnits.kip_force_per_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def KSI_or_ksi_or_kip_f_mathrm_in_2(self):
        """Set value using KSI_or_ksi_or_kip_f_mathrm_in_2 units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def KSI(self):
        """Set value using KSI units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def ksi(self):
        """Set value using ksi units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def kip_f_in_2(self):
        """Set value using kip_f_in_2 units (alias for kip_force_per_square_inch)."""
        return self.kip_force_per_square_inch
    
    @property
    def megapascal(self):
        """Set value using megapascal units."""
        unit_const = units.StressUnits.megapascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def MPa(self):
        """Set value using MPa units (alias for megapascal)."""
        return self.megapascal
    
    @property
    def newton_per_square_meter(self):
        """Set value using newton per square meter units."""
        unit_const = units.StressUnits.newton_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_N_mathrm_m_2(self):
        """Set value using mathrm_N_mathrm_m_2 units (alias for newton_per_square_meter)."""
        return self.newton_per_square_meter
    
    @property
    def ounce_force_per_square_inch(self):
        """Set value using ounce force per square inch units."""
        unit_const = units.StressUnits.ounce_force_per_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def OSI_or_osi_or_mathrm_oz_mathrm_f_mathrm_in_2(self):
        """Set value using OSI_or_osi_or_mathrm_oz_mathrm_f_mathrm_in_2 units (alias for ounce_force_per_square_inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def OSI(self):
        """Set value using OSI units (alias for ounce_force_per_square_inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def osi(self):
        """Set value using osi units (alias for ounce_force_per_square_inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def oz_f_in_2(self):
        """Set value using oz_f_in_2 units (alias for ounce_force_per_square_inch)."""
        return self.ounce_force_per_square_inch
    
    @property
    def pascal(self):
        """Set value using pascal units."""
        unit_const = units.StressUnits.pascal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Pa(self):
        """Set value using Pa units (alias for pascal)."""
        return self.pascal
    
    @property
    def pound_force_per_square_foot(self):
        """Set value using pound force per square foot units."""
        unit_const = units.StressUnits.pound_force_per_square_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def PSF_or_psf_or_mathrm_lb_mathrm_f_mathrm_ft_2(self):
        """Set value using PSF_or_psf_or_mathrm_lb_mathrm_f_mathrm_ft_2 units (alias for pound_force_per_square_foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def PSF(self):
        """Set value using PSF units (alias for pound_force_per_square_foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def psf(self):
        """Set value using psf units (alias for pound_force_per_square_foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def lb_f_ft_2(self):
        """Set value using lb_f_ft_2 units (alias for pound_force_per_square_foot)."""
        return self.pound_force_per_square_foot
    
    @property
    def pound_force_per_square_inch(self):
        """Set value using pound force per square inch units."""
        unit_const = units.StressUnits.pound_force_per_square_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def psi(self):
        """Set value using psi units (alias for pound_force_per_square_inch)."""
        return self.pound_force_per_square_inch
    

class SurfaceMassDensitySetter(TypeSafeSetter):
    """SurfaceMassDensity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_square_centimeter(self):
        """Set value using gram per square centimeter units."""
        unit_const = units.SurfaceMassDensityUnits.gram_per_square_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_cm_2(self):
        """Set value using mathrm_kg_mathrm_cm_2 units (alias for gram_per_square_centimeter)."""
        return self.gram_per_square_centimeter
    
    @property
    def gram_per_square_meter(self):
        """Set value using gram per square meter units."""
        unit_const = units.SurfaceMassDensityUnits.gram_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_m_2(self):
        """Set value using mathrm_g_mathrm_m_2 units (alias for gram_per_square_meter)."""
        return self.gram_per_square_meter
    
    @property
    def kilogram_per_square_meter(self):
        """Set value using kilogram per square meter units."""
        unit_const = units.SurfaceMassDensityUnits.kilogram_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_2(self):
        """Set value using mathrm_kg_mathrm_m_2 units (alias for kilogram_per_square_meter)."""
        return self.kilogram_per_square_meter
    
    @property
    def pound_mass(self):
        """Set value using pound (mass) per square foot units."""
        unit_const = units.SurfaceMassDensityUnits.pound_mass
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_ft_2(self):
        """Set value using mathrm_lb_mathrm_ft_2 units (alias for pound_mass)."""
        return self.pound_mass
    

class SurfaceTensionSetter(TypeSafeSetter):
    """SurfaceTension-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def dyne_per_centimeter(self):
        """Set value using dyne per centimeter units."""
        unit_const = units.SurfaceTensionUnits.dyne_per_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_cm(self):
        """Set value using dyn_cm units (alias for dyne_per_centimeter)."""
        return self.dyne_per_centimeter
    
    @property
    def gram_force_per_centimeter(self):
        """Set value using gram force per centimeter units."""
        unit_const = units.SurfaceTensionUnits.gram_force_per_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_f_mathrm_cm(self):
        """Set value using mathrm_g_mathrm_f_mathrm_cm units (alias for gram_force_per_centimeter)."""
        return self.gram_force_per_centimeter
    
    @property
    def newton_per_meter(self):
        """Set value using newton per meter units."""
        unit_const = units.SurfaceTensionUnits.newton_per_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def N_m(self):
        """Set value using N_m units (alias for newton_per_meter)."""
        return self.newton_per_meter
    
    @property
    def pound_force_per_foot(self):
        """Set value using pound force per foot units."""
        unit_const = units.SurfaceTensionUnits.pound_force_per_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_ft(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_ft units (alias for pound_force_per_foot)."""
        return self.pound_force_per_foot
    
    @property
    def pound_force_per_inch(self):
        """Set value using pound force per inch units."""
        unit_const = units.SurfaceTensionUnits.pound_force_per_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_in(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_in units (alias for pound_force_per_inch)."""
        return self.pound_force_per_inch
    

class TemperatureSetter(TypeSafeSetter):
    """Temperature-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def degree_celsius_unit_size(self):
        """Set value using degree Celsius (unit size) units."""
        unit_const = units.TemperatureUnits.degree_celsius_unit_size
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_C_circ(self):
        """Set value using mathrm_C_circ units (alias for degree_celsius_unit_size)."""
        return self.degree_celsius_unit_size
    
    @property
    def degree_fahrenheit_unit_size(self):
        """Set value using degree Fahrenheit (unit size) units."""
        unit_const = units.TemperatureUnits.degree_fahrenheit_unit_size
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_F_circ(self):
        """Set value using mathrm_F_circ units (alias for degree_fahrenheit_unit_size)."""
        return self.degree_fahrenheit_unit_size
    
    @property
    def degree_r_aumur_unit_size(self):
        """Set value using degree Réaumur (unit size) units."""
        unit_const = units.TemperatureUnits.degree_r_aumur_unit_size
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def R_circ(self):
        """Set value using R_circ units (alias for degree_r_aumur_unit_size)."""
        return self.degree_r_aumur_unit_size
    
    @property
    def kelvin_absolute_scale(self):
        """Set value using kelvin (absolute scale) units."""
        unit_const = units.TemperatureUnits.kelvin_absolute_scale
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def K(self):
        """Set value using K units (alias for kelvin_absolute_scale)."""
        return self.kelvin_absolute_scale
    
    @property
    def rankine_absolute_scale(self):
        """Set value using Rankine (absolute scale) units."""
        unit_const = units.TemperatureUnits.rankine_absolute_scale
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def circ_mathrm_R(self):
        """Set value using circ_mathrm_R units (alias for rankine_absolute_scale)."""
        return self.rankine_absolute_scale
    

class ThermalConductivitySetter(TypeSafeSetter):
    """ThermalConductivity-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def btu_it(self):
        """Set value using Btu (IT) per inch per hour per degree Fahrenheit units."""
        unit_const = units.ThermalConductivityUnits.btu_it
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_IT_in_hr_circ_mathrm_F(self):
        """Set value using Btu_IT_in_hr_circ_mathrm_F units (alias for btu_it)."""
        return self.btu_it
    
    @property
    def btu_therm(self):
        """Set value using Btu (therm) per foot per hour per degree Fahrenheit units."""
        unit_const = units.ThermalConductivityUnits.btu_therm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Btu_left_mathrm_ft_mathrm_hr_circ_mathrm_F_right(self):
        """Set value using mathrm_Btu_left_mathrm_ft_mathrm_hr_circ_mathrm_F_right units (alias for btu_therm)."""
        return self.btu_therm
    
    @property
    def calorie_therm(self):
        """Set value using calorie (therm) per centimeter per second per degree Celsius units."""
        unit_const = units.ThermalConductivityUnits.calorie_therm
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def operatorname_cal_mathrm_IT_left_mathrm_cm_mathrm_s_circ_mathrm_C_right(self):
        """Set value using operatorname_cal_mathrm_IT_left_mathrm_cm_mathrm_s_circ_mathrm_C_right units (alias for calorie_therm)."""
        return self.calorie_therm
    
    @property
    def joule_per_second_per_centimeter_per_kelvin(self):
        """Set value using joule per second per centimeter per kelvin units."""
        unit_const = units.ThermalConductivityUnits.joule_per_second_per_centimeter_per_kelvin
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def J_cm_s_K(self):
        """Set value using J_cm_s_K units (alias for joule_per_second_per_centimeter_per_kelvin)."""
        return self.joule_per_second_per_centimeter_per_kelvin
    
    @property
    def watt_per_centimeter_per_kelvin(self):
        """Set value using watt per centimeter per kelvin units."""
        unit_const = units.ThermalConductivityUnits.watt_per_centimeter_per_kelvin
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def W_cm_K(self):
        """Set value using W_cm_K units (alias for watt_per_centimeter_per_kelvin)."""
        return self.watt_per_centimeter_per_kelvin
    
    @property
    def watt_per_meter_per_kelvin(self):
        """Set value using watt per meter per kelvin units."""
        unit_const = units.ThermalConductivityUnits.watt_per_meter_per_kelvin
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def W_m_K(self):
        """Set value using W_m_K units (alias for watt_per_meter_per_kelvin)."""
        return self.watt_per_meter_per_kelvin
    

class TimeSetter(TypeSafeSetter):
    """Time-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def blink(self):
        """Set value using blink units."""
        unit_const = units.TimeUnits.blink
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def century(self):
        """Set value using century units."""
        unit_const = units.TimeUnits.century
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unnamed(self):
        """Set value using unnamed units (alias for century)."""
        return self.century
    
    @property
    def chronon_or_tempon(self):
        """Set value using chronon or tempon units."""
        unit_const = units.TimeUnits.chronon_or_tempon
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gigan_or_eon(self):
        """Set value using gigan or eon units."""
        unit_const = units.TimeUnits.gigan_or_eon
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Ga_or_eon(self):
        """Set value using Ga_or_eon units (alias for gigan_or_eon)."""
        return self.gigan_or_eon
    
    @property
    def Ga(self):
        """Set value using Ga units (alias for gigan_or_eon)."""
        return self.gigan_or_eon
    
    @property
    def eon(self):
        """Set value using eon units (alias for gigan_or_eon)."""
        return self.gigan_or_eon
    
    @property
    def hour(self):
        """Set value using hour units."""
        unit_const = units.TimeUnits.hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def h_or_hr(self):
        """Set value using h_or_hr units (alias for hour)."""
        return self.hour
    
    @property
    def h(self):
        """Set value using h units (alias for hour)."""
        return self.hour
    
    @property
    def hr(self):
        """Set value using hr units (alias for hour)."""
        return self.hour
    
    @property
    def julian_year(self):
        """Set value using Julian year units."""
        unit_const = units.TimeUnits.julian_year
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def a_jul_or_yr(self):
        """Set value using a_jul_or_yr units (alias for julian_year)."""
        return self.julian_year
    
    @property
    def a_jul(self):
        """Set value using a_jul units (alias for julian_year)."""
        return self.julian_year
    
    @property
    def yr(self):
        """Set value using yr units (alias for julian_year)."""
        return self.julian_year
    
    @property
    def mean_solar_day(self):
        """Set value using mean solar day units."""
        unit_const = units.TimeUnits.mean_solar_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def da_or_d(self):
        """Set value using da_or_d units (alias for mean_solar_day)."""
        return self.mean_solar_day
    
    @property
    def da(self):
        """Set value using da units (alias for mean_solar_day)."""
        return self.mean_solar_day
    
    @property
    def d(self):
        """Set value using d units (alias for mean_solar_day)."""
        return self.mean_solar_day
    
    @property
    def millenium(self):
        """Set value using millenium units."""
        unit_const = units.TimeUnits.millenium
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def minute(self):
        """Set value using minute units."""
        unit_const = units.TimeUnits.minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def min(self):
        """Set value using min units (alias for minute)."""
        return self.minute
    
    @property
    def second(self):
        """Set value using second units."""
        unit_const = units.TimeUnits.second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def s(self):
        """Set value using s units (alias for second)."""
        return self.second
    
    @property
    def shake(self):
        """Set value using shake units."""
        unit_const = units.TimeUnits.shake
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def sidereal_year_1900_ad(self):
        """Set value using sidereal year (1900 AD) units."""
        unit_const = units.TimeUnits.sidereal_year_1900_ad
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def a_sider_or_yr(self):
        """Set value using a_sider_or_yr units (alias for sidereal_year_1900_ad)."""
        return self.sidereal_year_1900_ad
    
    @property
    def a_sider(self):
        """Set value using a_sider units (alias for sidereal_year_1900_ad)."""
        return self.sidereal_year_1900_ad
    
    @property
    def tropical_year(self):
        """Set value using tropical year units."""
        unit_const = units.TimeUnits.tropical_year
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def a_trop(self):
        """Set value using a_trop units (alias for tropical_year)."""
        return self.tropical_year
    
    @property
    def wink(self):
        """Set value using wink units."""
        unit_const = units.TimeUnits.wink
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def year(self):
        """Set value using year units."""
        unit_const = units.TimeUnits.year
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def a_or_y_or_yr(self):
        """Set value using a_or_y_or_yr units (alias for year)."""
        return self.year
    
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ms(self):
        """Set value using ms units (alias for millisecond)."""
        return self.millisecond
    
    @property
    def microsecond(self):
        """Set value using microsecond units."""
        unit_const = units.TimeUnits.microsecond
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def nanosecond(self):
        """Set value using nanosecond units."""
        unit_const = units.TimeUnits.nanosecond
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ns(self):
        """Set value using ns units (alias for nanosecond)."""
        return self.nanosecond
    
    @property
    def picosecond(self):
        """Set value using picosecond units."""
        unit_const = units.TimeUnits.picosecond
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cm_kg_mathrm_f(self):
        """Set value using cm_kg_mathrm_f units (alias for centimeter_kilogram_force)."""
        return self.centimeter_kilogram_force
    
    @property
    def dyne_centimeter(self):
        """Set value using dyne centimeter units."""
        unit_const = units.TorqueUnits.dyne_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_cm(self):
        """Set value using dyn_cm units (alias for dyne_centimeter)."""
        return self.dyne_centimeter
    
    @property
    def foot_kilogram_force(self):
        """Set value using foot kilogram force units."""
        unit_const = units.TorqueUnits.foot_kilogram_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_kg_mathrm_f(self):
        """Set value using mathrm_ft_mathrm_kg_mathrm_f units (alias for foot_kilogram_force)."""
        return self.foot_kilogram_force
    
    @property
    def foot_pound_force(self):
        """Set value using foot pound force units."""
        unit_const = units.TorqueUnits.foot_pound_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_lb_mathrm_f(self):
        """Set value using mathrm_ft_mathrm_lb_mathrm_f units (alias for foot_pound_force)."""
        return self.foot_pound_force
    
    @property
    def foot_poundal(self):
        """Set value using foot poundal units."""
        unit_const = units.TorqueUnits.foot_poundal
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_pdl(self):
        """Set value using ft_pdl units (alias for foot_poundal)."""
        return self.foot_poundal
    
    @property
    def in_pound_force(self):
        """Set value using in pound force units."""
        unit_const = units.TorqueUnits.in_pound_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_mathrm_lb_mathrm_f(self):
        """Set value using in_mathrm_lb_mathrm_f units (alias for in_pound_force)."""
        return self.in_pound_force
    
    @property
    def inch_ounce_force(self):
        """Set value using inch ounce force units."""
        unit_const = units.TorqueUnits.inch_ounce_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_mathrm_OZ_mathrm_f(self):
        """Set value using in_mathrm_OZ_mathrm_f units (alias for inch_ounce_force)."""
        return self.inch_ounce_force
    
    @property
    def meter_kilogram_force(self):
        """Set value using meter kilogram force units."""
        unit_const = units.TorqueUnits.meter_kilogram_force
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_mathrm_kg_mathrm_f(self):
        """Set value using mathrm_m_mathrm_kg_mathrm_f units (alias for meter_kilogram_force)."""
        return self.meter_kilogram_force
    
    @property
    def newton_centimeter(self):
        """Set value using newton centimeter units."""
        unit_const = units.TorqueUnits.newton_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def N_cm(self):
        """Set value using N_cm units (alias for newton_centimeter)."""
        return self.newton_centimeter
    
    @property
    def newton_meter(self):
        """Set value using newton meter units."""
        unit_const = units.TorqueUnits.newton_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def N_m(self):
        """Set value using N_m units (alias for newton_meter)."""
        return self.newton_meter
    

class TurbulenceEnergyDissipationRateSetter(TypeSafeSetter):
    """TurbulenceEnergyDissipationRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def square_foot_per_cubic_second(self):
        """Set value using square foot per cubic second units."""
        unit_const = units.TurbulenceEnergyDissipationRateUnits.square_foot_per_cubic_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_mathrm_s_3_or_sq_ft_sec_3(self):
        """Set value using mathrm_ft_2_mathrm_s_3_or_sq_ft_sec_3 units (alias for square_foot_per_cubic_second)."""
        return self.square_foot_per_cubic_second
    
    @property
    def ft_2_s_3(self):
        """Set value using ft_2_s_3 units (alias for square_foot_per_cubic_second)."""
        return self.square_foot_per_cubic_second
    
    @property
    def sq_ft_sec_3(self):
        """Set value using sq_ft_sec_3 units (alias for square_foot_per_cubic_second)."""
        return self.square_foot_per_cubic_second
    
    @property
    def square_meter_per_cubic_second(self):
        """Set value using square meter per cubic second units."""
        unit_const = units.TurbulenceEnergyDissipationRateUnits.square_meter_per_cubic_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2_mathrm_s_3(self):
        """Set value using mathrm_m_2_mathrm_s_3 units (alias for square_meter_per_cubic_second)."""
        return self.square_meter_per_cubic_second
    

class VelocityAngularSetter(TypeSafeSetter):
    """VelocityAngular-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def degree_per_minute(self):
        """Set value using degree per minute units."""
        unit_const = units.VelocityAngularUnits.degree_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def deg_min_or_circ_mathrm_min(self):
        """Set value using deg_min_or_circ_mathrm_min units (alias for degree_per_minute)."""
        return self.degree_per_minute
    
    @property
    def deg_min(self):
        """Set value using deg_min units (alias for degree_per_minute)."""
        return self.degree_per_minute
    
    @property
    def circ_min(self):
        """Set value using circ_min units (alias for degree_per_minute)."""
        return self.degree_per_minute
    
    @property
    def degree_per_second(self):
        """Set value using degree per second units."""
        unit_const = units.VelocityAngularUnits.degree_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def deg_s_or_circ_s(self):
        """Set value using deg_s_or_circ_s units (alias for degree_per_second)."""
        return self.degree_per_second
    
    @property
    def deg_s(self):
        """Set value using deg_s units (alias for degree_per_second)."""
        return self.degree_per_second
    
    @property
    def circ_s(self):
        """Set value using circ_s units (alias for degree_per_second)."""
        return self.degree_per_second
    
    @property
    def grade_per_minute(self):
        """Set value using grade per minute units."""
        unit_const = units.VelocityAngularUnits.grade_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gon_min_or_grad_min(self):
        """Set value using gon_min_or_grad_min units (alias for grade_per_minute)."""
        return self.grade_per_minute
    
    @property
    def gon_min(self):
        """Set value using gon_min units (alias for grade_per_minute)."""
        return self.grade_per_minute
    
    @property
    def grad_min(self):
        """Set value using grad_min units (alias for grade_per_minute)."""
        return self.grade_per_minute
    
    @property
    def radian_per_minute(self):
        """Set value using radian per minute units."""
        unit_const = units.VelocityAngularUnits.radian_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_rad_mathrm_min(self):
        """Set value using mathrm_rad_mathrm_min units (alias for radian_per_minute)."""
        return self.radian_per_minute
    
    @property
    def radian_per_second(self):
        """Set value using radian per second units."""
        unit_const = units.VelocityAngularUnits.radian_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_rad_mathrm_s(self):
        """Set value using mathrm_rad_mathrm_s units (alias for radian_per_second)."""
        return self.radian_per_second
    
    @property
    def revolution_per_minute(self):
        """Set value using revolution per minute units."""
        unit_const = units.VelocityAngularUnits.revolution_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def rev_m_or_rpm(self):
        """Set value using rev_m_or_rpm units (alias for revolution_per_minute)."""
        return self.revolution_per_minute
    
    @property
    def rev_m(self):
        """Set value using rev_m units (alias for revolution_per_minute)."""
        return self.revolution_per_minute
    
    @property
    def rpm(self):
        """Set value using rpm units (alias for revolution_per_minute)."""
        return self.revolution_per_minute
    
    @property
    def revolution_per_second(self):
        """Set value using revolution per second units."""
        unit_const = units.VelocityAngularUnits.revolution_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def rev_s_or_rps(self):
        """Set value using rev_s_or_rps units (alias for revolution_per_second)."""
        return self.revolution_per_second
    
    @property
    def rev_s(self):
        """Set value using rev_s units (alias for revolution_per_second)."""
        return self.revolution_per_second
    
    @property
    def rps(self):
        """Set value using rps units (alias for revolution_per_second)."""
        return self.revolution_per_second
    
    @property
    def turn_per_minute(self):
        """Set value using turn per minute units."""
        unit_const = units.VelocityAngularUnits.turn_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def tr_min(self):
        """Set value using tr_min units (alias for turn_per_minute)."""
        return self.turn_per_minute
    

class VelocityLinearSetter(TypeSafeSetter):
    """VelocityLinear-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def foot_per_hour(self):
        """Set value using foot per hour units."""
        unit_const = units.VelocityLinearUnits.foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_h_or_ft_hr_or_fph(self):
        """Set value using ft_h_or_ft_hr_or_fph units (alias for foot_per_hour)."""
        return self.foot_per_hour
    
    @property
    def ft_h(self):
        """Set value using ft_h units (alias for foot_per_hour)."""
        return self.foot_per_hour
    
    @property
    def ft_hr(self):
        """Set value using ft_hr units (alias for foot_per_hour)."""
        return self.foot_per_hour
    
    @property
    def fph(self):
        """Set value using fph units (alias for foot_per_hour)."""
        return self.foot_per_hour
    
    @property
    def foot_per_minute(self):
        """Set value using foot per minute units."""
        unit_const = units.VelocityLinearUnits.foot_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_min_or_fpm(self):
        """Set value using ft_min_or_fpm units (alias for foot_per_minute)."""
        return self.foot_per_minute
    
    @property
    def ft_min(self):
        """Set value using ft_min units (alias for foot_per_minute)."""
        return self.foot_per_minute
    
    @property
    def fpm(self):
        """Set value using fpm units (alias for foot_per_minute)."""
        return self.foot_per_minute
    
    @property
    def foot_per_second(self):
        """Set value using foot per second units."""
        unit_const = units.VelocityLinearUnits.foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ft_s_or_fps(self):
        """Set value using ft_s_or_fps units (alias for foot_per_second)."""
        return self.foot_per_second
    
    @property
    def ft_s(self):
        """Set value using ft_s units (alias for foot_per_second)."""
        return self.foot_per_second
    
    @property
    def fps(self):
        """Set value using fps units (alias for foot_per_second)."""
        return self.foot_per_second
    
    @property
    def inch_per_second(self):
        """Set value using inch per second units."""
        unit_const = units.VelocityLinearUnits.inch_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def in_s_or_ips(self):
        """Set value using in_s_or_ips units (alias for inch_per_second)."""
        return self.inch_per_second
    
    @property
    def in_s(self):
        """Set value using in_s units (alias for inch_per_second)."""
        return self.inch_per_second
    
    @property
    def ips(self):
        """Set value using ips units (alias for inch_per_second)."""
        return self.inch_per_second
    
    @property
    def international_knot(self):
        """Set value using international knot units."""
        unit_const = units.VelocityLinearUnits.international_knot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def knot(self):
        """Set value using knot units (alias for international_knot)."""
        return self.international_knot
    
    @property
    def kilometer_per_hour(self):
        """Set value using kilometer per hour units."""
        unit_const = units.VelocityLinearUnits.kilometer_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def km_h_ot_kph(self):
        """Set value using km_h_ot_kph units (alias for kilometer_per_hour)."""
        return self.kilometer_per_hour
    
    @property
    def kilometer_per_second(self):
        """Set value using kilometer per second units."""
        unit_const = units.VelocityLinearUnits.kilometer_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def km_s(self):
        """Set value using km_s units (alias for kilometer_per_second)."""
        return self.kilometer_per_second
    
    @property
    def meter_per_second(self):
        """Set value using meter per second units."""
        unit_const = units.VelocityLinearUnits.meter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_mathrm_s(self):
        """Set value using mathrm_m_mathrm_s units (alias for meter_per_second)."""
        return self.meter_per_second
    
    @property
    def mile_per_hour(self):
        """Set value using mile per hour units."""
        unit_const = units.VelocityLinearUnits.mile_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mi_mathrm_h_or_mathrm_mi_mathrm_hr_or_mph(self):
        """Set value using mathrm_mi_mathrm_h_or_mathrm_mi_mathrm_hr_or_mph units (alias for mile_per_hour)."""
        return self.mile_per_hour
    
    @property
    def mi_h(self):
        """Set value using mi_h units (alias for mile_per_hour)."""
        return self.mile_per_hour
    
    @property
    def mi_hr(self):
        """Set value using mi_hr units (alias for mile_per_hour)."""
        return self.mile_per_hour
    
    @property
    def mph(self):
        """Set value using mph units (alias for mile_per_hour)."""
        return self.mile_per_hour
    

class ViscosityDynamicSetter(TypeSafeSetter):
    """ViscosityDynamic-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def centipoise(self):
        """Set value using centipoise units."""
        unit_const = units.ViscosityDynamicUnits.centipoise
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cP_or_cPo(self):
        """Set value using cP_or_cPo units (alias for centipoise)."""
        return self.centipoise
    
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dyn_s_mathrm_cm_2(self):
        """Set value using dyn_s_mathrm_cm_2 units (alias for dyne_second_per_square_centimeter)."""
        return self.dyne_second_per_square_centimeter
    
    @property
    def kilopound_second_per_square_meter(self):
        """Set value using kilopound second per square meter units."""
        unit_const = units.ViscosityDynamicUnits.kilopound_second_per_square_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kip_mathrm_s_mathrm_m_2(self):
        """Set value using kip_mathrm_s_mathrm_m_2 units (alias for kilopound_second_per_square_meter)."""
        return self.kilopound_second_per_square_meter
    
    @property
    def millipoise(self):
        """Set value using millipoise units."""
        unit_const = units.ViscosityDynamicUnits.millipoise
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mP_or_mPo(self):
        """Set value using mP_or_mPo units (alias for millipoise)."""
        return self.millipoise
    
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_N_mathrm_s_mathrm_m_2(self):
        """Set value using mathrm_N_mathrm_s_mathrm_m_2 units (alias for newton_second_per_square_meter)."""
        return self.newton_second_per_square_meter
    
    @property
    def pascal_second(self):
        """Set value using pascal second units."""
        unit_const = units.ViscosityDynamicUnits.pascal_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Pa_s_or_PI(self):
        """Set value using Pa_s_or_PI units (alias for pascal_second)."""
        return self.pascal_second
    
    @property
    def Pa_s(self):
        """Set value using Pa_s units (alias for pascal_second)."""
        return self.pascal_second
    
    @property
    def PI(self):
        """Set value using PI units (alias for pascal_second)."""
        return self.pascal_second
    
    @property
    def poise(self):
        """Set value using poise units."""
        unit_const = units.ViscosityDynamicUnits.poise
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def P_or_Po(self):
        """Set value using P_or_Po units (alias for poise)."""
        return self.poise
    
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_h_mathrm_ft_2_or_mathrm_lb_mathrm_hr_mathrm_sq_ft(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_h_mathrm_ft_2_or_mathrm_lb_mathrm_hr_mathrm_sq_ft units (alias for pound_force_hour_per_square_foot)."""
        return self.pound_force_hour_per_square_foot
    
    @property
    def lb_f_h_ft_2(self):
        """Set value using lb_f_h_ft_2 units (alias for pound_force_hour_per_square_foot)."""
        return self.pound_force_hour_per_square_foot
    
    @property
    def lb_hr_sq_ft(self):
        """Set value using lb_hr_sq_ft units (alias for pound_force_hour_per_square_foot)."""
        return self.pound_force_hour_per_square_foot
    
    @property
    def pound_force_second_per_square_foot(self):
        """Set value using pound force second per square foot units."""
        unit_const = units.ViscosityDynamicUnits.pound_force_second_per_square_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_f_mathrm_s_mathrm_ft_2_or_mathrm_lb_mathrm_sec_mathrm_sq_ft(self):
        """Set value using mathrm_lb_mathrm_f_mathrm_s_mathrm_ft_2_or_mathrm_lb_mathrm_sec_mathrm_sq_ft units (alias for pound_force_second_per_square_foot)."""
        return self.pound_force_second_per_square_foot
    
    @property
    def lb_f_s_ft_2(self):
        """Set value using lb_f_s_ft_2 units (alias for pound_force_second_per_square_foot)."""
        return self.pound_force_second_per_square_foot
    
    @property
    def lb_sec_sq_ft(self):
        """Set value using lb_sec_sq_ft units (alias for pound_force_second_per_square_foot)."""
        return self.pound_force_second_per_square_foot
    

class ViscosityKinematicSetter(TypeSafeSetter):
    """ViscosityKinematic-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def centistokes(self):
        """Set value using centistokes units."""
        unit_const = units.ViscosityKinematicUnits.centistokes
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cSt(self):
        """Set value using cSt units (alias for centistokes)."""
        return self.centistokes
    
    @property
    def millistokes(self):
        """Set value using millistokes units."""
        unit_const = units.ViscosityKinematicUnits.millistokes
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mSt(self):
        """Set value using mSt units (alias for millistokes)."""
        return self.millistokes
    
    @property
    def square_centimeter_per_second(self):
        """Set value using square centimeter per second units."""
        unit_const = units.ViscosityKinematicUnits.square_centimeter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_2_mathrm_s(self):
        """Set value using mathrm_cm_2_mathrm_s units (alias for square_centimeter_per_second)."""
        return self.square_centimeter_per_second
    
    @property
    def square_foot_per_hour(self):
        """Set value using square foot per hour units."""
        unit_const = units.ViscosityKinematicUnits.square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_mathrm_h_or_mathrm_ft_2_mathrm_hr(self):
        """Set value using mathrm_ft_2_mathrm_h_or_mathrm_ft_2_mathrm_hr units (alias for square_foot_per_hour)."""
        return self.square_foot_per_hour
    
    @property
    def ft_2_h(self):
        """Set value using ft_2_h units (alias for square_foot_per_hour)."""
        return self.square_foot_per_hour
    
    @property
    def ft_2_hr(self):
        """Set value using ft_2_hr units (alias for square_foot_per_hour)."""
        return self.square_foot_per_hour
    
    @property
    def square_foot_per_second(self):
        """Set value using square foot per second units."""
        unit_const = units.ViscosityKinematicUnits.square_foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_2_mathrm_s(self):
        """Set value using mathrm_ft_2_mathrm_s units (alias for square_foot_per_second)."""
        return self.square_foot_per_second
    
    @property
    def square_meters_per_second(self):
        """Set value using square meters per second units."""
        unit_const = units.ViscosityKinematicUnits.square_meters_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_2_mathrm_s(self):
        """Set value using mathrm_m_2_mathrm_s units (alias for square_meters_per_second)."""
        return self.square_meters_per_second
    
    @property
    def stokes(self):
        """Set value using stokes units."""
        unit_const = units.ViscosityKinematicUnits.stokes
        self.variable.quantity = Quantity(self.value, unit_const)
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ac_ft(self):
        """Set value using ac_ft units (alias for acre_foot)."""
        return self.acre_foot
    
    @property
    def acre_inch(self):
        """Set value using acre inch units."""
        unit_const = units.VolumeUnits.acre_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ac_in(self):
        """Set value using ac_in units (alias for acre_inch)."""
        return self.acre_inch
    
    @property
    def barrel_us_liquid(self):
        """Set value using barrel (US Liquid) units."""
        unit_const = units.VolumeUnits.barrel_us_liquid
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def bbl_US_liq(self):
        """Set value using bbl_US_liq units (alias for barrel_us_liquid)."""
        return self.barrel_us_liquid
    
    @property
    def barrel_us_petro(self):
        """Set value using barrel (US, Petro) units."""
        unit_const = units.VolumeUnits.barrel_us_petro
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def bbl(self):
        """Set value using bbl units (alias for barrel_us_petro)."""
        return self.barrel_us_petro
    
    @property
    def board_foot_measure(self):
        """Set value using board foot measure units."""
        unit_const = units.VolumeUnits.board_foot_measure
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def BM_or_fbm(self):
        """Set value using BM_or_fbm units (alias for board_foot_measure)."""
        return self.board_foot_measure
    
    @property
    def BM(self):
        """Set value using BM units (alias for board_foot_measure)."""
        return self.board_foot_measure
    
    @property
    def fbm(self):
        """Set value using fbm units (alias for board_foot_measure)."""
        return self.board_foot_measure
    
    @property
    def bushel_us_dry(self):
        """Set value using bushel (US Dry) units."""
        unit_const = units.VolumeUnits.bushel_us_dry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def bu_US_dry(self):
        """Set value using bu_US_dry units (alias for bushel_us_dry)."""
        return self.bushel_us_dry
    
    @property
    def centiliter(self):
        """Set value using centiliter units."""
        unit_const = units.VolumeUnits.centiliter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cl_or_cL(self):
        """Set value using cl_or_cL units (alias for centiliter)."""
        return self.centiliter
    
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
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cord_or_cd(self):
        """Set value using cord_or_cd units (alias for cord)."""
        return self.cord
    
    @property
    def cd(self):
        """Set value using cd units (alias for cord)."""
        return self.cord
    
    @property
    def cord_foot(self):
        """Set value using cord foot units."""
        unit_const = units.VolumeUnits.cord_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cord_ft(self):
        """Set value using cord_ft units (alias for cord_foot)."""
        return self.cord_foot
    
    @property
    def cubic_centimeter(self):
        """Set value using cubic centimeter units."""
        unit_const = units.VolumeUnits.cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_3_or_cc(self):
        """Set value using mathrm_cm_3_or_cc units (alias for cubic_centimeter)."""
        return self.cubic_centimeter
    
    @property
    def cm_3(self):
        """Set value using cm_3 units (alias for cubic_centimeter)."""
        return self.cubic_centimeter
    
    @property
    def cc(self):
        """Set value using cc units (alias for cubic_centimeter)."""
        return self.cubic_centimeter
    
    @property
    def cubic_decameter(self):
        """Set value using cubic decameter units."""
        unit_const = units.VolumeUnits.cubic_decameter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dam_3(self):
        """Set value using dam_3 units (alias for cubic_decameter)."""
        return self.cubic_decameter
    
    @property
    def cubic_decimeter(self):
        """Set value using cubic decimeter units."""
        unit_const = units.VolumeUnits.cubic_decimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_dm_3(self):
        """Set value using mathrm_dm_3 units (alias for cubic_decimeter)."""
        return self.cubic_decimeter
    
    @property
    def cubic_foot(self):
        """Set value using cubic foot units."""
        unit_const = units.VolumeUnits.cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_ft_or_ft_3(self):
        """Set value using cu_ft_or_ft_3 units (alias for cubic_foot)."""
        return self.cubic_foot
    
    @property
    def cu_ft(self):
        """Set value using cu_ft units (alias for cubic_foot)."""
        return self.cubic_foot
    
    @property
    def ft_3(self):
        """Set value using ft_3 units (alias for cubic_foot)."""
        return self.cubic_foot
    
    @property
    def cubic_inch(self):
        """Set value using cubic inch units."""
        unit_const = units.VolumeUnits.cubic_inch
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_in_or_mathrm_in_3(self):
        """Set value using cu_in_or_mathrm_in_3 units (alias for cubic_inch)."""
        return self.cubic_inch
    
    @property
    def cu_in(self):
        """Set value using cu_in units (alias for cubic_inch)."""
        return self.cubic_inch
    
    @property
    def in_3(self):
        """Set value using in_3 units (alias for cubic_inch)."""
        return self.cubic_inch
    
    @property
    def cubic_kilometer(self):
        """Set value using cubic kilometer units."""
        unit_const = units.VolumeUnits.cubic_kilometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_km_3(self):
        """Set value using mathrm_km_3 units (alias for cubic_kilometer)."""
        return self.cubic_kilometer
    
    @property
    def cubic_meter(self):
        """Set value using cubic meter units."""
        unit_const = units.VolumeUnits.cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3(self):
        """Set value using mathrm_m_3 units (alias for cubic_meter)."""
        return self.cubic_meter
    
    @property
    def cubic_micrometer(self):
        """Set value using cubic micrometer units."""
        unit_const = units.VolumeUnits.cubic_micrometer
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_m_3(self):
        """Set value using mu_mathrm_m_3 units (alias for cubic_micrometer)."""
        return self.cubic_micrometer
    
    @property
    def cubic_mile_us_intl(self):
        """Set value using cubic mile (US, Intl) units."""
        unit_const = units.VolumeUnits.cubic_mile_us_intl
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_mi(self):
        """Set value using cu_mi units (alias for cubic_mile_us_intl)."""
        return self.cubic_mile_us_intl
    
    @property
    def cubic_millimeter(self):
        """Set value using cubic millimeter units."""
        unit_const = units.VolumeUnits.cubic_millimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_mm_3(self):
        """Set value using mathrm_mm_3 units (alias for cubic_millimeter)."""
        return self.cubic_millimeter
    
    @property
    def cubic_yard(self):
        """Set value using cubic yard units."""
        unit_const = units.VolumeUnits.cubic_yard
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def cu_yd_or_mathrm_yd_3(self):
        """Set value using cu_yd_or_mathrm_yd_3 units (alias for cubic_yard)."""
        return self.cubic_yard
    
    @property
    def cu_yd(self):
        """Set value using cu_yd units (alias for cubic_yard)."""
        return self.cubic_yard
    
    @property
    def yd_3(self):
        """Set value using yd_3 units (alias for cubic_yard)."""
        return self.cubic_yard
    
    @property
    def decast_re(self):
        """Set value using decastére units."""
        unit_const = units.VolumeUnits.decast_re
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dast(self):
        """Set value using dast units (alias for decast_re)."""
        return self.decast_re
    
    @property
    def deciliter(self):
        """Set value using deciliter units."""
        unit_const = units.VolumeUnits.deciliter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def dl_or_dL(self):
        """Set value using dl_or_dL units (alias for deciliter)."""
        return self.deciliter
    
    @property
    def dl(self):
        """Set value using dl units (alias for deciliter)."""
        return self.deciliter
    
    @property
    def dL(self):
        """Set value using dL units (alias for deciliter)."""
        return self.deciliter
    
    @property
    def fluid_drachm_uk(self):
        """Set value using fluid drachm (UK) units."""
        unit_const = units.VolumeUnits.fluid_drachm_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fl_dr_UK(self):
        """Set value using fl_dr_UK units (alias for fluid_drachm_uk)."""
        return self.fluid_drachm_uk
    
    @property
    def fluid_dram_us(self):
        """Set value using fluid dram (US) units."""
        unit_const = units.VolumeUnits.fluid_dram_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fl_dr_US_liq(self):
        """Set value using fl_dr_US_liq units (alias for fluid_dram_us)."""
        return self.fluid_dram_us
    
    @property
    def fluid_ounce_us(self):
        """Set value using fluid ounce (US) units."""
        unit_const = units.VolumeUnits.fluid_ounce_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def fl_oz(self):
        """Set value using fl_oz units (alias for fluid_ounce_us)."""
        return self.fluid_ounce_us
    
    @property
    def gallon_imperial_uk(self):
        """Set value using gallon (Imperial UK) units."""
        unit_const = units.VolumeUnits.gallon_imperial_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_UK_or_Imp_gal(self):
        """Set value using gal_UK_or_Imp_gal units (alias for gallon_imperial_uk)."""
        return self.gallon_imperial_uk
    
    @property
    def gal_UK(self):
        """Set value using gal_UK units (alias for gallon_imperial_uk)."""
        return self.gallon_imperial_uk
    
    @property
    def Imp_gal(self):
        """Set value using Imp_gal units (alias for gallon_imperial_uk)."""
        return self.gallon_imperial_uk
    
    @property
    def gallon_us_dry(self):
        """Set value using gallon (US Dry) units."""
        unit_const = units.VolumeUnits.gallon_us_dry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_US_dry(self):
        """Set value using gal_US_dry units (alias for gallon_us_dry)."""
        return self.gallon_us_dry
    
    @property
    def gallon_us_liquid(self):
        """Set value using gallon (US Liquid) units."""
        unit_const = units.VolumeUnits.gallon_us_liquid
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal(self):
        """Set value using gal units (alias for gallon_us_liquid)."""
        return self.gallon_us_liquid
    
    @property
    def last(self):
        """Set value using last units."""
        unit_const = units.VolumeUnits.last
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def liter(self):
        """Set value using liter units."""
        unit_const = units.VolumeUnits.liter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1_or_L(self):
        """Set value using unit_1_or_L units (alias for liter)."""
        return self.liter
    
    @property
    def unit_1(self):
        """Set value using unit_1 units (alias for liter)."""
        return self.liter
    
    @property
    def L(self):
        """Set value using L units (alias for liter)."""
        return self.liter
    
    @property
    def microliter(self):
        """Set value using microliter units."""
        unit_const = units.VolumeUnits.microliter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mu_mathrm_l_or_mu_mathrm_L(self):
        """Set value using mu_mathrm_l_or_mu_mathrm_L units (alias for microliter)."""
        return self.microliter
    
    @property
    def mu_l(self):
        """Set value using mu_l units (alias for microliter)."""
        return self.microliter
    
    @property
    def mu_L(self):
        """Set value using mu_L units (alias for microliter)."""
        return self.microliter
    
    @property
    def milliliter(self):
        """Set value using milliliter units."""
        unit_const = units.VolumeUnits.milliliter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def ml(self):
        """Set value using ml units (alias for milliliter)."""
        return self.milliliter
    
    @property
    def mohr_centicube(self):
        """Set value using Mohr centicube units."""
        unit_const = units.VolumeUnits.mohr_centicube
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pint_uk(self):
        """Set value using pint (UK) units."""
        unit_const = units.VolumeUnits.pint_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pt_UK(self):
        """Set value using pt_UK units (alias for pint_uk)."""
        return self.pint_uk
    
    @property
    def pint_us_dry(self):
        """Set value using pint (US Dry) units."""
        unit_const = units.VolumeUnits.pint_us_dry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pt_US_dry(self):
        """Set value using pt_US_dry units (alias for pint_us_dry)."""
        return self.pint_us_dry
    
    @property
    def pint_us_liquid(self):
        """Set value using pint (US Liquid) units."""
        unit_const = units.VolumeUnits.pint_us_liquid
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def pt(self):
        """Set value using pt units (alias for pint_us_liquid)."""
        return self.pint_us_liquid
    
    @property
    def quart_us_dry(self):
        """Set value using quart (US Dry) units."""
        unit_const = units.VolumeUnits.quart_us_dry
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def qt_US_dry(self):
        """Set value using qt_US_dry units (alias for quart_us_dry)."""
        return self.quart_us_dry
    
    @property
    def st_re(self):
        """Set value using stére units."""
        unit_const = units.VolumeUnits.st_re
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def st(self):
        """Set value using st units (alias for st_re)."""
        return self.st_re
    
    @property
    def tablespoon_metric(self):
        """Set value using tablespoon (Metric) units."""
        unit_const = units.VolumeUnits.tablespoon_metric
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def tbsp_Metric(self):
        """Set value using tbsp_Metric units (alias for tablespoon_metric)."""
        return self.tablespoon_metric
    
    @property
    def tablespoon_us(self):
        """Set value using tablespoon (US) units."""
        unit_const = units.VolumeUnits.tablespoon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def tbsp(self):
        """Set value using tbsp units (alias for tablespoon_us)."""
        return self.tablespoon_us
    
    @property
    def teaspoon_us(self):
        """Set value using teaspoon (US) units."""
        unit_const = units.VolumeUnits.teaspoon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def tsp(self):
        """Set value using tsp units (alias for teaspoon_us)."""
        return self.teaspoon_us
    

class VolumeFractionOfISetter(TypeSafeSetter):
    """VolumeFractionOfI-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_centimeters_of_i_per_cubic_meter_total(self):
        """Set value using cubic centimeters of "i" per cubic meter total units."""
        unit_const = units.VolumeFractionOfIUnits.cubic_centimeters_of_i_per_cubic_meter_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cm_mathrm_i_3_mathrm_m_3_or_mathrm_cc_mathrm_i_mathrm_m_3(self):
        """Set value using mathrm_cm_mathrm_i_3_mathrm_m_3_or_mathrm_cc_mathrm_i_mathrm_m_3 units (alias for cubic_centimeters_of_i_per_cubic_meter_total)."""
        return self.cubic_centimeters_of_i_per_cubic_meter_total
    
    @property
    def cm_i_3_m_3(self):
        """Set value using cm_i_3_m_3 units (alias for cubic_centimeters_of_i_per_cubic_meter_total)."""
        return self.cubic_centimeters_of_i_per_cubic_meter_total
    
    @property
    def cc_i_m_3(self):
        """Set value using cc_i_m_3 units (alias for cubic_centimeters_of_i_per_cubic_meter_total)."""
        return self.cubic_centimeters_of_i_per_cubic_meter_total
    
    @property
    def cubic_foot_of_i_per_cubic_foot_total(self):
        """Set value using cubic foot of "i" per cubic foot total units."""
        unit_const = units.VolumeFractionOfIUnits.cubic_foot_of_i_per_cubic_foot_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_mathrm_i_3_mathrm_ft_3_or_mathrm_cft_mathrm_i_mathrm_cft(self):
        """Set value using mathrm_ft_mathrm_i_3_mathrm_ft_3_or_mathrm_cft_mathrm_i_mathrm_cft units (alias for cubic_foot_of_i_per_cubic_foot_total)."""
        return self.cubic_foot_of_i_per_cubic_foot_total
    
    @property
    def ft_i_3_ft_3(self):
        """Set value using ft_i_3_ft_3 units (alias for cubic_foot_of_i_per_cubic_foot_total)."""
        return self.cubic_foot_of_i_per_cubic_foot_total
    
    @property
    def cft_i_cft(self):
        """Set value using cft_i_cft units (alias for cubic_foot_of_i_per_cubic_foot_total)."""
        return self.cubic_foot_of_i_per_cubic_foot_total
    
    @property
    def cubic_meters_of_i_per_cubic_meter_total(self):
        """Set value using cubic meters of " i " per cubic meter total units."""
        unit_const = units.VolumeFractionOfIUnits.cubic_meters_of_i_per_cubic_meter_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_mathrm_i_3_mathrm_m_3(self):
        """Set value using mathrm_m_mathrm_i_3_mathrm_m_3 units (alias for cubic_meters_of_i_per_cubic_meter_total)."""
        return self.cubic_meters_of_i_per_cubic_meter_total
    
    @property
    def gallons_of_i_per_gallon_total(self):
        """Set value using gallons of "i" per gallon total units."""
        unit_const = units.VolumeFractionOfIUnits.gallons_of_i_per_gallon_total
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_gal_mathrm_i_mathrm_gal(self):
        """Set value using mathrm_gal_mathrm_i_mathrm_gal units (alias for gallons_of_i_per_gallon_total)."""
        return self.gallons_of_i_per_gallon_total
    

class VolumetricCalorificHeatingValueSetter(TypeSafeSetter):
    """VolumetricCalorificHeatingValue-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def british_thermal_unit_per_cubic_foot(self):
        """Set value using British thermal unit per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.british_thermal_unit_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Btu_mathrm_ft_3_or_Btu_cft(self):
        """Set value using mathrm_Btu_mathrm_ft_3_or_Btu_cft units (alias for british_thermal_unit_per_cubic_foot)."""
        return self.british_thermal_unit_per_cubic_foot
    
    @property
    def Btu_ft_3(self):
        """Set value using Btu_ft_3 units (alias for british_thermal_unit_per_cubic_foot)."""
        return self.british_thermal_unit_per_cubic_foot
    
    @property
    def Btu_cft(self):
        """Set value using Btu_cft units (alias for british_thermal_unit_per_cubic_foot)."""
        return self.british_thermal_unit_per_cubic_foot
    
    @property
    def british_thermal_unit_per_gallon_uk(self):
        """Set value using British thermal unit per gallon (UK) units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.british_thermal_unit_per_gallon_uk
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_gal_UK(self):
        """Set value using Btu_gal_UK units (alias for british_thermal_unit_per_gallon_uk)."""
        return self.british_thermal_unit_per_gallon_uk
    
    @property
    def british_thermal_unit_per_gallon_us(self):
        """Set value using British thermal unit per gallon (US) units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.british_thermal_unit_per_gallon_us
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def Btu_gal_US(self):
        """Set value using Btu_gal_US units (alias for british_thermal_unit_per_gallon_us)."""
        return self.british_thermal_unit_per_gallon_us
    
    @property
    def calorie_per_cubic_centimeter(self):
        """Set value using calorie per cubic centimeter units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.calorie_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_cal_mathrm_cm_3_or_mathrm_cal_mathrm_cc(self):
        """Set value using mathrm_cal_mathrm_cm_3_or_mathrm_cal_mathrm_cc units (alias for calorie_per_cubic_centimeter)."""
        return self.calorie_per_cubic_centimeter
    
    @property
    def cal_cm_3(self):
        """Set value using cal_cm_3 units (alias for calorie_per_cubic_centimeter)."""
        return self.calorie_per_cubic_centimeter
    
    @property
    def cal_cc(self):
        """Set value using cal_cc units (alias for calorie_per_cubic_centimeter)."""
        return self.calorie_per_cubic_centimeter
    
    @property
    def chu_per_cubic_foot(self):
        """Set value using Chu per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.chu_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_Chu_mathrm_ft_3_or_mathrm_Chu_mathrm_cft(self):
        """Set value using mathrm_Chu_mathrm_ft_3_or_mathrm_Chu_mathrm_cft units (alias for chu_per_cubic_foot)."""
        return self.chu_per_cubic_foot
    
    @property
    def Chu_ft_3(self):
        """Set value using Chu_ft_3 units (alias for chu_per_cubic_foot)."""
        return self.chu_per_cubic_foot
    
    @property
    def Chu_cft(self):
        """Set value using Chu_cft units (alias for chu_per_cubic_foot)."""
        return self.chu_per_cubic_foot
    
    @property
    def joule_per_cubic_meter(self):
        """Set value using joule per cubic meter units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.joule_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_J_mathrm_m_3(self):
        """Set value using mathrm_J_mathrm_m_3 units (alias for joule_per_cubic_meter)."""
        return self.joule_per_cubic_meter
    
    @property
    def kilocalorie_per_cubic_foot(self):
        """Set value using kilocalorie per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.kilocalorie_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kcal_mathrm_ft_3_or_mathrm_kcal_mathrm_cft(self):
        """Set value using mathrm_kcal_mathrm_ft_3_or_mathrm_kcal_mathrm_cft units (alias for kilocalorie_per_cubic_foot)."""
        return self.kilocalorie_per_cubic_foot
    
    @property
    def kcal_ft_3(self):
        """Set value using kcal_ft_3 units (alias for kilocalorie_per_cubic_foot)."""
        return self.kilocalorie_per_cubic_foot
    
    @property
    def kcal_cft(self):
        """Set value using kcal_cft units (alias for kilocalorie_per_cubic_foot)."""
        return self.kilocalorie_per_cubic_foot
    
    @property
    def kilocalorie_per_cubic_meter(self):
        """Set value using kilocalorie per cubic meter units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.kilocalorie_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kcal_mathrm_m_3(self):
        """Set value using mathrm_kcal_mathrm_m_3 units (alias for kilocalorie_per_cubic_meter)."""
        return self.kilocalorie_per_cubic_meter
    
    @property
    def therm_100_k_btu(self):
        """Set value using therm ( 100 K Btu ) per cubic foot units."""
        unit_const = units.VolumetricCalorificHeatingValueUnits.therm_100_k_btu
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def thm_cft(self):
        """Set value using thm_cft units (alias for therm_100_k_btu)."""
        return self.therm_100_k_btu
    

class VolumetricCoefficientOfExpansionSetter(TypeSafeSetter):
    """VolumetricCoefficientOfExpansion-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_cubic_centimeter_per_kelvin_or_degree_celsius(self):
        """Set value using gram per cubic centimeter per kelvin (or degree Celsius) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.gram_per_cubic_centimeter_per_kelvin_or_degree_celsius
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_mathrm_cm_3_mathrm_K_or_g_cc_circ_mathrm_C(self):
        """Set value using mathrm_g_mathrm_cm_3_mathrm_K_or_g_cc_circ_mathrm_C units (alias for gram_per_cubic_centimeter_per_kelvin_or_degree_celsius)."""
        return self.gram_per_cubic_centimeter_per_kelvin_or_degree_celsius
    
    @property
    def g_cm_3_K(self):
        """Set value using g_cm_3_K units (alias for gram_per_cubic_centimeter_per_kelvin_or_degree_celsius)."""
        return self.gram_per_cubic_centimeter_per_kelvin_or_degree_celsius
    
    @property
    def g_cc_circ_C(self):
        """Set value using g_cc_circ_C units (alias for gram_per_cubic_centimeter_per_kelvin_or_degree_celsius)."""
        return self.gram_per_cubic_centimeter_per_kelvin_or_degree_celsius
    
    @property
    def kilogram_per_cubic_meter_per_kelvin_or_degree_celsius(self):
        """Set value using kilogram per cubic meter per kelvin (or degree Celsius) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.kilogram_per_cubic_meter_per_kelvin_or_degree_celsius
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_mathrm_m_3_mathrm_K_or_mathrm_kg_mathrm_m_3_circ_C(self):
        """Set value using mathrm_kg_mathrm_m_3_mathrm_K_or_mathrm_kg_mathrm_m_3_circ_C units (alias for kilogram_per_cubic_meter_per_kelvin_or_degree_celsius)."""
        return self.kilogram_per_cubic_meter_per_kelvin_or_degree_celsius
    
    @property
    def kg_m_3_K(self):
        """Set value using kg_m_3_K units (alias for kilogram_per_cubic_meter_per_kelvin_or_degree_celsius)."""
        return self.kilogram_per_cubic_meter_per_kelvin_or_degree_celsius
    
    @property
    def kg_m_3_circ_C(self):
        """Set value using kg_m_3_circ_C units (alias for kilogram_per_cubic_meter_per_kelvin_or_degree_celsius)."""
        return self.kilogram_per_cubic_meter_per_kelvin_or_degree_celsius
    
    @property
    def pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine(self):
        """Set value using pound per cubic foot per degree Fahrenheit (or degree Rankine) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_ft_3_circ_mathrm_R_or_mathrm_lb_mathrm_cft_circ_mathrm_F(self):
        """Set value using mathrm_lb_mathrm_ft_3_circ_mathrm_R_or_mathrm_lb_mathrm_cft_circ_mathrm_F units (alias for pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine)."""
        return self.pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine
    
    @property
    def lb_ft_3_circ_R(self):
        """Set value using lb_ft_3_circ_R units (alias for pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine)."""
        return self.pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine
    
    @property
    def lb_cft_circ_F(self):
        """Set value using lb_cft_circ_F units (alias for pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine)."""
        return self.pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine
    
    @property
    def pound_per_cubic_foot_per_kelvin_or_degree_celsius(self):
        """Set value using pound per cubic foot per kelvin (or degree Celsius) units."""
        unit_const = units.VolumetricCoefficientOfExpansionUnits.pound_per_cubic_foot_per_kelvin_or_degree_celsius
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_mathrm_ft_3_mathrm_K_or_mathrm_lb_mathrm_cft_circ_mathrm_C(self):
        """Set value using mathrm_lb_mathrm_ft_3_mathrm_K_or_mathrm_lb_mathrm_cft_circ_mathrm_C units (alias for pound_per_cubic_foot_per_kelvin_or_degree_celsius)."""
        return self.pound_per_cubic_foot_per_kelvin_or_degree_celsius
    
    @property
    def lb_ft_3_K(self):
        """Set value using lb_ft_3_K units (alias for pound_per_cubic_foot_per_kelvin_or_degree_celsius)."""
        return self.pound_per_cubic_foot_per_kelvin_or_degree_celsius
    
    @property
    def lb_cft_circ_C(self):
        """Set value using lb_cft_circ_C units (alias for pound_per_cubic_foot_per_kelvin_or_degree_celsius)."""
        return self.pound_per_cubic_foot_per_kelvin_or_degree_celsius
    

class VolumetricFlowRateSetter(TypeSafeSetter):
    """VolumetricFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_feet_per_day(self):
        """Set value using cubic feet per day units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_mathrm_d_or_mathrm_cft_mathrm_da_or_cfd(self):
        """Set value using mathrm_ft_3_mathrm_d_or_mathrm_cft_mathrm_da_or_cfd units (alias for cubic_feet_per_day)."""
        return self.cubic_feet_per_day
    
    @property
    def ft_3_d(self):
        """Set value using ft_3_d units (alias for cubic_feet_per_day)."""
        return self.cubic_feet_per_day
    
    @property
    def cft_da(self):
        """Set value using cft_da units (alias for cubic_feet_per_day)."""
        return self.cubic_feet_per_day
    
    @property
    def cfd(self):
        """Set value using cfd units (alias for cubic_feet_per_day)."""
        return self.cubic_feet_per_day
    
    @property
    def cubic_feet_per_hour(self):
        """Set value using cubic feet per hour units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_mathrm_h_or_mathrm_cft_mathrm_hr_or_cfh(self):
        """Set value using mathrm_ft_3_mathrm_h_or_mathrm_cft_mathrm_hr_or_cfh units (alias for cubic_feet_per_hour)."""
        return self.cubic_feet_per_hour
    
    @property
    def ft_3_h(self):
        """Set value using ft_3_h units (alias for cubic_feet_per_hour)."""
        return self.cubic_feet_per_hour
    
    @property
    def cft_hr(self):
        """Set value using cft_hr units (alias for cubic_feet_per_hour)."""
        return self.cubic_feet_per_hour
    
    @property
    def cfh(self):
        """Set value using cfh units (alias for cubic_feet_per_hour)."""
        return self.cubic_feet_per_hour
    
    @property
    def cubic_feet_per_minute(self):
        """Set value using cubic feet per minute units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_mathrm_min_or_mathrm_cft_mathrm_min_or_cfm(self):
        """Set value using mathrm_ft_3_mathrm_min_or_mathrm_cft_mathrm_min_or_cfm units (alias for cubic_feet_per_minute)."""
        return self.cubic_feet_per_minute
    
    @property
    def ft_3_min(self):
        """Set value using ft_3_min units (alias for cubic_feet_per_minute)."""
        return self.cubic_feet_per_minute
    
    @property
    def cft_min(self):
        """Set value using cft_min units (alias for cubic_feet_per_minute)."""
        return self.cubic_feet_per_minute
    
    @property
    def cfm(self):
        """Set value using cfm units (alias for cubic_feet_per_minute)."""
        return self.cubic_feet_per_minute
    
    @property
    def cubic_feet_per_second(self):
        """Set value using cubic feet per second units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_feet_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_mathrm_s_or_cft_sec_or_cfs(self):
        """Set value using mathrm_ft_3_mathrm_s_or_cft_sec_or_cfs units (alias for cubic_feet_per_second)."""
        return self.cubic_feet_per_second
    
    @property
    def ft_3_s(self):
        """Set value using ft_3_s units (alias for cubic_feet_per_second)."""
        return self.cubic_feet_per_second
    
    @property
    def cft_sec(self):
        """Set value using cft_sec units (alias for cubic_feet_per_second)."""
        return self.cubic_feet_per_second
    
    @property
    def cfs(self):
        """Set value using cfs units (alias for cubic_feet_per_second)."""
        return self.cubic_feet_per_second
    
    @property
    def cubic_meters_per_day(self):
        """Set value using cubic meters per day units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_mathrm_d(self):
        """Set value using mathrm_m_3_mathrm_d units (alias for cubic_meters_per_day)."""
        return self.cubic_meters_per_day
    
    @property
    def cubic_meters_per_hour(self):
        """Set value using cubic meters per hour units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_mathrm_h(self):
        """Set value using mathrm_m_3_mathrm_h units (alias for cubic_meters_per_hour)."""
        return self.cubic_meters_per_hour
    
    @property
    def cubic_meters_per_minute(self):
        """Set value using cubic meters per minute units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_min(self):
        """Set value using mathrm_m_3_min units (alias for cubic_meters_per_minute)."""
        return self.cubic_meters_per_minute
    
    @property
    def cubic_meters_per_second(self):
        """Set value using cubic meters per second units."""
        unit_const = units.VolumetricFlowRateUnits.cubic_meters_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_mathrm_s(self):
        """Set value using mathrm_m_3_mathrm_s units (alias for cubic_meters_per_second)."""
        return self.cubic_meters_per_second
    
    @property
    def gallons_per_day(self):
        """Set value using gallons per day units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_d_or_gpd_or_gal_da(self):
        """Set value using gal_d_or_gpd_or_gal_da units (alias for gallons_per_day)."""
        return self.gallons_per_day
    
    @property
    def gal_d(self):
        """Set value using gal_d units (alias for gallons_per_day)."""
        return self.gallons_per_day
    
    @property
    def gpd(self):
        """Set value using gpd units (alias for gallons_per_day)."""
        return self.gallons_per_day
    
    @property
    def gal_da(self):
        """Set value using gal_da units (alias for gallons_per_day)."""
        return self.gallons_per_day
    
    @property
    def gallons_per_hour(self):
        """Set value using gallons per hour units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_h_or_gph_or_gal_hr(self):
        """Set value using gal_h_or_gph_or_gal_hr units (alias for gallons_per_hour)."""
        return self.gallons_per_hour
    
    @property
    def gal_h(self):
        """Set value using gal_h units (alias for gallons_per_hour)."""
        return self.gallons_per_hour
    
    @property
    def gph(self):
        """Set value using gph units (alias for gallons_per_hour)."""
        return self.gallons_per_hour
    
    @property
    def gal_hr(self):
        """Set value using gal_hr units (alias for gallons_per_hour)."""
        return self.gallons_per_hour
    
    @property
    def gallons_per_minute(self):
        """Set value using gallons per minute units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_min_or_gpm(self):
        """Set value using gal_min_or_gpm units (alias for gallons_per_minute)."""
        return self.gallons_per_minute
    
    @property
    def gal_min(self):
        """Set value using gal_min units (alias for gallons_per_minute)."""
        return self.gallons_per_minute
    
    @property
    def gpm(self):
        """Set value using gpm units (alias for gallons_per_minute)."""
        return self.gallons_per_minute
    
    @property
    def gallons_per_second(self):
        """Set value using gallons per second units."""
        unit_const = units.VolumetricFlowRateUnits.gallons_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def gal_s_or_gps_or_gal_sec(self):
        """Set value using gal_s_or_gps_or_gal_sec units (alias for gallons_per_second)."""
        return self.gallons_per_second
    
    @property
    def gal_s(self):
        """Set value using gal_s units (alias for gallons_per_second)."""
        return self.gallons_per_second
    
    @property
    def gps(self):
        """Set value using gps units (alias for gallons_per_second)."""
        return self.gallons_per_second
    
    @property
    def gal_sec(self):
        """Set value using gal_sec units (alias for gallons_per_second)."""
        return self.gallons_per_second
    
    @property
    def liters_per_day(self):
        """Set value using liters per day units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1_d(self):
        """Set value using unit_1_d units (alias for liters_per_day)."""
        return self.liters_per_day
    
    @property
    def liters_per_hour(self):
        """Set value using liters per hour units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1_h(self):
        """Set value using unit_1_h units (alias for liters_per_hour)."""
        return self.liters_per_hour
    
    @property
    def liters_per_minute(self):
        """Set value using liters per minute units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_second(self):
        """Set value using liters per second units."""
        unit_const = units.VolumetricFlowRateUnits.liters_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1_s(self):
        """Set value using unit_1_s units (alias for liters_per_second)."""
        return self.liters_per_second
    

class VolumetricFluxSetter(TypeSafeSetter):
    """VolumetricFlux-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def cubic_feet_per_square_foot_per_day(self):
        """Set value using cubic feet per square foot per day units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_left_mathrm_ft_2_mathrm_d_right_or_mathrm_cft_mathrm_sqft_da(self):
        """Set value using mathrm_ft_3_left_mathrm_ft_2_mathrm_d_right_or_mathrm_cft_mathrm_sqft_da units (alias for cubic_feet_per_square_foot_per_day)."""
        return self.cubic_feet_per_square_foot_per_day
    
    @property
    def ft_3_left_ft_2_dright(self):
        """Set value using ft_3_left_ft_2_dright units (alias for cubic_feet_per_square_foot_per_day)."""
        return self.cubic_feet_per_square_foot_per_day
    
    @property
    def cft_sqft_da(self):
        """Set value using cft_sqft_da units (alias for cubic_feet_per_square_foot_per_day)."""
        return self.cubic_feet_per_square_foot_per_day
    
    @property
    def cubic_feet_per_square_foot_per_hour(self):
        """Set value using cubic feet per square foot per hour units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_left_mathrm_ft_2_mathrm_h_right_or_mathrm_cft_mathrm_sqft_hr(self):
        """Set value using mathrm_ft_3_left_mathrm_ft_2_mathrm_h_right_or_mathrm_cft_mathrm_sqft_hr units (alias for cubic_feet_per_square_foot_per_hour)."""
        return self.cubic_feet_per_square_foot_per_hour
    
    @property
    def ft_3_left_ft_2_hright(self):
        """Set value using ft_3_left_ft_2_hright units (alias for cubic_feet_per_square_foot_per_hour)."""
        return self.cubic_feet_per_square_foot_per_hour
    
    @property
    def cft_sqft_hr(self):
        """Set value using cft_sqft_hr units (alias for cubic_feet_per_square_foot_per_hour)."""
        return self.cubic_feet_per_square_foot_per_hour
    
    @property
    def cubic_feet_per_square_foot_per_minute(self):
        """Set value using cubic feet per square foot per minute units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_left_mathrm_ft_2_min_right_or_mathrm_cft_sqft_min(self):
        """Set value using mathrm_ft_3_left_mathrm_ft_2_min_right_or_mathrm_cft_sqft_min units (alias for cubic_feet_per_square_foot_per_minute)."""
        return self.cubic_feet_per_square_foot_per_minute
    
    @property
    def ft_3_left_ft_2_min_right(self):
        """Set value using ft_3_left_ft_2_min_right units (alias for cubic_feet_per_square_foot_per_minute)."""
        return self.cubic_feet_per_square_foot_per_minute
    
    @property
    def cft_sqft_min(self):
        """Set value using cft_sqft_min units (alias for cubic_feet_per_square_foot_per_minute)."""
        return self.cubic_feet_per_square_foot_per_minute
    
    @property
    def cubic_feet_per_square_foot_per_second(self):
        """Set value using cubic feet per square foot per second units."""
        unit_const = units.VolumetricFluxUnits.cubic_feet_per_square_foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_ft_3_left_mathrm_ft_2_mathrm_s_right_or_cft_sqft_sec(self):
        """Set value using mathrm_ft_3_left_mathrm_ft_2_mathrm_s_right_or_cft_sqft_sec units (alias for cubic_feet_per_square_foot_per_second)."""
        return self.cubic_feet_per_square_foot_per_second
    
    @property
    def ft_3_left_ft_2_sright(self):
        """Set value using ft_3_left_ft_2_sright units (alias for cubic_feet_per_square_foot_per_second)."""
        return self.cubic_feet_per_square_foot_per_second
    
    @property
    def cft_sqft_sec(self):
        """Set value using cft_sqft_sec units (alias for cubic_feet_per_square_foot_per_second)."""
        return self.cubic_feet_per_square_foot_per_second
    
    @property
    def cubic_meters_per_square_meter_per_day(self):
        """Set value using cubic meters per square meter per day units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_left_mathrm_m_2_mathrm_d_right(self):
        """Set value using mathrm_m_3_left_mathrm_m_2_mathrm_d_right units (alias for cubic_meters_per_square_meter_per_day)."""
        return self.cubic_meters_per_square_meter_per_day
    
    @property
    def cubic_meters_per_square_meter_per_hour(self):
        """Set value using cubic meters per square meter per hour units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_left_mathrm_m_2_mathrm_h_right(self):
        """Set value using mathrm_m_3_left_mathrm_m_2_mathrm_h_right units (alias for cubic_meters_per_square_meter_per_hour)."""
        return self.cubic_meters_per_square_meter_per_hour
    
    @property
    def cubic_meters_per_square_meter_per_minute(self):
        """Set value using cubic meters per square meter per minute units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_left_mathrm_m_2_mathrm_min_right(self):
        """Set value using mathrm_m_3_left_mathrm_m_2_mathrm_min_right units (alias for cubic_meters_per_square_meter_per_minute)."""
        return self.cubic_meters_per_square_meter_per_minute
    
    @property
    def cubic_meters_per_square_meter_per_second(self):
        """Set value using cubic meters per square meter per second units."""
        unit_const = units.VolumetricFluxUnits.cubic_meters_per_square_meter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_m_3_left_mathrm_m_2_mathrm_s_right(self):
        """Set value using mathrm_m_3_left_mathrm_m_2_mathrm_s_right units (alias for cubic_meters_per_square_meter_per_second)."""
        return self.cubic_meters_per_square_meter_per_second
    
    @property
    def gallons_per_square_foot_per_day(self):
        """Set value using gallons per square foot per day units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_gal_left_mathrm_ft_2_mathrm_d_right_or_gal_sqft_da(self):
        """Set value using mathrm_gal_left_mathrm_ft_2_mathrm_d_right_or_gal_sqft_da units (alias for gallons_per_square_foot_per_day)."""
        return self.gallons_per_square_foot_per_day
    
    @property
    def gal_left_ft_2_dright(self):
        """Set value using gal_left_ft_2_dright units (alias for gallons_per_square_foot_per_day)."""
        return self.gallons_per_square_foot_per_day
    
    @property
    def gal_sqft_da(self):
        """Set value using gal_sqft_da units (alias for gallons_per_square_foot_per_day)."""
        return self.gallons_per_square_foot_per_day
    
    @property
    def gallons_per_square_foot_per_hour(self):
        """Set value using gallons per square foot per hour units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_gal_left_mathrm_ft_2_mathrm_h_right_or_gal_sqft_hr(self):
        """Set value using mathrm_gal_left_mathrm_ft_2_mathrm_h_right_or_gal_sqft_hr units (alias for gallons_per_square_foot_per_hour)."""
        return self.gallons_per_square_foot_per_hour
    
    @property
    def gal_left_ft_2_hright(self):
        """Set value using gal_left_ft_2_hright units (alias for gallons_per_square_foot_per_hour)."""
        return self.gallons_per_square_foot_per_hour
    
    @property
    def gal_sqft_hr(self):
        """Set value using gal_sqft_hr units (alias for gallons_per_square_foot_per_hour)."""
        return self.gallons_per_square_foot_per_hour
    
    @property
    def gallons_per_square_foot_per_minute(self):
        """Set value using gallons per square foot per minute units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_gal_left_mathrm_ft_2_mathrm_min_right_or_gal_sqft_min_or_gpm_sqft(self):
        """Set value using mathrm_gal_left_mathrm_ft_2_mathrm_min_right_or_gal_sqft_min_or_gpm_sqft units (alias for gallons_per_square_foot_per_minute)."""
        return self.gallons_per_square_foot_per_minute
    
    @property
    def gal_left_ft_2_minright(self):
        """Set value using gal_left_ft_2_minright units (alias for gallons_per_square_foot_per_minute)."""
        return self.gallons_per_square_foot_per_minute
    
    @property
    def gal_sqft_min(self):
        """Set value using gal_sqft_min units (alias for gallons_per_square_foot_per_minute)."""
        return self.gallons_per_square_foot_per_minute
    
    @property
    def gpm_sqft(self):
        """Set value using gpm_sqft units (alias for gallons_per_square_foot_per_minute)."""
        return self.gallons_per_square_foot_per_minute
    
    @property
    def gallons_per_square_foot_per_second(self):
        """Set value using gallons per square foot per second units."""
        unit_const = units.VolumetricFluxUnits.gallons_per_square_foot_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_gal_left_mathrm_ft_2_mathrm_s_right_or_gal_mathrm_sqft_mathrm_sec(self):
        """Set value using mathrm_gal_left_mathrm_ft_2_mathrm_s_right_or_gal_mathrm_sqft_mathrm_sec units (alias for gallons_per_square_foot_per_second)."""
        return self.gallons_per_square_foot_per_second
    
    @property
    def gal_left_ft_2_sright(self):
        """Set value using gal_left_ft_2_sright units (alias for gallons_per_square_foot_per_second)."""
        return self.gallons_per_square_foot_per_second
    
    @property
    def gal_sqft_sec(self):
        """Set value using gal_sqft_sec units (alias for gallons_per_square_foot_per_second)."""
        return self.gallons_per_square_foot_per_second
    
    @property
    def liters_per_square_meter_per_day(self):
        """Set value using liters per square meter per day units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_day
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_square_meter_per_hour(self):
        """Set value using liters per square meter per hour units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_hour
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_square_meter_per_minute(self):
        """Set value using liters per square meter per minute units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_minute
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def liters_per_square_meter_per_second(self):
        """Set value using liters per square meter per second units."""
        unit_const = units.VolumetricFluxUnits.liters_per_square_meter_per_second
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    

class VolumetricMassFlowRateSetter(TypeSafeSetter):
    """VolumetricMassFlowRate-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def gram_per_second_per_cubic_centimeter(self):
        """Set value using gram per second per cubic centimeter units."""
        unit_const = units.VolumetricMassFlowRateUnits.gram_per_second_per_cubic_centimeter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_g_left_mathrm_s_mathrm_cm_3_right_or_g_s_cc_or_mathrm_g_mathrm_cc_mathrm_sec(self):
        """Set value using mathrm_g_left_mathrm_s_mathrm_cm_3_right_or_g_s_cc_or_mathrm_g_mathrm_cc_mathrm_sec units (alias for gram_per_second_per_cubic_centimeter)."""
        return self.gram_per_second_per_cubic_centimeter
    
    @property
    def g_left_s_cm_3right(self):
        """Set value using g_left_s_cm_3right units (alias for gram_per_second_per_cubic_centimeter)."""
        return self.gram_per_second_per_cubic_centimeter
    
    @property
    def g_s_cc(self):
        """Set value using g_s_cc units (alias for gram_per_second_per_cubic_centimeter)."""
        return self.gram_per_second_per_cubic_centimeter
    
    @property
    def g_cc_sec(self):
        """Set value using g_cc_sec units (alias for gram_per_second_per_cubic_centimeter)."""
        return self.gram_per_second_per_cubic_centimeter
    
    @property
    def kilogram_per_hour_per_cubic_foot(self):
        """Set value using kilogram per hour per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.kilogram_per_hour_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_h_ft_3_or_kg_hr_cft(self):
        """Set value using kg_h_ft_3_or_kg_hr_cft units (alias for kilogram_per_hour_per_cubic_foot)."""
        return self.kilogram_per_hour_per_cubic_foot
    
    @property
    def kg_h_ft_3(self):
        """Set value using kg_h_ft_3 units (alias for kilogram_per_hour_per_cubic_foot)."""
        return self.kilogram_per_hour_per_cubic_foot
    
    @property
    def kg_hr_cft(self):
        """Set value using kg_hr_cft units (alias for kilogram_per_hour_per_cubic_foot)."""
        return self.kilogram_per_hour_per_cubic_foot
    
    @property
    def kilogram_per_hour_per_cubic_meter(self):
        """Set value using kilogram per hour per cubic meter units."""
        unit_const = units.VolumetricMassFlowRateUnits.kilogram_per_hour_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def kg_h_m3_or_kg_hr_cu_m(self):
        """Set value using kg_h_m3_or_kg_hr_cu_m units (alias for kilogram_per_hour_per_cubic_meter)."""
        return self.kilogram_per_hour_per_cubic_meter
    
    @property
    def kg_h_m3(self):
        """Set value using kg_h_m3 units (alias for kilogram_per_hour_per_cubic_meter)."""
        return self.kilogram_per_hour_per_cubic_meter
    
    @property
    def kg_hr_cu_m(self):
        """Set value using kg_hr_cu_m units (alias for kilogram_per_hour_per_cubic_meter)."""
        return self.kilogram_per_hour_per_cubic_meter
    
    @property
    def kilogram_per_second_per_cubic_meter(self):
        """Set value using kilogram per second per cubic meter units."""
        unit_const = units.VolumetricMassFlowRateUnits.kilogram_per_second_per_cubic_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_kg_left_mathrm_s_mathrm_m_3_right_or_kg_sec_cu_m(self):
        """Set value using mathrm_kg_left_mathrm_s_mathrm_m_3_right_or_kg_sec_cu_m units (alias for kilogram_per_second_per_cubic_meter)."""
        return self.kilogram_per_second_per_cubic_meter
    
    @property
    def kg_left_s_m_3right(self):
        """Set value using kg_left_s_m_3right units (alias for kilogram_per_second_per_cubic_meter)."""
        return self.kilogram_per_second_per_cubic_meter
    
    @property
    def kg_sec_cu_m(self):
        """Set value using kg_sec_cu_m units (alias for kilogram_per_second_per_cubic_meter)."""
        return self.kilogram_per_second_per_cubic_meter
    
    @property
    def pound_per_hour_per_cubic_foot(self):
        """Set value using pound per hour per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.pound_per_hour_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def mathrm_lb_left_mathrm_h_mathrm_ft_3_right_or_mathrm_lb_mathrm_hr_mathrm_cft_or_PPH_cft(self):
        """Set value using mathrm_lb_left_mathrm_h_mathrm_ft_3_right_or_mathrm_lb_mathrm_hr_mathrm_cft_or_PPH_cft units (alias for pound_per_hour_per_cubic_foot)."""
        return self.pound_per_hour_per_cubic_foot
    
    @property
    def lb_left_h_ft_3right(self):
        """Set value using lb_left_h_ft_3right units (alias for pound_per_hour_per_cubic_foot)."""
        return self.pound_per_hour_per_cubic_foot
    
    @property
    def lb_hr_cft(self):
        """Set value using lb_hr_cft units (alias for pound_per_hour_per_cubic_foot)."""
        return self.pound_per_hour_per_cubic_foot
    
    @property
    def PPH_cft(self):
        """Set value using PPH_cft units (alias for pound_per_hour_per_cubic_foot)."""
        return self.pound_per_hour_per_cubic_foot
    
    @property
    def pound_per_minute_per_cubic_foot(self):
        """Set value using pound per minute per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.pound_per_minute_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def lb_min_mathrm_ft_3_or_lb_mathrm_min_mathrm_cft(self):
        """Set value using lb_min_mathrm_ft_3_or_lb_mathrm_min_mathrm_cft units (alias for pound_per_minute_per_cubic_foot)."""
        return self.pound_per_minute_per_cubic_foot
    
    @property
    def lb_min_ft_3(self):
        """Set value using lb_min_ft_3 units (alias for pound_per_minute_per_cubic_foot)."""
        return self.pound_per_minute_per_cubic_foot
    
    @property
    def lb_min_cft(self):
        """Set value using lb_min_cft units (alias for pound_per_minute_per_cubic_foot)."""
        return self.pound_per_minute_per_cubic_foot
    
    @property
    def pound_per_second_per_cubic_foot(self):
        """Set value using pound per second per cubic foot units."""
        unit_const = units.VolumetricMassFlowRateUnits.pound_per_second_per_cubic_foot
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def b_s_ft_3_or_lb_sec_cft(self):
        """Set value using b_s_ft_3_or_lb_sec_cft units (alias for pound_per_second_per_cubic_foot)."""
        return self.pound_per_second_per_cubic_foot
    
    @property
    def b_s_ft_3(self):
        """Set value using b_s_ft_3 units (alias for pound_per_second_per_cubic_foot)."""
        return self.pound_per_second_per_cubic_foot
    
    @property
    def lb_sec_cft(self):
        """Set value using lb_sec_cft units (alias for pound_per_second_per_cubic_foot)."""
        return self.pound_per_second_per_cubic_foot
    

class WavenumberSetter(TypeSafeSetter):
    """Wavenumber-specific setter with optimized unit properties."""
    __slots__ = ()
    
    @property
    def diopter(self):
        """Set value using diopter units."""
        unit_const = units.WavenumberUnits.diopter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def D(self):
        """Set value using D units (alias for diopter)."""
        return self.diopter
    
    @property
    def kayser(self):
        """Set value using kayser units."""
        unit_const = units.WavenumberUnits.kayser
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def K(self):
        """Set value using K units (alias for kayser)."""
        return self.kayser
    
    @property
    def reciprocal_meter(self):
        """Set value using reciprocal meter units."""
        unit_const = units.WavenumberUnits.reciprocal_meter
        self.variable.quantity = Quantity(self.value, unit_const)
        return self.variable
    
    @property
    def unit_1_m(self):
        """Set value using unit_1_m units (alias for reciprocal_meter)."""
        return self.reciprocal_meter
    

