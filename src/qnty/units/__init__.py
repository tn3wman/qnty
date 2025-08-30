"""
Units Package with Auto-Discovery and Registration
=================================================

Automatically discovers and registers all unit modules, then populates
their unit constant classes.
"""

import importlib
import pkgutil
from ..unit import registry

# Auto-discover and register all unit modules
for importer, modname, ispkg in pkgutil.iter_modules(__path__):
    if modname not in ['__init__', 'base']:
        module = importlib.import_module(f'.{modname}', __name__)
        
        # Register definitions to global registry (modules may have pre-populated some)
        if hasattr(module, 'UNIT_MODULE'):
            module.UNIT_MODULE.register_to_registry(registry)

# Finalize registry after all registrations
registry.finalize_registration()

# Export unit classes for public API
from .length import LengthUnits
from .pressure import PressureUnits  
from .dimensionless import DimensionlessUnits
from .time import TimeUnits
from .temperature import TemperatureUnits
from .absorbed_radiation_dose import AbsorbedDoseUnits
from .acceleration import AccelerationUnits
from .angle_plane import AnglePlaneUnits
from .mass_fraction_of_i import MassFractionOfIUnits
from .force_body import ForcebodyUnits
from .luminance_self import LuminanceselfUnits
from .second_radiation_constant_planck import SecondRadiationConstantplanckUnits
from .viscosity_kinematic import ViscosityKinematicUnits
from .electric_charge import ElectricChargeUnits
from .power_per_unit_volume import PowerPerUnitVolumeOrPowerDensityUnits
from .dynamic_fluidity import DynamicFluidityUnits
from .mass_density import MassDensityUnits
from .volume_fraction_of_i import VolumeFractionOfIUnits
from .angle_solid import AngleSolidUnits
from .frequency_voltage_ratio import FrequencyVoltageRatioUnits
from .specific_enthalpy import SpecificEnthalpyUnits
from .linear_mass_density import LinearMassDensityUnits
from .atomic_weight import AtomicWeightUnits
from .molar_heat_capacity import MolarHeatCapacityUnits
from .mass_flux import MassFluxUnits
from .heat_of_fusion import HeatOfFusionUnits
from .specific_volume import SpecificVolumeUnits
from .volumetric_mass_flow_rate import VolumetricMassFlowRateUnits
from .permeability import PermeabilityUnits
from .stress import StressUnits
from .volume import VolumeUnits
from .absorbed_radiation_dose import AbsorbedDoseUnits
from .molality_of_solute_i import MolalityOfSoluteIUnits
from .moment_of_inertia import MomentOfInertiaUnits
from .radioactivity import RadioactivityUnits
from .electric_resistance import ElectricResistanceUnits
from .molarity_of_i import MolarityOfIUnits
from .area import AreaUnits
from .mass_flow_rate import MassFlowRateUnits
from .energy_heat_work import EnergyHeatWorkUnits
from .electric_potential import ElectricPotentialUnits
from .viscosity_dynamic import ViscosityDynamicUnits
from .torque import TorqueUnits
from .electric_field_strength import ElectricFieldStrengthUnits
from .velocity_linear import VelocityLinearUnits
from .molar_concentration_by_mass import MolarConcentrationByMassUnits
from .luminous_intensity import LuminousIntensityUnits
from .energy_flux import EnergyFluxUnits
from .molar_flux import MolarFluxUnits
from .angular_momentum import AngularMomentumUnits
from .electric_dipole_moment import ElectricDipoleMomentUnits
from .surface_tension import SurfaceTensionUnits
from .heat_transfer_coefficient import HeatTransferCoefficientUnits
from .magnetic_flux import MagneticFluxUnits
from .volumetric_flow_rate import VolumetricFlowRateUnits
from .momentum_flux import MomentumFluxUnits
from .force import ForceUnits
from .specific_gravity import SpecificGravityUnits
from .volumetric_flux import VolumetricFluxUnits
from .concentration import ConcentrationUnits
from .electrical_conductance import ElectricalConductanceUnits
from .surface_mass_density import SurfaceMassDensityUnits
from .magnetic_field import MagneticFieldUnits
from .momentum_flow_rate import MomentumFlowRateUnits
from .molar_flow_rate import MolarFlowRateUnits
from .force_per_unit_mass import ForcePerUnitMassUnits
from .thermal_conductivity import ThermalConductivityUnits
from .mass import MassUnits
from .luminous_flux import LuminousFluxUnits
from .electrical_permittivity import ElectricalPermittivityUnits
from .mass_transfer_coefficient import MassTransferCoefficientUnits
from .magnetic_permeability import MagneticPermeabilityUnits
from .volumetric_coefficient_of_expansion import VolumetricCoefficientOfExpansionUnits
from .magnetomotive_force import MagnetomotiveForceUnits
from .photon_emission_rate import PhotonEmissionRateUnits
from .electric_capacitance import ElectricCapacitanceUnits
from .magnetic_induction_field_strength import MagneticInductionFieldStrengthUnits
from .power_per_unit_mass import PowerPerUnitMassOrSpecificPowerUnits
from .velocity_angular import VelocityAngularUnits
from .linear_momentum import LinearMomentumUnits
from .kinetic_energy_of_turbulence import KineticEnergyOfTurbulenceUnits
from .turbulence_energy_dissipation_rate import TurbulenceEnergyDissipationRateUnits
from .angle_plane import AnglePlaneUnits
from .fuel_consumption import FuelConsumptionUnits
from .heat_of_combustion import HeatOfCombustionUnits
from .electrical_resistivity import ElectricalResistivityUnits
from .energy_per_unit_area import EnergyPerUnitAreaUnits
from .amount_of_substance import AmountOfSubstanceUnits
from .magnetic_moment import MagneticMomentUnits
from .heat_of_vaporization import HeatOfVaporizationUnits
from .area_per_unit_volume import AreaPerUnitVolumeUnits
from .specific_heat_capacity_constant_pressure import SpecificHeatCapacityconstantPressureUnits
from .second_moment_of_area import SecondMomentOfAreaUnits
from .particle_density import ParticleDensityUnits
from .specific_length import SpecificLengthUnits
from .radiation_exposure import RadiationExposureUnits
from .activation_energy import ActivationEnergyUnits
from .illuminance import IlluminanceUnits
from .angular_acceleration import AngularAccelerationUnits
from .wavenumber import WavenumberUnits
from .radiation_dose_equivalent import RadiationDoseEquivalentUnits
from .power_thermal_duty import PowerThermalDutyUnits
from .specific_surface import SpecificSurfaceUnits
from .electric_current_intensity import ElectricCurrentIntensityUnits
from .electric_inductance import ElectricInductanceUnits
from .mole_fraction_of_i import MoleFractionOfIUnits
from .volumetric_calorific_heating_value import VolumetricCalorificheatingValueUnits
from .normality_of_solution import NormalityOfSolutionUnits

__all__ = ['LengthUnits', 'PressureUnits', 'DimensionlessUnits', 'TimeUnits', 'TemperatureUnits', 'AbsorbedDoseUnits', 'AccelerationUnits', 'AngleUnits', 'MassFractionOfIUnits', 'ForcebodyUnits', 'LuminanceselfUnits', 'SecondRadiationConstantplanckUnits', 'ViscosityKinematicUnits', 'ElectricChargeUnits', 'PowerPerUnitVolumeOrPowerDensityUnits', 'DynamicFluidityUnits', 'MassDensityUnits', 'VolumeFractionOfIUnits', 'AngleSolidUnits', 'FrequencyVoltageRatioUnits', 'SpecificEnthalpyUnits', 'LinearMassDensityUnits', 'AtomicWeightUnits', 'MolarHeatCapacityUnits', 'MassFluxUnits', 'HeatOfFusionUnits', 'SpecificVolumeUnits', 'VolumetricMassFlowRateUnits', 'PermeabilityUnits', 'StressUnits', 'VolumeUnits', 'MolalityOfSoluteIUnits', 'MomentOfInertiaUnits', 'RadioactivityUnits', 'ElectricResistanceUnits', 'MolarityOfIUnits', 'AreaUnits', 'MassFlowRateUnits', 'EnergyHeatWorkUnits', 'ElectricPotentialUnits', 'ViscosityDynamicUnits', 'TorqueUnits', 'ElectricFieldStrengthUnits', 'VelocityLinearUnits', 'MolarConcentrationByMassUnits', 'LuminousIntensityUnits', 'EnergyFluxUnits', 'MolarFluxUnits', 'AngularMomentumUnits', 'ElectricDipoleMomentUnits', 'SurfaceTensionUnits', 'HeatTransferCoefficientUnits', 'MagneticFluxUnits', 'VolumetricFlowRateUnits', 'MomentumFluxUnits', 'ForceUnits', 'SpecificGravityUnits', 'VolumetricFluxUnits', 'ConcentrationUnits', 'ElectricalConductanceUnits', 'SurfaceMassDensityUnits', 'MagneticFieldUnits', 'MomentumFlowRateUnits', 'MolarFlowRateUnits', 'ForcePerUnitMassUnits', 'ThermalConductivityUnits', 'MassUnits', 'LuminousFluxUnits', 'ElectricalPermittivityUnits', 'MassTransferCoefficientUnits', 'MagneticPermeabilityUnits', 'VolumetricCoefficientOfExpansionUnits', 'MagnetomotiveForceUnits', 'PhotonEmissionRateUnits', 'ElectricCapacitanceUnits', 'MagneticInductionFieldStrengthUnits', 'PowerPerUnitMassOrSpecificPowerUnits', 'VelocityAngularUnits', 'LinearMomentumUnits', 'KineticEnergyOfTurbulenceUnits', 'TurbulenceEnergyDissipationRateUnits', 'AnglePlaneUnits', 'FuelConsumptionUnits', 'HeatOfCombustionUnits', 'ElectricalResistivityUnits', 'EnergyPerUnitAreaUnits', 'AmountOfSubstanceUnits', 'MagneticMomentUnits', 'HeatOfVaporizationUnits', 'AreaPerUnitVolumeUnits', 'SpecificHeatCapacityconstantPressureUnits', 'SecondMomentOfAreaUnits', 'ParticleDensityUnits', 'SpecificLengthUnits', 'RadiationExposureUnits', 'ActivationEnergyUnits', 'IlluminanceUnits', 'AngularAccelerationUnits', 'WavenumberUnits', 'RadiationDoseEquivalentUnits', 'PowerThermalDutyUnits', 'SpecificSurfaceUnits', 'ElectricCurrentIntensityUnits', 'ElectricInductanceUnits', 'MoleFractionOfIUnits', 'VolumetricCalorificheatingValueUnits', 'NormalityOfSolutionUnits']