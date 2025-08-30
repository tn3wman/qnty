"""
EnergyHeatWork Variable Module
===============================

Type-safe energy, heat, work variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY
from ..units import EnergyHeatWorkUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class EnergyHeatWorkSetter(TypeSafeSetter):
    """EnergyHeatWork-specific setter with only energy, heat, work units."""
    
    def __init__(self, variable: 'EnergyHeatWork', value: float):
        super().__init__(variable, value)
    
    # Only energy, heat, work units available - compile-time safe!
    @property
    def barrel_oil_equivalents(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.barrel_oil_equivalent)
        return cast('EnergyHeatWork', self.variable)
    @property
    def billion_electronvolts(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.billion_electronvolt)
        return cast('EnergyHeatWork', self.variable)
    @property
    def british_thermal_units(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.british_thermal_unit)
        return cast('EnergyHeatWork', self.variable)
    @property
    def british_thermal_units(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.british_thermal_unit)
        return cast('EnergyHeatWork', self.variable)
    @property
    def british_thermal_unit_international_steam_tables(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.british_thermal_unit_international_steam_tables)
        return cast('EnergyHeatWork', self.variable)
    @property
    def british_thermal_unit_isotc_12s(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.british_thermal_unit_isotc_12)
        return cast('EnergyHeatWork', self.variable)
    @property
    def british_thermal_unit_means(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.british_thermal_unit_mean)
        return cast('EnergyHeatWork', self.variable)
    @property
    def british_thermal_unit_thermochemicals(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.british_thermal_unit_thermochemical)
        return cast('EnergyHeatWork', self.variable)
    @property
    def calories(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.calorie)
        return cast('EnergyHeatWork', self.variable)
    @property
    def calories(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.calorie)
        return cast('EnergyHeatWork', self.variable)
    @property
    def calorie_international_steam_tables(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.calorie_international_steam_tables)
        return cast('EnergyHeatWork', self.variable)
    @property
    def calorie_means(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.calorie_mean)
        return cast('EnergyHeatWork', self.variable)
    @property
    def calorie_nutritionals(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.calorie_nutritional)
        return cast('EnergyHeatWork', self.variable)
    @property
    def calorie_thermochemicals(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.calorie_thermochemical)
        return cast('EnergyHeatWork', self.variable)
    @property
    def celsius(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.celsius)
        return cast('EnergyHeatWork', self.variable)
    @property
    def celsius(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.celsius)
        return cast('EnergyHeatWork', self.variable)
    @property
    def electron_volts(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.electron_volt)
        return cast('EnergyHeatWork', self.variable)
    @property
    def ergs(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.erg)
        return cast('EnergyHeatWork', self.variable)
    @property
    def foot_pound_force_duty(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.foot_pound_force_duty)
        return cast('EnergyHeatWork', self.variable)
    @property
    def footpoundals(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.footpoundal)
        return cast('EnergyHeatWork', self.variable)
    @property
    def frigories(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.frigorie)
        return cast('EnergyHeatWork', self.variable)
    @property
    def hartree_atomic_unit_of_energy(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.hartree_atomic_unit_of_energy)
        return cast('EnergyHeatWork', self.variable)
    @property
    def joules(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.joule)
        return cast('EnergyHeatWork', self.variable)
    @property
    def joule_internationals(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.joule_international)
        return cast('EnergyHeatWork', self.variable)
    @property
    def kilocalorie_thermals(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.kilocalorie_thermal)
        return cast('EnergyHeatWork', self.variable)
    @property
    def kilogram_force_meters(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.kilogram_force_meter)
        return cast('EnergyHeatWork', self.variable)
    @property
    def kiloton_tnts(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.kiloton_tnt)
        return cast('EnergyHeatWork', self.variable)
    @property
    def kilowatt_hours(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.kilowatt_hour)
        return cast('EnergyHeatWork', self.variable)
    @property
    def liter_atmospheres(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.liter_atmosphere)
        return cast('EnergyHeatWork', self.variable)
    @property
    def megaton_tnts(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.megaton_tnt)
        return cast('EnergyHeatWork', self.variable)
    @property
    def pound_centigrade_units(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.pound_centigrade_unit)
        return cast('EnergyHeatWork', self.variable)
    @property
    def prouts(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.prout)
        return cast('EnergyHeatWork', self.variable)
    @property
    def q_units(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.q_unit)
        return cast('EnergyHeatWork', self.variable)
    @property
    def quad_quadrillion_btus(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.quad_quadrillion_btu)
        return cast('EnergyHeatWork', self.variable)
    @property
    def rydbergs(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.rydberg)
        return cast('EnergyHeatWork', self.variable)
    @property
    def therm_eegs(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.therm_eeg)
        return cast('EnergyHeatWork', self.variable)
    @property
    def therm_refineries(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.therm_refineries)
        return cast('EnergyHeatWork', self.variable)
    @property
    def therm_us(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.therm_us)
        return cast('EnergyHeatWork', self.variable)
    @property
    def ton_coal_equivalents(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.ton_coal_equivalent)
        return cast('EnergyHeatWork', self.variable)
    @property
    def ton_oil_equivalents(self) -> 'EnergyHeatWork':
        self.variable.quantity = FastQuantity(self.value, EnergyHeatWorkUnits.ton_oil_equivalent)
        return cast('EnergyHeatWork', self.variable)
    
    # Short aliases for convenience
    pass


class EnergyHeatWork(TypedVariable):
    """Type-safe energy, heat, work variable with expression capabilities."""
    
    _setter_class = EnergyHeatWorkSetter
    _expected_dimension = ENERGY
    _default_unit_property = "joules"
    
    def set(self, value: float) -> EnergyHeatWorkSetter:
        """Create a energy, heat, work setter for this variable with proper type annotation."""
        return EnergyHeatWorkSetter(self, value)


class EnergyHeatWorkModule(VariableModule):
    """EnergyHeatWork variable module definition."""
    
    def get_variable_class(self):
        return EnergyHeatWork
    
    def get_setter_class(self):
        return EnergyHeatWorkSetter
    
    def get_expected_dimension(self):
        return ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = EnergyHeatWorkModule()