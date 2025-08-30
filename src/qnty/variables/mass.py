"""
Mass Variable Module
=====================

Type-safe mass variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MASS
from ..units import MassUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MassSetter(TypeSafeSetter):
    """Mass-specific setter with only mass units."""
    
    def __init__(self, variable: 'Mass', value: float):
        super().__init__(variable, value)
    
    # Only mass units available - compile-time safe!
    @property
    def slugs(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.slug)
        return cast('Mass', self.variable)
    @property
    def atomic_mass_units(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.atomic_mass_unit)
        return cast('Mass', self.variable)
    @property
    def carat_metrics(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.carat_metric)
        return cast('Mass', self.variable)
    @property
    def centals(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.cental)
        return cast('Mass', self.variable)
    @property
    def centigrams(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.centigram)
        return cast('Mass', self.variable)
    @property
    def clove_uks(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.clove_uk)
        return cast('Mass', self.variable)
    @property
    def drachm_apothecary(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.drachm_apothecary)
        return cast('Mass', self.variable)
    @property
    def dram_avoirdupois(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.dram_avoirdupois)
        return cast('Mass', self.variable)
    @property
    def dram_troy(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.dram_troy)
        return cast('Mass', self.variable)
    @property
    def grains(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.grain)
        return cast('Mass', self.variable)
    @property
    def grams(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.gram)
        return cast('Mass', self.variable)
    @property
    def hundredweight_longs(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.hundredweight_long)
        return cast('Mass', self.variable)
    @property
    def hundredweight_shorts(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.hundredweight_short)
        return cast('Mass', self.variable)
    @property
    def kilograms(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.kilogram)
        return cast('Mass', self.variable)
    @property
    def kips(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.kip)
        return cast('Mass', self.variable)
    @property
    def micrograms(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.microgram)
        return cast('Mass', self.variable)
    @property
    def milligrams(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.milligram)
        return cast('Mass', self.variable)
    @property
    def ounce_apothecary(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.ounce_apothecary)
        return cast('Mass', self.variable)
    @property
    def ounce_avoirdupois(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.ounce_avoirdupois)
        return cast('Mass', self.variable)
    @property
    def ounce_troy(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.ounce_troy)
        return cast('Mass', self.variable)
    @property
    def pennyweight_troy(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.pennyweight_troy)
        return cast('Mass', self.variable)
    @property
    def pood_russias(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.pood_russia)
        return cast('Mass', self.variable)
    @property
    def pound_apothecary(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.pound_apothecary)
        return cast('Mass', self.variable)
    @property
    def pound_avoirdupois(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.pound_avoirdupois)
        return cast('Mass', self.variable)
    @property
    def pound_troy(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.pound_troy)
        return cast('Mass', self.variable)
    @property
    def pound_mass(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.pound_mass)
        return cast('Mass', self.variable)
    @property
    def quarter_uks(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.quarter_uk)
        return cast('Mass', self.variable)
    @property
    def quintal_metrics(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.quintal_metric)
        return cast('Mass', self.variable)
    @property
    def quital_us(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.quital_us)
        return cast('Mass', self.variable)
    @property
    def scruple_avoirdupois(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.scruple_avoirdupois)
        return cast('Mass', self.variable)
    @property
    def stone_uks(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.stone_uk)
        return cast('Mass', self.variable)
    @property
    def ton_metrics(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.ton_metric)
        return cast('Mass', self.variable)
    @property
    def ton_us_longs(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.ton_us_long)
        return cast('Mass', self.variable)
    @property
    def ton_us_shorts(self) -> 'Mass':
        self.variable.quantity = FastQuantity(self.value, MassUnits.ton_us_short)
        return cast('Mass', self.variable)
    
    # Short aliases for convenience
    pass


class Mass(TypedVariable):
    """Type-safe mass variable with expression capabilities."""
    
    _setter_class = MassSetter
    _expected_dimension = MASS
    _default_unit_property = "kilograms"
    
    def set(self, value: float) -> MassSetter:
        """Create a mass setter for this variable with proper type annotation."""
        return MassSetter(self, value)


class MassModule(VariableModule):
    """Mass variable module definition."""
    
    def get_variable_class(self):
        return Mass
    
    def get_setter_class(self):
        return MassSetter
    
    def get_expected_dimension(self):
        return MASS


# Register this module for auto-discovery
VARIABLE_MODULE = MassModule()