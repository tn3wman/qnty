"""
FuelConsumption Variable Module
================================

Type-safe fuel consumption variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import FUEL_CONSUMPTION
from ..units import FuelConsumptionUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class FuelConsumptionSetter(TypeSafeSetter):
    """FuelConsumption-specific setter with only fuel consumption units."""
    
    def __init__(self, variable: 'FuelConsumption', value: float):
        super().__init__(variable, value)
    
    # Only fuel consumption units available - compile-time safe!
    @property
    def unit_100_km_per_liters(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.unit_100_km_per_liter)
        return cast('FuelConsumption', self.variable)
    @property
    def gallons_uk_per_100_miles(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.gallons_uk_per_100_miles)
        return cast('FuelConsumption', self.variable)
    @property
    def gallons_us_per_100_miles(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.gallons_us_per_100_miles)
        return cast('FuelConsumption', self.variable)
    @property
    def kilometers_per_gallon_uks(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.kilometers_per_gallon_uk)
        return cast('FuelConsumption', self.variable)
    @property
    def kilometers_per_gallon_us(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.kilometers_per_gallon_us)
        return cast('FuelConsumption', self.variable)
    @property
    def kilometers_per_liters(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.kilometers_per_liter)
        return cast('FuelConsumption', self.variable)
    @property
    def liters_per_100_kms(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.liters_per_100_km)
        return cast('FuelConsumption', self.variable)
    @property
    def liters_per_kilometers(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.liters_per_kilometer)
        return cast('FuelConsumption', self.variable)
    @property
    def meters_per_gallon_uks(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.meters_per_gallon_uk)
        return cast('FuelConsumption', self.variable)
    @property
    def meters_per_gallon_us(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.meters_per_gallon_us)
        return cast('FuelConsumption', self.variable)
    @property
    def miles_per_gallon_uks(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.miles_per_gallon_uk)
        return cast('FuelConsumption', self.variable)
    @property
    def miles_per_gallon_us(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.miles_per_gallon_us)
        return cast('FuelConsumption', self.variable)
    @property
    def miles_per_liters(self) -> 'FuelConsumption':
        self.variable.quantity = FastQuantity(self.value, FuelConsumptionUnits.miles_per_liter)
        return cast('FuelConsumption', self.variable)
    
    # Short aliases for convenience
    pass


class FuelConsumption(TypedVariable):
    """Type-safe fuel consumption variable with expression capabilities."""
    
    _setter_class = FuelConsumptionSetter
    _expected_dimension = FUEL_CONSUMPTION
    _default_unit_property = "kilometers_per_liters"
    
    def set(self, value: float) -> FuelConsumptionSetter:
        """Create a fuel consumption setter for this variable with proper type annotation."""
        return FuelConsumptionSetter(self, value)


class FuelConsumptionModule(VariableModule):
    """FuelConsumption variable module definition."""
    
    def get_variable_class(self):
        return FuelConsumption
    
    def get_setter_class(self):
        return FuelConsumptionSetter
    
    def get_expected_dimension(self):
        return FUEL_CONSUMPTION


# Register this module for auto-discovery
VARIABLE_MODULE = FuelConsumptionModule()