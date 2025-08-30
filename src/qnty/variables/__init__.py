"""
Variables Package with Auto-Discovery and Registration
======================================================

Automatically discovers and registers all variable modules, providing
a clean API for type-safe engineering variables.
"""

import importlib
import pkgutil

from .base import VariableRegistry

# Create global variable registry
variable_registry = VariableRegistry()

# Auto-discover and register all variable modules
for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    if modname not in ['__init__', 'base']:
        module = importlib.import_module(f'.{modname}', __name__)
        
        # Register variable module if it has the VARIABLE_MODULE attribute
        if hasattr(module, 'VARIABLE_MODULE'):
            var_module = module.VARIABLE_MODULE
            var_module.register_to_registry(variable_registry)

# Import all variable classes for public API
from .dimensionless import Dimensionless, DimensionlessSetter
from .length import Length, LengthSetter
from .pressure import Pressure, PressureSetter
from .time import Time, TimeSetter
from .absorbed_dose import AbsorbedDose, AbsorbedDoseSetter
from .acceleration import Acceleration, AccelerationSetter
from .angle import Angle, AngleSetter

# Also import base classes for extensibility
from .base import VariableModule, VariableRegistry

# Import TypeSafeSetter from variable module for backward compatibility
from ..variable import TypeSafeSetter
from .mass_fraction_of_i import MassFractionOfI, MassFractionOfISetter
from .force_body import Forcebody, ForcebodySetter
from .luminance_self import Luminanceself, LuminanceselfSetter
from .second_radiation_constant_planck import SecondRadiationConstantplanck, SecondRadiationConstantplanckSetter
from .viscosity_kinematic import ViscosityKinematic, ViscosityKinematicSetter
from .electric_charge import ElectricCharge, ElectricChargeSetter
from .power_per_unit_volume import PowerPerUnitVolumeOrPowerDensity, PowerPerUnitVolumeOrPowerDensitySetter
from .dynamic_fluidity import DynamicFluidity, DynamicFluiditySetter
from .mass_density import MassDensity, MassDensitySetter
from .volume_fraction_of_i import VolumeFractionOfI, VolumeFractionOfISetter
from .angle_solid import AngleSolid, AngleSolidSetter
from .frequency_voltage_ratio import FrequencyVoltageRatio, FrequencyVoltageRatioSetter
from .specific_enthalpy import SpecificEnthalpy, SpecificEnthalpySetter
from .linear_mass_density import LinearMassDensity, LinearMassDensitySetter
from .atomic_weight import AtomicWeight, AtomicWeightSetter
from .molar_heat_capacity import MolarHeatCapacity, MolarHeatCapacitySetter
from .mass_flux import MassFlux, MassFluxSetter
from .heat_of_fusion import HeatOfFusion, HeatOfFusionSetter
from .specific_volume import SpecificVolume, SpecificVolumeSetter
from .volumetric_mass_flow_rate import VolumetricMassFlowRate, VolumetricMassFlowRateSetter
from .permeability import Permeability, PermeabilitySetter
from .stress import Stress, StressSetter
from .volume import Volume, VolumeSetter
from .absorbed_radiation_dose import AbsorbedDose, AbsorbedDoseSetter
from .molality_of_solute_i import MolalityOfSoluteI, MolalityOfSoluteISetter
from .moment_of_inertia import MomentOfInertia, MomentOfInertiaSetter
from .radioactivity import Radioactivity, RadioactivitySetter
from .electric_resistance import ElectricResistance, ElectricResistanceSetter
from .molarity_of_i import MolarityOfI, MolarityOfISetter
from .area import Area, AreaSetter
from .mass_flow_rate import MassFlowRate, MassFlowRateSetter
from .energy_heat_work import EnergyHeatWork, EnergyHeatWorkSetter
from .electric_potential import ElectricPotential, ElectricPotentialSetter
from .viscosity_dynamic import ViscosityDynamic, ViscosityDynamicSetter
from .torque import Torque, TorqueSetter
from .electric_field_strength import ElectricFieldStrength, ElectricFieldStrengthSetter
from .velocity_linear import VelocityLinear, VelocityLinearSetter
from .molar_concentration_by_mass import MolarConcentrationByMass, MolarConcentrationByMassSetter
from .luminous_intensity import LuminousIntensity, LuminousIntensitySetter
from .energy_flux import EnergyFlux, EnergyFluxSetter
from .molar_flux import MolarFlux, MolarFluxSetter
from .angular_momentum import AngularMomentum, AngularMomentumSetter
from .electric_dipole_moment import ElectricDipoleMoment, ElectricDipoleMomentSetter
from .surface_tension import SurfaceTension, SurfaceTensionSetter
from .heat_transfer_coefficient import HeatTransferCoefficient, HeatTransferCoefficientSetter
from .magnetic_flux import MagneticFlux, MagneticFluxSetter
from .volumetric_flow_rate import VolumetricFlowRate, VolumetricFlowRateSetter
from .momentum_flux import MomentumFlux, MomentumFluxSetter
from .force import Force, ForceSetter
from .specific_gravity import SpecificGravity, SpecificGravitySetter
from .volumetric_flux import VolumetricFlux, VolumetricFluxSetter
from .concentration import Concentration, ConcentrationSetter
from .electrical_conductance import ElectricalConductance, ElectricalConductanceSetter
from .surface_mass_density import SurfaceMassDensity, SurfaceMassDensitySetter
from .magnetic_field import MagneticField, MagneticFieldSetter
from .momentum_flow_rate import MomentumFlowRate, MomentumFlowRateSetter
from .molar_flow_rate import MolarFlowRate, MolarFlowRateSetter
from .force_per_unit_mass import ForcePerUnitMass, ForcePerUnitMassSetter
from .thermal_conductivity import ThermalConductivity, ThermalConductivitySetter
from .mass import Mass, MassSetter
from .luminous_flux import LuminousFlux, LuminousFluxSetter
from .electrical_permittivity import ElectricalPermittivity, ElectricalPermittivitySetter
from .mass_transfer_coefficient import MassTransferCoefficient, MassTransferCoefficientSetter
from .magnetic_permeability import MagneticPermeability, MagneticPermeabilitySetter
from .volumetric_coefficient_of_expansion import VolumetricCoefficientOfExpansion, VolumetricCoefficientOfExpansionSetter
from .magnetomotive_force import MagnetomotiveForce, MagnetomotiveForceSetter
from .photon_emission_rate import PhotonEmissionRate, PhotonEmissionRateSetter
from .electric_capacitance import ElectricCapacitance, ElectricCapacitanceSetter
from .magnetic_induction_field_strength import MagneticInductionFieldStrength, MagneticInductionFieldStrengthSetter
from .power_per_unit_mass import PowerPerUnitMassOrSpecificPower, PowerPerUnitMassOrSpecificPowerSetter
from .velocity_angular import VelocityAngular, VelocityAngularSetter
from .linear_momentum import LinearMomentum, LinearMomentumSetter
from .kinetic_energy_of_turbulence import KineticEnergyOfTurbulence, KineticEnergyOfTurbulenceSetter
from .turbulence_energy_dissipation_rate import TurbulenceEnergyDissipationRate, TurbulenceEnergyDissipationRateSetter
from .angle_plane import AnglePlane, AnglePlaneSetter
from .fuel_consumption import FuelConsumption, FuelConsumptionSetter
from .heat_of_combustion import HeatOfCombustion, HeatOfCombustionSetter
from .electrical_resistivity import ElectricalResistivity, ElectricalResistivitySetter
from .temperature import Temperature, TemperatureSetter
from .energy_per_unit_area import EnergyPerUnitArea, EnergyPerUnitAreaSetter
from .amount_of_substance import AmountOfSubstance, AmountOfSubstanceSetter
from .magnetic_moment import MagneticMoment, MagneticMomentSetter
from .heat_of_vaporization import HeatOfVaporization, HeatOfVaporizationSetter
from .area_per_unit_volume import AreaPerUnitVolume, AreaPerUnitVolumeSetter
from .specific_heat_capacity_constant_pressure import SpecificHeatCapacityconstantPressure, SpecificHeatCapacityconstantPressureSetter
from .second_moment_of_area import SecondMomentOfArea, SecondMomentOfAreaSetter
from .particle_density import ParticleDensity, ParticleDensitySetter
from .specific_length import SpecificLength, SpecificLengthSetter
from .radiation_exposure import RadiationExposure, RadiationExposureSetter
from .activation_energy import ActivationEnergy, ActivationEnergySetter
from .illuminance import Illuminance, IlluminanceSetter
from .angular_acceleration import AngularAcceleration, AngularAccelerationSetter
from .wavenumber import Wavenumber, WavenumberSetter
from .radiation_dose_equivalent import RadiationDoseEquivalent, RadiationDoseEquivalentSetter
from .power_thermal_duty import PowerThermalDuty, PowerThermalDutySetter
from .specific_surface import SpecificSurface, SpecificSurfaceSetter
from .electric_current_intensity import ElectricCurrentIntensity, ElectricCurrentIntensitySetter
from .electric_inductance import ElectricInductance, ElectricInductanceSetter
from .mole_fraction_of_i import MoleFractionOfI, MoleFractionOfISetter
from .volumetric_calorific_heating_value import VolumetricCalorificheatingValue, VolumetricCalorificheatingValueSetter
from .normality_of_solution import NormalityOfSolution, NormalityOfSolutionSetter

__all__ = [
    # Variable classes
    'Length',
    'Pressure',
    'Dimensionless',
    'Time',
    'AbsorbedDose',
    'Acceleration',
    'Angle',
    'MassFractionOfI',
    'Forcebody',
    'Luminanceself',
    'SecondRadiationConstantplanck',
    'ViscosityKinematic',
    'ElectricCharge',
    'PowerPerUnitVolumeOrPowerDensity',
    'DynamicFluidity',
    'MassDensity',
    'VolumeFractionOfI',
    'AngleSolid',
    'FrequencyVoltageRatio',
    'SpecificEnthalpy',
    'LinearMassDensity',
    'AtomicWeight',
    'MolarHeatCapacity',
    'MassFlux',
    'HeatOfFusion',
    'SpecificVolume',
    'VolumetricMassFlowRate',
    'Permeability',
    'Stress',
    'Volume',
    'MolalityOfSoluteI',
    'MomentOfInertia',
    'Radioactivity',
    'ElectricResistance',
    'MolarityOfI',
    'Area',
    'MassFlowRate',
    'EnergyHeatWork',
    'ElectricPotential',
    'ViscosityDynamic',
    'Torque',
    'ElectricFieldStrength',
    'VelocityLinear',
    'MolarConcentrationByMass',
    'LuminousIntensity',
    'EnergyFlux',
    'MolarFlux',
    'AngularMomentum',
    'ElectricDipoleMoment',
    'SurfaceTension',
    'HeatTransferCoefficient',
    'MagneticFlux',
    'VolumetricFlowRate',
    'MomentumFlux',
    'Force',
    'SpecificGravity',
    'VolumetricFlux',
    'Concentration',
    'ElectricalConductance',
    'SurfaceMassDensity',
    'MagneticField',
    'MomentumFlowRate',
    'MolarFlowRate',
    'ForcePerUnitMass',
    'ThermalConductivity',
    'Mass',
    'LuminousFlux',
    'ElectricalPermittivity',
    'MassTransferCoefficient',
    'MagneticPermeability',
    'VolumetricCoefficientOfExpansion',
    'MagnetomotiveForce',
    'PhotonEmissionRate',
    'ElectricCapacitance',
    'MagneticInductionFieldStrength',
    'PowerPerUnitMassOrSpecificPower',
    'VelocityAngular',
    'LinearMomentum',
    'KineticEnergyOfTurbulence',
    'TurbulenceEnergyDissipationRate',
    'AnglePlane',
    'FuelConsumption',
    'HeatOfCombustion',
    'ElectricalResistivity',
    'Temperature',
    'EnergyPerUnitArea',
    'AmountOfSubstance',
    'MagneticMoment',
    'HeatOfVaporization',
    'AreaPerUnitVolume',
    'SpecificHeatCapacityconstantPressure',
    'SecondMomentOfArea',
    'ParticleDensity',
    'SpecificLength',
    'RadiationExposure',
    'ActivationEnergy',
    'Illuminance',
    'AngularAcceleration',
    'Wavenumber',
    'RadiationDoseEquivalent',
    'PowerThermalDuty',
    'SpecificSurface',
    'ElectricCurrentIntensity',
    'ElectricInductance',
    'MoleFractionOfI',
    'VolumetricCalorificheatingValue',
    'NormalityOfSolution',
    # Setter classes
    'LengthSetter',
    'PressureSetter',
    'DimensionlessSetter',
    'TimeSetter',
    'AbsorbedDoseSetter',
    'AccelerationSetter',
    'AngleSetter',
    'TypeSafeSetter',
    'MassFractionOfISetter',
    'ForcebodySetter',
    'LuminanceselfSetter',
    'SecondRadiationConstantplanckSetter',
    'ViscosityKinematicSetter',
    'ElectricChargeSetter',
    'PowerPerUnitVolumeOrPowerDensitySetter',
    'DynamicFluiditySetter',
    'MassDensitySetter',
    'VolumeFractionOfISetter',
    'AngleSolidSetter',
    'FrequencyVoltageRatioSetter',
    'SpecificEnthalpySetter',
    'LinearMassDensitySetter',
    'AtomicWeightSetter',
    'MolarHeatCapacitySetter',
    'MassFluxSetter',
    'HeatOfFusionSetter',
    'SpecificVolumeSetter',
    'VolumetricMassFlowRateSetter',
    'PermeabilitySetter',
    'StressSetter',
    'VolumeSetter',
    'MolalityOfSoluteISetter',
    'MomentOfInertiaSetter',
    'RadioactivitySetter',
    'ElectricResistanceSetter',
    'MolarityOfISetter',
    'AreaSetter',
    'MassFlowRateSetter',
    'EnergyHeatWorkSetter',
    'ElectricPotentialSetter',
    'ViscosityDynamicSetter',
    'TorqueSetter',
    'ElectricFieldStrengthSetter',
    'VelocityLinearSetter',
    'MolarConcentrationByMassSetter',
    'LuminousIntensitySetter',
    'EnergyFluxSetter',
    'MolarFluxSetter',
    'AngularMomentumSetter',
    'ElectricDipoleMomentSetter',
    'SurfaceTensionSetter',
    'HeatTransferCoefficientSetter',
    'MagneticFluxSetter',
    'VolumetricFlowRateSetter',
    'MomentumFluxSetter',
    'ForceSetter',
    'SpecificGravitySetter',
    'VolumetricFluxSetter',
    'ConcentrationSetter',
    'ElectricalConductanceSetter',
    'SurfaceMassDensitySetter',
    'MagneticFieldSetter',
    'MomentumFlowRateSetter',
    'MolarFlowRateSetter',
    'ForcePerUnitMassSetter',
    'ThermalConductivitySetter',
    'MassSetter',
    'LuminousFluxSetter',
    'ElectricalPermittivitySetter',
    'MassTransferCoefficientSetter',
    'MagneticPermeabilitySetter',
    'VolumetricCoefficientOfExpansionSetter',
    'MagnetomotiveForceSetter',
    'PhotonEmissionRateSetter',
    'ElectricCapacitanceSetter',
    'MagneticInductionFieldStrengthSetter',
    'PowerPerUnitMassOrSpecificPowerSetter',
    'VelocityAngularSetter',
    'LinearMomentumSetter',
    'KineticEnergyOfTurbulenceSetter',
    'TurbulenceEnergyDissipationRateSetter',
    'AnglePlaneSetter',
    'FuelConsumptionSetter',
    'HeatOfCombustionSetter',
    'ElectricalResistivitySetter',
    'TemperatureSetter',
    'EnergyPerUnitAreaSetter',
    'AmountOfSubstanceSetter',
    'MagneticMomentSetter',
    'HeatOfVaporizationSetter',
    'AreaPerUnitVolumeSetter',
    'SpecificHeatCapacityconstantPressureSetter',
    'SecondMomentOfAreaSetter',
    'ParticleDensitySetter',
    'SpecificLengthSetter',
    'RadiationExposureSetter',
    'ActivationEnergySetter',
    'IlluminanceSetter',
    'AngularAccelerationSetter',
    'WavenumberSetter',
    'RadiationDoseEquivalentSetter',
    'PowerThermalDutySetter',
    'SpecificSurfaceSetter',
    'ElectricCurrentIntensitySetter',
    'ElectricInductanceSetter',
    'MoleFractionOfISetter',
    'VolumetricCalorificheatingValueSetter',
    'NormalityOfSolutionSetter',
    'VariableModule',
    'VariableRegistry',
    'variable_registry'
]