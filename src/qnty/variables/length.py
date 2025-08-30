"""
Length Variable Module
=======================

Type-safe length variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import LENGTH
from ..units import LengthUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class LengthSetter(TypeSafeSetter):
    """Length-specific setter with only length units."""
    
    def __init__(self, variable: 'Length', value: float):
        super().__init__(variable, value)
    
    # Only length units available - compile-time safe!
    @property
    def ångströms(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.ångström)
        return cast('Length', self.variable)
    @property
    def arpent_quebecs(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.arpent_quebec)
        return cast('Length', self.variable)
    @property
    def astronomic_units(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.astronomic_unit)
        return cast('Length', self.variable)
    @property
    def attometers(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.attometer)
        return cast('Length', self.variable)
    @property
    def calibre_centinchs(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.calibre_centinch)
        return cast('Length', self.variable)
    @property
    def centimeters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.centimeter)
        return cast('Length', self.variable)
    @property
    def chain_engrs(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.chain_engrs)
        return cast('Length', self.variable)
    @property
    def chain_gunters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.chain_gunters)
        return cast('Length', self.variable)
    @property
    def chain_surveyors(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.chain_surveyors)
        return cast('Length', self.variable)
    @property
    def cubit_uks(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.cubit_uk)
        return cast('Length', self.variable)
    @property
    def ells(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.ell)
        return cast('Length', self.variable)
    @property
    def fathoms(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.fathom)
        return cast('Length', self.variable)
    @property
    def femtometres(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.femtometre)
        return cast('Length', self.variable)
    @property
    def fermis(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.fermi)
        return cast('Length', self.variable)
    @property
    def foots(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.foot)
        return cast('Length', self.variable)
    @property
    def feet(self) -> 'Length':
        """Alias for foots property."""
        self.variable.quantity = FastQuantity(self.value, LengthUnits.foot)
        return cast('Length', self.variable)
    @property
    def furlong_uk_and_us(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.furlong_uk_and_us)
        return cast('Length', self.variable)
    @property
    def inchs(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.inch)
        return cast('Length', self.variable)
    @property
    def inches(self) -> 'Length':
        """Alias for inchs property."""
        self.variable.quantity = FastQuantity(self.value, LengthUnits.inch)
        return cast('Length', self.variable)
    @property
    def kilometers(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.kilometer)
        return cast('Length', self.variable)
    @property
    def league_us_statutes(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.league_us_statute)
        return cast('Length', self.variable)
    @property
    def lieue_metrics(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.lieue_metric)
        return cast('Length', self.variable)
    @property
    def ligne_metrics(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.ligne_metric)
        return cast('Length', self.variable)
    @property
    def line_us(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.line_us)
        return cast('Length', self.variable)
    @property
    def link_surveyors(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.link_surveyors)
        return cast('Length', self.variable)
    @property
    def meters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.meter)
        return cast('Length', self.variable)
    @property
    def micrometers(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.micrometer)
        return cast('Length', self.variable)
    @property
    def microns(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.micron)
        return cast('Length', self.variable)
    @property
    def mils(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.mil)
        return cast('Length', self.variable)
    @property
    def mile_geographicals(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.mile_geographical)
        return cast('Length', self.variable)
    @property
    def mile_us_nauticals(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.mile_us_nautical)
        return cast('Length', self.variable)
    @property
    def mile_us_statutes(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.mile_us_statute)
        return cast('Length', self.variable)
    @property
    def mile_us_survey(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.mile_us_survey)
        return cast('Length', self.variable)
    @property
    def millimeters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.millimeter)
        return cast('Length', self.variable)
    @property
    def millimicrons(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.millimicron)
        return cast('Length', self.variable)
    @property
    def nanometers(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.nanometer)
        return cast('Length', self.variable)
    @property
    def parsecs(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.parsec)
        return cast('Length', self.variable)
    @property
    def perches(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.perche)
        return cast('Length', self.variable)
    @property
    def picas(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.pica)
        return cast('Length', self.variable)
    @property
    def picometers(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.picometer)
        return cast('Length', self.variable)
    @property
    def point_didots(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.point_didot)
        return cast('Length', self.variable)
    @property
    def point_us(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.point_us)
        return cast('Length', self.variable)
    @property
    def rods(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.rod)
        return cast('Length', self.variable)
    @property
    def spans(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.span)
        return cast('Length', self.variable)
    @property
    def thou_millinchs(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.thou_millinch)
        return cast('Length', self.variable)
    @property
    def toise_metrics(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.toise_metric)
        return cast('Length', self.variable)
    @property
    def yards(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.yard)
        return cast('Length', self.variable)
    
    # Short aliases for convenience
    pass


class Length(TypedVariable):
    """Type-safe length variable with expression capabilities."""
    
    _setter_class = LengthSetter
    _expected_dimension = LENGTH
    _default_unit_property = "meters"
    
    def set(self, value: float) -> LengthSetter:
        """Create a length setter for this variable with proper type annotation."""
        return LengthSetter(self, value)


class LengthModule(VariableModule):
    """Length variable module definition."""
    
    def get_variable_class(self):
        return Length
    
    def get_setter_class(self):
        return LengthSetter
    
    def get_expected_dimension(self):
        return LENGTH


# Register this module for auto-discovery
VARIABLE_MODULE = LengthModule()