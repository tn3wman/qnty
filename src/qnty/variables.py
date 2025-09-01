"""
Consolidated Variables Module - Complete Edition
===============================================

Consolidated variable definitions for all variable types.
Uses the exact same source of truth and approach as consolidated units system.
Auto-generated from parsed_units.json and dimension_mapping.json.
"""

from typing import Dict, Any, Type, cast
from .dimension import DimensionSignature, DIMENSIONLESS

# Import all dimensions using the same approach as consolidated units
from .dimension import *  # Import all dimension constants

# Import consolidated unit definitions to create unit constants
from .units import UNIT_DEFINITIONS as UNIT_DEFS
from .variable import FastQuantity, TypeSafeSetter, UnitDefinition
from .variable_types.typed_variable import TypedVariable
from .units import DimensionlessUnits

# Consolidated variable definitions
VARIABLE_DEFINITIONS = {
    "AbsorbedDose": {
        "dimension": ABSORBED_DOSE,
        "default_unit": "erg per grams",
        "units": [
            ("erg per gram", "erg per grams", 0.0001, "Gy"),
            ("gram-rad", "gram-rads", 0.01, "Gy"),
            ("gray", "grays", 1.0, "Gy"),
            ("rad", "rads", 0.01, "Gy")
        ],
        "field_name": "absorbed_dose",
        "display_name": "Absorbed Radiation Dose",
    },
    "Acceleration": {
        "dimension": ACCELERATION,
        "default_unit": "foot per second squareds",
        "units": [
            ("foot per second squared", "foot per second squareds", 0.3048, "$\\mathrm{m} / \\mathrm{s}^{2}$"),
            ("meter per second squared", "meter per second squareds", 1.0, "$\\mathrm{m} / \\mathrm{s}^{2}$")
        ],
        "field_name": "acceleration",
        "display_name": "Acceleration",
    },
    "ActivationEnergy": {
        "dimension": ACTIVATION_ENERGY,
        "default_unit": "Btu per pound moles",
        "units": [
            ("Btu per pound mole", "Btu per pound moles", 2326.0, "J/mol"),
            ("calorie (mean) per gram mole", "calorie (mean) per gram moles", 4.18675, "J/mol"),
            ("joule per gram mole", "joule per gram moles", 1.0, "J/mol"),
            ("joule per kilogram mole", "joule per kilogram moles", 1000.0, "J/mol"),
            ("kilocalorie per kilogram mole", "kilocalorie per kilogram moles", 4.18675, "J/mol")
        ],
        "field_name": "activation_energy",
        "display_name": "Activation Energy",
    },
    "AmountOfSubstance": {
        "dimension": AMOUNT_OF_SUBSTANCE,
        "default_unit": "kilogram mol or kmols",
        "units": [
            ("kilogram mol or kmol", "kilogram mol or kmols", 1000.0, "mol"),
            ("mole (gram)", "mole (gram)s", 1.0, "mol"),
            ("pound-mole", "pound-moles", 453.6, "mol")
        ],
        "field_name": "amount_of_substance",
        "display_name": "Amount of Substance",
    },
    "AnglePlane": {
        "dimension": ANGLE_PLANE,
        "default_unit": "degrees",
        "units": [
            ("degree", "degrees", 0.0174533, "rad"),
            ("gon", "gons", 0.015708, "rad"),
            ("grade", "grades", 0.015708, "rad"),
            ("minute (new)", "minute (new)s", 0.00015708, "rad"),
            ("minute of angle", "minute of angles", 0.000290888, "rad"),
            ("percent", "percents", 0.062832, "rad"),
            ("plane angle", "plane angles", 3.141593, "rad"),
            ("quadrant", "quadrants", 1.570796, "rad"),
            ("radian", "radians", 1.0, "rad"),
            ("right angle", "right angles", 1.570796, "rad"),
            ("round", "rounds", 6.283185, "rad"),
            ("second (new)", "second (new)s", 1.5707999999999999e-06, "rad"),
            ("second of angle", "second of angles", 4.848099999999999e-06, "rad"),
            ("thousandth (US)", "thousandth (US)s", 0.0015708, "rad"),
            ("turn", "turns", 6.283185, "rad")
        ],
        "field_name": "angle_plane",
        "display_name": "Angle, Plane",
    },
    "AngleSolid": {
        "dimension": ANGLE_SOLID,
        "default_unit": "spats",
        "units": [
            ("spat", "spats", 12.5663, "sr"),
            ("square degree", "square degrees", 0.000304617, "sr"),
            ("square gon", "square gons", 0.00024674, "sr"),
            ("steradian", "steradians", 1.0, "sr")
        ],
        "field_name": "angle_solid",
        "display_name": "Angle, Solid",
    },
    "AngularAcceleration": {
        "dimension": ANGULAR_ACCELERATION,
        "default_unit": "radian per second squareds",
        "units": [
            ("radian per second squared", "radian per second squareds", 1.0, "$\\mathrm{rad} / \\mathrm{s}^{2}$"),
            ("revolution per second squared", "revolution per second squareds", 6.2832, "$\\mathrm{rad} / \\mathrm{s}^{2}$"),
            ("rpm (or revolution per minute) per minute", "rpm (or revolution per minute) per minutes", 0.001745, "$\\mathrm{rad} / \\mathrm{s}^{2}$")
        ],
        "field_name": "angular_acceleration",
        "display_name": "Angular Acceleration",
    },
    "AngularMomentum": {
        "dimension": ANGULAR_MOMENTUM,
        "default_unit": "gram centimeter squared per seconds",
        "units": [
            ("gram centimeter squared per second", "gram centimeter squared per seconds", 1e-07, "$\\mathrm{kg} \\mathrm{m}^{2} / \\mathrm{s}$"),
            ("kilogram meter squared per second", "kilogram meter squared per seconds", 1.0, "$\\mathrm{kg} \\mathrm{m}^{2} / \\mathrm{s}$"),
            ("pound force square foot per second", "pound force square foot per seconds", 0.04214, "$\\mathrm{kg} \\mathrm{m}^{2} / \\mathrm{s}$")
        ],
        "field_name": "angular_momentum",
        "display_name": "Angular Momentum",
    },
    "Area": {
        "dimension": AREA,
        "default_unit": "acre (general)s",
        "units": [
            ("acre (general)", "acre (general)s", 4046.856, "$\\mathrm{m}^{2}$"),
            ("are", "ares", 100.0, "$\\mathrm{m}^{2}$"),
            ("arpent (Quebec)", "arpent (Quebec)s", 3418.89, "$\\mathrm{m}^{2}$"),
            ("barn", "barns", 1e-28, "$\\mathrm{m}^{2}$"),
            ("circular inch", "circular inchs", 0.000506707, "$\\mathrm{m}^{2}$"),
            ("circular mil", "circular mils", 5.07e-10, "$\\mathrm{m}^{2}$"),
            ("hectare", "hectares", 10000.0, "$\\mathrm{m}^{2}$"),
            ("shed", "sheds", 1e-52, "$\\mathrm{m}^{2}$"),
            ("square centimeter", "square centimeters", 0.0001, "$\\mathrm{m}^{2}$"),
            ("square chain (Ramsden)", "square chain (Ramsden)s", 929.03, "$\\mathrm{m}^{2}$"),
            ("square chain (Survey, Gunter's)", "square chain (Survey, Gunter's)s", 404.6856, "$\\mathrm{m}^{2}$"),
            ("square decimeter", "square decimeters", 0.01, "$\\mathrm{m}^{2}$"),
            ("square fermi", "square fermis", 1e-30, "$\\mathrm{m}^{2}$"),
            ("square foot", "square foots", 0.092903, "$\\mathrm{m}^{2}$"),
            ("square hectometer", "square hectometers", 10000.0, "$\\mathrm{m}^{2}$"),
            ("square inch", "square inchs", 0.00064516, "$\\mathrm{m}^{2}$"),
            ("square kilometer", "square kilometers", 1000000.0, "$\\mathrm{m}^{2}$"),
            ("square league (statute)", "square league (statute)s", 23310000.0, "$\\mathrm{m}^{2}$"),
            ("square meter", "square meters", 1.0, "$\\mathrm{m}^{2}$"),
            ("square micron", "square microns", 1e-12, "$\\mathrm{m}^{2}$"),
            ("square mile (statute)", "square mile (statute)s", 2590000.0, "$\\mathrm{m}^{2}$"),
            ("square mile (US survey)", "square mile (US survey)s", 2590000.0, "$\\mathrm{m}^{2}$"),
            ("square millimeter", "square millimeters", 1e-06, "$\\mathrm{m}^{2}$"),
            ("square nanometer", "square nanometers", 1e-18, "$\\mathrm{m}^{2}$"),
            ("square yard", "square yards", 0.836131, "$\\mathrm{m}^{2}$"),
            ("township (US)", "township (US)s", 93240000.0, "$\\mathrm{m}^{2}$")
        ],
        "field_name": "area",
        "display_name": "Area",
    },
    "AreaPerUnitVolume": {
        "dimension": AREA_PER_UNIT_VOLUME,
        "default_unit": "square centimeter per cubic centimeters",
        "units": [
            ("square centimeter per cubic centimeter", "square centimeter per cubic centimeters", 100.0, "$\\mathrm{m}^{2} / \\mathrm{m}^{3}$"),
            ("square foot per cubic foot", "square foot per cubic foots", 3.2808, "$\\mathrm{m}^{2} / \\mathrm{m}^{3}$"),
            ("square inch per cubic inch", "square inch per cubic inchs", 1.0, "$\\mathrm{m}^{2} / \\mathrm{m}^{3}$"),
            ("square meter per cubic meter", "square meter per cubic meters", 1.0, "$\\mathrm{m}^{2} / \\mathrm{m}^{3}$")
        ],
        "field_name": "area_per_unit_volume",
        "display_name": "Area per Unit Volume",
    },
    "AtomicWeight": {
        "dimension": ATOMIC_WEIGHT,
        "default_unit": "atomic mass unit (12C)s",
        "units": [
            ("atomic mass unit (12C)", "atomic mass unit (12C)s", 1.0, "g/mol"),
            ("grams per mole", "grams per moles", 1.0, "g/mol"),
            ("kilograms per kilomole", "kilograms per kilomoles", 1.0, "g/mol"),
            ("pounds per pound mole", "pounds per pound moles", 1.0, "g/mol")
        ],
        "field_name": "atomic_weight",
        "display_name": "Atomic Weight",
    },
    "Concentration": {
        "dimension": CONCENTRATION,
        "default_unit": "grains of \"i\" per cubic foots",
        "units": [
            ("grains of \"i\" per cubic foot", "grains of \"i\" per cubic foots", 0.002288, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("grains of \"i\" per gallon (US)", "grains of \"i\" per gallon (US)s", 0.017115, "$\\mathrm{kg} / \\mathrm{m}^{3}$")
        ],
        "field_name": "concentration",
        "display_name": "Concentration",
    },
    "DynamicFluidity": {
        "dimension": DYNAMIC_FLUIDITY,
        "default_unit": "meter-seconds per kilograms",
        "units": [
            ("meter-seconds per kilogram", "meter-seconds per kilograms", 1.0, ""),
            ("rhe", "rhes", 1.0, "$\\mathrm{m}^{2} /(\\mathrm{N} \\mathrm{s})$"),
            ("square foot per pound second", "square foot per pound seconds", 0.002086, "$\\mathrm{m}^{2} /(\\mathrm{N} \\mathrm{s})$"),
            ("square meters per newton per second", "square meters per newton per seconds", 1.0, "$\\mathrm{m}^{2} /(\\mathrm{N} \\mathrm{s})$")
        ],
        "field_name": "dynamic_fluidity",
        "display_name": "Dynamic Fluidity",
    },
    "ElectricCapacitance": {
        "dimension": ELECTRIC_CAPACITANCE,
        "default_unit": "\"cm\"s",
        "units": [
            ("\"cm\"", "\"cm\"s", 1.1111e-12, "F"),
            ("abfarad", "abfarads", 1000000000.0, "F"),
            ("farad", "farads", 1.0, "F"),
            ("farad (intl)", "farad (intl)s", 0.99951, "F"),
            ("jar", "jars", 1.1111e-09, "F"),
            ("puff", "puffs", 1e-12, "F"),
            ("statfarad", "statfarads", 1.113e-12, "F")
        ],
        "field_name": "electric_capacitance",
        "display_name": "Electric Capacitance",
    },
    "ElectricCharge": {
        "dimension": ELECTRIC_CHARGE,
        "default_unit": "abcoulombs",
        "units": [
            ("abcoulomb", "abcoulombs", 0.000103643, "F"),
            ("ampere-hour", "ampere-hours", 0.03731138, "F"),
            ("coulomb", "coulombs", 1.0364000000000001e-05, "F"),
            ("faraday (C12)", "faraday (C12)s", 1.0, "F"),
            ("franklin", "franklins", 3.45715e-15, "F"),
            ("statcoulomb", "statcoulombs", 3.45715e-15, "F"),
            ("u.a. charge", "u.a. charges", 1.66054e-24, "F")
        ],
        "field_name": "electric_charge",
        "display_name": "Electric Charge",
    },
    "ElectricCurrentIntensity": {
        "dimension": ELECTRIC_CURRENT_INTENSITY,
        "default_unit": "abamperes",
        "units": [
            ("abampere", "abamperes", 10.0, "A"),
            ("ampere (intl mean)", "ampere (intl mean)s", 0.99985, "A"),
            ("ampere (intl US)", "ampere (intl US)s", 0.999835, "A"),
            ("ampere or amp", "ampere or amps", 1.0, "A"),
            ("biot", "biots", 10.0, "A"),
            ("statampere", "statamperes", 3.33564e-10, "A"),
            ("u.a. or current", "u.a. or currents", 0.00662362, "A")
        ],
        "field_name": "electric_current_intensity",
        "display_name": "Electric Current Intensity",
    },
    "ElectricDipoleMoment": {
        "dimension": ELECTRIC_DIPOLE_MOMENT,
        "default_unit": "ampere meter seconds",
        "units": [
            ("ampere meter second", "ampere meter seconds", 1.0, "A m s"),
            ("coulomb meter", "coulomb meters", 1.0, "A m s"),
            ("debye", "debyes", 3.3356e-30, "A m s"),
            ("electron meter", "electron meters", 1.6022e-19, "A m s")
        ],
        "field_name": "electric_dipole_moment",
        "display_name": "Electric Dipole Moment",
    },
    "ElectricFieldStrength": {
        "dimension": ELECTRIC_FIELD_STRENGTH,
        "default_unit": "volt per centimeters",
        "units": [
            ("volt per centimeter", "volt per centimeters", 100.0, "V/m"),
            ("volt per meter", "volt per meters", 1.0, "V/m")
        ],
        "field_name": "electric_field_strength",
        "display_name": "Electric Field Strength",
    },
    "ElectricInductance": {
        "dimension": ELECTRIC_INDUCTANCE,
        "default_unit": "abhenrys",
        "units": [
            ("abhenry", "abhenrys", 1e-09, "H"),
            ("cm", "cms", 1e-09, "H"),
            ("henry", "henrys", 1.0, "H"),
            ("henry (intl mean)", "henry (intl mean)s", 1.00049, "H"),
            ("henry (intl US)", "henry (intl US)s", 1.000495, "H"),
            ("mic", "mics", 1e-06, "H"),
            ("stathenry", "stathenrys", 898760000000.0, "H")
        ],
        "field_name": "electric_inductance",
        "display_name": "Electric Inductance",
    },
    "ElectricPotential": {
        "dimension": ELECTRIC_POTENTIAL,
        "default_unit": "abvolts",
        "units": [
            ("abvolt", "abvolts", 1e-08, "V"),
            ("statvolt", "statvolts", 299.792, "V"),
            ("u.a. potential", "u.a. potentials", 27.2114, "V"),
            ("volt", "volts", 1.0, "V"),
            ("volt (intl mean)", "volt (intl mean)s", 1.00034, "V"),
            ("volt (US)", "volt (US)s", 1.00033, "V")
        ],
        "field_name": "electric_potential",
        "display_name": "Electric Potential",
    },
    "ElectricResistance": {
        "dimension": ELECTRIC_RESISTANCE,
        "default_unit": "abohms",
        "units": [
            ("abohm", "abohms", 1e-09, "$\\Omega$"),
            ("jacobi", "jacobis", 0.64, "$\\Omega$"),
            ("lenz", "lenzs", 80000.0, "$\\Omega$"),
            ("ohm", "ohms", 1.0, "$\\Omega$"),
            ("ohm (intl mean)", "ohm (intl mean)s", 1.00049, "$\\Omega$"),
            ("ohm (intl US)", "ohm (intl US)s", 1.000495, "$\\Omega$"),
            ("ohm (legal)", "ohm (legal)s", 0.9972, "$\\Omega$"),
            ("preece", "preeces", 1000000.0, "$\\Omega$"),
            ("statohm", "statohms", 8.987552, "$\\Omega$"),
            ("wheatstone", "wheatstones", 0.0025, "$\\Omega$")
        ],
        "field_name": "electric_resistance",
        "display_name": "Electric Resistance",
    },
    "ElectricalConductance": {
        "dimension": ELECTRICAL_CONDUCTANCE,
        "default_unit": "emu cgss",
        "units": [
            ("emu cgs", "emu cgss", 1000000000.0, "S"),
            ("esu cgs", "esu cgss", 1.1127e-12, "S"),
            ("mho", "mhos", 1.0, "S"),
            ("microsiemens", "microsiemenss", 1e-06, "S"),
            ("siemens", "siemenss", 1.0, "S")
        ],
        "field_name": "electrical_conductance",
        "display_name": "Electrical Conductance",
    },
    "ElectricalPermittivity": {
        "dimension": ELECTRICAL_PERMITTIVITY,
        "default_unit": "farad per meters",
        "units": [
            ("farad per meter", "farad per meters", 1.0, "F/m")
        ],
        "field_name": "electrical_permittivity",
        "display_name": "Electrical Permittivity",
    },
    "ElectricalResistivity": {
        "dimension": ELECTRICAL_RESISTIVITY,
        "default_unit": "circular mil-ohm per foots",
        "units": [
            ("circular mil-ohm per foot", "circular mil-ohm per foots", 1.6624000000000002e-09, "$\\Omega \\mathrm{m}$"),
            ("emu cgs", "emu cgss", 1e-11, "$\\boldsymbol{\\Omega} \\mathrm{m}$"),
            ("microhm-inch", "microhm-inchs", 2.5400000000000002e-08, "$\\Omega \\mathrm{m}$"),
            ("ohm-centimeter", "ohm-centimeters", 0.01, "$\\Omega \\mathrm{m}$"),
            ("ohm-meter", "ohm-meters", 1.0, "$\\Omega \\mathrm{m}$")
        ],
        "field_name": "electrical_resistivity",
        "display_name": "Electrical Resistivity",
    },
    "EnergyFlux": {
        "dimension": ENERGY_FLUX,
        "default_unit": "Btu per square foot per hours",
        "units": [
            ("Btu per square foot per hour", "Btu per square foot per hours", 3.1546, "$\\mathrm{W} / \\mathrm{m}^{2}$"),
            ("calorie per square centimeter per second", "calorie per square centimeter per seconds", 41868.0, "$\\mathrm{W} / \\mathrm{m}^{2}$"),
            ("Celsius heat units (Chu) per square foot per hour", "Celsius heat units (Chu) per square foot per hours", 5.6784, "$\\mathrm{W} / \\mathrm{m}^{2}$"),
            ("kilocalorie per square foot per hour", "kilocalorie per square foot per hours", 12.518, "$\\mathrm{W} / \\mathrm{m}^{2}$"),
            ("kilocalorie per square meter per hour", "kilocalorie per square meter per hours", 1.163, "$\\mathrm{W} / \\mathrm{m}^{2}$"),
            ("watt per square meter", "watt per square meters", 1.0, "$\\mathrm{W} / \\mathrm{m}^{2}$")
        ],
        "field_name": "energy_flux",
        "display_name": "Energy Flux",
    },
    "EnergyHeatWork": {
        "dimension": ENERGY_HEAT_WORK,
        "default_unit": "barrel oil equivalent or equivalent barrels",
        "units": [
            ("barrel oil equivalent or equivalent barrel", "barrel oil equivalent or equivalent barrels", 6120000000.0, "J"),
            ("billion electronvolt", "billion electronvolts", 1.6022000000000002e-10, "J"),
            ("British thermal unit ( $4^{\\circ} \\mathrm{C}$ )", "British thermal unit ( $4^{\\circ} \\mathrm{C}$ )s", 1059.67, "J"),
            ("British thermal unit ( $60^{\\circ} \\mathrm{F}$ )", "British thermal unit ( $60^{\\circ} \\mathrm{F}$ )s", 1054.678, "J"),
            ("British thermal unit (international steam tables)", "British thermal unit (international steam tables)s", 1055.055853, "J"),
            ("British thermal unit (ISO/TC 12)", "British thermal unit (ISO/TC 12)s", 1055.06, "J"),
            ("British thermal unit (mean)", "British thermal unit (mean)s", 1055.87, "J"),
            ("British thermal unit (thermochemical)", "British thermal unit (thermochemical)s", 1054.35, "J"),
            ("calorie ( $20^{\\circ} \\mathrm{C}$ )", "calorie ( $20^{\\circ} \\mathrm{C}$ )s", 4.1819, "J"),
            ("calorie ( $4^{\\circ} \\mathrm{C}$ )", "calorie ( $4^{\\circ} \\mathrm{C}$ )s", 4.2045, "J"),
            ("calorie (international steam tables)", "calorie (international steam tables)s", 4.18674, "J"),
            ("calorie (mean)", "calorie (mean)s", 4.19002, "J"),
            ("Calorie (nutritional)", "Calorie (nutritional)s", 4184.0, "J"),
            ("calorie (thermochemical)", "calorie (thermochemical)s", 4.184, "J"),
            ("Celsius heat unit", "Celsius heat units", 1899.18, "J"),
            ("Celsius heat unit ( $15{ }^{\\circ} \\mathrm{C}$ )", "Celsius heat unit ( $15{ }^{\\circ} \\mathrm{C}$ )s", 1899.1, "J"),
            ("electron volt", "electron volts", 1.6022e-19, "J"),
            ("erg", "ergs", 1e-07, "J"),
            ("foot pound force (duty)", "foot pound force (duty)s", 1.355818, "J"),
            ("foot-poundal", "foot-poundals", 0.04214, "J"),
            ("frigorie", "frigories", 4190.0, "J"),
            ("hartree (atomic unit of energy)", "hartree (atomic unit of energy)s", 4.359700000000001e-18, "J"),
            ("joule", "joules", 1.0, "J"),
            ("joule (international)", "joule (international)s", 1.000165, "J"),
            ("kilocalorie (thermal)", "kilocalorie (thermal)s", 4184.0, "J"),
            ("kilogram force meter", "kilogram force meters", 9.80665, "J"),
            ("kiloton (TNT)", "kiloton (TNT)s", 4.1799999999999995e+18, "J"),
            ("kilowatt hour", "kilowatt hours", 3600000.0, "J"),
            ("liter atmosphere", "liter atmospheres", 101.325, "J"),
            ("megaton (TNT)", "megaton (TNT)s", 4.1799999999999995e+21, "J"),
            ("pound centigrade unit ( $15^{\\circ} \\mathrm{C}$ )", "pound centigrade unit ( $15^{\\circ} \\mathrm{C}$ )s", 1899.1, "J"),
            ("prout", "prouts", 2.9638e-14, "J"),
            ("Q unit", "Q units", 1.055e+21, "J"),
            ("quad (quadrillion Btu)", "quad (quadrillion Btu)s", 1.0550999999999999e+18, "J"),
            ("rydberg", "rydbergs", 2.1799000000000002e-18, "J"),
            ("therm (EEG)", "therm (EEG)s", 105510000.0, "J"),
            ("therm (refineries)", "therm (refineries)s", 1055900000.0000001, "J"),
            ("therm (US)", "therm (US)s", 105480000.0, "J"),
            ("ton coal equivalent", "ton coal equivalents", 292900000.0, "J"),
            ("ton oil equivalent", "ton oil equivalents", 418700000.0, "J")
        ],
        "field_name": "energy_heat_work",
        "display_name": "Energy, Heat, Work",
    },
    "EnergyPerUnitArea": {
        "dimension": ENERGY_PER_UNIT_AREA,
        "default_unit": "British thermal unit per square foots",
        "units": [
            ("British thermal unit per square foot", "British thermal unit per square foots", 11354.0, "$\\mathrm{J} / \\mathrm{m}^{2}$"),
            ("joule per square meter", "joule per square meters", 1.0, "$\\mathrm{J} / \\mathrm{m}^{2}$"),
            ("Langley", "Langleys", 41840.0, "$\\mathrm{J} / \\mathrm{m}^{2}$")
        ],
        "field_name": "energy_per_unit_area",
        "display_name": "Energy per Unit Area",
    },
    "Force": {
        "dimension": FORCE,
        "default_unit": "crinals",
        "units": [
            ("crinal", "crinals", 0.1, "N"),
            ("dyne", "dynes", 1e-05, "N"),
            ("funal", "funals", 1000.0, "N"),
            ("kilogram force", "kilogram forces", 9.80665, "N"),
            ("kip force", "kip forces", 4448.22, "N"),
            ("newton", "newtons", 1.0, "N"),
            ("ounce force", "ounce forces", 0.27801385, "N"),
            ("pond", "ponds", 0.0098066, "N"),
            ("pound force", "pound forces", 4.4482216, "N"),
            ("poundal", "poundals", 0.13825495, "N"),
            ("slug force", "slug forces", 143.117, "N"),
            ("sthène", "sthènes", 1000.0, "N"),
            ("ton (force, long)", "ton (force, long)s", 9964.016, "N"),
            ("ton (force, metric)", "ton (force, metric)s", 9806.65, "N"),
            ("ton (force, short)", "ton (force, short)s", 8896.44, "N")
        ],
        "field_name": "force",
        "display_name": "Force",
    },
    "ForceBody": {
        "dimension": FORCE_BODY,
        "default_unit": "dyne per cubic centimeters",
        "units": [
            ("dyne per cubic centimeter", "dyne per cubic centimeters", 10.0, "$\\mathrm{N} / \\mathrm{m}^{3}$"),
            ("kilogram force per cubic centimeter", "kilogram force per cubic centimeters", 9806700.0, "$\\mathrm{N} / \\mathrm{m}^{3}$"),
            ("kilogram force per cubic meter", "kilogram force per cubic meters", 9.80665, "$\\mathrm{N} / \\mathrm{m}^{3}$"),
            ("newton per cubic meter", "newton per cubic meters", 1.0, "$\\mathrm{N} / \\mathrm{m}^{3}$"),
            ("pound force per cubic foot", "pound force per cubic foots", 157.087, "$\\mathrm{N} / \\mathrm{m}^{3}$"),
            ("pound force per cubic inch", "pound force per cubic inchs", 271450.0, "$\\mathrm{N} / \\mathrm{m}^{3}$"),
            ("ton force per cubic foot", "ton force per cubic foots", 351880.0, "$\\mathrm{N} / \\mathrm{m}^{3}$")
        ],
        "field_name": "force_body",
        "display_name": "Force (Body)",
    },
    "ForcePerUnitMass": {
        "dimension": FORCE_PER_UNIT_MASS,
        "default_unit": "dyne per grams",
        "units": [
            ("dyne per gram", "dyne per grams", 0.01, "N/kg"),
            ("kilogram force per kilogram", "kilogram force per kilograms", 9.80665, "N/kg"),
            ("newton per kilogram", "newton per kilograms", 1.0, "N/kg"),
            ("pound force per pound mass", "pound force per pound masss", 9.80665, "N/kg"),
            ("pound force per slug", "pound force per slugs", 0.3048, "N/kg")
        ],
        "field_name": "force_per_unit_mass",
        "display_name": "Force per Unit Mass",
    },
    "FrequencyVoltageRatio": {
        "dimension": FREQUENCY_VOLTAGE_RATIO,
        "default_unit": "cycles per second per volts",
        "units": [
            ("cycles per second per volt", "cycles per second per volts", 1.0, "Hz/V"),
            ("hertz per volt", "hertz per volts", 1.0, "Hz/V"),
            ("terahertz per volt", "terahertz per volts", 1000000000000.0, "Hz/V")
        ],
        "field_name": "frequency_voltage_ratio",
        "display_name": "Frequency Voltage Ratio",
    },
    "FuelConsumption": {
        "dimension": FUEL_CONSUMPTION,
        "default_unit": "100 km per liters",
        "units": [
            ("100 km per liter", "100 km per liters", 100.0, "km/l"),
            ("gallons (UK) per 100 miles", "gallons (UK) per 100 miless", 35.4, "km/l"),
            ("gallons (US) per 100 miles", "gallons (US) per 100 miless", 42.51, "km/l"),
            ("kilometers per gallon (UK)", "kilometers per gallon (UK)s", 0.21997, "km/l"),
            ("kilometers per gallon (US)", "kilometers per gallon (US)s", 0.26417, "km/l"),
            ("kilometers per liter", "kilometers per liters", 1.0, "km/l"),
            ("liters per 100 km", "liters per 100 kms", 100.0, "km/l"),
            ("liters per kilometer", "liters per kilometers", 1.0, "km/l"),
            ("meters per gallon (UK)", "meters per gallon (UK)s", 0.00021997, "km/l"),
            ("meters per gallon (US)", "meters per gallon (US)s", 0.00022642000000000004, "km/l"),
            ("miles per gallon (UK)", "miles per gallon (UK)s", 0.35401, "km/l"),
            ("miles per gallon (US)", "miles per gallon (US)s", 0.42514, "km/l"),
            ("miles per liter", "miles per liters", 1.6093, "km/l")
        ],
        "field_name": "fuel_consumption",
        "display_name": "Fuel Consumption",
    },
    "HeatOfCombustion": {
        "dimension": HEAT_OF_COMBUSTION,
        "default_unit": "British thermal unit per pounds",
        "units": [
            ("British thermal unit per pound", "British thermal unit per pounds", 2326.0, "J/kg"),
            ("calorie per gram", "calorie per grams", 4186.0, "J/kg"),
            ("Chu per pound", "Chu per pounds", 4186.8, "J/kg"),
            ("joule per kilogram", "joule per kilograms", 1.0, "J/kg")
        ],
        "field_name": "heat_of_combustion",
        "display_name": "Heat of Combustion",
    },
    "HeatOfFusion": {
        "dimension": HEAT_OF_FUSION,
        "default_unit": "British thermal unit (mean) per pounds",
        "units": [
            ("British thermal unit (mean) per pound", "British thermal unit (mean) per pounds", 2327.79, "J/kg"),
            ("British thermal unit per pound", "British thermal unit per pounds", 2326.0, "J/kg"),
            ("calorie per gram", "calorie per grams", 4186.0, "J/kg"),
            ("Chu per pound", "Chu per pounds", 4186.8, "J/kg"),
            ("joule per kilogram", "joule per kilograms", 1.0, "J/kg")
        ],
        "field_name": "heat_of_fusion",
        "display_name": "Heat of Fusion",
    },
    "HeatOfVaporization": {
        "dimension": HEAT_OF_VAPORIZATION,
        "default_unit": "British thermal unit per pounds",
        "units": [
            ("British thermal unit per pound", "British thermal unit per pounds", 2326.0, "J/kg"),
            ("calorie per gram", "calorie per grams", 4186.0, "J/kg"),
            ("Chu per pound", "Chu per pounds", 4186.8, "J/kg"),
            ("joule per kilogram", "joule per kilograms", 1.0, "J/kg")
        ],
        "field_name": "heat_of_vaporization",
        "display_name": "Heat of Vaporization",
    },
    "HeatTransferCoefficient": {
        "dimension": HEAT_TRANSFER_COEFFICIENT,
        "default_unit": "Btu per square foot per hour per degree Fahrenheit (or Rankine)s",
        "units": [
            ("Btu per square foot per hour per degree Fahrenheit (or Rankine)", "Btu per square foot per hour per degree Fahrenheit (or Rankine)s", 5.679, "W/ ( $\\mathrm{m}^{2}{ }^{\\circ} \\mathrm{C}$ )"),
            ("watt per square meter per degree Celsius (or kelvin)", "watt per square meter per degree Celsius (or kelvin)s", 1.0, "W/ ( $\\mathrm{m}^{2}{ }^{\\circ} \\mathrm{C}$ )")
        ],
        "field_name": "heat_transfer_coefficient",
        "display_name": "Heat Transfer Coefficient",
    },
    "Illuminance": {
        "dimension": ILLUMINANCE,
        "default_unit": "foot-candles",
        "units": [
            ("foot-candle", "foot-candles", 10.76391, "1x"),
            ("lux", "luxs", 1.0, "lx"),
            ("nox", "noxs", 0.001, "1x"),
            ("phot", "phots", 10000.0, "lx"),
            ("skot", "skots", 0.001, "lx")
        ],
        "field_name": "illuminance",
        "display_name": "Illuminance",
    },
    "KineticEnergyOfTurbulence": {
        "dimension": KINETIC_ENERGY_OF_TURBULENCE,
        "default_unit": "square foot per second squareds",
        "units": [
            ("square foot per second squared", "square foot per second squareds", 0.0929, "$\\mathrm{m}^{2} / \\mathrm{s}^{2}$"),
            ("square meters per second squared", "square meters per second squareds", 1.0, "$\\mathrm{m}^{2} / \\mathrm{s}^{2}$")
        ],
        "field_name": "kinetic_energy_of_turbulence",
        "display_name": "Kinetic Energy of Turbulence",
    },
    "Length": {
        "dimension": LENGTH,
        "default_unit": "ångströms",
        "units": [
            ("ångström", "ångströms", 1e-10, "m"),
            ("arpent (Quebec)", "arpent (Quebec)s", 58.47, "m"),
            ("astronomic unit", "astronomic units", 149600000000.0, "m"),
            ("attometer", "attometers", 1e-18, "m"),
            ("calibre (centinch)", "calibre (centinch)s", 0.000254, "m"),
            ("centimeter", "centimeters", 0.01, "m"),
            ("chain (Engr's or Ramsden)", "chain (Engr's or Ramsden)s", 30.48, "m"),
            ("chain (Gunter's)", "chain (Gunter's)s", 20.1168, "m"),
            ("chain (surveyors)", "chain (surveyors)s", 20.1168, "m"),
            ("cubit (UK)", "cubit (UK)s", 0.4572, "m"),
            ("ell", "ells", 1.143, "m"),
            ("fathom", "fathoms", 1.8288, "m"),
            ("femtometre", "femtometres", 1e-15, "m"),
            ("fermi", "fermis", 1e-15, "m"),
            ("foot", "feet", 0.3048, "m"),
            ("furlong (UK and US)", "furlong (UK and US)s", 201.168, "m"),
            ("inch", "inches", 0.0254, "m"),
            ("kilometer", "kilometers", 1000.0, "m"),
            ("league (US, statute)", "league (US, statute)s", 4828.0, "m"),
            ("lieue (metric)", "lieue (metric)s", 4000.0, "m"),
            ("ligne (metric)", "ligne (metric)s", 0.0023, "m"),
            ("line (US)", "line (US)s", 0.000635, "m"),
            ("link (surveyors)", "link (surveyors)s", 0.201168, "m"),
            ("meter", "meters", 1.0, "m"),
            ("micrometer", "micrometers", 1e-06, "m"),
            ("micron", "microns", 1e-06, "m"),
            ("mil", "mils", 2.54e-05, "m"),
            ("mile (geographical)", "mile (geographical)s", 7421.59, "m"),
            ("mile (US, nautical)", "mile (US, nautical)s", 1853.2, "m"),
            ("mile (US, statute)", "mile (US, statute)s", 1609.344, "m"),
            ("mile (US, survey)", "mile (US, survey)s", 1609.3, "m"),
            ("millimeter", "millimeters", 0.001, "m"),
            ("millimicron", "millimicrons", 1e-09, "m"),
            ("nanometer or nanon", "nanometer or nanons", 1e-09, "m"),
            ("parsec", "parsecs", 3.086e+16, "m"),
            ("perche", "perches", 5.0292, "m"),
            ("pica", "picas", 0.0042175, "m"),
            ("picometer", "picometers", 1e-12, "m"),
            ("point (Didot)", "point (Didot)s", 0.00037597, "m"),
            ("point (US)", "point (US)s", 0.00035146, "m"),
            ("rod or pole", "rod or poles", 5.0292, "m"),
            ("span", "spans", 0.2286, "m"),
            ("thou (millinch)", "thou (millinch)s", 2.54e-05, "m"),
            ("toise (metric)", "toise (metric)s", 2.0, "m"),
            ("yard", "yards", 0.9144, "m")
        ],
        "field_name": "length",
        "display_name": "Length",
    },
    "LinearMassDensity": {
        "dimension": LINEAR_MASS_DENSITY,
        "default_unit": "deniers",
        "units": [
            ("denier", "deniers", 1.111e-07, "kg/m"),
            ("kilogram per centimeter", "kilogram per centimeters", 100.0, "kg/m"),
            ("kilogram per meter", "kilogram per meters", 1.0, "kg/m"),
            ("pound per foot", "pound per foots", 1.488, "kg/m"),
            ("pound per inch", "pound per inchs", 17.858, "kg/m"),
            ("pound per yard", "pound per yards", 0.49606, "kg/m"),
            ("ton (metric) per kilometer", "ton (metric) per kilometers", 1.0, "kg/m"),
            ("ton (metric) per meter", "ton (metric) per meters", 1000.0, "kg/m")
        ],
        "field_name": "linear_mass_density",
        "display_name": "Linear Mass Density",
    },
    "LinearMomentum": {
        "dimension": LINEAR_MOMENTUM,
        "default_unit": "foot pounds force per hours",
        "units": [
            ("foot pounds force per hour", "foot pounds force per hours", 3.8400000000000005e-05, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}$"),
            ("foot pounds force per minute", "foot pounds force per minutes", 0.0023042, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}$"),
            ("foot pounds force per second", "foot pounds force per seconds", 0.13825, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}$"),
            ("gram centimeters per second", "gram centimeters per seconds", 1e-05, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}$"),
            ("kilogram meters per second", "kilogram meters per seconds", 1.0, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}$")
        ],
        "field_name": "linear_momentum",
        "display_name": "Linear Momentum",
    },
    "LuminanceSelf": {
        "dimension": LUMINANCE_SELF,
        "default_unit": "apostilbs",
        "units": [
            ("apostilb", "apostilbs", 0.31831, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("blondel", "blondels", 0.31831, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("candela per square meter", "candela per square meters", 1.0, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("foot-lambert", "foot-lamberts", 3.426259, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("lambert", "lamberts", 3183.1, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("luxon", "luxons", 10000.0, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("nit", "nits", 1.0, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("stilb", "stilbs", 10000.0, "$\\mathrm{cd} / \\mathrm{m}^{2}$"),
            ("troland", "trolands", 10000.0, "$\\mathrm{cd} / \\mathrm{m}^{2}$")
        ],
        "field_name": "luminance_self",
        "display_name": "Luminance (self)",
    },
    "LuminousFlux": {
        "dimension": LUMINOUS_FLUX,
        "default_unit": "candela steradians",
        "units": [
            ("candela steradian", "candela steradians", 1.0, "lumen"),
            ("lumen", "lumens", 1.0, "lumen")
        ],
        "field_name": "luminous_flux",
        "display_name": "Luminous Flux",
    },
    "LuminousIntensity": {
        "dimension": LUMINOUS_INTENSITY,
        "default_unit": "candelas",
        "units": [
            ("candela", "candelas", 1.0, "cd"),
            ("candle (international)", "candle (international)s", 1.01937, "cd"),
            ("carcel", "carcels", 10.0, "cd"),
            ("Hefner unit", "Hefner units", 0.903, "cd")
        ],
        "field_name": "luminous_intensity",
        "display_name": "Luminous Intensity",
    },
    "MagneticField": {
        "dimension": MAGNETIC_FIELD,
        "default_unit": "ampere per meters",
        "units": [
            ("ampere per meter", "ampere per meters", 1.0, "A/m"),
            ("lenz", "lenzs", 1.0, "A/m"),
            ("oersted", "oersteds", 79.57747, "A/m"),
            ("praoersted", "praoersteds", 11459.08, "A/m")
        ],
        "field_name": "magnetic_field",
        "display_name": "Magnetic Field",
    },
    "MagneticFlux": {
        "dimension": MAGNETIC_FLUX,
        "default_unit": "kapp lines",
        "units": [
            ("kapp line", "kapp lines", 6.000000000000001e-05, "Wb"),
            ("line", "lines", 1e-08, "Wb"),
            ("maxwell", "maxwells", 1e-08, "Wb"),
            ("unit pole", "unit poles", 1.2565999999999998e-07, "Wb"),
            ("weber", "webers", 1.0, "Wb")
        ],
        "field_name": "magnetic_flux",
        "display_name": "Magnetic Flux",
    },
    "MagneticInductionFieldStrength": {
        "dimension": MAGNETIC_INDUCTION_FIELD_STRENGTH,
        "default_unit": "gammas",
        "units": [
            ("gamma", "gammas", 1e-09, "T"),
            ("gauss", "gausss", 0.0001, "T"),
            ("line per square centimeter", "line per square centimeters", 0.0001, "T"),
            ("maxwell per square centimeter", "maxwell per square centimeters", 0.0001, "T"),
            ("tesla", "teslas", 1.0, "T"),
            ("u.a.", "u.a.s", 2350520000000000.0, "T"),
            ("weber per square meter", "weber per square meters", 1.0, "T")
        ],
        "field_name": "magnetic_induction_field_strength",
        "display_name": "Magnetic Induction Field Strength",
    },
    "MagneticMoment": {
        "dimension": MAGNETIC_MOMENT,
        "default_unit": "Bohr magnetons",
        "units": [
            ("Bohr magneton", "Bohr magnetons", 9.273999999999999e-24, "J/T"),
            ("joule per tesla", "joule per teslas", 1.0, "J/T"),
            ("nuclear magneton", "nuclear magnetons", 5.0508e-27, "J/T")
        ],
        "field_name": "magnetic_moment",
        "display_name": "Magnetic Moment",
    },
    "MagneticPermeability": {
        "dimension": MAGNETIC_PERMEABILITY,
        "default_unit": "henrys per meters",
        "units": [
            ("henrys per meter", "henrys per meters", 1.0, "H/m"),
            ("newton per square ampere", "newton per square amperes", 1.0, "H/m")
        ],
        "field_name": "magnetic_permeability",
        "display_name": "Magnetic Permeability",
    },
    "MagnetomotiveForce": {
        "dimension": MAGNETOMOTIVE_FORCE,
        "default_unit": "abampere-turns",
        "units": [
            ("abampere-turn", "abampere-turns", 10.0, "A"),
            ("ampere", "amperes", 1.0, "A"),
            ("ampere-turn", "ampere-turns", 2864.77, "A"),
            ("gilbert", "gilberts", 0.79577, "A")
        ],
        "field_name": "magnetomotive_force",
        "display_name": "Magnetomotive Force",
    },
    "Mass": {
        "dimension": MASS,
        "default_unit": "slugs",
        "units": [
            ("slug", "slugs", 14.594, "kg"),
            ("atomic mass unit ( ${ }^{12} \\mathrm{C}$ )", "atomic mass unit ( ${ }^{12} \\mathrm{C}$ )s", 1.6605000000000002e-27, "kg"),
            ("carat (metric)", "carat (metric)s", 0.0002, "kg"),
            ("cental", "centals", 45.359, "kg"),
            ("centigram", "centigrams", 1e-05, "kg"),
            ("clove (UK)", "clove (UK)s", 3.6287, "kg"),
            ("drachm (apothecary)", "drachm (apothecary)s", 0.0038879, "kg"),
            ("dram (avoirdupois)", "dram (avoirdupois)s", 0.0017718, "kg"),
            ("dram (troy)", "dram (troy)s", 0.0038879, "kg"),
            ("grain", "grains", 6.4799e-05, "kg"),
            ("gram", "grams", 0.001, "kg"),
            ("hundredweight, long or gross", "hundredweight, long or grosss", 50.802, "kg"),
            ("hundredweight, short or net", "hundredweight, short or nets", 45.359, "kg"),
            ("kilogram", "kilograms", 1.0, "kg"),
            ("kip", "kips", 453.59, "kg"),
            ("microgram", "micrograms", 1e-09, "kg"),
            ("milligram", "milligrams", 1e-06, "kg"),
            ("ounce (apothecary)", "ounce (apothecary)s", 0.031103, "kg"),
            ("ounce (avoirdupois)", "ounce (avoirdupois)s", 0.02835, "kg"),
            ("ounce (troy)", "ounce (troy)s", 0.031103, "kg"),
            ("pennyweight (troy)", "pennyweight (troy)s", 0.0015552, "kg"),
            ("pood, (Russia)", "pood, (Russia)s", 16.38, "kg"),
            ("pound (apothecary)", "pound (apothecary)s", 0.37324, "kg"),
            ("pound (avoirdupois)", "pound (avoirdupois)s", 0.45359, "kg"),
            ("pound (troy)", "pound (troy)s", 0.37324, "kg"),
            ("pound mass", "pound masss", 0.45359, "kg"),
            ("quarter (UK)", "quarter (UK)s", 12.7, "kg"),
            ("quintal, metric", "quintal, metrics", 100.0, "kg"),
            ("quital, US", "quital, USs", 45.359, "kg"),
            ("scruple (avoirdupois)", "scruple (avoirdupois)s", 0.001575, "kg"),
            ("stone (UK)", "stone (UK)s", 6.3503, "kg"),
            ("ton, metric", "ton, metrics", 1000.0, "kg"),
            ("ton, US, long", "ton, US, longs", 1016.0, "kg"),
            ("ton, US, short", "ton, US, shorts", 907.18, "kg")
        ],
        "field_name": "mass",
        "display_name": "Mass",
    },
    "MassDensity": {
        "dimension": MASS_DENSITY,
        "default_unit": "gram per cubic centimeters",
        "units": [
            ("gram per cubic centimeter", "gram per cubic centimeters", 1000.0, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("gram per cubic decimeter", "gram per cubic decimeters", 1.0, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("gram per cubic meter", "gram per cubic meters", 0.001, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("gram per liter", "gram per liters", 1.0, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("kilogram per cubic meter", "kilogram per cubic meters", 1.0, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("ounce (avdp) per US gallon", "ounce (avdp) per US gallons", 7.489152, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("pound (avdp) per cubic foot", "pound (avdp) per cubic foots", 16.01846, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("pound (avdp) per US gallon", "pound (avdp) per US gallons", 119.826, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("pound (mass) per cubic inch", "pound (mass) per cubic inchs", 0.000276799, "$\\mathrm{kg} / \\mathrm{m}^{3}$"),
            ("ton (metric) per cubic meter", "ton (metric) per cubic meters", 1000.0, "$\\mathrm{kg} / \\mathrm{m}^{3}$")
        ],
        "field_name": "mass_density",
        "display_name": "Mass Density",
    },
    "MassFlowRate": {
        "dimension": MASS_FLOW_RATE,
        "default_unit": "kilograms per days",
        "units": [
            ("kilograms per day", "kilograms per days", 1.1574000000000001e-05, "kg/s"),
            ("kilograms per hour", "kilograms per hours", 0.00027778, "kg/s"),
            ("kilograms per minute", "kilograms per minutes", 0.016667, "kg/s"),
            ("kilograms per second", "kilograms per seconds", 1.0, "kg/s"),
            ("metric tons per day", "metric tons per days", 0.01157, "kg/s"),
            ("metric tons per hour", "metric tons per hours", 0.2778, "kg/s"),
            ("metric tons per minute", "metric tons per minutes", 16.67, "kg/s"),
            ("metric tons per second", "metric tons per seconds", 1000.0, "kg/s"),
            ("metric tons per year (365 d)", "metric tons per year (365 d)s", 3.171e-05, "kg/s"),
            ("pounds per day", "pounds per days", 5.248999999999999e-06, "kg/s"),
            ("pounds per hour", "pounds per hours", 0.00012598, "kg/s"),
            ("pounds per minute", "pounds per minutes", 0.0075586, "kg/s"),
            ("pounds per second", "pounds per seconds", 0.45351, "kg/s")
        ],
        "field_name": "mass_flow_rate",
        "display_name": "Mass Flow Rate",
    },
    "MassFlux": {
        "dimension": MASS_FLUX,
        "default_unit": "kilogram per square meter per days",
        "units": [
            ("kilogram per square meter per day", "kilogram per square meter per days", 1.1574000000000001e-05, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("kilogram per square meter per hour", "kilogram per square meter per hours", 0.00027778000000000004, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("kilogram per square meter per minute", "kilogram per square meter per minutes", 0.016667, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("kilogram per square meter per second", "kilogram per square meter per seconds", 1.0, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound per square foot per day", "pound per square foot per days", 5.6478000000000004e-05, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound per square foot per hour", "pound per square foot per hours", 0.0013555, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound per square foot per minute", "pound per square foot per minutes", 0.081329, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound per square foot per second", "pound per square foot per seconds", 4.8797, "kg/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )")
        ],
        "field_name": "mass_flux",
        "display_name": "Mass Flux",
    },
    "MassFractionOfI": {
        "dimension": MASS_FRACTION_OF_I,
        "default_unit": "grains of \"i\" per pound totals",
        "units": [
            ("grains of \"i\" per pound total", "grains of \"i\" per pound totals", 0.00014286, "$\\mathrm{kg}_{\\mathrm{i}} / \\mathrm{kg}$"),
            ("gram of \"i\" per kilogram total", "gram of \"i\" per kilogram totals", 0.001, "$\\mathrm{kg}_{\\mathrm{i}} / \\mathrm{kg}$"),
            ("kilogram of \"i\" per kilogram total", "kilogram of \"i\" per kilogram totals", 1.0, "$\\mathrm{kg}_{\\mathrm{i}} / \\mathrm{kg}$"),
            ("pound of \"i\" per pound total", "pound of \"i\" per pound totals", 1.0, "$\\mathrm{kg}_{\\mathrm{i}} / \\mathrm{kg}$")
        ],
        "field_name": "mass_fraction_of_i",
        "display_name": "Mass Fraction of \"i\"",
    },
    "MassTransferCoefficient": {
        "dimension": MASS_TRANSFER_COEFFICIENT,
        "default_unit": "gram per square centimeter per seconds",
        "units": [
            ("gram per square centimeter per second", "gram per square centimeter per seconds", 0.1, "$\\mathrm{kg} / \\mathrm{m}^{2} / \\mathrm{s}$"),
            ("kilogram per square meter per second", "kilogram per square meter per seconds", 1.0, "$\\mathrm{kg} / \\mathrm{m}^{2} / \\mathrm{s}$"),
            ("pounds force per cubic foot per hour", "pounds force per cubic foot per hours", 15.709, "$\\mathrm{kg} / \\mathrm{m}^{2} / \\mathrm{s}$"),
            ("pounds mass per square foot per hour", "pounds mass per square foot per hours", 0.00013562, "$\\mathrm{kg} / \\mathrm{m}^{2} / \\mathrm{s}$"),
            ("pounds mass per square foot per second", "pounds mass per square foot per seconds", 0.48824, "$\\mathrm{kg} / \\mathrm{m}^{2} / \\mathrm{s}$")
        ],
        "field_name": "mass_transfer_coefficient",
        "display_name": "Mass Transfer Coefficient",
    },
    "MolalityOfSoluteI": {
        "dimension": MOLALITY_OF_SOLUTE_I,
        "default_unit": "gram moles of \"i\" per kilograms",
        "units": [
            ("gram moles of \"i\" per kilogram", "gram moles of \"i\" per kilograms", 1.0, "$\\mathrm{mol}_{\\mathrm{i}} / \\mathrm{kg}$"),
            ("kilogram mols of \"i\" per kilogram", "kilogram mols of \"i\" per kilograms", 1000.0, "$\\mathrm{mol}_{\\mathrm{i}} / \\mathrm{kg}$"),
            ("kmols of \"i\" per kilogram", "kmols of \"i\" per kilograms", 1000.0, "$\\mathrm{mol}_{\\mathrm{i}} / \\mathrm{kg}$"),
            ("mols of \"i\" per gram", "mols of \"i\" per grams", 1000.0, "$\\mathrm{mol}_{\\mathrm{i}} / \\mathrm{kg}$"),
            ("pound moles of \"i\" per pound mass", "pound moles of \"i\" per pound masss", 1000.0, "$\\mathrm{mol}_{\\mathrm{i}} / \\mathrm{kg}$")
        ],
        "field_name": "molality_of_solute_i",
        "display_name": "Molality of Solute \"i\"",
    },
    "MolarConcentrationByMass": {
        "dimension": MOLAR_CONCENTRATION_BY_MASS,
        "default_unit": "gram mole or mole per grams",
        "units": [
            ("gram mole or mole per gram", "gram mole or mole per grams", 1.0, "kmol/kg"),
            ("gram mole or mole per kilogram", "gram mole or mole per kilograms", 0.001, "kmol/kg"),
            ("kilogram mole or kmol per kilogram", "kilogram mole or kmol per kilograms", 1.0, "kmol/kg"),
            ("micromole per gram", "micromole per grams", 1e-06, "kmol/kg"),
            ("millimole per gram", "millimole per grams", 0.001, "kmol/kg"),
            ("picomole per gram", "picomole per grams", 1e-12, "kmol/kg"),
            ("pound mole per pound", "pound mole per pounds", 1.0, "kmol/kg")
        ],
        "field_name": "molar_concentration_by_mass",
        "display_name": "Molar Concentration by Mass",
    },
    "MolarFlowRate": {
        "dimension": MOLAR_FLOW_RATE,
        "default_unit": "gram mole per days",
        "units": [
            ("gram mole per day", "gram mole per days", 4.167e-05, "kmol/h"),
            ("gram mole per hour", "gram mole per hours", 0.001, "kmol/h"),
            ("gram mole per minute", "gram mole per minutes", 0.06, "kmol/h"),
            ("gram mole per second", "gram mole per seconds", 3.6, "kmol/h"),
            ("kilogram mole or kmol per day", "kilogram mole or kmol per days", 0.04167, "kmol/h"),
            ("kilogram mole or kmol per hour", "kilogram mole or kmol per hours", 1.0, "kmol/h"),
            ("kilogram mole or kmol per minute", "kilogram mole or kmol per minutes", 60.0, "kmol/h"),
            ("kilogram mole or kmol per second", "kilogram mole or kmol per seconds", 3600.0, "kmol/h"),
            ("pound mole or lb-mol per day", "pound mole or lb-mol per days", 0.0189, "kmol/h"),
            ("pound mole or lb-mol per hour", "pound mole or lb-mol per hours", 0.4535, "kmol/h"),
            ("pound mole or lb-mol per minute", "pound mole or lb-mol per minutes", 27.21, "kmol/h"),
            ("pound mole or lb-mol per second", "pound mole or lb-mol per seconds", 1633.0, "kmol/h")
        ],
        "field_name": "molar_flow_rate",
        "display_name": "Molar Flow Rate",
    },
    "MolarFlux": {
        "dimension": MOLAR_FLUX,
        "default_unit": "kmol per square meter per days",
        "units": [
            ("kmol per square meter per day", "kmol per square meter per days", 1.1574000000000001e-05, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("kmol per square meter per hour", "kmol per square meter per hours", 0.00027778000000000004, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("kmol per square meter per minute", "kmol per square meter per minutes", 0.016667, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("kmol per square meter per second", "kmol per square meter per seconds", 1.0, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound mole per square foot per day", "pound mole per square foot per days", 5.6478000000000004e-05, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound mole per square foot per hour", "pound mole per square foot per hours", 0.0013555, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound mole per square foot per minute", "pound mole per square foot per minutes", 0.081329, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("pound mole per square foot per second", "pound mole per square foot per seconds", 4.8797, "kmol/ ( $\\mathrm{m}^{2} \\mathrm{~s}$ )")
        ],
        "field_name": "molar_flux",
        "display_name": "Molar Flux",
    },
    "MolarHeatCapacity": {
        "dimension": MOLAR_HEAT_CAPACITY,
        "default_unit": "Btu per pound mole per degree Fahrenheit (or degree Rankine)s",
        "units": [
            ("Btu per pound mole per degree Fahrenheit (or degree Rankine)", "Btu per pound mole per degree Fahrenheit (or degree Rankine)s", 4.1868, "J/ (mol K)"),
            ("calories per gram mole per kelvin (or degree Celsius)", "calories per gram mole per kelvin (or degree Celsius)s", 4.1868, "J/ (mol K)"),
            ("joule per gram mole per kelvin (or degree Celsius)", "joule per gram mole per kelvin (or degree Celsius)s", 1.0, "J/ (mol K)")
        ],
        "field_name": "molar_heat_capacity",
        "display_name": "Molar Heat Capacity",
    },
    "MolarityOfI": {
        "dimension": MOLARITY_OF_I,
        "default_unit": "gram moles of \"i\" per cubic meters",
        "units": [
            ("gram moles of \"i\" per cubic meter", "gram moles of \"i\" per cubic meters", 1.0, "$\\mathrm{mol} / \\mathrm{m}^{3}$"),
            ("gram moles of \"i\" per liter", "gram moles of \"i\" per liters", 1000.0, "$\\mathrm{mol} / \\mathrm{m}^{3}$"),
            ("kilogram moles of \"i\" per cubic meter", "kilogram moles of \"i\" per cubic meters", 1000.0, "$\\mathrm{mol} / \\mathrm{m}^{3}$"),
            ("kilogram moles of \"i\" per liter", "kilogram moles of \"i\" per liters", 1000000.0, "$\\mathrm{mol} / \\mathrm{m}^{3}$"),
            ("pound moles of \"i\" per cubic foot", "pound moles of \"i\" per cubic foots", 77844.0, "$\\mathrm{mol} / \\mathrm{m}^{3}$"),
            ("pound moles of \" $i$ \" per gallon (US)", "pound moles of \" $i$ \" per gallon (US)s", 10406.0, "$\\mathrm{mol} / \\mathrm{m}^{3}$")
        ],
        "field_name": "molarity_of_i",
        "display_name": "Molarity of \"i\"",
    },
    "MoleFractionOfI": {
        "dimension": MOLE_FRACTION_OF_I,
        "default_unit": "gram mole of \"i\" per gram mole totals",
        "units": [
            ("gram mole of \"i\" per gram mole total", "gram mole of \"i\" per gram mole totals", 1.0, "$\\mathrm{mol}_{\\mathrm{i}} /$ mol"),
            ("kilogram mole of \"i\" per kilogram mole total", "kilogram mole of \"i\" per kilogram mole totals", 1.0, "$\\mathrm{mol}_{\\mathrm{i}} /$ mol"),
            ("kilomole of \"i\" per kilomole total", "kilomole of \"i\" per kilomole totals", 1.0, "$\\mathrm{mol}_{\\mathrm{i}} /$ mol"),
            ("pound mole of \"i\" per pound mole total", "pound mole of \"i\" per pound mole totals", 1.0, "$\\mathrm{mol}_{\\mathrm{i}} /$ mol")
        ],
        "field_name": "mole_fraction_of_i",
        "display_name": "Mole Fraction of \"i\"",
    },
    "MomentOfInertia": {
        "dimension": MOMENT_OF_INERTIA,
        "default_unit": "gram force centimeter square seconds",
        "units": [
            ("gram force centimeter square second", "gram force centimeter square seconds", 9.8067e-05, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("gram square centimeter", "gram square centimeters", 1e-07, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("kilogram force centimeter square second", "kilogram force centimeter square seconds", 0.098067, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("kilogram force meter square second", "kilogram force meter square seconds", 9.8067, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("kilogram square centimeter", "kilogram square centimeters", 0.0001, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("kilogram square meter", "kilogram square meters", 1.0, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("ounce force inch square second", "ounce force inch square seconds", 0.0070616, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("ounce mass square inch", "ounce mass square inchs", 1.8290000000000003e-05, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("pound mass square foot", "pound mass square foots", 0.04214, "$\\mathrm{kg} \\mathrm{m}^{2}$"),
            ("pound mass square inch", "pound mass square inchs", 0.00029264000000000004, "$\\mathrm{kg} \\mathrm{m}^{2}$")
        ],
        "field_name": "moment_of_inertia",
        "display_name": "Moment of Inertia",
    },
    "MomentumFlowRate": {
        "dimension": MOMENTUM_FLOW_RATE,
        "default_unit": "foot pounds per square hours",
        "units": [
            ("foot pounds per square hour", "foot pounds per square hours", 1.0671e-08, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}^{2}$"),
            ("foot pounds per square minute", "foot pounds per square minutes", 3.8417e-05, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}^{2}$"),
            ("foot pounds per square second", "foot pounds per square seconds", 0.1383, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}^{2}$"),
            ("gram centimeters per square second", "gram centimeters per square seconds", 1e-05, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}^{2}$"),
            ("kilogram meters per square second", "kilogram meters per square seconds", 1.0, "$\\mathrm{kg} \\mathrm{m} / \\mathrm{s}^{2}$")
        ],
        "field_name": "momentum_flow_rate",
        "display_name": "Momentum Flow Rate",
    },
    "MomentumFlux": {
        "dimension": MOMENTUM_FLUX,
        "default_unit": "dyne per square centimeters",
        "units": [
            ("dyne per square centimeter", "dyne per square centimeters", 10.0, "$\\mathrm{N} / \\mathrm{m}^{2}$"),
            ("gram per centimeter per square second", "gram per centimeter per square seconds", 10.0, "$\\mathrm{N} / \\mathrm{m}^{2}$"),
            ("newton per square meter", "newton per square meters", 1.0, "$\\mathrm{N} / \\mathrm{m}^{2}$"),
            ("pound force per square foot", "pound force per square foots", 478.8, "$\\mathrm{N} / \\mathrm{m}^{2}$"),
            ("pound mass per foot per square second", "pound mass per foot per square seconds", 14.882, "$\\mathrm{N} / \\mathrm{m}^{2}$")
        ],
        "field_name": "momentum_flux",
        "display_name": "Momentum Flux",
    },
    "NormalityOfSolution": {
        "dimension": NORMALITY_OF_SOLUTION,
        "default_unit": "gram equivalents per cubic meters",
        "units": [
            ("gram equivalents per cubic meter", "gram equivalents per cubic meters", 1.0, "$\\mathrm{eq}_{\\mathrm{i}} / \\mathrm{m}^{3}$"),
            ("gram equivalents per liter", "gram equivalents per liters", 1000.0, "$\\mathrm{eq}_{\\mathrm{i}} / \\mathrm{m}^{3}$"),
            ("pound equivalents per cubic foot", "pound equivalents per cubic foots", 77844.0, "$\\mathrm{eq}_{\\mathrm{i}} / \\mathrm{m}^{3}$"),
            ("pound equivalents per gallon", "pound equivalents per gallons", 10406.0, "$\\mathrm{eq}_{\\mathrm{i}} / \\mathrm{m}^{3}$")
        ],
        "field_name": "normality_of_solution",
        "display_name": "Normality of Solution",
    },
    "ParticleDensity": {
        "dimension": PARTICLE_DENSITY,
        "default_unit": "particles per cubic centimeters",
        "units": [
            ("particles per cubic centimeter", "particles per cubic centimeters", 10000.0, "part $/ \\mathrm{m}^{3}$"),
            ("particles per cubic foot", "particles per cubic foots", 35.31, "part $/ \\mathrm{m}^{3}$"),
            ("particles per cubic meter", "particles per cubic meters", 1.0, "part $/ \\mathrm{m}^{3}$"),
            ("particles per gallon (US)", "particles per gallon (US)s", 264.14, "part $/ \\mathrm{m}^{3}$"),
            ("particles per liter", "particles per liters", 1000.0, "part $/ \\mathrm{m}^{3}$"),
            ("particles per milliliter", "particles per milliliters", 10000.0, "part $/ \\mathrm{m}^{3}$")
        ],
        "field_name": "particle_density",
        "display_name": "Particle Density",
    },
    "Permeability": {
        "dimension": PERMEABILITY,
        "default_unit": "darcys",
        "units": [
            ("darcy", "darcys", 9.8692e-13, "m2"),
            ("square feet", "square feets", 0.0929, "m2"),
            ("square meters", "square meterss", 1.0, "m2")
        ],
        "field_name": "permeability",
        "display_name": "Permeability",
    },
    "PhotonEmissionRate": {
        "dimension": PHOTON_EMISSION_RATE,
        "default_unit": "rayleighs",
        "units": [
            ("rayleigh", "rayleighs", 10000000000.0, "1/ ( $\\mathrm{m}^{2} \\mathrm{sec}$ )"),
            ("reciprocal square meter second", "reciprocal square meter seconds", 1.0, "1/ ( $\\mathrm{m}^{2} \\mathrm{sec}$ )")
        ],
        "field_name": "photon_emission_rate",
        "display_name": "Photon Emission Rate",
    },
    "PowerPerUnitMass": {
        "dimension": POWER_PER_UNIT_MASS,
        "default_unit": "British thermal unit per hour per pound masss",
        "units": [
            ("British thermal unit per hour per pound mass", "British thermal unit per hour per pound masss", 0.64612, "W/kg"),
            ("calorie per second per gram", "calorie per second per grams", 4186.8, "W/kg"),
            ("kilocalorie per hour per kilogram", "kilocalorie per hour per kilograms", 1.163, "W/kg"),
            ("watt per kilogram", "watt per kilograms", 1.0, "W/kg")
        ],
        "field_name": "power_per_unit_mass",
        "display_name": "Power per Unit Mass or Specific Power",
    },
    "PowerPerUnitVolume": {
        "dimension": POWER_PER_UNIT_VOLUME,
        "default_unit": "British thermal unit per hour per cubic foots",
        "units": [
            ("British thermal unit per hour per cubic foot", "British thermal unit per hour per cubic foots", 10.35, "$\\mathrm{W} / \\mathrm{m}^{3}$"),
            ("calorie per second per cubic centimeter", "calorie per second per cubic centimeters", 4186800.0, "$\\mathrm{W} / \\mathrm{m}^{3}$"),
            ("Chu per hour per cubic foot", "Chu per hour per cubic foots", 18.63, "$\\mathrm{W} / \\mathrm{m}^{3}$"),
            ("kilocalorie per hour per cubic centimeter", "kilocalorie per hour per cubic centimeters", 1.163, "$\\mathrm{W} / \\mathrm{m}^{3}$"),
            ("kilocalorie per hour per cubic foot", "kilocalorie per hour per cubic foots", 41.071, "$\\mathrm{W} / \\mathrm{m}^{3}$"),
            ("kilocalorie per second per cubic centimeter", "kilocalorie per second per cubic centimeters", 4186800000.0, "$\\mathrm{W} / \\mathrm{m}^{3}$"),
            ("watt per cubic meter", "watt per cubic meters", 1.0, "$\\mathrm{W} / \\mathrm{m}^{3}$")
        ],
        "field_name": "power_per_unit_volume",
        "display_name": "Power per Unit Volume or Power Density",
    },
    "PowerThermalDuty": {
        "dimension": POWER_THERMAL_DUTY,
        "default_unit": "abwatt (emu of power)s",
        "units": [
            ("abwatt (emu of power)", "abwatt (emu of power)s", 1e-08, "W"),
            ("boiler horsepower", "boiler horsepowers", 9809.5, "W"),
            ("British thermal unit (mean) per hour", "British thermal unit (mean) per hours", 0.293297, "W"),
            ("British thermal unit (mean) per minute", "British thermal unit (mean) per minutes", 17.597833, "W"),
            ("British thermal unit (thermochemical) per hour", "British thermal unit (thermochemical) per hours", 0.292875, "W"),
            ("British thermal unit (thermochemical) per minute", "British thermal unit (thermochemical) per minutes", 17.5725, "W"),
            ("calorie (mean) per hour", "calorie (mean) per hours", 0.00116389, "W"),
            ("calorie (thermochemical) per hour", "calorie (thermochemical) per hours", 0.00116222, "W"),
            ("donkey", "donkeys", 250.0, "W"),
            ("erg per second", "erg per seconds", 1e-07, "W"),
            ("foot pondal per second", "foot pondal per seconds", 0.04214, "W"),
            ("foot pound force per hour", "foot pound force per hours", 0.00037044000000000004, "W"),
            ("foot pound force per minute", "foot pound force per minutes", 0.022597, "W"),
            ("foot pound force per second", "foot pound force per seconds", 1.355818, "W"),
            ("horsepower ( $550 \\mathrm{ft} \\mathrm{lb}_{\\mathrm{f}} / \\mathrm{s}$ )", "horsepower ( $550 \\mathrm{ft} \\mathrm{lb}_{\\mathrm{f}} / \\mathrm{s}$ )s", 745.7, "W"),
            ("horsepower (electric)", "horsepower (electric)s", 746.0, "W"),
            ("horsepower (UK)", "horsepower (UK)s", 745.7, "W"),
            ("kcal per hour", "kcal per hours", 1.16389, "W"),
            ("kilogram force meter per second", "kilogram force meter per seconds", 9.80665, "W"),
            ("kilowatt", "kilowatts", 1000.0, "W"),
            ("megawatt", "megawatts", 1000000.0, "W"),
            ("metric horsepower", "metric horsepowers", 735.499, "W"),
            ("million British thermal units per hour (petroleum)", "million British thermal units per hour (petroleum)s", 293297.0, "W"),
            ("million kilocalorie per hour", "million kilocalorie per hours", 1163890.0, "W"),
            ("prony", "pronys", 98.0665, "W"),
            ("ton of refrigeration (US)", "ton of refrigeration (US)s", 3516.8, "W"),
            ("ton or refrigeration (UK)", "ton or refrigeration (UK)s", 3922.7, "W"),
            ("volt-ampere", "volt-amperes", 1.0, "W"),
            ("water horsepower", "water horsepowers", 746.043, "W"),
            ("watt", "watts", 1.0, "W"),
            ("watt (international, mean)", "watt (international, mean)s", 1.00019, "W"),
            ("watt (international, US)", "watt (international, US)s", 1.000165, "W")
        ],
        "field_name": "power_thermal_duty",
        "display_name": "Power, Thermal Duty",
    },
    "Pressure": {
        "dimension": PRESSURE,
        "default_unit": "atmosphere, standards",
        "units": [
            ("atmosphere, standard", "atmosphere, standards", 101325.0, "Pa"),
            ("bar", "bars", 100000.0, "Pa"),
            ("barye", "baryes", 0.1, "Pa"),
            ("dyne per square centimeter", "dyne per square centimeters", 0.1, "Pa"),
            ("foot of mercury ( $60{ }^{\\circ} \\mathrm{F}$ )", "foot of mercury ( $60{ }^{\\circ} \\mathrm{F}$ )s", 40526.0, "Pa"),
            ("foot of water ( $60{ }^{\\circ} \\mathrm{F}$ )", "foot of water ( $60{ }^{\\circ} \\mathrm{F}$ )s", 2989.0, "Pa"),
            ("gigapascal", "gigapascals", 1000000000.0, "Pa"),
            ("hectopascal", "hectopascals", 100.0, "Pa"),
            ("inch of mercury ( $60{ }^{\\circ} \\mathrm{F}$ )", "inch of mercury ( $60{ }^{\\circ} \\mathrm{F}$ )s", 3386.4, "Pa"),
            ("inch of water ( $60{ }^{\\circ} \\mathrm{F}$ )", "inch of water ( $60{ }^{\\circ} \\mathrm{F}$ )s", 248.845, "Pa"),
            ("kilogram force per square centimeter", "kilogram force per square centimeters", 98067.0, "Pa"),
            ("kilogram force per square meter", "kilogram force per square meters", 9.80665, "Pa"),
            ("kip force per square inch", "kip force per square inchs", 6894800.0, "Pa"),
            ("megapascal", "megapascals", 1000000.0, "Pa"),
            ("meter of water ( $4^{\\circ} \\mathrm{C}$ )", "meter of water ( $4^{\\circ} \\mathrm{C}$ )s", 9806.4, "Pa"),
            ("microbar", "microbars", 0.1, "Pa"),
            ("millibar", "millibars", 100.0, "Pa"),
            ("millimeter of mercury ( $4^{\\circ} \\mathrm{C}$ )", "millimeter of mercury ( $4^{\\circ} \\mathrm{C}$ )s", 133.322, "Pa"),
            ("millimeter of water ( $4^{\\circ} \\mathrm{C}$ )", "millimeter of water ( $4^{\\circ} \\mathrm{C}$ )s", 9.806375, "Pa"),
            ("newton per square meter", "newton per square meters", 1.0, "Pa"),
            ("ounce force per square inch", "ounce force per square inchs", 430.922, "Pa"),
            ("pascal", "pascals", 1.0, "Pa"),
            ("pièze", "pièzes", 1000.0, "Pa"),
            ("pound force per square foot", "pound force per square foots", 47.880259, "Pa"),
            ("pound force per square inch", "pound force per square inchs", 6894.8, "Pa"),
            ("torr", "torrs", 133.322, "Pa")
        ],
        "field_name": "pressure",
        "display_name": "Pressure",
    },
    "RadiationDoseEquivalent": {
        "dimension": RADIATION_DOSE_EQUIVALENT,
        "default_unit": "rems",
        "units": [
            ("rem", "rems", 0.01, "Sv"),
            ("sievert", "sieverts", 1.0, "Sv")
        ],
        "field_name": "radiation_dose_equivalent",
        "display_name": "Radiation Dose Equivalent",
    },
    "RadiationExposure": {
        "dimension": RADIATION_EXPOSURE,
        "default_unit": "coulomb per kilograms",
        "units": [
            ("coulomb per kilogram", "coulomb per kilograms", 1.0, "C/kg"),
            ("D unit", "D units", 0.0258, "C/kg"),
            ("pastille dose (B unit)", "pastille dose (B unit)s", 0.129, "C/kg"),
            ("röentgen", "röentgens", 0.000258, "C/kg")
        ],
        "field_name": "radiation_exposure",
        "display_name": "Radiation Exposure",
    },
    "Radioactivity": {
        "dimension": RADIOACTIVITY,
        "default_unit": "becquerels",
        "units": [
            ("becquerel", "becquerels", 1.0, "Bq"),
            ("curie", "curies", 37000000000.0, "Bq"),
            ("Mache unit", "Mache units", 13.32, "Bq"),
            ("rutherford", "rutherfords", 1000000.0, "Bq"),
            ("stat", "stats", 1.34e-16, "Bq")
        ],
        "field_name": "radioactivity",
        "display_name": "Radioactivity",
    },
    "SecondMomentOfArea": {
        "dimension": SECOND_MOMENT_OF_AREA,
        "default_unit": "inch quadrupleds",
        "units": [
            ("inch quadrupled", "inch quadrupleds", 4.1623e-07, "$\\mathrm{m}^{4}$"),
            ("centimeter quadrupled", "centimeter quadrupleds", 1e-08, "$\\mathrm{m}^{4}$"),
            ("foot quadrupled", "foot quadrupleds", 0.008631, "$\\mathrm{m}^{4}$"),
            ("meter quadrupled", "meter quadrupleds", 1.0, "$\\mathrm{m}^{4}$")
        ],
        "field_name": "second_moment_of_area",
        "display_name": "Second Moment of Area",
    },
    "SecondRadiationConstantPlanck": {
        "dimension": SECOND_RADIATION_CONSTANT_PLANCK,
        "default_unit": "meter kelvins",
        "units": [
            ("meter kelvin", "meter kelvins", 1.0, "m K")
        ],
        "field_name": "second_radiation_constant_planck",
        "display_name": "Second Radiation Constant (Planck)",
    },
    "SpecificEnthalpy": {
        "dimension": SPECIFIC_ENTHALPY,
        "default_unit": "British thermal unit (mean) per pounds",
        "units": [
            ("British thermal unit (mean) per pound", "British thermal unit (mean) per pounds", 2327.8, "J/kg"),
            ("British thermal unit per pound", "British thermal unit per pounds", 2324.4, "J/kg"),
            ("calorie per gram", "calorie per grams", 4186.8, "J/kg"),
            ("Chu per pound", "Chu per pounds", 4186.8, "J/kg"),
            ("joule per kilogram", "joule per kilograms", 1.0, "J/kg"),
            ("kilojoule per kilogram", "kilojoule per kilograms", 1000.0, "J/kg")
        ],
        "field_name": "specific_enthalpy",
        "display_name": "Specific Enthalpy",
    },
    "SpecificGravity": {
        "dimension": SPECIFIC_GRAVITY,
        "default_unit": "Dimensionlesss",
        "units": [
            ("Dimensionless", "Dimensionlesss", 1.0, "Dmls")
        ],
        "field_name": "specific_gravity",
        "display_name": "Specific Gravity",
    },
    "SpecificHeatCapacityConstantPressure": {
        "dimension": SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE,
        "default_unit": "Btu per pound per degree Fahrenheit (or degree Rankine)s",
        "units": [
            ("Btu per pound per degree Fahrenheit (or degree Rankine)", "Btu per pound per degree Fahrenheit (or degree Rankine)s", 4186.8, "J/(kg K)"),
            ("calories per gram per kelvin (or degree Celsius)", "calories per gram per kelvin (or degree Celsius)s", 4186.8, "J/(kg K)"),
            ("joules per kilogram per kelvin (or degree Celsius)", "joules per kilogram per kelvin (or degree Celsius)s", 1.0, "J/(kg K)")
        ],
        "field_name": "specific_heat_capacity_constant_pressure",
        "display_name": "Specific Heat Capacity (Constant Pressure)",
    },
    "SpecificLength": {
        "dimension": SPECIFIC_LENGTH,
        "default_unit": "centimeter per grams",
        "units": [
            ("centimeter per gram", "centimeter per grams", 10.0, "m/kg"),
            ("cotton count", "cotton counts", 590500000.0, "m/kg"),
            ("ft per pound", "ft per pounds", 0.67192, "m/kg"),
            ("meters per kilogram", "meters per kilograms", 1.0, "m/kg"),
            ("newton meter", "newton meters", 1000.0, "m/kg"),
            ("worsted", "worsteds", 888679999.9999999, "m/kg")
        ],
        "field_name": "specific_length",
        "display_name": "Specific Length",
    },
    "SpecificSurface": {
        "dimension": SPECIFIC_SURFACE,
        "default_unit": "square centimeter per grams",
        "units": [
            ("square centimeter per gram", "square centimeter per grams", 0.1, "$\\mathrm{m}^{2} / \\mathrm{kg}$"),
            ("square foot per kilogram", "square foot per kilograms", 0.092903, "$\\mathrm{m}^{2} / \\mathrm{kg}$"),
            ("square foot per pound", "square foot per pounds", 0.20482, "$\\mathrm{m}^{2} / \\mathrm{kg}$"),
            ("square meter per gram", "square meter per grams", 1000.0, "$\\mathrm{m}^{2} / \\mathrm{kg}$"),
            ("square meter per kilogram", "square meter per kilograms", 1.0, "$\\mathrm{m}^{2} / \\mathrm{kg}$")
        ],
        "field_name": "specific_surface",
        "display_name": "Specific Surface",
    },
    "SpecificVolume": {
        "dimension": SPECIFIC_VOLUME,
        "default_unit": "cubic centimeter per grams",
        "units": [
            ("cubic centimeter per gram", "cubic centimeter per grams", 0.001, "$\\mathrm{m}^{3} / \\mathrm{kg}$"),
            ("cubic foot per kilogram", "cubic foot per kilograms", 0.028317, "$\\mathrm{m}^{3} / \\mathrm{kg}$"),
            ("cubic foot per pound", "cubic foot per pounds", 0.062428, "$\\mathrm{m}^{3} / \\mathrm{kg}$"),
            ("cubic meter per kilogram", "cubic meter per kilograms", 1.0, "$\\mathrm{m}^{3} / \\mathrm{kg}$")
        ],
        "field_name": "specific_volume",
        "display_name": "Specific Volume",
    },
    "Stress": {
        "dimension": STRESS,
        "default_unit": "dyne per square centimeters",
        "units": [
            ("dyne per square centimeter", "dyne per square centimeters", 0.1, "Pa"),
            ("gigapascal", "gigapascals", 1000000000.0, "Pa"),
            ("hectopascal", "hectopascals", 100.0, "Pa"),
            ("kilogram force per square centimeter", "kilogram force per square centimeters", 98067.0, "Pa"),
            ("kilogram force per square meter", "kilogram force per square meters", 9.80665, "Pa"),
            ("kip force per square inch", "kip force per square inchs", 6894800.0, "Pa"),
            ("megapascal", "megapascals", 1000000.0, "Pa"),
            ("newton per square meter", "newton per square meters", 1.0, "Pa"),
            ("ounce force per square inch", "ounce force per square inchs", 430.922, "Pa"),
            ("pascal", "pascals", 1.0, "Pa"),
            ("pound force per square foot", "pound force per square foots", 47.880259, "Pa"),
            ("pound force per square inch", "pound force per square inchs", 6894.8, "Pa")
        ],
        "field_name": "stress",
        "display_name": "Stress",
    },
    "SurfaceMassDensity": {
        "dimension": SURFACE_MASS_DENSITY,
        "default_unit": "gram per square centimeters",
        "units": [
            ("gram per square centimeter", "gram per square centimeters", 10.0, "$\\mathrm{kg} / \\mathrm{m}^{2}$"),
            ("gram per square meter", "gram per square meters", 0.001, "$\\mathrm{kg} / \\mathrm{m}^{2}$"),
            ("kilogram per square meter", "kilogram per square meters", 1.0, "$\\mathrm{kg} / \\mathrm{m}^{2}$"),
            ("pound (mass) per square foot", "pound (mass) per square foots", 4.882427, "$\\mathrm{kg} / \\mathrm{m}^{2}$"),
            ("pound (mass) per square inch", "pound (mass) per square inchs", 703.07, "$\\mathrm{kg} / \\mathrm{m}^{2}$")
        ],
        "field_name": "surface_mass_density",
        "display_name": "Surface Mass Density",
    },
    "SurfaceTension": {
        "dimension": SURFACE_TENSION,
        "default_unit": "dyne per centimeters",
        "units": [
            ("dyne per centimeter", "dyne per centimeters", 0.001, "N/m"),
            ("gram force per centimeter", "gram force per centimeters", 0.0102, "N/m"),
            ("newton per meter", "newton per meters", 1.0, "N/m"),
            ("pound force per foot", "pound force per foots", 14.594, "N/m"),
            ("pound force per inch", "pound force per inchs", 175.13, "N/m")
        ],
        "field_name": "surface_tension",
        "display_name": "Surface Tension",
    },
    "Temperature": {
        "dimension": TEMPERATURE,
        "default_unit": "degree Celsius (unit size)s",
        "units": [
            ("degree Celsius (unit size)", "degree Celsius (unit size)s", 1.0, "K"),
            ("degree Fahrenheit (unit size)", "degree Fahrenheit (unit size)s", 0.555556, "K"),
            ("degree Réaumur (unit size)", "degree Réaumur (unit size)s", 1.25, "K"),
            ("kelvin (absolute scale)", "kelvin (absolute scale)s", 1.0, "K"),
            ("Rankine (absolute scale)", "Rankine (absolute scale)s", 0.555556, "K")
        ],
        "field_name": "temperature",
        "display_name": "Temperature",
    },
    "ThermalConductivity": {
        "dimension": THERMAL_CONDUCTIVITY,
        "default_unit": "Btu (IT) per inch per hour per degree Fahrenheits",
        "units": [
            ("Btu (IT) per inch per hour per degree Fahrenheit", "Btu (IT) per inch per hour per degree Fahrenheits", 0.207688, "W/ (cm K)"),
            ("Btu (therm) per foot per hour per degree Fahrenheit", "Btu (therm) per foot per hour per degree Fahrenheits", 0.017296, "W/ (cm K)"),
            ("Btu (therm) per inch per hour per degree Fahrenheit", "Btu (therm) per inch per hour per degree Fahrenheits", 0.207549, "W/ (cm K)"),
            ("calorie (therm) per centimeter per second per degree Celsius", "calorie (therm) per centimeter per second per degree Celsiuss", 4.184, "W/ (cm K)"),
            ("joule per second per centimeter per kelvin", "joule per second per centimeter per kelvins", 0.01, "W/ (cm K)"),
            ("watt per centimeter per kelvin", "watt per centimeter per kelvins", 1.0, "W/ (cm K)"),
            ("watt per meter per kelvin", "watt per meter per kelvins", 0.01, "W/ (cm K)")
        ],
        "field_name": "thermal_conductivity",
        "display_name": "Thermal Conductivity",
    },
    "Time": {
        "dimension": TIME,
        "default_unit": "blinks",
        "units": [
            ("blink", "blinks", 0.864, "s"),
            ("century", "centurys", 3155800000.0, "s"),
            ("chronon or tempon", "chronon or tempons", 1e-23, "s"),
            ("gigan or eon", "gigan or eons", 3.1558e+16, "s"),
            ("hour", "hours", 3600.0, "s"),
            ("Julian year", "Julian years", 31557000.0, "s"),
            ("mean solar day", "mean solar days", 86400.0, "s"),
            ("millenium", "milleniums", 31558000000.0, "s"),
            ("minute", "minutes", 60.0, "s"),
            ("second", "seconds", 1.0, "s"),
            ("shake", "shakes", 1e-08, "s"),
            ("sidereal year (1900 AD)", "sidereal year (1900 AD)s", 31551999.999999996, "s"),
            ("tropical year", "tropical years", 31557000.0, "s"),
            ("wink", "winks", 3.33333e-12, "s"),
            ("year", "years", 31558000.0, "s")
        ],
        "field_name": "time",
        "display_name": "Time",
    },
    "Torque": {
        "dimension": TORQUE,
        "default_unit": "centimeter kilogram forces",
        "units": [
            ("centimeter kilogram force", "centimeter kilogram forces", 0.098067, "N m"),
            ("dyne centimeter", "dyne centimeters", 1e-07, "N m"),
            ("foot kilogram force", "foot kilogram forces", 2.9891, "N m"),
            ("foot pound force", "foot pound forces", 1.3558, "N m"),
            ("foot poundal", "foot poundals", 0.04214, "N m"),
            ("in pound force", "in pound forces", 0.11298, "N m"),
            ("inch ounce force", "inch ounce forces", 0.0070616, "N m"),
            ("meter kilogram force", "meter kilogram forces", 9.8067, "Nm"),
            ("newton centimeter", "newton centimeters", 0.01, "N m"),
            ("newton meter", "newton meters", 1.0, "N m")
        ],
        "field_name": "torque",
        "display_name": "Torque",
    },
    "TurbulenceEnergyDissipationRate": {
        "dimension": TURBULENCE_ENERGY_DISSIPATION_RATE,
        "default_unit": "square foot per cubic seconds",
        "units": [
            ("square foot per cubic second", "square foot per cubic seconds", 0.0929, "$\\mathrm{m}^{2} / \\mathrm{s}^{3}$"),
            ("square meter per cubic second", "square meter per cubic seconds", 1.0, "$\\mathrm{m}^{2} / \\mathrm{s}^{3}$")
        ],
        "field_name": "turbulence_energy_dissipation_rate",
        "display_name": "Turbulence Energy Dissipation Rate",
    },
    "VelocityAngular": {
        "dimension": VELOCITY_ANGULAR,
        "default_unit": "degree per minutes",
        "units": [
            ("degree per minute", "degree per minutes", 0.000290888, "$\\mathrm{rad} / \\mathrm{s}$"),
            ("degree per second", "degree per seconds", 0.0174533, "$\\mathrm{rad} / \\mathrm{s}$"),
            ("grade per minute", "grade per minutes", 0.000261799, "$\\mathrm{rad} / \\mathrm{s}$"),
            ("radian per minute", "radian per minutes", 0.016667, "$\\mathrm{rad} / \\mathrm{s}$"),
            ("radian per second", "radian per seconds", 1.0, "$\\mathrm{rad} / \\mathrm{s}$"),
            ("revolution per minute", "revolution per minutes", 0.010472, "$\\mathrm{rad} / \\mathrm{s}$"),
            ("revolution per second", "revolution per seconds", 6.283185, "$\\mathrm{rad} / \\mathrm{s}$"),
            ("turn per minute", "turn per minutes", 0.010472, "$\\mathrm{rad} / \\mathrm{s}$")
        ],
        "field_name": "velocity_angular",
        "display_name": "Velocity, Angular",
    },
    "VelocityLinear": {
        "dimension": VELOCITY_LINEAR,
        "default_unit": "foot per hours",
        "units": [
            ("foot per hour", "foot per hours", 8.4667e-05, "$\\mathrm{m} / \\mathrm{s}$"),
            ("foot per minute", "foot per minutes", 0.00508, "$\\mathrm{m} / \\mathrm{s}$"),
            ("foot per second", "foot per seconds", 0.3048, "$\\mathrm{m} / \\mathrm{s}$"),
            ("inch per second", "inch per seconds", 0.0254, "$\\mathrm{m} / \\mathrm{s}$"),
            ("international knot", "international knots", 0.0514444, "$\\mathrm{m} / \\mathrm{s}$"),
            ("kilometer per hour", "kilometer per hours", 0.027778, "$\\mathrm{m} / \\mathrm{s}$"),
            ("kilometer per second", "kilometer per seconds", 1000.0, "$\\mathrm{m} / \\mathrm{s}$"),
            ("meter per second", "meter per seconds", 1.0, "$\\mathrm{m} / \\mathrm{s}$"),
            ("mile per hour", "mile per hours", 0.0444704, "$\\mathrm{m} / \\mathrm{s}$")
        ],
        "field_name": "velocity_linear",
        "display_name": "Velocity, Linear",
    },
    "ViscosityDynamic": {
        "dimension": VISCOSITY_DYNAMIC,
        "default_unit": "centipoises",
        "units": [
            ("centipoise", "centipoises", 0.01, "P"),
            ("dyne second per square centimeter", "dyne second per square centimeters", 1.0, "P"),
            ("kilopound second per square meter", "kilopound second per square meters", 98.0665, "P"),
            ("millipoise", "millipoises", 0.001, "P"),
            ("newton second per square meter", "newton second per square meters", 10.0, "P"),
            ("pascal second", "pascal seconds", 10.0, "P"),
            ("poise", "poises", 1.0, "P"),
            ("pound force hour per square foot", "pound force hour per square foots", 1723690.0, "P"),
            ("pound force second per square foot", "pound force second per square foots", 478.803, "P")
        ],
        "field_name": "viscosity_dynamic",
        "display_name": "Viscosity, Dynamic",
    },
    "ViscosityKinematic": {
        "dimension": VISCOSITY_KINEMATIC,
        "default_unit": "centistokess",
        "units": [
            ("centistokes", "centistokess", 1e-06, "$\\mathrm{m}^{2} / \\mathrm{s}$"),
            ("millistokes", "millistokess", 1e-07, "$\\mathrm{m}^{2} / \\mathrm{s}$"),
            ("square centimeter per second", "square centimeter per seconds", 0.0001, "$\\mathrm{m}^{2} / \\mathrm{s}$"),
            ("square foot per hour", "square foot per hours", 2.58064e-05, "$\\mathrm{m}^{2} / \\mathrm{s}$"),
            ("square foot per second", "square foot per seconds", 0.092903, "$\\mathrm{m}^{2} / \\mathrm{s}$"),
            ("square meters per second", "square meters per seconds", 1.0, "$\\mathrm{m}^{2} / \\mathrm{s}$"),
            ("stokes", "stokess", 0.0001, "$\\mathrm{m}^{2} / \\mathrm{s}$")
        ],
        "field_name": "viscosity_kinematic",
        "display_name": "Viscosity, Kinematic",
    },
    "Volume": {
        "dimension": VOLUME,
        "default_unit": "acre foots",
        "units": [
            ("acre foot", "acre foots", 1233.48, "$\\mathrm{m}^{3}$"),
            ("acre inch", "acre inchs", 102.79, "$\\mathrm{m}^{3}$"),
            ("barrel (US Liquid)", "barrel (US Liquid)s", 0.1192405, "$\\mathrm{m}^{3}$"),
            ("barrel (US, Petro)", "barrel (US, Petro)s", 0.158987, "$\\mathrm{m}^{3}$"),
            ("board foot measure", "board foot measures", 0.00235974, "$\\mathrm{m}^{3}$"),
            ("bushel (US Dry)", "bushel (US Dry)s", 0.0352391, "$\\mathrm{m}^{3}$"),
            ("centiliter", "centiliters", 1e-05, "$\\mathrm{m}^{3}$"),
            ("cord", "cords", 3.62456, "$\\mathrm{m}^{3}$"),
            ("cord foot", "cord foots", 0.4530695, "$\\mathrm{m}^{3}$"),
            ("cubic centimeter", "cubic centimeters", 1e-06, "$\\mathrm{m}^{3}$"),
            ("cubic decameter", "cubic decameters", 1000.0, "$\\mathrm{m}^{3}$"),
            ("cubic decimeter", "cubic decimeters", 0.001, "$\\mathrm{m}^{3}$"),
            ("cubic foot", "cubic foots", 0.0283168, "$\\mathrm{m}^{3}$"),
            ("cubic inch", "cubic inchs", 1.63871e-05, "$\\mathrm{m}^{3}$"),
            ("cubic kilometer", "cubic kilometers", 1000000000.0, "$\\mathrm{m}^{3}$"),
            ("cubic meter", "cubic meters", 1.0, "$\\mathrm{m}^{3}$"),
            ("cubic micrometer", "cubic micrometers", 1e-18, "$\\mathrm{m}^{3}$"),
            ("cubic mile (US, Intl)", "cubic mile (US, Intl)s", 4168180000.0000005, "$\\mathrm{m}^{3}$"),
            ("cubic millimeter", "cubic millimeters", 1e-09, "$\\mathrm{m}^{3}$"),
            ("cubic yard", "cubic yards", 0.7645549, "$\\mathrm{m}^{3}$"),
            ("decastére", "decastéres", 10.0, "$\\mathrm{m}^{3}$"),
            ("deciliter", "deciliters", 0.0001, "$\\mathrm{m}^{3}$"),
            ("fluid drachm (UK)", "fluid drachm (UK)s", 3.5516299999999996e-06, "$\\mathrm{m}^{3}$"),
            ("fluid dram (US)", "fluid dram (US)s", 3.69669e-06, "$\\mathrm{m}^{3}$"),
            ("fluid ounce (US)", "fluid ounce (US)s", 2.95735e-05, "$\\mathrm{m}^{3}$"),
            ("gallon (Imperial UK)", "gallon (Imperial UK)s", 0.00454609, "$\\mathrm{m}^{3}$"),
            ("gallon (US Dry)", "gallon (US Dry)s", 0.004404884, "$\\mathrm{m}^{3}$"),
            ("gallon (US Liquid)", "gallon (US Liquid)s", 0.003785412, "$\\mathrm{m}^{3}$"),
            ("last", "lasts", 2.9095, "$\\mathrm{m}^{3}$"),
            ("liter", "liters", 0.001, "$\\mathrm{m}^{3}$"),
            ("microliter", "microliters", 1e-09, "$\\mathrm{m}^{3}$"),
            ("milliliter", "milliliters", 1e-06, "$\\mathrm{m}^{3}$"),
            ("Mohr centicube", "Mohr centicubes", 1.00238e-06, "$\\mathrm{m}^{3}$"),
            ("pint (UK)", "pint (UK)s", 0.000568262, "$\\mathrm{m}^{3}$"),
            ("pint (US Dry)", "pint (US Dry)s", 0.000550611, "$\\mathrm{m}^{3}$"),
            ("pint (US Liquid)", "pint (US Liquid)s", 0.000473176, "$\\mathrm{m}^{3}$"),
            ("quart (US Dry)", "quart (US Dry)s", 0.00110122, "$\\mathrm{m}^{3}$"),
            ("stére", "stéres", 1.0, "$\\mathrm{m}^{3}$"),
            ("tablespoon (Metric)", "tablespoon (Metric)s", 1.5000000000000002e-05, "$\\mathrm{m}^{3}$"),
            ("tablespoon (US)", "tablespoon (US)s", 1.47868e-05, "$\\mathrm{m}^{3}$"),
            ("teaspoon (US)", "teaspoon (US)s", 4.928919999999999e-06, "$\\mathrm{m}^{3}$")
        ],
        "field_name": "volume",
        "display_name": "Volume",
    },
    "VolumeFractionOfI": {
        "dimension": VOLUME_FRACTION_OF_I,
        "default_unit": "cubic centimeters of \"i\" per cubic meter totals",
        "units": [
            ("cubic centimeters of \"i\" per cubic meter total", "cubic centimeters of \"i\" per cubic meter totals", 0.0001, "$\\mathrm{m}_{\\mathrm{i}}^{3} / \\mathrm{m}^{3}$"),
            ("cubic foot of \"i\" per cubic foot total", "cubic foot of \"i\" per cubic foot totals", 1.0, "$\\mathrm{m}_{\\mathrm{i}}^{3} / \\mathrm{m}^{3}$"),
            ("cubic meters of \" i \" per cubic meter total", "cubic meters of \" i \" per cubic meter totals", 1.0, "$\\mathrm{m}_{\\mathrm{i}}^{3} / \\mathrm{m}^{3}$"),
            ("gallons of \"i\" per gallon total", "gallons of \"i\" per gallon totals", 1.0, "$\\mathrm{m}_{\\mathrm{i}}^{3} / \\mathrm{m}^{3}$")
        ],
        "field_name": "volume_fraction_of_i",
        "display_name": "Volume Fraction of \"i\"",
    },
    "VolumetricCalorificHeatingValue": {
        "dimension": VOLUMETRIC_CALORIFIC_HEATING_VALUE,
        "default_unit": "British thermal unit per cubic foots",
        "units": [
            ("British thermal unit per cubic foot", "British thermal unit per cubic foots", 37260.0, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("British thermal unit per gallon (UK)", "British thermal unit per gallon (UK)s", 232090.0, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("British thermal unit per gallon (US)", "British thermal unit per gallon (US)s", 193260.0, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("calorie per cubic centimeter", "calorie per cubic centimeters", 4186800.0, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("Chu per cubic foot", "Chu per cubic foots", 67067.0, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("joule per cubic meter", "joule per cubic meters", 1.0, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("kilocalorie per cubic foot", "kilocalorie per cubic foots", 147860.0, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("kilocalorie per cubic meter", "kilocalorie per cubic meters", 4186.8, "$\\mathrm{J} / \\mathrm{m}^{3}$"),
            ("therm ( 100 K Btu ) per cubic foot", "therm ( 100 K Btu ) per cubic foots", 3726000000.0, "$\\mathrm{J} / \\mathrm{m}^{3}$")
        ],
        "field_name": "volumetric_calorific_heating_value",
        "display_name": "Volumetric Calorific (Heating) Value",
    },
    "VolumetricCoefficientOfExpansion": {
        "dimension": VOLUMETRIC_COEFFICIENT_OF_EXPANSION,
        "default_unit": "gram per cubic centimeter per kelvin (or degree Celsius)s",
        "units": [
            ("gram per cubic centimeter per kelvin (or degree Celsius)", "gram per cubic centimeter per kelvin (or degree Celsius)s", 1000.0, "$\\mathrm{kg} / \\mathrm{m}^{3} / \\mathrm{K}$"),
            ("kilogram per cubic meter per kelvin (or degree Celsius)", "kilogram per cubic meter per kelvin (or degree Celsius)s", 1.0, "kg/m ${ }^{3}$ /K"),
            ("pound per cubic foot per degree Fahrenheit (or degree Rankine)", "pound per cubic foot per degree Fahrenheit (or degree Rankine)s", 28.833, "$\\mathrm{kg} / \\mathrm{m}^{3} / \\mathrm{K}$"),
            ("pound per cubic foot per kelvin (or degree Celsius)", "pound per cubic foot per kelvin (or degree Celsius)s", 16.018, "$\\mathrm{kg} / \\mathrm{m}^{3} / \\mathrm{K}$")
        ],
        "field_name": "volumetric_coefficient_of_expansion",
        "display_name": "Volumetric Coefficient of Expansion",
    },
    "VolumetricFlowRate": {
        "dimension": VOLUMETRIC_FLOW_RATE,
        "default_unit": "cubic feet per days",
        "units": [
            ("cubic feet per day", "cubic feet per days", 3.2778e-07, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("cubic feet per hour", "cubic feet per hours", 7.866699999999999e-06, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("cubic feet per minute", "cubic feet per minutes", 0.000472, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("cubic feet per second", "cubic feet per seconds", 0.02832, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("cubic meters per day", "cubic meters per days", 1.1574000000000001e-05, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("cubic meters per hour", "cubic meters per hours", 0.00027778, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("cubic meters per minute", "cubic meters per minutes", 0.016667, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("cubic meters per second", "cubic meters per seconds", 1.0, "$\\mathrm{m}^{3} / \\mathrm{s}$"),
            ("gallons per day", "gallons per days", 0.002628, "$1 / \\mathrm{min}$"),
            ("gallons per hour", "gallons per hours", 0.06308, "$1 / \\min$"),
            ("gallons per minute", "gallons per minutes", 3.785, "$1 / \\mathrm{min}$"),
            ("gallons per second", "gallons per seconds", 227.1, "$1 / \\mathrm{min}$"),
            ("liters per day", "liters per days", 0.00069444, "$1 / \\mathrm{min}$"),
            ("liters per hour", "liters per hours", 0.016667, "$1 / \\mathrm{min}$"),
            ("liters per minute", "liters per minutes", 1.0, "$1 / \\mathrm{min}$"),
            ("liters per second", "liters per seconds", 60.0, "$1 / \\mathrm{min}$")
        ],
        "field_name": "volumetric_flow_rate",
        "display_name": "Volumetric Flow Rate",
    },
    "VolumetricFlux": {
        "dimension": VOLUMETRIC_FLUX,
        "default_unit": "cubic feet per square foot per days",
        "units": [
            ("cubic feet per square foot per day", "cubic feet per square foot per days", 3.5276e-06, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("cubic feet per square foot per hour", "cubic feet per square foot per hours", 8.466300000000001e-05, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("cubic feet per square foot per minute", "cubic feet per square foot per minutes", 0.0050798, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("cubic feet per square foot per second", "cubic feet per square foot per seconds", 0.30479, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("cubic meters per square meter per day", "cubic meters per square meter per days", 1.1574000000000001e-05, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("cubic meters per square meter per hour", "cubic meters per square meter per hours", 0.00027778, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("cubic meters per square meter per minute", "cubic meters per square meter per minutes", 0.016667, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("cubic meters per square meter per second", "cubic meters per square meter per seconds", 1.0, "$\\mathrm{m}^{3}$ / ( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("gallons per square foot per day", "gallons per square foot per days", 0.00047138000000000003, "1/( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("gallons per square foot per hour", "gallons per square foot per hours", 0.011313, "1/( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("gallons per square foot per minute", "gallons per square foot per minutes", 0.67878, "1/( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("gallons per square foot per second", "gallons per square foot per seconds", 40.727, "1/( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("liters per square meter per day", "liters per square meter per days", 1.1574000000000001e-05, "$1 /\\left(\\mathrm{m}^{2} \\mathrm{~s}\\right)$"),
            ("liters per square meter per hour", "liters per square meter per hours", 0.00027778, "1/( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("liters per square meter per minute", "liters per square meter per minutes", 0.016667, "1/( $\\mathrm{m}^{2} \\mathrm{~s}$ )"),
            ("liters per square meter per second", "liters per square meter per seconds", 1.0, "$1 /\\left(\\mathrm{m}^{2} \\mathrm{~s}\\right)$")
        ],
        "field_name": "volumetric_flux",
        "display_name": "Volumetric Flux",
    },
    "VolumetricMassFlowRate": {
        "dimension": VOLUMETRIC_MASS_FLOW_RATE,
        "default_unit": "gram per second per cubic centimeters",
        "units": [
            ("gram per second per cubic centimeter", "gram per second per cubic centimeters", 1000.0, "kg/ ( $\\mathrm{s} \\mathrm{m}^{3}$ )"),
            ("kilogram per hour per cubic foot", "kilogram per hour per cubic foots", 0.0098096, "kg/ ( $\\mathrm{s} \\mathrm{m}^{3}$ )"),
            ("kilogram per hour per cubic meter", "kilogram per hour per cubic meters", 0.00027778000000000004, "kg/ ( $\\mathrm{s} \\mathrm{m}^{3}$ )"),
            ("kilogram per second per cubic meter", "kilogram per second per cubic meters", 1.0, "kg/ ( $\\mathrm{s} \\mathrm{m}^{3}$ )"),
            ("pound per hour per cubic foot", "pound per hour per cubic foots", 0.0044496, "kg/ ( $\\mathrm{s} \\mathrm{m}^{3}$ )"),
            ("pound per minute per cubic foot", "pound per minute per cubic foots", 0.26697, "kg/ ( $\\mathrm{s} \\mathrm{m}^{3}$ )"),
            ("pound per second per cubic foot", "pound per second per cubic foots", 16.018, "kg/ ( $\\mathrm{s} \\mathrm{m}^{3}$ )")
        ],
        "field_name": "volumetric_mass_flow_rate",
        "display_name": "Volumetric Mass Flow Rate",
    },
    "Wavenumber": {
        "dimension": WAVENUMBER,
        "default_unit": "diopters",
        "units": [
            ("diopter", "diopters", 1.0, "$1 / \\mathrm{m}$"),
            ("kayser", "kaysers", 100.0, "$1 / \\mathrm{m}$"),
            ("reciprocal meter", "reciprocal meters", 1.0, "$1 / \\mathrm{m}$")
        ],
        "field_name": "wavenumber",
        "display_name": "Wavenumber",
    }
}

# Special Dimensionless variable - handcrafted for proper behavior
class DimensionlessSetter(TypeSafeSetter):
    """Dimensionless-specific setter with only dimensionless units."""
    
    def __init__(self, variable: 'Dimensionless', value: float):
        super().__init__(variable, value)
    
    # Dimensionless units
    @property
    def dimensionless(self) -> 'Dimensionless':
        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)
        return cast('Dimensionless', self.variable)
    
    # Common alias for no units
    @property
    def unitless(self) -> 'Dimensionless':
        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)
        return cast('Dimensionless', self.variable)


class Dimensionless(TypedVariable):
    """Type-safe dimensionless variable with expression capabilities."""

    _setter_class = DimensionlessSetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "dimensionless"
    
    def set(self, value: float) -> DimensionlessSetter:
        """Create a dimensionless setter for this variable with proper type annotation."""
        return DimensionlessSetter(self, value)



def create_setter_class(class_name: str, variable_name: str, definition: Dict[str, Any]) -> Type:
    """Dynamically create a setter class with unit properties."""
    
    # Create base setter class
    setter_class = type(
        class_name,
        (TypeSafeSetter,),
        {
            '__init__': lambda self, variable, value: TypeSafeSetter.__init__(self, variable, value),
            '__doc__': f"{variable_name}-specific setter with only {variable_name.lower()} units."
        }
    )
    
    # Add properties for each unit using unit data directly
    for unit_name, property_name, si_factor, symbol in definition["units"]:
        # Create a unit definition from the consolidated data
        def make_property(unit_nm, si_fac, sym):
            def getter(self):
                # Create unit definition directly from consolidated unit data
                unit_def = UnitDefinition(
                    name=unit_nm,
                    symbol=sym,
                    dimension=definition["dimension"],
                    si_factor=si_fac
                )
                self.variable.quantity = FastQuantity(self.value, unit_def)
                return cast(variable_name, self.variable)
            return property(getter)
        
        # Add the property to the class
        setattr(setter_class, property_name, make_property(unit_name, si_factor, symbol))
    
    return setter_class


def create_variable_class(class_name: str, definition: Dict[str, Any], setter_class: Type) -> Type:
    """Dynamically create a variable class."""
    
    # Create the variable class
    variable_class = type(
        class_name,
        (TypedVariable,),
        {
            '_setter_class': setter_class,
            '_expected_dimension': definition["dimension"],
            '_default_unit_property': definition["default_unit"],
            '__doc__': f"Type-safe {class_name.lower()} variable with expression capabilities.",
            'set': lambda self, value: setter_class(self, value)
        }
    )
    
    # Add type hint for set method
    variable_class.set.__annotations__ = {'value': float, 'return': setter_class}
    
    return variable_class


# Create all variable and setter classes dynamically
for var_name, var_def in VARIABLE_DEFINITIONS.items():
    # Create setter class
    setter_name = f"{var_name}Setter"
    setter_class = create_setter_class(setter_name, var_name, var_def)
    
    # Create variable class
    variable_class = create_variable_class(var_name, var_def, setter_class)
    
    # Export them to module namespace
    globals()[setter_name] = setter_class
    globals()[var_name] = variable_class

# Individual exports for easier import
# Special Dimensionless class is already defined above

AbsorbedDoseSetter = globals()['AbsorbedDoseSetter']
AbsorbedDose = globals()['AbsorbedDose']
AccelerationSetter = globals()['AccelerationSetter']
Acceleration = globals()['Acceleration']
ActivationEnergySetter = globals()['ActivationEnergySetter']
ActivationEnergy = globals()['ActivationEnergy']
AmountOfSubstanceSetter = globals()['AmountOfSubstanceSetter']
AmountOfSubstance = globals()['AmountOfSubstance']
AnglePlaneSetter = globals()['AnglePlaneSetter']
AnglePlane = globals()['AnglePlane']
AngleSolidSetter = globals()['AngleSolidSetter']
AngleSolid = globals()['AngleSolid']
AngularAccelerationSetter = globals()['AngularAccelerationSetter']
AngularAcceleration = globals()['AngularAcceleration']
AngularMomentumSetter = globals()['AngularMomentumSetter']
AngularMomentum = globals()['AngularMomentum']
AreaSetter = globals()['AreaSetter']
Area = globals()['Area']
AreaPerUnitVolumeSetter = globals()['AreaPerUnitVolumeSetter']
AreaPerUnitVolume = globals()['AreaPerUnitVolume']
AtomicWeightSetter = globals()['AtomicWeightSetter']
AtomicWeight = globals()['AtomicWeight']
ConcentrationSetter = globals()['ConcentrationSetter']
Concentration = globals()['Concentration']
DynamicFluiditySetter = globals()['DynamicFluiditySetter']
DynamicFluidity = globals()['DynamicFluidity']
ElectricCapacitanceSetter = globals()['ElectricCapacitanceSetter']
ElectricCapacitance = globals()['ElectricCapacitance']
ElectricChargeSetter = globals()['ElectricChargeSetter']
ElectricCharge = globals()['ElectricCharge']
ElectricCurrentIntensitySetter = globals()['ElectricCurrentIntensitySetter']
ElectricCurrentIntensity = globals()['ElectricCurrentIntensity']
ElectricDipoleMomentSetter = globals()['ElectricDipoleMomentSetter']
ElectricDipoleMoment = globals()['ElectricDipoleMoment']
ElectricFieldStrengthSetter = globals()['ElectricFieldStrengthSetter']
ElectricFieldStrength = globals()['ElectricFieldStrength']
ElectricInductanceSetter = globals()['ElectricInductanceSetter']
ElectricInductance = globals()['ElectricInductance']
ElectricPotentialSetter = globals()['ElectricPotentialSetter']
ElectricPotential = globals()['ElectricPotential']
ElectricResistanceSetter = globals()['ElectricResistanceSetter']
ElectricResistance = globals()['ElectricResistance']
ElectricalConductanceSetter = globals()['ElectricalConductanceSetter']
ElectricalConductance = globals()['ElectricalConductance']
ElectricalPermittivitySetter = globals()['ElectricalPermittivitySetter']
ElectricalPermittivity = globals()['ElectricalPermittivity']
ElectricalResistivitySetter = globals()['ElectricalResistivitySetter']
ElectricalResistivity = globals()['ElectricalResistivity']
EnergyFluxSetter = globals()['EnergyFluxSetter']
EnergyFlux = globals()['EnergyFlux']
EnergyHeatWorkSetter = globals()['EnergyHeatWorkSetter']
EnergyHeatWork = globals()['EnergyHeatWork']
EnergyPerUnitAreaSetter = globals()['EnergyPerUnitAreaSetter']
EnergyPerUnitArea = globals()['EnergyPerUnitArea']
ForceSetter = globals()['ForceSetter']
Force = globals()['Force']
ForceBodySetter = globals()['ForceBodySetter']
ForceBody = globals()['ForceBody']
ForcePerUnitMassSetter = globals()['ForcePerUnitMassSetter']
ForcePerUnitMass = globals()['ForcePerUnitMass']
FrequencyVoltageRatioSetter = globals()['FrequencyVoltageRatioSetter']
FrequencyVoltageRatio = globals()['FrequencyVoltageRatio']
FuelConsumptionSetter = globals()['FuelConsumptionSetter']
FuelConsumption = globals()['FuelConsumption']
HeatOfCombustionSetter = globals()['HeatOfCombustionSetter']
HeatOfCombustion = globals()['HeatOfCombustion']
HeatOfFusionSetter = globals()['HeatOfFusionSetter']
HeatOfFusion = globals()['HeatOfFusion']
HeatOfVaporizationSetter = globals()['HeatOfVaporizationSetter']
HeatOfVaporization = globals()['HeatOfVaporization']
HeatTransferCoefficientSetter = globals()['HeatTransferCoefficientSetter']
HeatTransferCoefficient = globals()['HeatTransferCoefficient']
IlluminanceSetter = globals()['IlluminanceSetter']
Illuminance = globals()['Illuminance']
KineticEnergyOfTurbulenceSetter = globals()['KineticEnergyOfTurbulenceSetter']
KineticEnergyOfTurbulence = globals()['KineticEnergyOfTurbulence']
LengthSetter = globals()['LengthSetter']
Length = globals()['Length']
LinearMassDensitySetter = globals()['LinearMassDensitySetter']
LinearMassDensity = globals()['LinearMassDensity']
LinearMomentumSetter = globals()['LinearMomentumSetter']
LinearMomentum = globals()['LinearMomentum']
LuminanceSelfSetter = globals()['LuminanceSelfSetter']
LuminanceSelf = globals()['LuminanceSelf']
LuminousFluxSetter = globals()['LuminousFluxSetter']
LuminousFlux = globals()['LuminousFlux']
LuminousIntensitySetter = globals()['LuminousIntensitySetter']
LuminousIntensity = globals()['LuminousIntensity']
MagneticFieldSetter = globals()['MagneticFieldSetter']
MagneticField = globals()['MagneticField']
MagneticFluxSetter = globals()['MagneticFluxSetter']
MagneticFlux = globals()['MagneticFlux']
MagneticInductionFieldStrengthSetter = globals()['MagneticInductionFieldStrengthSetter']
MagneticInductionFieldStrength = globals()['MagneticInductionFieldStrength']
MagneticMomentSetter = globals()['MagneticMomentSetter']
MagneticMoment = globals()['MagneticMoment']
MagneticPermeabilitySetter = globals()['MagneticPermeabilitySetter']
MagneticPermeability = globals()['MagneticPermeability']
MagnetomotiveForceSetter = globals()['MagnetomotiveForceSetter']
MagnetomotiveForce = globals()['MagnetomotiveForce']
MassSetter = globals()['MassSetter']
Mass = globals()['Mass']
MassDensitySetter = globals()['MassDensitySetter']
MassDensity = globals()['MassDensity']
MassFlowRateSetter = globals()['MassFlowRateSetter']
MassFlowRate = globals()['MassFlowRate']
MassFluxSetter = globals()['MassFluxSetter']
MassFlux = globals()['MassFlux']
MassFractionOfISetter = globals()['MassFractionOfISetter']
MassFractionOfI = globals()['MassFractionOfI']
MassTransferCoefficientSetter = globals()['MassTransferCoefficientSetter']
MassTransferCoefficient = globals()['MassTransferCoefficient']
MolalityOfSoluteISetter = globals()['MolalityOfSoluteISetter']
MolalityOfSoluteI = globals()['MolalityOfSoluteI']
MolarConcentrationByMassSetter = globals()['MolarConcentrationByMassSetter']
MolarConcentrationByMass = globals()['MolarConcentrationByMass']
MolarFlowRateSetter = globals()['MolarFlowRateSetter']
MolarFlowRate = globals()['MolarFlowRate']
MolarFluxSetter = globals()['MolarFluxSetter']
MolarFlux = globals()['MolarFlux']
MolarHeatCapacitySetter = globals()['MolarHeatCapacitySetter']
MolarHeatCapacity = globals()['MolarHeatCapacity']
MolarityOfISetter = globals()['MolarityOfISetter']
MolarityOfI = globals()['MolarityOfI']
MoleFractionOfISetter = globals()['MoleFractionOfISetter']
MoleFractionOfI = globals()['MoleFractionOfI']
MomentOfInertiaSetter = globals()['MomentOfInertiaSetter']
MomentOfInertia = globals()['MomentOfInertia']
MomentumFlowRateSetter = globals()['MomentumFlowRateSetter']
MomentumFlowRate = globals()['MomentumFlowRate']
MomentumFluxSetter = globals()['MomentumFluxSetter']
MomentumFlux = globals()['MomentumFlux']
NormalityOfSolutionSetter = globals()['NormalityOfSolutionSetter']
NormalityOfSolution = globals()['NormalityOfSolution']
ParticleDensitySetter = globals()['ParticleDensitySetter']
ParticleDensity = globals()['ParticleDensity']
PermeabilitySetter = globals()['PermeabilitySetter']
Permeability = globals()['Permeability']
PhotonEmissionRateSetter = globals()['PhotonEmissionRateSetter']
PhotonEmissionRate = globals()['PhotonEmissionRate']
PowerPerUnitMassSetter = globals()['PowerPerUnitMassSetter']
PowerPerUnitMass = globals()['PowerPerUnitMass']
PowerPerUnitVolumeSetter = globals()['PowerPerUnitVolumeSetter']
PowerPerUnitVolume = globals()['PowerPerUnitVolume']
PowerThermalDutySetter = globals()['PowerThermalDutySetter']
PowerThermalDuty = globals()['PowerThermalDuty']
PressureSetter = globals()['PressureSetter']
Pressure = globals()['Pressure']
RadiationDoseEquivalentSetter = globals()['RadiationDoseEquivalentSetter']
RadiationDoseEquivalent = globals()['RadiationDoseEquivalent']
RadiationExposureSetter = globals()['RadiationExposureSetter']
RadiationExposure = globals()['RadiationExposure']
RadioactivitySetter = globals()['RadioactivitySetter']
Radioactivity = globals()['Radioactivity']
SecondMomentOfAreaSetter = globals()['SecondMomentOfAreaSetter']
SecondMomentOfArea = globals()['SecondMomentOfArea']
SecondRadiationConstantPlanckSetter = globals()['SecondRadiationConstantPlanckSetter']
SecondRadiationConstantPlanck = globals()['SecondRadiationConstantPlanck']
SpecificEnthalpySetter = globals()['SpecificEnthalpySetter']
SpecificEnthalpy = globals()['SpecificEnthalpy']
SpecificGravitySetter = globals()['SpecificGravitySetter']
SpecificGravity = globals()['SpecificGravity']
SpecificHeatCapacityConstantPressureSetter = globals()['SpecificHeatCapacityConstantPressureSetter']
SpecificHeatCapacityConstantPressure = globals()['SpecificHeatCapacityConstantPressure']
SpecificLengthSetter = globals()['SpecificLengthSetter']
SpecificLength = globals()['SpecificLength']
SpecificSurfaceSetter = globals()['SpecificSurfaceSetter']
SpecificSurface = globals()['SpecificSurface']
SpecificVolumeSetter = globals()['SpecificVolumeSetter']
SpecificVolume = globals()['SpecificVolume']
StressSetter = globals()['StressSetter']
Stress = globals()['Stress']
SurfaceMassDensitySetter = globals()['SurfaceMassDensitySetter']
SurfaceMassDensity = globals()['SurfaceMassDensity']
SurfaceTensionSetter = globals()['SurfaceTensionSetter']
SurfaceTension = globals()['SurfaceTension']
TemperatureSetter = globals()['TemperatureSetter']
Temperature = globals()['Temperature']
ThermalConductivitySetter = globals()['ThermalConductivitySetter']
ThermalConductivity = globals()['ThermalConductivity']
TimeSetter = globals()['TimeSetter']
Time = globals()['Time']
TorqueSetter = globals()['TorqueSetter']
Torque = globals()['Torque']
TurbulenceEnergyDissipationRateSetter = globals()['TurbulenceEnergyDissipationRateSetter']
TurbulenceEnergyDissipationRate = globals()['TurbulenceEnergyDissipationRate']
VelocityAngularSetter = globals()['VelocityAngularSetter']
VelocityAngular = globals()['VelocityAngular']
VelocityLinearSetter = globals()['VelocityLinearSetter']
VelocityLinear = globals()['VelocityLinear']
ViscosityDynamicSetter = globals()['ViscosityDynamicSetter']
ViscosityDynamic = globals()['ViscosityDynamic']
ViscosityKinematicSetter = globals()['ViscosityKinematicSetter']
ViscosityKinematic = globals()['ViscosityKinematic']
VolumeSetter = globals()['VolumeSetter']
Volume = globals()['Volume']
VolumeFractionOfISetter = globals()['VolumeFractionOfISetter']
VolumeFractionOfI = globals()['VolumeFractionOfI']
VolumetricCalorificHeatingValueSetter = globals()['VolumetricCalorificHeatingValueSetter']
VolumetricCalorificHeatingValue = globals()['VolumetricCalorificHeatingValue']
VolumetricCoefficientOfExpansionSetter = globals()['VolumetricCoefficientOfExpansionSetter']
VolumetricCoefficientOfExpansion = globals()['VolumetricCoefficientOfExpansion']
VolumetricFlowRateSetter = globals()['VolumetricFlowRateSetter']
VolumetricFlowRate = globals()['VolumetricFlowRate']
VolumetricFluxSetter = globals()['VolumetricFluxSetter']
VolumetricFlux = globals()['VolumetricFlux']
VolumetricMassFlowRateSetter = globals()['VolumetricMassFlowRateSetter']
VolumetricMassFlowRate = globals()['VolumetricMassFlowRate']
WavenumberSetter = globals()['WavenumberSetter']
Wavenumber = globals()['Wavenumber']


# Module registration compatibility
def get_consolidated_variable_modules():
    """Return module-like objects for consolidated variables."""
    
    class ConsolidatedVariableModule:
        """Mock module object for compatibility with existing registration system."""
        
        def __init__(self, var_name: str):
            self.var_name = var_name
            self.definition = VARIABLE_DEFINITIONS[var_name]
            self.variable_class = globals()[var_name]
            self.setter_class = globals()[f"{var_name}Setter"]
        
        def get_variable_class(self):
            return self.variable_class
        
        def get_setter_class(self):
            return self.setter_class
        
        def get_expected_dimension(self):
            return self.definition["dimension"]
    
    return [
        ConsolidatedVariableModule("AbsorbedDose"),
        ConsolidatedVariableModule("Acceleration"),
        ConsolidatedVariableModule("ActivationEnergy"),
        ConsolidatedVariableModule("AmountOfSubstance"),
        ConsolidatedVariableModule("AnglePlane"),
        ConsolidatedVariableModule("AngleSolid"),
        ConsolidatedVariableModule("AngularAcceleration"),
        ConsolidatedVariableModule("AngularMomentum"),
        ConsolidatedVariableModule("Area"),
        ConsolidatedVariableModule("AreaPerUnitVolume"),
        ConsolidatedVariableModule("AtomicWeight"),
        ConsolidatedVariableModule("Concentration"),
        ConsolidatedVariableModule("DynamicFluidity"),
        ConsolidatedVariableModule("ElectricCapacitance"),
        ConsolidatedVariableModule("ElectricCharge"),
        ConsolidatedVariableModule("ElectricCurrentIntensity"),
        ConsolidatedVariableModule("ElectricDipoleMoment"),
        ConsolidatedVariableModule("ElectricFieldStrength"),
        ConsolidatedVariableModule("ElectricInductance"),
        ConsolidatedVariableModule("ElectricPotential"),
        ConsolidatedVariableModule("ElectricResistance"),
        ConsolidatedVariableModule("ElectricalConductance"),
        ConsolidatedVariableModule("ElectricalPermittivity"),
        ConsolidatedVariableModule("ElectricalResistivity"),
        ConsolidatedVariableModule("EnergyFlux"),
        ConsolidatedVariableModule("EnergyHeatWork"),
        ConsolidatedVariableModule("EnergyPerUnitArea"),
        ConsolidatedVariableModule("Force"),
        ConsolidatedVariableModule("ForceBody"),
        ConsolidatedVariableModule("ForcePerUnitMass"),
        ConsolidatedVariableModule("FrequencyVoltageRatio"),
        ConsolidatedVariableModule("FuelConsumption"),
        ConsolidatedVariableModule("HeatOfCombustion"),
        ConsolidatedVariableModule("HeatOfFusion"),
        ConsolidatedVariableModule("HeatOfVaporization"),
        ConsolidatedVariableModule("HeatTransferCoefficient"),
        ConsolidatedVariableModule("Illuminance"),
        ConsolidatedVariableModule("KineticEnergyOfTurbulence"),
        ConsolidatedVariableModule("Length"),
        ConsolidatedVariableModule("LinearMassDensity"),
        ConsolidatedVariableModule("LinearMomentum"),
        ConsolidatedVariableModule("LuminanceSelf"),
        ConsolidatedVariableModule("LuminousFlux"),
        ConsolidatedVariableModule("LuminousIntensity"),
        ConsolidatedVariableModule("MagneticField"),
        ConsolidatedVariableModule("MagneticFlux"),
        ConsolidatedVariableModule("MagneticInductionFieldStrength"),
        ConsolidatedVariableModule("MagneticMoment"),
        ConsolidatedVariableModule("MagneticPermeability"),
        ConsolidatedVariableModule("MagnetomotiveForce"),
        ConsolidatedVariableModule("Mass"),
        ConsolidatedVariableModule("MassDensity"),
        ConsolidatedVariableModule("MassFlowRate"),
        ConsolidatedVariableModule("MassFlux"),
        ConsolidatedVariableModule("MassFractionOfI"),
        ConsolidatedVariableModule("MassTransferCoefficient"),
        ConsolidatedVariableModule("MolalityOfSoluteI"),
        ConsolidatedVariableModule("MolarConcentrationByMass"),
        ConsolidatedVariableModule("MolarFlowRate"),
        ConsolidatedVariableModule("MolarFlux"),
        ConsolidatedVariableModule("MolarHeatCapacity"),
        ConsolidatedVariableModule("MolarityOfI"),
        ConsolidatedVariableModule("MoleFractionOfI"),
        ConsolidatedVariableModule("MomentOfInertia"),
        ConsolidatedVariableModule("MomentumFlowRate"),
        ConsolidatedVariableModule("MomentumFlux"),
        ConsolidatedVariableModule("NormalityOfSolution"),
        ConsolidatedVariableModule("ParticleDensity"),
        ConsolidatedVariableModule("Permeability"),
        ConsolidatedVariableModule("PhotonEmissionRate"),
        ConsolidatedVariableModule("PowerPerUnitMass"),
        ConsolidatedVariableModule("PowerPerUnitVolume"),
        ConsolidatedVariableModule("PowerThermalDuty"),
        ConsolidatedVariableModule("Pressure"),
        ConsolidatedVariableModule("RadiationDoseEquivalent"),
        ConsolidatedVariableModule("RadiationExposure"),
        ConsolidatedVariableModule("Radioactivity"),
        ConsolidatedVariableModule("SecondMomentOfArea"),
        ConsolidatedVariableModule("SecondRadiationConstantPlanck"),
        ConsolidatedVariableModule("SpecificEnthalpy"),
        ConsolidatedVariableModule("SpecificGravity"),
        ConsolidatedVariableModule("SpecificHeatCapacityConstantPressure"),
        ConsolidatedVariableModule("SpecificLength"),
        ConsolidatedVariableModule("SpecificSurface"),
        ConsolidatedVariableModule("SpecificVolume"),
        ConsolidatedVariableModule("Stress"),
        ConsolidatedVariableModule("SurfaceMassDensity"),
        ConsolidatedVariableModule("SurfaceTension"),
        ConsolidatedVariableModule("Temperature"),
        ConsolidatedVariableModule("ThermalConductivity"),
        ConsolidatedVariableModule("Time"),
        ConsolidatedVariableModule("Torque"),
        ConsolidatedVariableModule("TurbulenceEnergyDissipationRate"),
        ConsolidatedVariableModule("VelocityAngular"),
        ConsolidatedVariableModule("VelocityLinear"),
        ConsolidatedVariableModule("ViscosityDynamic"),
        ConsolidatedVariableModule("ViscosityKinematic"),
        ConsolidatedVariableModule("Volume"),
        ConsolidatedVariableModule("VolumeFractionOfI"),
        ConsolidatedVariableModule("VolumetricCalorificHeatingValue"),
        ConsolidatedVariableModule("VolumetricCoefficientOfExpansion"),
        ConsolidatedVariableModule("VolumetricFlowRate"),
        ConsolidatedVariableModule("VolumetricFlux"),
        ConsolidatedVariableModule("VolumetricMassFlowRate"),
        ConsolidatedVariableModule("Wavenumber")
    ]
