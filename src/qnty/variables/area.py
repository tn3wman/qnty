"""
Area Variable Module
=====================

Type-safe area variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import AREA
from ..units import AreaUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AreaSetter(TypeSafeSetter):
    """Area-specific setter with only area units."""
    
    def __init__(self, variable: 'Area', value: float):
        super().__init__(variable, value)
    
    # Only area units available - compile-time safe!
    @property
    def acre_generals(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.acre_general)
        return cast('Area', self.variable)
    @property
    def ares(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.are)
        return cast('Area', self.variable)
    @property
    def arpent_quebecs(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.arpent_quebec)
        return cast('Area', self.variable)
    @property
    def barns(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.barn)
        return cast('Area', self.variable)
    @property
    def circular_inchs(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.circular_inch)
        return cast('Area', self.variable)
    @property
    def circular_mils(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.circular_mil)
        return cast('Area', self.variable)
    @property
    def hectares(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.hectare)
        return cast('Area', self.variable)
    @property
    def sheds(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.shed)
        return cast('Area', self.variable)
    @property
    def square_centimeters(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_centimeter)
        return cast('Area', self.variable)
    @property
    def square_chain_ramsdens(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_chain_ramsden)
        return cast('Area', self.variable)
    @property
    def square_chain_survey_gunters(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_chain_survey_gunters)
        return cast('Area', self.variable)
    @property
    def square_decimeters(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_decimeter)
        return cast('Area', self.variable)
    @property
    def square_fermis(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_fermi)
        return cast('Area', self.variable)
    @property
    def square_foots(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_foot)
        return cast('Area', self.variable)
    @property
    def square_hectometers(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_hectometer)
        return cast('Area', self.variable)
    @property
    def square_inchs(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_inch)
        return cast('Area', self.variable)
    @property
    def square_kilometers(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_kilometer)
        return cast('Area', self.variable)
    @property
    def square_league_statutes(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_league_statute)
        return cast('Area', self.variable)
    @property
    def square_meters(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_meter)
        return cast('Area', self.variable)
    @property
    def square_microns(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_micron)
        return cast('Area', self.variable)
    @property
    def square_mile_statutes(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_mile_statute)
        return cast('Area', self.variable)
    @property
    def square_mile_us_survey(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_mile_us_survey)
        return cast('Area', self.variable)
    @property
    def square_millimeters(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_millimeter)
        return cast('Area', self.variable)
    @property
    def square_nanometers(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_nanometer)
        return cast('Area', self.variable)
    @property
    def square_yards(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.square_yard)
        return cast('Area', self.variable)
    @property
    def township_us(self) -> 'Area':
        self.variable.quantity = FastQuantity(self.value, AreaUnits.township_us)
        return cast('Area', self.variable)
    
    # Short aliases for convenience
    pass


class Area(TypedVariable):
    """Type-safe area variable with expression capabilities."""
    
    _setter_class = AreaSetter
    _expected_dimension = AREA
    _default_unit_property = "square_meters"
    
    def set(self, value: float) -> AreaSetter:
        """Create a area setter for this variable with proper type annotation."""
        return AreaSetter(self, value)


class AreaModule(VariableModule):
    """Area variable module definition."""
    
    def get_variable_class(self):
        return Area
    
    def get_setter_class(self):
        return AreaSetter
    
    def get_expected_dimension(self):
        return AREA


# Register this module for auto-discovery
VARIABLE_MODULE = AreaModule()