"""
Volume Variable Module
=======================

Type-safe volume variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import VOLUME
from ..units import VolumeUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VolumeSetter(TypeSafeSetter):
    """Volume-specific setter with only volume units."""
    
    def __init__(self, variable: 'Volume', value: float):
        super().__init__(variable, value)
    
    # Only volume units available - compile-time safe!
    @property
    def acre_foots(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.acre_foot)
        return cast('Volume', self.variable)
    @property
    def acre_inchs(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.acre_inch)
        return cast('Volume', self.variable)
    @property
    def barrel_us_liquids(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.barrel_us_liquid)
        return cast('Volume', self.variable)
    @property
    def barrel_us_petros(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.barrel_us_petro)
        return cast('Volume', self.variable)
    @property
    def board_foot_measures(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.board_foot_measure)
        return cast('Volume', self.variable)
    @property
    def bushel_us_dry(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.bushel_us_dry)
        return cast('Volume', self.variable)
    @property
    def centiliters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.centiliter)
        return cast('Volume', self.variable)
    @property
    def cords(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cord)
        return cast('Volume', self.variable)
    @property
    def cord_foots(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cord_foot)
        return cast('Volume', self.variable)
    @property
    def cubic_centimeters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_centimeter)
        return cast('Volume', self.variable)
    @property
    def cubic_decameters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_decameter)
        return cast('Volume', self.variable)
    @property
    def cubic_decimeters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_decimeter)
        return cast('Volume', self.variable)
    @property
    def cubic_foots(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_foot)
        return cast('Volume', self.variable)
    @property
    def cubic_inchs(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_inch)
        return cast('Volume', self.variable)
    @property
    def cubic_kilometers(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_kilometer)
        return cast('Volume', self.variable)
    @property
    def cubic_meters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_meter)
        return cast('Volume', self.variable)
    @property
    def cubic_micrometers(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_micrometer)
        return cast('Volume', self.variable)
    @property
    def cubic_mile_us_intls(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_mile_us_intl)
        return cast('Volume', self.variable)
    @property
    def cubic_millimeters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_millimeter)
        return cast('Volume', self.variable)
    @property
    def cubic_yards(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.cubic_yard)
        return cast('Volume', self.variable)
    @property
    def decastéres(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.decastére)
        return cast('Volume', self.variable)
    @property
    def deciliters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.deciliter)
        return cast('Volume', self.variable)
    @property
    def fluid_drachm_uks(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.fluid_drachm_uk)
        return cast('Volume', self.variable)
    @property
    def fluid_dram_us(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.fluid_dram_us)
        return cast('Volume', self.variable)
    @property
    def fluid_ounce_us(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.fluid_ounce_us)
        return cast('Volume', self.variable)
    @property
    def gallon_imperial_uks(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.gallon_imperial_uk)
        return cast('Volume', self.variable)
    @property
    def gallon_us_dry(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.gallon_us_dry)
        return cast('Volume', self.variable)
    @property
    def gallon_us_liquids(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.gallon_us_liquid)
        return cast('Volume', self.variable)
    @property
    def lasts(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.last)
        return cast('Volume', self.variable)
    @property
    def liters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.liter)
        return cast('Volume', self.variable)
    @property
    def microliters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.microliter)
        return cast('Volume', self.variable)
    @property
    def milliliters(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.milliliter)
        return cast('Volume', self.variable)
    @property
    def mohr_centicubes(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.mohr_centicube)
        return cast('Volume', self.variable)
    @property
    def pint_uks(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.pint_uk)
        return cast('Volume', self.variable)
    @property
    def pint_us_dry(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.pint_us_dry)
        return cast('Volume', self.variable)
    @property
    def pint_us_liquids(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.pint_us_liquid)
        return cast('Volume', self.variable)
    @property
    def quart_us_dry(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.quart_us_dry)
        return cast('Volume', self.variable)
    @property
    def stéres(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.stére)
        return cast('Volume', self.variable)
    @property
    def tablespoon_metrics(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.tablespoon_metric)
        return cast('Volume', self.variable)
    @property
    def tablespoon_us(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.tablespoon_us)
        return cast('Volume', self.variable)
    @property
    def teaspoon_us(self) -> 'Volume':
        self.variable.quantity = FastQuantity(self.value, VolumeUnits.teaspoon_us)
        return cast('Volume', self.variable)
    
    # Short aliases for convenience
    pass


class Volume(TypedVariable):
    """Type-safe volume variable with expression capabilities."""
    
    _setter_class = VolumeSetter
    _expected_dimension = VOLUME
    _default_unit_property = "cubic_meters"
    
    def set(self, value: float) -> VolumeSetter:
        """Create a volume setter for this variable with proper type annotation."""
        return VolumeSetter(self, value)


class VolumeModule(VariableModule):
    """Volume variable module definition."""
    
    def get_variable_class(self):
        return Volume
    
    def get_setter_class(self):
        return VolumeSetter
    
    def get_expected_dimension(self):
        return VOLUME


# Register this module for auto-discovery
VARIABLE_MODULE = VolumeModule()