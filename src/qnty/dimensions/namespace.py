"""
Dimension System
================

This file contains dimension constants for all engineering fields.

THIS FILE IS AUTO-GENERATED - DO NOT EDIT MANUALLY
changes will be overwritten
see codegen/generate_dimensions.py
"""

from .core import Dimension

ABSORBED_DOSE = Dimension((2, 0, -2, 0, 0, 0, 0))  # L^2 T^-2
ACCELERATION = Dimension((1, 0, -2, 0, 0, 0, 0))  # L T^-2
ACTIVATION_ENERGY = Dimension((2, 0, -2, 0, 0, -1, 0))  # N^-1 L^2 T^-2
AMOUNT_OF_SUBSTANCE = Dimension((0, 0, 0, 0, 0, 1, 0))  # N
ANGLE_PLANE = Dimension((0, 0, 0, 0, 0, 0, 0))
ANGLE_SOLID = Dimension((0, 0, 0, 0, 0, 0, 0))
ANGULAR_ACCELERATION = Dimension((0, 0, -2, 0, 0, 0, 0))  # T^-2
ANGULAR_MOMENTUM = Dimension((2, 1, -1, 0, 0, 0, 0))  # L^2 M T^-1
AREA = Dimension((2, 0, 0, 0, 0, 0, 0))  # L^2
AREA_PER_UNIT_VOLUME = Dimension((-1, 0, 0, 0, 0, 0, 0))  # L^-1
ATOMIC_WEIGHT = Dimension((0, 1, 0, 0, 0, -1, 0))  # N^-1 M
CONCENTRATION = Dimension((-3, 1, 0, 0, 0, 0, 0))  # L^-3 M
DIMENSIONLESS = Dimension((0, 0, 0, 0, 0, 0, 0))
DYNAMIC_FLUIDITY = Dimension((1, -1, 1, 0, 0, 0, 0))  # L M^-1 T
ELECTRICAL_CONDUCTANCE = Dimension((-2, -1, 3, 2, 0, 0, 0))  # I^2 L^-2 M^-1 T^3
ELECTRICAL_PERMITTIVITY = Dimension((-3, -1, 4, 2, 0, 0, 0))  # I^2 L^-3 M^-1 T^4
ELECTRICAL_RESISTIVITY = Dimension((3, 1, -3, -2, 0, 0, 0))  # I^-2 L^3 M T^-3
ELECTRIC_CAPACITANCE = Dimension((-2, -1, 4, 2, 0, 0, 0))  # I^2 L^-2 M^-1 T^4
ELECTRIC_CHARGE = Dimension((0, 0, 1, 1, 0, -1, 0))  # N^-1 I T
ELECTRIC_CURRENT_INTENSITY = Dimension((0, 0, 0, 1, 0, 0, 0))  # I
ELECTRIC_DIPOLE_MOMENT = Dimension((1, 0, 1, 1, 0, 0, 0))  # I L T
ELECTRIC_FIELD_STRENGTH = Dimension((1, 1, -3, -1, 0, 0, 0))  # I^-1 L M T^-3
ELECTRIC_INDUCTANCE = Dimension((2, 1, -2, -2, 0, 0, 0))  # I^-2 L^2 M T^-2
ELECTRIC_POTENTIAL = Dimension((2, 1, -3, -1, 0, 0, 0))  # I^-1 L^2 M T^-3
ELECTRIC_RESISTANCE = Dimension((2, 1, -3, -2, 0, 0, 0))  # I^-2 L^2 M T^-3
ENERGY_FLUX = Dimension((0, 1, -3, 0, 0, 0, 0))  # M T^-3
ENERGY_HEAT_WORK = Dimension((2, 1, -2, 0, 0, 0, 0))  # L^2 M T^-2
ENERGY_PER_UNIT_AREA = Dimension((0, 1, -2, 0, 0, 0, 0))  # M T^-2
FORCE = Dimension((1, 1, -2, 0, 0, 0, 0))  # L M T^-2
FORCE_BODY = Dimension((-2, 1, -2, 0, 0, 0, 0))  # L^-2 M T^-2
FORCE_PER_UNIT_MASS = Dimension((1, 0, -2, 0, 0, 0, 0))  # L T^-2
FREQUENCY_VOLTAGE_RATIO = Dimension((-2, -1, 3, 1, 0, 0, 0))  # I L^-2 M^-1 T^3
FUEL_CONSUMPTION = Dimension((-2, 0, 0, 0, 0, 0, 0))  # L^-2
HEAT_OF_COMBUSTION = Dimension((2, 0, -2, 0, 0, 0, 0))  # L^2 T^-2
HEAT_OF_FUSION = Dimension((2, 0, -2, 0, 0, 0, 0))  # L^2 T^-2
HEAT_OF_VAPORIZATION = Dimension((2, 0, -2, 0, 0, 0, 0))  # L^2 T^-2
HEAT_TRANSFER_COEFFICIENT = Dimension((0, 1, -3, 0, 0, 0, 0))  # M T^-3
ILLUMINANCE = Dimension((-2, 0, 0, 0, 0, 0, 0))  # L^-2
KINETIC_ENERGY_OF_TURBULENCE = Dimension((2, 0, -2, 0, 0, 0, 0))  # L^2 T^-2
LENGTH = Dimension((1, 0, 0, 0, 0, 0, 0))  # L
LINEAR_MASS_DENSITY = Dimension((-1, 1, 0, 0, 0, 0, 0))  # L^-1 M
LINEAR_MOMENTUM = Dimension((1, 1, -1, 0, 0, 0, 0))  # L M T^-1
LUMINANCE_SELF = Dimension((-2, 0, 0, 0, 0, 0, 0))  # L^-2
LUMINOUS_FLUX = Dimension((0, 0, 0, 0, 0, 0, 0))
LUMINOUS_INTENSITY = Dimension((0, 0, 0, 0, 0, 0, 0))
MAGNETIC_FIELD = Dimension((-1, 0, 0, 1, 0, 0, 0))  # I L^-1
MAGNETIC_FLUX = Dimension((2, 1, -2, -1, 0, 0, 0))  # I^-1 L^2 M T^-2
MAGNETIC_INDUCTION_FIELD_STRENGTH = Dimension((0, 1, -2, -1, 0, 0, 0))  # I^-1 M T^-2
MAGNETIC_MOMENT = Dimension((2, 0, 0, 1, 0, 0, 0))  # I L^2
MAGNETIC_PERMEABILITY = Dimension((2, 1, -2, -2, 0, 0, 0))  # I^-2 L^2 M T^-2
MAGNETOMOTIVE_FORCE = Dimension((0, 0, 0, 1, 0, 0, 0))  # I
MASS = Dimension((0, 1, 0, 0, 0, 0, 0))  # M
MASS_DENSITY = Dimension((-3, 1, 0, 0, 0, 0, 0))  # L^-3 M
MASS_FLOW_RATE = Dimension((0, 1, -1, 0, 0, 0, 0))  # M T^-1
MASS_FLUX = Dimension((-2, 1, -1, 0, 0, 0, 0))  # L^-2 M T^-1
MASS_FRACTION_OF_I = Dimension((0, 0, 0, 0, 0, 0, 0))
MASS_TRANSFER_COEFFICIENT = Dimension((-2, 1, -1, 0, 0, 0, 0))  # L^-2 M T^-1
MOLALITY_OF_SOLUTE_I = Dimension((0, -1, 0, 0, 0, 1, 0))  # N M^-1
MOLARITY_OF_I = Dimension((-3, 0, 0, 0, 0, 1, 0))  # N L^-3
MOLAR_CONCENTRATION_BY_MASS = Dimension((0, 0, 0, 0, 0, 1, 0))  # N
MOLAR_FLOW_RATE = Dimension((0, 0, -1, 0, 0, 1, 0))  # N T^-1
MOLAR_FLUX = Dimension((-2, 0, -1, 0, 0, 1, 0))  # N L^-2 T^-1
MOLAR_HEAT_CAPACITY = Dimension((2, 0, -2, 0, 0, -1, 0))  # N^-1 L^2 T^-2
MOLE_FRACTION_OF_I = Dimension((0, 0, 0, 0, 0, 0, 0))
MOMENTUM_FLOW_RATE = Dimension((1, 1, -2, 0, 0, 0, 0))  # L M T^-2
MOMENTUM_FLUX = Dimension((-1, 1, -2, 0, 0, 0, 0))  # L^-1 M T^-2
MOMENT_OF_INERTIA = Dimension((2, 1, 0, 0, 0, 0, 0))  # L^2 M
NORMALITY_OF_SOLUTION = Dimension((-3, 0, 0, 0, 0, 1, 0))  # N L^-3
PARTICLE_DENSITY = Dimension((-3, 0, 0, 0, 0, 0, 0))  # L^-3
PERCENT = Dimension((0, 0, 0, 0, 0, 0, 0))
PERMEABILITY = Dimension((2, 0, 0, 0, 0, 0, 0))  # L^2
PHOTON_EMISSION_RATE = Dimension((-2, 0, -1, 0, 0, 0, 0))  # L^-2 T^-1
POWER_PER_UNIT_MASS = Dimension((2, 0, -3, 0, 0, 0, 0))  # L^2 T^-3
POWER_PER_UNIT_VOLUME = Dimension((-1, 1, -3, 0, 0, 0, 0))  # L^-1 M T^-3
POWER_THERMAL_DUTY = Dimension((2, 1, -3, 0, 0, 0, 0))  # L^2 M T^-3
PRESSURE = Dimension((-1, 1, -2, 0, 0, 0, 0))  # L^-1 M T^-2
RADIATION_DOSE_EQUIVALENT = Dimension((2, 0, -2, 0, 0, 0, 0))  # L^2 T^-2
RADIATION_EXPOSURE = Dimension((0, -1, 1, 1, 0, 0, 0))  # I M^-1 T
RADIOACTIVITY = Dimension((0, 0, -1, 0, 0, 0, 0))  # T^-1
SECOND_MOMENT_OF_AREA = Dimension((4, 0, 0, 0, 0, 0, 0))  # L^4
SECOND_RADIATION_CONSTANT_PLANCK = Dimension((1, 0, 0, 0, 0, 0, 0))  # L
SPECIFIC_ENTHALPY = Dimension((2, 0, -2, 0, 0, 0, 0))  # L^2 T^-2
SPECIFIC_GRAVITY = Dimension((0, 0, 0, 0, 0, 0, 0))
SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE = Dimension((2, 1, -2, 0, 0, 0, 0))  # L^2 M T^-2
SPECIFIC_LENGTH = Dimension((1, -1, 0, 0, 0, 0, 0))  # L M^-1
SPECIFIC_SURFACE = Dimension((2, -1, 0, 0, 0, 0, 0))  # L^2 M^-1
SPECIFIC_VOLUME = Dimension((3, -1, 0, 0, 0, 0, 0))  # L^3 M^-1
STRESS = Dimension((-1, 1, -2, 0, 0, 0, 0))  # L^-1 M T^-2
SURFACE_MASS_DENSITY = Dimension((-2, 1, 0, 0, 0, 0, 0))  # L^-2 M
SURFACE_TENSION = Dimension((0, 1, -2, 0, 0, 0, 0))  # M T^-2
TEMPERATURE = Dimension((0, 0, 0, 0, 0, 0, 0))
THERMAL_CONDUCTIVITY = Dimension((1, 1, -3, 0, 0, 0, 0))  # L M T^-3
TIME = Dimension((0, 0, 1, 0, 0, 0, 0))  # T
TORQUE = Dimension((2, 1, -2, 0, 0, 0, 0))  # L^2 M T^-2
TURBULENCE_ENERGY_DISSIPATION_RATE = Dimension((2, 0, -3, 0, 0, 0, 0))  # L^2 T^-3
VELOCITY_ANGULAR = Dimension((0, 0, -1, 0, 0, 0, 0))  # T^-1
VELOCITY_LINEAR = Dimension((1, 0, -1, 0, 0, 0, 0))  # L T^-1
VISCOSITY_DYNAMIC = Dimension((-1, 1, -1, 0, 0, 0, 0))  # L^-1 M T^-1
VISCOSITY_KINEMATIC = Dimension((2, 0, -1, 0, 0, 0, 0))  # L^2 T^-1
VOLUME = Dimension((3, 0, 0, 0, 0, 0, 0))  # L^3
VOLUMETRIC_CALORIFIC_HEATING_VALUE = Dimension((-1, 1, -2, 0, 0, 0, 0))  # L^-1 M T^-2
VOLUMETRIC_COEFFICIENT_OF_EXPANSION = Dimension((-3, 1, 0, 0, 0, 0, 0))  # L^-3 M
VOLUMETRIC_FLOW_RATE = Dimension((3, 0, -1, 0, 0, 0, 0))  # L^3 T^-1
VOLUMETRIC_FLUX = Dimension((1, 0, -1, 0, 0, 0, 0))  # L T^-1
VOLUMETRIC_MASS_FLOW_RATE = Dimension((-3, 1, -1, 0, 0, 0, 0))  # L^-3 M T^-1
VOLUME_FRACTION_OF_I = Dimension((0, 0, 0, 0, 0, 0, 0))
WAVENUMBER = Dimension((-1, 0, 0, 0, 0, 0, 0))  # L^-1
