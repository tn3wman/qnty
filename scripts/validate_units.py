#!/usr/bin/env python3
"""
Unit Validation Script
======================

This script validates all units in the qnty library by comparing their conversion factors
with equivalent units in external libraries (Pint, unyt, astropy.units).

It checks:
1. SI conversion factors match between libraries
2. Unit definitions are consistent
3. Identifies units that couldn't be matched in external libraries

Results are saved to validation reports for review.
"""

import os
import sys
import json
import importlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import traceback

# Add src to path
sys.path.insert(0, 'src')

@dataclass
class UnitComparison:
    """Represents a comparison between qnty unit and external library units."""
    qnty_name: str
    qnty_si_factor: float
    qnty_dimension: str
    pint_name: Optional[str] = None
    pint_si_factor: Optional[float] = None
    pint_match: bool = False
    unyt_name: Optional[str] = None
    unyt_si_factor: Optional[float] = None
    unyt_match: bool = False
    astropy_name: Optional[str] = None
    astropy_si_factor: Optional[float] = None
    astropy_match: bool = False
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []

@dataclass
class ValidationReport:
    """Summary report of unit validation."""
    total_units: int = 0
    matched_in_pint: int = 0
    matched_in_unyt: int = 0  
    matched_in_astropy: int = 0
    matched_in_any: int = 0
    conversion_mismatches: int = 0
    unmatched_units: List[str] = None
    
    def __post_init__(self):
        if self.unmatched_units is None:
            self.unmatched_units = []

class UnitValidator:
    """Main validator class for comparing qnty units with external libraries."""
    
    def __init__(self):
        self.pint = None
        self.unyt = None
        self.astropy_units = None
        self.comparisons: List[UnitComparison] = []
        self.report = ValidationReport()
        
        # Common unit name mappings between libraries
        self.name_mappings = {
            # Length units - comprehensive mappings
            'meter': ['m', 'meter', 'metre'],
            'meters': ['m', 'meter', 'metre'],
            'millimeter': ['mm', 'millimeter', 'millimetre'],
            'millimeters': ['mm', 'millimeter', 'millimetre'], 
            'centimeter': ['cm', 'centimeter', 'centimetre'],
            'centimeters': ['cm', 'centimeter', 'centimetre'],
            'kilometer': ['km', 'kilometer', 'kilometre'],
            'kilometers': ['km', 'kilometer', 'kilometre'],
            'inch': ['in', 'inch'],
            'inchs': ['in', 'inch'],
            'inches': ['in', 'inch'],
            'foot': ['ft', 'foot'],
            'foots': ['ft', 'foot'],
            'feet': ['ft', 'foot'],
            'yard': ['yd', 'yard'],
            'yards': ['yd', 'yard'],
            'mile_us_statute': ['mi', 'mile'],
            'miles_us_statute': ['mi', 'mile'],
            'ångström': ['angstrom', 'Angstrom', 'AA'],
            'ångströms': ['angstrom', 'Angstrom', 'AA'],
            'nanometer': ['nm', 'nanometer', 'nanometre'],
            'nanometers': ['nm', 'nanometer', 'nanometre'],
            'micrometer': ['um', 'micrometer', 'micrometre', 'micron'],
            'micrometers': ['um', 'micrometer', 'micrometre', 'micron'],
            'picometer': ['pm', 'picometer', 'picometre'],
            'picometers': ['pm', 'picometer', 'picometre'],
            'femtometer': ['fm', 'femtometer', 'femtometre'],
            'femtometers': ['fm', 'femtometer', 'femtometre'],
            'attometer': ['am', 'attometer', 'attometre'],
            'attometers': ['am', 'attometer', 'attometre'],
            
            # Mass units
            'kilogram': ['kg', 'kilogram'],
            'kilograms': ['kg', 'kilogram'],
            'gram': ['g', 'gram'],
            'grams': ['g', 'gram'],
            'milligram': ['mg', 'milligram'],
            'milligrams': ['mg', 'milligram'],
            'microgram': ['ug', 'microgram'],
            'micrograms': ['ug', 'microgram'],
            'pound': ['lb', 'pound', 'lbm'],
            'pounds': ['lb', 'pound', 'lbm'],
            'ounce': ['oz', 'ounce'],
            'ounces': ['oz', 'ounce'],
            'ton_metric': ['t', 'tonne', 'metric_ton'],
            'slug': ['slug'],
            
            # Time units  
            'second': ['s', 'sec', 'second'],
            'seconds': ['s', 'sec', 'second'],
            'minute': ['min', 'minute'],
            'minutes': ['min', 'minute'],
            'hour': ['h', 'hr', 'hour'],
            'hours': ['h', 'hr', 'hour'],
            'day': ['d', 'day'],
            'days': ['d', 'day'],
            'year': ['a', 'yr', 'year', 'annum'],
            'years': ['a', 'yr', 'year', 'annum'],
            
            # Area units
            'square_meter': ['m**2', 'm^2', 'meter**2'],
            'square_meters': ['m**2', 'm^2', 'meter**2'],
            'square_centimeter': ['cm**2', 'cm^2', 'centimeter**2'],
            'square_centimeters': ['cm**2', 'cm^2', 'centimeter**2'],
            'square_kilometer': ['km**2', 'km^2', 'kilometer**2'],
            'square_kilometers': ['km**2', 'km^2', 'kilometer**2'],
            'square_inch': ['in**2', 'in^2', 'inch**2'],
            'square_inches': ['in**2', 'in^2', 'inch**2'],
            'square_foot': ['ft**2', 'ft^2', 'foot**2'],
            'square_feet': ['ft**2', 'ft^2', 'foot**2'],
            'hectare': ['ha', 'hectare'],
            'hectares': ['ha', 'hectare'],
            'acre': ['ac', 'acre'],
            'acres': ['ac', 'acre'],
            
            # Volume units
            'cubic_meter': ['m**3', 'm^3', 'meter**3'],
            'cubic_meters': ['m**3', 'm^3', 'meter**3'],
            'liter': ['l', 'L', 'liter', 'litre'],
            'liters': ['l', 'L', 'liter', 'litre'],
            'milliliter': ['ml', 'mL', 'milliliter', 'millilitre'],
            'milliliters': ['ml', 'mL', 'milliliter', 'millilitre'],
            'cubic_centimeter': ['cm**3', 'cm^3', 'cc'],
            'cubic_centimeters': ['cm**3', 'cm^3', 'cc'],
            'gallon_us_liquid': ['gal', 'gallon'],
            'gallon_imperial_uk': ['imperial_gallon', 'UK_gallon'],
            
            # Pressure units
            'pascal': ['Pa', 'pascal'],
            'pascals': ['Pa', 'pascal'],
            'bar': ['bar'],
            'bars': ['bar'],
            'atmosphere_standard': ['atm', 'atmosphere'],
            'atmosphere_standards': ['atm', 'atmosphere'],
            'psi': ['psi', 'pound_force_per_square_inch'],
            'torr': ['torr', 'mmHg'],
            'torrs': ['torr', 'mmHg'],
            'hectopascal': ['hPa', 'hectopascal'],
            'hectopascals': ['hPa', 'hectopascal'],
            'kilopascal': ['kPa', 'kilopascal'],
            'kilopascals': ['kPa', 'kilopascal'],
            'megapascal': ['MPa', 'megapascal'],
            'megapascals': ['MPa', 'megapascal'],
            'gigapascal': ['GPa', 'gigapascal'],
            'gigapascals': ['GPa', 'gigapascal'],
            
            # Energy units
            'joule': ['J', 'joule'],
            'joules': ['J', 'joule'],
            'kilojoule': ['kJ', 'kilojoule'],
            'kilojoules': ['kJ', 'kilojoule'],
            'megajoule': ['MJ', 'megajoule'],
            'megajoules': ['MJ', 'megajoule'],
            'calorie': ['cal', 'calorie'],
            'calories': ['cal', 'calorie'],
            'kilocalorie': ['kcal', 'kilocalorie', 'Cal'],
            'kilocalories': ['kcal', 'kilocalorie', 'Cal'],
            'erg': ['erg'],
            'ergs': ['erg'],
            'electron_volt': ['eV', 'electronvolt'],
            'electron_volts': ['eV', 'electronvolt'],
            'btu': ['Btu', 'BTU', 'british_thermal_unit'],
            'kilowatt_hour': ['kWh', 'kilowatt_hour'],
            'kilowatt_hours': ['kWh', 'kilowatt_hour'],
            
            # Power units
            'watt': ['W', 'watt'],
            'watts': ['W', 'watt'],
            'kilowatt': ['kW', 'kilowatt'],
            'kilowatts': ['kW', 'kilowatt'],
            'megawatt': ['MW', 'megawatt'],
            'megawatts': ['MW', 'megawatt'],
            'horsepower': ['hp', 'horsepower'],
            'horsepowers': ['hp', 'horsepower'],
            
            # Temperature units
            'kelvin': ['K', 'kelvin'],
            'kelvins': ['K', 'kelvin'],
            'celsius': ['degC', 'deg_C', 'celsius'],
            'fahrenheit': ['degF', 'deg_F', 'fahrenheit'],
            'rankine': ['degR', 'deg_R', 'rankine'],
            
            # Electric units
            'ampere': ['A', 'amp', 'ampere'],
            'amperes': ['A', 'amp', 'ampere'],
            'volt': ['V', 'volt'],
            'volts': ['V', 'volt'],
            'ohm': ['ohm', 'Ohm'],
            'ohms': ['ohm', 'Ohm'],
            'farad': ['F', 'farad'],
            'farads': ['F', 'farad'],
            'henry': ['H', 'henry'],
            'henrys': ['H', 'henry'],
            'weber': ['Wb', 'weber'],
            'webers': ['Wb', 'weber'],
            'tesla': ['T', 'tesla'],
            'teslas': ['T', 'tesla'],
            'coulomb': ['C', 'coulomb'],
            'coulombs': ['C', 'coulomb'],
            'siemens': ['S', 'siemens'],
            
            # Force units
            'newton': ['N', 'newton'],
            'newtons': ['N', 'newton'],
            'kilonewton': ['kN', 'kilonewton'],
            'kilonewtons': ['kN', 'kilonewton'],
            'dyne': ['dyn', 'dyne'],
            'dynes': ['dyn', 'dyne'],
            'pound_force': ['lbf', 'pound_force'],
            'kilogram_force': ['kgf', 'kilogram_force'],
            
            # Frequency units
            'hertz': ['Hz', 'hertz'],
            'kilohertz': ['kHz', 'kilohertz'],
            'megahertz': ['MHz', 'megahertz'],
            'gigahertz': ['GHz', 'gigahertz'],
            
            # Velocity units
            'meter_per_second': ['m/s', 'meter/second'],
            'meters_per_second': ['m/s', 'meter/second'],
            'kilometer_per_hour': ['km/h', 'km/hr', 'kph'],
            'kilometers_per_hour': ['km/h', 'km/hr', 'kph'],
            'mile_per_hour': ['mph', 'mi/h', 'mile/hour'],
            'miles_per_hour': ['mph', 'mi/h', 'mile/hour'],
            'foot_per_second': ['ft/s', 'foot/second', 'fps'],
            'feet_per_second': ['ft/s', 'foot/second', 'fps'],
            
            # Angular units
            'radian': ['rad', 'radian'],
            'radians': ['rad', 'radian'],
            'degree': ['deg', 'degree'],
            'degrees': ['deg', 'degree'],
            'steradian': ['sr', 'steradian'],
            'steradians': ['sr', 'steradian'],
            
            # Luminous units
            'candela': ['cd', 'candela'],
            'candelas': ['cd', 'candela'],
            'lumen': ['lm', 'lumen'],
            'lumens': ['lm', 'lumen'],
            'lux': ['lx', 'lux'],
            
            # Amount of substance
            'mole': ['mol', 'mole'],
            'moles': ['mol', 'mole'],
            'kilomole': ['kmol', 'kilomole'],
            'kilomoles': ['kmol', 'kilomole'],
            
            # Special/dimensionless
            'dimensionless': ['dimensionless', 'unitless', '1'],
            'percent': ['%', 'percent'],
            'ppm': ['ppm', 'parts_per_million'],
            'ppb': ['ppb', 'parts_per_billion'],
        }
        
    def setup_external_libraries(self):
        """Import and setup external unit libraries."""
        print("Setting up external libraries...")
        
        # Setup Pint
        try:
            import pint
            self.pint = pint.UnitRegistry()
            print("  ✅ Pint loaded")
        except ImportError:
            print("  ⚠️  Pint not available")
            print("     Install with: pip install pint")
        
        # Setup unyt  
        try:
            import unyt
            self.unyt = unyt
            print("  ✅ unyt loaded")
        except ImportError:
            print("  ⚠️  unyt not available")
            print("     Install with: pip install unyt")
            
        # Setup astropy.units
        try:
            import astropy.units as u
            self.astropy_units = u
            print("  ✅ astropy.units loaded")
        except ImportError:
            print("  ⚠️  astropy.units not available")
            print("     Install with: pip install astropy")
    
    def find_all_qnty_units(self) -> Dict[str, List[Tuple[str, Any]]]:
        """Find all units defined in qnty library."""
        print("\nDiscovering qnty units...")
        
        units_classes = {}
        units_dir = Path('src/qnty/units')
        
        # Import main units module first
        try:
            main_units = importlib.import_module('qnty.units')
            for attr_name in dir(main_units):
                if attr_name.endswith('Units') and not attr_name.startswith('_'):
                    units_class = getattr(main_units, attr_name)
                    units_classes[attr_name] = self.extract_units_from_class(units_class)
                    print(f"  Found {len(units_classes[attr_name])} units in {attr_name}")
        except Exception as e:
            print(f"  ❌ Error importing main units module: {e}")
        
        print(f"  Total: {sum(len(units) for units in units_classes.values())} units across {len(units_classes)} classes")
        return units_classes
    
    def extract_units_from_class(self, units_class) -> List[Tuple[str, Any]]:
        """Extract all unit constants from a units class."""
        units = []
        for attr_name in dir(units_class):
            if not attr_name.startswith('_'):
                try:
                    unit = getattr(units_class, attr_name)
                    if hasattr(unit, 'si_factor'):
                        units.append((attr_name, unit))
                except Exception:
                    continue
        return units
    
    def get_possible_names(self, qnty_name: str) -> List[str]:
        """Get possible names for a unit in external libraries."""
        # Check direct mapping
        if qnty_name in self.name_mappings:
            return self.name_mappings[qnty_name]
        
        # Generate variations
        variations = [qnty_name]
        
        # Remove common suffixes/prefixes
        clean_name = qnty_name.replace('_', '').replace('-', '')
        if clean_name != qnty_name:
            variations.append(clean_name)
            
        # Add underscored version
        if '_' not in qnty_name and len(qnty_name) > 4:
            # Try to split camelCase
            import re
            split_name = re.sub('([a-z])([A-Z])', r'\1_\2', qnty_name).lower()
            if split_name != qnty_name:
                variations.append(split_name)
        
        # Add common abbreviations
        abbrev_map = {
            'meter': 'm', 'metre': 'm',
            'gram': 'g', 
            'second': 's', 'sec': 's',
            'pascal': 'Pa',
            'joule': 'J',
            'watt': 'W',
            'ampere': 'A', 'amp': 'A',
            'volt': 'V',
            'kelvin': 'K'
        }
        
        for full, abbrev in abbrev_map.items():
            if full in qnty_name:
                variations.append(qnty_name.replace(full, abbrev))
        
        return list(set(variations))  # Remove duplicates
    
    def compare_with_pint(self, qnty_name: str, qnty_unit: Any) -> Tuple[Optional[str], Optional[float], bool]:
        """Compare qnty unit with Pint equivalent."""
        if not self.pint:
            return None, None, False
            
        possible_names = self.get_possible_names(qnty_name)
        
        for name in possible_names:
            try:
                # Try to get the unit from Pint
                pint_unit = self.pint.parse_expression(name)
                
                # Convert to base units to get SI factor
                base_unit = pint_unit.to_base_units()
                pint_si_factor = base_unit.magnitude
                
                # Compare with tolerance for floating point precision
                tolerance = 1e-10
                matches = abs(qnty_unit.si_factor - pint_si_factor) < tolerance
                
                if matches or pint_si_factor is not None:
                    return name, pint_si_factor, matches
                    
            except Exception:
                continue
                
        return None, None, False
    
    def compare_with_unyt(self, qnty_name: str, qnty_unit: Any) -> Tuple[Optional[str], Optional[float], bool]:
        """Compare qnty unit with unyt equivalent."""
        if not self.unyt:
            return None, None, False
            
        possible_names = self.get_possible_names(qnty_name)
        
        for name in possible_names:
            try:
                # Try different ways to access unyt units
                unyt_unit = None
                
                # Method 1: Direct attribute access
                if hasattr(self.unyt, name):
                    unyt_unit = getattr(self.unyt, name)
                
                # Method 2: Try from unyt_array directly
                if unyt_unit is None:
                    try:
                        test_array = self.unyt.unyt_array(1.0, name)
                        unyt_unit = test_array.units
                    except:
                        pass
                
                # Method 3: Try Unit constructor
                if unyt_unit is None:
                    try:
                        unyt_unit = self.unyt.Unit(name)
                    except:
                        pass
                
                # Method 4: Try parsing with unyt_quantity
                if unyt_unit is None:
                    try:
                        test_qty = self.unyt.unyt_quantity(1.0, name)
                        unyt_unit = test_qty.units
                    except:
                        pass
                
                if unyt_unit is not None:
                    # Get SI conversion factor - unyt stores this in different ways
                    unyt_si_factor = None
                    
                    # Try to get base equivalent
                    try:
                        if hasattr(unyt_unit, 'get_base_equivalent'):
                            base_equiv = unyt_unit.get_base_equivalent()
                            if isinstance(base_equiv, tuple) and len(base_equiv) > 1:
                                unyt_si_factor = float(base_equiv[1])
                            else:
                                unyt_si_factor = float(base_equiv)
                        elif hasattr(unyt_unit, 'base_value'):
                            unyt_si_factor = float(unyt_unit.base_value)
                        elif hasattr(unyt_unit, 'get_conversion_factor'):
                            # Get conversion factor to SI base
                            unyt_si_factor = float(unyt_unit.get_conversion_factor(self.unyt.Unit("1")))
                        else:
                            # Fallback: create a test quantity and convert to base
                            test_qty = 1.0 * unyt_unit
                            if hasattr(test_qty, 'to_base'):
                                base_qty = test_qty.to_base()
                                unyt_si_factor = float(base_qty.value)
                            elif hasattr(test_qty, 'in_base'):
                                base_qty = test_qty.in_base()
                                unyt_si_factor = float(base_qty.value)
                    except Exception as e:
                        continue
                    
                    if unyt_si_factor is not None:
                        # Compare with tolerance
                        tolerance = 1e-10
                        matches = abs(qnty_unit.si_factor - unyt_si_factor) < tolerance
                        return name, unyt_si_factor, matches
                        
            except Exception:
                continue
                
        return None, None, False
    
    def compare_with_astropy(self, qnty_name: str, qnty_unit: Any) -> Tuple[Optional[str], Optional[float], bool]:
        """Compare qnty unit with astropy.units equivalent."""
        if not self.astropy_units:
            return None, None, False
            
        possible_names = self.get_possible_names(qnty_name)
        
        for name in possible_names:
            try:
                # Try different ways to access astropy units
                astropy_unit = None
                
                # Method 1: Direct attribute access
                if hasattr(self.astropy_units, name):
                    astropy_unit = getattr(self.astropy_units, name)
                
                # Method 2: Try Unit constructor  
                if astropy_unit is None:
                    try:
                        astropy_unit = self.astropy_units.Unit(name)
                    except:
                        pass
                
                # Method 3: Try common sub-modules
                if astropy_unit is None:
                    sub_modules = ['si', 'cgs', 'imperial', 'astrophys']
                    for sub_mod in sub_modules:
                        if hasattr(self.astropy_units, sub_mod):
                            sub_module = getattr(self.astropy_units, sub_mod)
                            if hasattr(sub_module, name):
                                astropy_unit = getattr(sub_module, name)
                                break
                
                # Method 4: Try parsing string expressions
                if astropy_unit is None:
                    try:
                        # Some units might need to be parsed as expressions
                        test_variations = [name, name.replace('_', ' '), name.replace('_', '')]
                        for variation in test_variations:
                            try:
                                astropy_unit = self.astropy_units.Unit(variation)
                                break
                            except:
                                continue
                    except:
                        pass
                
                if astropy_unit is not None:
                    # Get SI conversion factor - astropy has several methods
                    astropy_si_factor = None
                    
                    try:
                        # Method 1: Use scale property (direct scale to SI)
                        if hasattr(astropy_unit, 'scale'):
                            astropy_si_factor = float(astropy_unit.scale)
                        
                        # Method 2: Use to() method to convert to SI
                        elif hasattr(astropy_unit, 'to'):
                            # Try to find corresponding SI unit
                            si_candidates = []
                            if hasattr(astropy_unit, 'physical_type'):
                                # Try to get SI unit for this physical type
                                try:
                                    si_unit = astropy_unit.decompose()  # Decompose to basic SI
                                    if si_unit != astropy_unit:
                                        conversion = astropy_unit.to(si_unit)
                                        if hasattr(conversion, 'scale'):
                                            astropy_si_factor = float(conversion.scale)
                                except:
                                    pass
                        
                        # Method 3: Create quantity and convert to SI
                        if astropy_si_factor is None:
                            try:
                                test_qty = 1.0 * astropy_unit
                                si_qty = test_qty.si
                                astropy_si_factor = float(si_qty.value)
                            except:
                                pass
                        
                        # Method 4: Use decompose to get scale
                        if astropy_si_factor is None:
                            try:
                                decomposed = astropy_unit.decompose()
                                if hasattr(decomposed, 'scale'):
                                    astropy_si_factor = float(decomposed.scale)
                            except:
                                pass
                    
                    except Exception:
                        continue
                    
                    if astropy_si_factor is not None:
                        # Compare with tolerance
                        tolerance = 1e-10
                        matches = abs(qnty_unit.si_factor - astropy_si_factor) < tolerance
                        return name, astropy_si_factor, matches
                        
            except Exception:
                continue
                
        return None, None, False
    
    def validate_unit(self, qnty_name: str, qnty_unit: Any) -> UnitComparison:
        """Validate a single qnty unit against external libraries."""
        comparison = UnitComparison(
            qnty_name=qnty_name,
            qnty_si_factor=qnty_unit.si_factor,
            qnty_dimension=str(qnty_unit.dimension_signature) if hasattr(qnty_unit, 'dimension_signature') else 'unknown'
        )
        
        # Compare with Pint
        try:
            pint_name, pint_si_factor, pint_match = self.compare_with_pint(qnty_name, qnty_unit)
            comparison.pint_name = pint_name
            comparison.pint_si_factor = pint_si_factor
            comparison.pint_match = pint_match
        except Exception as e:
            comparison.errors.append(f"Pint error: {e}")
        
        # Compare with unyt
        try:
            unyt_name, unyt_si_factor, unyt_match = self.compare_with_unyt(qnty_name, qnty_unit)
            comparison.unyt_name = unyt_name
            comparison.unyt_si_factor = unyt_si_factor
            comparison.unyt_match = unyt_match
        except Exception as e:
            comparison.errors.append(f"unyt error: {e}")
        
        # Compare with astropy
        try:
            astropy_name, astropy_si_factor, astropy_match = self.compare_with_astropy(qnty_name, qnty_unit)
            comparison.astropy_name = astropy_name
            comparison.astropy_si_factor = astropy_si_factor
            comparison.astropy_match = astropy_match
        except Exception as e:
            comparison.errors.append(f"astropy error: {e}")
        
        return comparison
    
    def run_validation(self):
        """Run complete validation of all qnty units."""
        print("🔍 Starting unit validation...\n")
        
        # Setup external libraries
        self.setup_external_libraries()
        
        # Find all qnty units
        units_classes = self.find_all_qnty_units()
        
        # Validate each unit
        print("\nValidating units...")
        total_units = 0
        
        for class_name, units in units_classes.items():
            print(f"\n📊 Validating {class_name}...")
            
            for unit_name, unit_obj in units:
                total_units += 1
                comparison = self.validate_unit(unit_name, unit_obj)
                self.comparisons.append(comparison)
                
                # Print progress for important matches/mismatches
                status_symbols = []
                if comparison.pint_match:
                    status_symbols.append("P✅")
                elif comparison.pint_name:
                    status_symbols.append("P❌")
                else:
                    status_symbols.append("P❓")
                    
                if comparison.unyt_match:
                    status_symbols.append("U✅")
                elif comparison.unyt_name:
                    status_symbols.append("U❌")
                else:
                    status_symbols.append("U❓")
                    
                if comparison.astropy_match:
                    status_symbols.append("A✅")
                elif comparison.astropy_name:
                    status_symbols.append("A❌")
                else:
                    status_symbols.append("A❓")
                
                # Only print detailed progress for units with matches or mismatches
                if any(symbol.endswith('✅') or symbol.endswith('❌') for symbol in status_symbols):
                    print(f"    {' '.join(status_symbols)} {unit_name}")
        
        # Generate summary report
        self.generate_report()
        
        print(f"\n🎯 Validation Complete!")
        print(f"   Total units: {self.report.total_units}")
        print(f"   Matched in Pint: {self.report.matched_in_pint}")
        print(f"   Matched in unyt: {self.report.matched_in_unyt}")
        print(f"   Matched in astropy: {self.report.matched_in_astropy}")
        print(f"   Matched in any library: {self.report.matched_in_any}")
        print(f"   Conversion mismatches: {self.report.conversion_mismatches}")
        print(f"   Completely unmatched: {len(self.report.unmatched_units)}")
    
    def generate_report(self):
        """Generate summary report and detailed results."""
        self.report.total_units = len(self.comparisons)
        
        for comp in self.comparisons:
            if comp.pint_match:
                self.report.matched_in_pint += 1
            if comp.unyt_match:
                self.report.matched_in_unyt += 1
            if comp.astropy_match:
                self.report.matched_in_astropy += 1
            
            # Check if matched in any library
            if comp.pint_match or comp.unyt_match or comp.astropy_match:
                self.report.matched_in_any += 1
            
            # Check for conversion mismatches (found but wrong conversion)
            has_mismatch = False
            if comp.pint_name and not comp.pint_match:
                has_mismatch = True
            if comp.unyt_name and not comp.unyt_match:
                has_mismatch = True
            if comp.astropy_name and not comp.astropy_match:
                has_mismatch = True
            
            if has_mismatch:
                self.report.conversion_mismatches += 1
            
            # Check if completely unmatched
            if not comp.pint_name and not comp.unyt_name and not comp.astropy_name:
                self.report.unmatched_units.append(comp.qnty_name)
    
    def save_results(self):
        """Save detailed results to JSON files."""
        print("\n💾 Saving results...")
        
        # Save detailed comparisons
        comparisons_data = [asdict(comp) for comp in self.comparisons]
        with open('unit_validation_detailed.json', 'w') as f:
            json.dump(comparisons_data, f, indent=2)
        print("  📄 Detailed results: unit_validation_detailed.json")
        
        # Save summary report
        with open('unit_validation_summary.json', 'w') as f:
            json.dump(asdict(self.report), f, indent=2)
        print("  📄 Summary report: unit_validation_summary.json")
        
        # Separate unmatched units from validation mismatches
        completely_unmatched = []
        validation_mismatches = []
        
        for comp in self.comparisons:
            # Check if completely unmatched (not found in any library)
            if not comp.pint_name and not comp.unyt_name and not comp.astropy_name:
                completely_unmatched.append(comp)
            # Check if found but has validation mismatches
            elif ((comp.pint_name and not comp.pint_match) or 
                  (comp.unyt_name and not comp.unyt_match) or 
                  (comp.astropy_name and not comp.astropy_match)):
                validation_mismatches.append(comp)
        
        # Save completely unmatched units
        with open('unmatched_units.txt', 'w') as f:
            f.write("Units NOT FOUND in any external library (Pint, unyt, astropy.units):\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total: {len(completely_unmatched)} units\n\n")
            for comp in sorted(completely_unmatched, key=lambda x: x.qnty_name):
                f.write(f"{comp.qnty_name}\n")
                f.write(f"  qnty SI factor: {comp.qnty_si_factor}\n")
                f.write(f"  qnty dimension: {comp.qnty_dimension}\n")
                if comp.errors:
                    f.write(f"  errors: {', '.join(comp.errors)}\n")
                f.write("\n")
        print(f"  📄 Completely unmatched units ({len(completely_unmatched)}): unmatched_units.txt")
        
        # Save validation mismatches
        with open('validation_mismatches.txt', 'w') as f:
            f.write("Units FOUND but with INCORRECT conversion factors:\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total: {len(validation_mismatches)} units\n\n")
            for comp in sorted(validation_mismatches, key=lambda x: x.qnty_name):
                f.write(f"Unit: {comp.qnty_name}\n")
                f.write(f"  qnty SI factor: {comp.qnty_si_factor}\n")
                f.write(f"  qnty dimension: {comp.qnty_dimension}\n")
                
                if comp.pint_name:
                    status = "✅ MATCH" if comp.pint_match else "❌ MISMATCH"
                    f.write(f"  Pint '{comp.pint_name}': {comp.pint_si_factor} {status}\n")
                    if not comp.pint_match and comp.pint_si_factor is not None:
                        ratio = comp.qnty_si_factor / comp.pint_si_factor if comp.pint_si_factor != 0 else float('inf')
                        f.write(f"    Ratio (qnty/pint): {ratio:.2e}\n")
                        
                if comp.unyt_name:
                    status = "✅ MATCH" if comp.unyt_match else "❌ MISMATCH"
                    f.write(f"  unyt '{comp.unyt_name}': {comp.unyt_si_factor} {status}\n")
                    if not comp.unyt_match and comp.unyt_si_factor is not None:
                        ratio = comp.qnty_si_factor / comp.unyt_si_factor if comp.unyt_si_factor != 0 else float('inf')
                        f.write(f"    Ratio (qnty/unyt): {ratio:.2e}\n")
                        
                if comp.astropy_name:
                    status = "✅ MATCH" if comp.astropy_match else "❌ MISMATCH"
                    f.write(f"  astropy '{comp.astropy_name}': {comp.astropy_si_factor} {status}\n")
                    if not comp.astropy_match and comp.astropy_si_factor is not None:
                        ratio = comp.qnty_si_factor / comp.astropy_si_factor if comp.astropy_si_factor != 0 else float('inf')
                        f.write(f"    Ratio (qnty/astropy): {ratio:.2e}\n")
                        
                if comp.errors:
                    f.write(f"  errors: {', '.join(comp.errors)}\n")
                f.write("\n")
        print(f"  📄 Validation mismatches ({len(validation_mismatches)}): validation_mismatches.txt")
        
        # Also keep the old conversion_mismatches.txt for backward compatibility
        with open('conversion_mismatches.txt', 'w') as f:
            f.write("Units with conversion factor mismatches (LEGACY FILE - see validation_mismatches.txt):\n")
            f.write("=" * 80 + "\n\n")
            for comp in validation_mismatches:
                f.write(f"Unit: {comp.qnty_name}\n")
                f.write(f"  qnty SI factor: {comp.qnty_si_factor}\n")
                if comp.pint_name and not comp.pint_match:
                    f.write(f"  Pint '{comp.pint_name}': {comp.pint_si_factor}\n")
                if comp.unyt_name and not comp.unyt_match:
                    f.write(f"  unyt '{comp.unyt_name}': {comp.unyt_si_factor}\n")
                if comp.astropy_name and not comp.astropy_match:
                    f.write(f"  astropy '{comp.astropy_name}': {comp.astropy_si_factor}\n")
                f.write("\n")
        print("  📄 Legacy conversion mismatches: conversion_mismatches.txt")

def main():
    """Main function."""
    print("🔬 qnty Unit Validation Tool")
    print("=" * 40)
    
    validator = UnitValidator()
    validator.run_validation()
    validator.save_results()
    
    print("\n✨ Validation complete! Check the generated files for detailed results.")

if __name__ == "__main__":
    main()