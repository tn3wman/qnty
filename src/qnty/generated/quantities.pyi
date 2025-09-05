"""
Type stubs for quantities module - Complete Edition.

Provides complete type hints for IDE autocomplete and type checking
for quantity classes and their setter relationships.
Contains 107 quantity types with 871 total units.

Auto-generated from unit_data.json.
"""

from typing import Any

from ..quantities.typed_quantity import TypedQuantity
from . import dimensions as dim
from . import setters as ts

# ===== QUANTITY CLASSES =====
# Type stubs for quantity classes with setter relationships

class AbsorbedDose(TypedQuantity):
    """Type-safe absorbed radiation dose quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AbsorbedDoseSetter
    _expected_dimension = dim.ABSORBED_DOSE
    
    def set(self, value: float) -> ts.AbsorbedDoseSetter:
        """Create a setter for this quantity."""
        ...
    

class Acceleration(TypedQuantity):
    """Type-safe acceleration quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AccelerationSetter
    _expected_dimension = dim.ACCELERATION
    
    def set(self, value: float) -> ts.AccelerationSetter:
        """Create a setter for this quantity."""
        ...
    

class ActivationEnergy(TypedQuantity):
    """Type-safe activation energy quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ActivationEnergySetter
    _expected_dimension = dim.ACTIVATION_ENERGY
    
    def set(self, value: float) -> ts.ActivationEnergySetter:
        """Create a setter for this quantity."""
        ...
    

class AmountOfSubstance(TypedQuantity):
    """Type-safe amount of substance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AmountOfSubstanceSetter
    _expected_dimension = dim.AMOUNT_OF_SUBSTANCE
    
    def set(self, value: float) -> ts.AmountOfSubstanceSetter:
        """Create a setter for this quantity."""
        ...
    

class AnglePlane(TypedQuantity):
    """Type-safe angle, plane quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AnglePlaneSetter
    _expected_dimension = dim.ANGLE_PLANE
    
    def set(self, value: float) -> ts.AnglePlaneSetter:
        """Create a setter for this quantity."""
        ...
    

class AngleSolid(TypedQuantity):
    """Type-safe angle, solid quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AngleSolidSetter
    _expected_dimension = dim.ANGLE_SOLID
    
    def set(self, value: float) -> ts.AngleSolidSetter:
        """Create a setter for this quantity."""
        ...
    

class AngularAcceleration(TypedQuantity):
    """Type-safe angular acceleration quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AngularAccelerationSetter
    _expected_dimension = dim.ANGULAR_ACCELERATION
    
    def set(self, value: float) -> ts.AngularAccelerationSetter:
        """Create a setter for this quantity."""
        ...
    

class AngularMomentum(TypedQuantity):
    """Type-safe angular momentum quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AngularMomentumSetter
    _expected_dimension = dim.ANGULAR_MOMENTUM
    
    def set(self, value: float) -> ts.AngularMomentumSetter:
        """Create a setter for this quantity."""
        ...
    

class Area(TypedQuantity):
    """Type-safe area quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AreaSetter
    _expected_dimension = dim.AREA
    
    def set(self, value: float) -> ts.AreaSetter:
        """Create a setter for this quantity."""
        ...
    

class AreaPerUnitVolume(TypedQuantity):
    """Type-safe area per unit volume quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AreaPerUnitVolumeSetter
    _expected_dimension = dim.AREA_PER_UNIT_VOLUME
    
    def set(self, value: float) -> ts.AreaPerUnitVolumeSetter:
        """Create a setter for this quantity."""
        ...
    

class AtomicWeight(TypedQuantity):
    """Type-safe atomic weight quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AtomicWeightSetter
    _expected_dimension = dim.ATOMIC_WEIGHT
    
    def set(self, value: float) -> ts.AtomicWeightSetter:
        """Create a setter for this quantity."""
        ...
    

class Concentration(TypedQuantity):
    """Type-safe concentration quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ConcentrationSetter
    _expected_dimension = dim.CONCENTRATION
    
    def set(self, value: float) -> ts.ConcentrationSetter:
        """Create a setter for this quantity."""
        ...
    

class Dimensionless(TypedQuantity):
    """Type-safe dimensionless quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.DimensionlessSetter
    _expected_dimension = dim.DIMENSIONLESS
    
    def set(self, value: float) -> ts.DimensionlessSetter:
        """Create a setter for this quantity."""
        ...
    

class DynamicFluidity(TypedQuantity):
    """Type-safe dynamic fluidity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.DynamicFluiditySetter
    _expected_dimension = dim.DYNAMIC_FLUIDITY
    
    def set(self, value: float) -> ts.DynamicFluiditySetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricCapacitance(TypedQuantity):
    """Type-safe electric capacitance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricCapacitanceSetter
    _expected_dimension = dim.ELECTRIC_CAPACITANCE
    
    def set(self, value: float) -> ts.ElectricCapacitanceSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricCharge(TypedQuantity):
    """Type-safe electric charge quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricChargeSetter
    _expected_dimension = dim.ELECTRIC_CHARGE
    
    def set(self, value: float) -> ts.ElectricChargeSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricCurrentIntensity(TypedQuantity):
    """Type-safe electric current intensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricCurrentIntensitySetter
    _expected_dimension = dim.ELECTRIC_CURRENT_INTENSITY
    
    def set(self, value: float) -> ts.ElectricCurrentIntensitySetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricDipoleMoment(TypedQuantity):
    """Type-safe electric dipole moment quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricDipoleMomentSetter
    _expected_dimension = dim.ELECTRIC_DIPOLE_MOMENT
    
    def set(self, value: float) -> ts.ElectricDipoleMomentSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricFieldStrength(TypedQuantity):
    """Type-safe electric field strength quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricFieldStrengthSetter
    _expected_dimension = dim.ELECTRIC_FIELD_STRENGTH
    
    def set(self, value: float) -> ts.ElectricFieldStrengthSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricInductance(TypedQuantity):
    """Type-safe electric inductance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricInductanceSetter
    _expected_dimension = dim.ELECTRIC_INDUCTANCE
    
    def set(self, value: float) -> ts.ElectricInductanceSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricPotential(TypedQuantity):
    """Type-safe electric potential quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricPotentialSetter
    _expected_dimension = dim.ELECTRIC_POTENTIAL
    
    def set(self, value: float) -> ts.ElectricPotentialSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricResistance(TypedQuantity):
    """Type-safe electric resistance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricResistanceSetter
    _expected_dimension = dim.ELECTRIC_RESISTANCE
    
    def set(self, value: float) -> ts.ElectricResistanceSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricalConductance(TypedQuantity):
    """Type-safe electrical conductance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricalConductanceSetter
    _expected_dimension = dim.ELECTRICAL_CONDUCTANCE
    
    def set(self, value: float) -> ts.ElectricalConductanceSetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricalPermittivity(TypedQuantity):
    """Type-safe electrical permittivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricalPermittivitySetter
    _expected_dimension = dim.ELECTRICAL_PERMITTIVITY
    
    def set(self, value: float) -> ts.ElectricalPermittivitySetter:
        """Create a setter for this quantity."""
        ...
    

class ElectricalResistivity(TypedQuantity):
    """Type-safe electrical resistivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricalResistivitySetter
    _expected_dimension = dim.ELECTRICAL_RESISTIVITY
    
    def set(self, value: float) -> ts.ElectricalResistivitySetter:
        """Create a setter for this quantity."""
        ...
    

class EnergyFlux(TypedQuantity):
    """Type-safe energy flux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.EnergyFluxSetter
    _expected_dimension = dim.ENERGY_FLUX
    
    def set(self, value: float) -> ts.EnergyFluxSetter:
        """Create a setter for this quantity."""
        ...
    

class EnergyHeatWork(TypedQuantity):
    """Type-safe energy, heat, work quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.EnergyHeatWorkSetter
    _expected_dimension = dim.ENERGY_HEAT_WORK
    
    def set(self, value: float) -> ts.EnergyHeatWorkSetter:
        """Create a setter for this quantity."""
        ...
    

class EnergyPerUnitArea(TypedQuantity):
    """Type-safe energy per unit area quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.EnergyPerUnitAreaSetter
    _expected_dimension = dim.ENERGY_PER_UNIT_AREA
    
    def set(self, value: float) -> ts.EnergyPerUnitAreaSetter:
        """Create a setter for this quantity."""
        ...
    

class Force(TypedQuantity):
    """Type-safe force quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ForceSetter
    _expected_dimension = dim.FORCE
    
    def set(self, value: float) -> ts.ForceSetter:
        """Create a setter for this quantity."""
        ...
    

class ForceBody(TypedQuantity):
    """Type-safe force (body) quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ForceBodySetter
    _expected_dimension = dim.FORCE_BODY
    
    def set(self, value: float) -> ts.ForceBodySetter:
        """Create a setter for this quantity."""
        ...
    

class ForcePerUnitMass(TypedQuantity):
    """Type-safe force per unit mass quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ForcePerUnitMassSetter
    _expected_dimension = dim.FORCE_PER_UNIT_MASS
    
    def set(self, value: float) -> ts.ForcePerUnitMassSetter:
        """Create a setter for this quantity."""
        ...
    

class FrequencyVoltageRatio(TypedQuantity):
    """Type-safe frequency voltage ratio quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.FrequencyVoltageRatioSetter
    _expected_dimension = dim.FREQUENCY_VOLTAGE_RATIO
    
    def set(self, value: float) -> ts.FrequencyVoltageRatioSetter:
        """Create a setter for this quantity."""
        ...
    

class FuelConsumption(TypedQuantity):
    """Type-safe fuel consumption quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.FuelConsumptionSetter
    _expected_dimension = dim.FUEL_CONSUMPTION
    
    def set(self, value: float) -> ts.FuelConsumptionSetter:
        """Create a setter for this quantity."""
        ...
    

class HeatOfCombustion(TypedQuantity):
    """Type-safe heat of combustion quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatOfCombustionSetter
    _expected_dimension = dim.HEAT_OF_COMBUSTION
    
    def set(self, value: float) -> ts.HeatOfCombustionSetter:
        """Create a setter for this quantity."""
        ...
    

class HeatOfFusion(TypedQuantity):
    """Type-safe heat of fusion quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatOfFusionSetter
    _expected_dimension = dim.HEAT_OF_FUSION
    
    def set(self, value: float) -> ts.HeatOfFusionSetter:
        """Create a setter for this quantity."""
        ...
    

class HeatOfVaporization(TypedQuantity):
    """Type-safe heat of vaporization quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatOfVaporizationSetter
    _expected_dimension = dim.HEAT_OF_VAPORIZATION
    
    def set(self, value: float) -> ts.HeatOfVaporizationSetter:
        """Create a setter for this quantity."""
        ...
    

class HeatTransferCoefficient(TypedQuantity):
    """Type-safe heat transfer coefficient quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatTransferCoefficientSetter
    _expected_dimension = dim.HEAT_TRANSFER_COEFFICIENT
    
    def set(self, value: float) -> ts.HeatTransferCoefficientSetter:
        """Create a setter for this quantity."""
        ...
    

class Illuminance(TypedQuantity):
    """Type-safe illuminance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.IlluminanceSetter
    _expected_dimension = dim.ILLUMINANCE
    
    def set(self, value: float) -> ts.IlluminanceSetter:
        """Create a setter for this quantity."""
        ...
    

class KineticEnergyOfTurbulence(TypedQuantity):
    """Type-safe kinetic energy of turbulence quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.KineticEnergyOfTurbulenceSetter
    _expected_dimension = dim.KINETIC_ENERGY_OF_TURBULENCE
    
    def set(self, value: float) -> ts.KineticEnergyOfTurbulenceSetter:
        """Create a setter for this quantity."""
        ...
    

class Length(TypedQuantity):
    """Type-safe length quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LengthSetter
    _expected_dimension = dim.LENGTH
    
    def set(self, value: float) -> ts.LengthSetter:
        """Create a setter for this quantity."""
        ...
    

class LinearMassDensity(TypedQuantity):
    """Type-safe linear mass density quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LinearMassDensitySetter
    _expected_dimension = dim.LINEAR_MASS_DENSITY
    
    def set(self, value: float) -> ts.LinearMassDensitySetter:
        """Create a setter for this quantity."""
        ...
    

class LinearMomentum(TypedQuantity):
    """Type-safe linear momentum quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LinearMomentumSetter
    _expected_dimension = dim.LINEAR_MOMENTUM
    
    def set(self, value: float) -> ts.LinearMomentumSetter:
        """Create a setter for this quantity."""
        ...
    

class LuminanceSelf(TypedQuantity):
    """Type-safe luminance (self) quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LuminanceSelfSetter
    _expected_dimension = dim.LUMINANCE_SELF
    
    def set(self, value: float) -> ts.LuminanceSelfSetter:
        """Create a setter for this quantity."""
        ...
    

class LuminousFlux(TypedQuantity):
    """Type-safe luminous flux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LuminousFluxSetter
    _expected_dimension = dim.LUMINOUS_FLUX
    
    def set(self, value: float) -> ts.LuminousFluxSetter:
        """Create a setter for this quantity."""
        ...
    

class LuminousIntensity(TypedQuantity):
    """Type-safe luminous intensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LuminousIntensitySetter
    _expected_dimension = dim.LUMINOUS_INTENSITY
    
    def set(self, value: float) -> ts.LuminousIntensitySetter:
        """Create a setter for this quantity."""
        ...
    

class MagneticField(TypedQuantity):
    """Type-safe magnetic field quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticFieldSetter
    _expected_dimension = dim.MAGNETIC_FIELD
    
    def set(self, value: float) -> ts.MagneticFieldSetter:
        """Create a setter for this quantity."""
        ...
    

class MagneticFlux(TypedQuantity):
    """Type-safe magnetic flux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticFluxSetter
    _expected_dimension = dim.MAGNETIC_FLUX
    
    def set(self, value: float) -> ts.MagneticFluxSetter:
        """Create a setter for this quantity."""
        ...
    

class MagneticInductionFieldStrength(TypedQuantity):
    """Type-safe magnetic induction field strength quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticInductionFieldStrengthSetter
    _expected_dimension = dim.MAGNETIC_INDUCTION_FIELD_STRENGTH
    
    def set(self, value: float) -> ts.MagneticInductionFieldStrengthSetter:
        """Create a setter for this quantity."""
        ...
    

class MagneticMoment(TypedQuantity):
    """Type-safe magnetic moment quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticMomentSetter
    _expected_dimension = dim.MAGNETIC_MOMENT
    
    def set(self, value: float) -> ts.MagneticMomentSetter:
        """Create a setter for this quantity."""
        ...
    

class MagneticPermeability(TypedQuantity):
    """Type-safe magnetic permeability quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticPermeabilitySetter
    _expected_dimension = dim.MAGNETIC_PERMEABILITY
    
    def set(self, value: float) -> ts.MagneticPermeabilitySetter:
        """Create a setter for this quantity."""
        ...
    

class MagnetomotiveForce(TypedQuantity):
    """Type-safe magnetomotive force quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagnetomotiveForceSetter
    _expected_dimension = dim.MAGNETOMOTIVE_FORCE
    
    def set(self, value: float) -> ts.MagnetomotiveForceSetter:
        """Create a setter for this quantity."""
        ...
    

class Mass(TypedQuantity):
    """Type-safe mass quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassSetter
    _expected_dimension = dim.MASS
    
    def set(self, value: float) -> ts.MassSetter:
        """Create a setter for this quantity."""
        ...
    

class MassDensity(TypedQuantity):
    """Type-safe mass density quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassDensitySetter
    _expected_dimension = dim.MASS_DENSITY
    
    def set(self, value: float) -> ts.MassDensitySetter:
        """Create a setter for this quantity."""
        ...
    

class MassFlowRate(TypedQuantity):
    """Type-safe mass flow rate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassFlowRateSetter
    _expected_dimension = dim.MASS_FLOW_RATE
    
    def set(self, value: float) -> ts.MassFlowRateSetter:
        """Create a setter for this quantity."""
        ...
    

class MassFlux(TypedQuantity):
    """Type-safe mass flux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassFluxSetter
    _expected_dimension = dim.MASS_FLUX
    
    def set(self, value: float) -> ts.MassFluxSetter:
        """Create a setter for this quantity."""
        ...
    

class MassFractionOfI(TypedQuantity):
    """Type-safe mass fraction of "i" quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassFractionOfISetter
    _expected_dimension = dim.MASS_FRACTION_OF_I
    
    def set(self, value: float) -> ts.MassFractionOfISetter:
        """Create a setter for this quantity."""
        ...
    

class MassTransferCoefficient(TypedQuantity):
    """Type-safe mass transfer coefficient quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassTransferCoefficientSetter
    _expected_dimension = dim.MASS_TRANSFER_COEFFICIENT
    
    def set(self, value: float) -> ts.MassTransferCoefficientSetter:
        """Create a setter for this quantity."""
        ...
    

class MolalityOfSoluteI(TypedQuantity):
    """Type-safe molality of solute "i" quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolalityOfSoluteISetter
    _expected_dimension = dim.MOLALITY_OF_SOLUTE_I
    
    def set(self, value: float) -> ts.MolalityOfSoluteISetter:
        """Create a setter for this quantity."""
        ...
    

class MolarConcentrationByMass(TypedQuantity):
    """Type-safe molar concentration by mass quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarConcentrationByMassSetter
    _expected_dimension = dim.MOLAR_CONCENTRATION_BY_MASS
    
    def set(self, value: float) -> ts.MolarConcentrationByMassSetter:
        """Create a setter for this quantity."""
        ...
    

class MolarFlowRate(TypedQuantity):
    """Type-safe molar flow rate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarFlowRateSetter
    _expected_dimension = dim.MOLAR_FLOW_RATE
    
    def set(self, value: float) -> ts.MolarFlowRateSetter:
        """Create a setter for this quantity."""
        ...
    

class MolarFlux(TypedQuantity):
    """Type-safe molar flux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarFluxSetter
    _expected_dimension = dim.MOLAR_FLUX
    
    def set(self, value: float) -> ts.MolarFluxSetter:
        """Create a setter for this quantity."""
        ...
    

class MolarHeatCapacity(TypedQuantity):
    """Type-safe molar heat capacity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarHeatCapacitySetter
    _expected_dimension = dim.MOLAR_HEAT_CAPACITY
    
    def set(self, value: float) -> ts.MolarHeatCapacitySetter:
        """Create a setter for this quantity."""
        ...
    

class MolarityOfI(TypedQuantity):
    """Type-safe molarity of "i" quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarityOfISetter
    _expected_dimension = dim.MOLARITY_OF_I
    
    def set(self, value: float) -> ts.MolarityOfISetter:
        """Create a setter for this quantity."""
        ...
    

class MoleFractionOfI(TypedQuantity):
    """Type-safe mole fraction of "i" quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MoleFractionOfISetter
    _expected_dimension = dim.MOLE_FRACTION_OF_I
    
    def set(self, value: float) -> ts.MoleFractionOfISetter:
        """Create a setter for this quantity."""
        ...
    

class MomentOfInertia(TypedQuantity):
    """Type-safe moment of inertia quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MomentOfInertiaSetter
    _expected_dimension = dim.MOMENT_OF_INERTIA
    
    def set(self, value: float) -> ts.MomentOfInertiaSetter:
        """Create a setter for this quantity."""
        ...
    

class MomentumFlowRate(TypedQuantity):
    """Type-safe momentum flow rate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MomentumFlowRateSetter
    _expected_dimension = dim.MOMENTUM_FLOW_RATE
    
    def set(self, value: float) -> ts.MomentumFlowRateSetter:
        """Create a setter for this quantity."""
        ...
    

class MomentumFlux(TypedQuantity):
    """Type-safe momentum flux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MomentumFluxSetter
    _expected_dimension = dim.MOMENTUM_FLUX
    
    def set(self, value: float) -> ts.MomentumFluxSetter:
        """Create a setter for this quantity."""
        ...
    

class NormalityOfSolution(TypedQuantity):
    """Type-safe normality of solution quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.NormalityOfSolutionSetter
    _expected_dimension = dim.NORMALITY_OF_SOLUTION
    
    def set(self, value: float) -> ts.NormalityOfSolutionSetter:
        """Create a setter for this quantity."""
        ...
    

class ParticleDensity(TypedQuantity):
    """Type-safe particle density quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ParticleDensitySetter
    _expected_dimension = dim.PARTICLE_DENSITY
    
    def set(self, value: float) -> ts.ParticleDensitySetter:
        """Create a setter for this quantity."""
        ...
    

class Percent(TypedQuantity):
    """Type-safe percent quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PercentSetter
    _expected_dimension = dim.PERCENT
    
    def set(self, value: float) -> ts.PercentSetter:
        """Create a setter for this quantity."""
        ...
    

class Permeability(TypedQuantity):
    """Type-safe permeability quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PermeabilitySetter
    _expected_dimension = dim.PERMEABILITY
    
    def set(self, value: float) -> ts.PermeabilitySetter:
        """Create a setter for this quantity."""
        ...
    

class PhotonEmissionRate(TypedQuantity):
    """Type-safe photon emission rate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PhotonEmissionRateSetter
    _expected_dimension = dim.PHOTON_EMISSION_RATE
    
    def set(self, value: float) -> ts.PhotonEmissionRateSetter:
        """Create a setter for this quantity."""
        ...
    

class PowerPerUnitMass(TypedQuantity):
    """Type-safe power per unit mass or specific power quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PowerPerUnitMassSetter
    _expected_dimension = dim.POWER_PER_UNIT_MASS
    
    def set(self, value: float) -> ts.PowerPerUnitMassSetter:
        """Create a setter for this quantity."""
        ...
    

class PowerPerUnitVolume(TypedQuantity):
    """Type-safe power per unit volume or power density quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PowerPerUnitVolumeSetter
    _expected_dimension = dim.POWER_PER_UNIT_VOLUME
    
    def set(self, value: float) -> ts.PowerPerUnitVolumeSetter:
        """Create a setter for this quantity."""
        ...
    

class PowerThermalDuty(TypedQuantity):
    """Type-safe power, thermal duty quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PowerThermalDutySetter
    _expected_dimension = dim.POWER_THERMAL_DUTY
    
    def set(self, value: float) -> ts.PowerThermalDutySetter:
        """Create a setter for this quantity."""
        ...
    

class Pressure(TypedQuantity):
    """Type-safe pressure quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PressureSetter
    _expected_dimension = dim.PRESSURE
    
    def set(self, value: float) -> ts.PressureSetter:
        """Create a setter for this quantity."""
        ...
    

class RadiationDoseEquivalent(TypedQuantity):
    """Type-safe radiation dose equivalent quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.RadiationDoseEquivalentSetter
    _expected_dimension = dim.RADIATION_DOSE_EQUIVALENT
    
    def set(self, value: float) -> ts.RadiationDoseEquivalentSetter:
        """Create a setter for this quantity."""
        ...
    

class RadiationExposure(TypedQuantity):
    """Type-safe radiation exposure quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.RadiationExposureSetter
    _expected_dimension = dim.RADIATION_EXPOSURE
    
    def set(self, value: float) -> ts.RadiationExposureSetter:
        """Create a setter for this quantity."""
        ...
    

class Radioactivity(TypedQuantity):
    """Type-safe radioactivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.RadioactivitySetter
    _expected_dimension = dim.RADIOACTIVITY
    
    def set(self, value: float) -> ts.RadioactivitySetter:
        """Create a setter for this quantity."""
        ...
    

class SecondMomentOfArea(TypedQuantity):
    """Type-safe second moment of area quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SecondMomentOfAreaSetter
    _expected_dimension = dim.SECOND_MOMENT_OF_AREA
    
    def set(self, value: float) -> ts.SecondMomentOfAreaSetter:
        """Create a setter for this quantity."""
        ...
    

class SecondRadiationConstantPlanck(TypedQuantity):
    """Type-safe second radiation constant (planck) quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SecondRadiationConstantPlanckSetter
    _expected_dimension = dim.SECOND_RADIATION_CONSTANT_PLANCK
    
    def set(self, value: float) -> ts.SecondRadiationConstantPlanckSetter:
        """Create a setter for this quantity."""
        ...
    

class SpecificEnthalpy(TypedQuantity):
    """Type-safe specific enthalpy quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificEnthalpySetter
    _expected_dimension = dim.SPECIFIC_ENTHALPY
    
    def set(self, value: float) -> ts.SpecificEnthalpySetter:
        """Create a setter for this quantity."""
        ...
    

class SpecificGravity(TypedQuantity):
    """Type-safe specific gravity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificGravitySetter
    _expected_dimension = dim.SPECIFIC_GRAVITY
    
    def set(self, value: float) -> ts.SpecificGravitySetter:
        """Create a setter for this quantity."""
        ...
    

class SpecificHeatCapacityConstantPressure(TypedQuantity):
    """Type-safe specific heat capacity (constant pressure) quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificHeatCapacityConstantPressureSetter
    _expected_dimension = dim.SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE
    
    def set(self, value: float) -> ts.SpecificHeatCapacityConstantPressureSetter:
        """Create a setter for this quantity."""
        ...
    

class SpecificLength(TypedQuantity):
    """Type-safe specific length quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificLengthSetter
    _expected_dimension = dim.SPECIFIC_LENGTH
    
    def set(self, value: float) -> ts.SpecificLengthSetter:
        """Create a setter for this quantity."""
        ...
    

class SpecificSurface(TypedQuantity):
    """Type-safe specific surface quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificSurfaceSetter
    _expected_dimension = dim.SPECIFIC_SURFACE
    
    def set(self, value: float) -> ts.SpecificSurfaceSetter:
        """Create a setter for this quantity."""
        ...
    

class SpecificVolume(TypedQuantity):
    """Type-safe specific volume quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificVolumeSetter
    _expected_dimension = dim.SPECIFIC_VOLUME
    
    def set(self, value: float) -> ts.SpecificVolumeSetter:
        """Create a setter for this quantity."""
        ...
    

class Stress(TypedQuantity):
    """Type-safe stress quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.StressSetter
    _expected_dimension = dim.STRESS
    
    def set(self, value: float) -> ts.StressSetter:
        """Create a setter for this quantity."""
        ...
    

class SurfaceMassDensity(TypedQuantity):
    """Type-safe surface mass density quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SurfaceMassDensitySetter
    _expected_dimension = dim.SURFACE_MASS_DENSITY
    
    def set(self, value: float) -> ts.SurfaceMassDensitySetter:
        """Create a setter for this quantity."""
        ...
    

class SurfaceTension(TypedQuantity):
    """Type-safe surface tension quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SurfaceTensionSetter
    _expected_dimension = dim.SURFACE_TENSION
    
    def set(self, value: float) -> ts.SurfaceTensionSetter:
        """Create a setter for this quantity."""
        ...
    

class Temperature(TypedQuantity):
    """Type-safe temperature quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TemperatureSetter
    _expected_dimension = dim.TEMPERATURE
    
    def set(self, value: float) -> ts.TemperatureSetter:
        """Create a setter for this quantity."""
        ...
    

class ThermalConductivity(TypedQuantity):
    """Type-safe thermal conductivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ThermalConductivitySetter
    _expected_dimension = dim.THERMAL_CONDUCTIVITY
    
    def set(self, value: float) -> ts.ThermalConductivitySetter:
        """Create a setter for this quantity."""
        ...
    

class Time(TypedQuantity):
    """Type-safe time quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TimeSetter
    _expected_dimension = dim.TIME
    
    def set(self, value: float) -> ts.TimeSetter:
        """Create a setter for this quantity."""
        ...
    

class Torque(TypedQuantity):
    """Type-safe torque quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TorqueSetter
    _expected_dimension = dim.TORQUE
    
    def set(self, value: float) -> ts.TorqueSetter:
        """Create a setter for this quantity."""
        ...
    

class TurbulenceEnergyDissipationRate(TypedQuantity):
    """Type-safe turbulence energy dissipation rate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TurbulenceEnergyDissipationRateSetter
    _expected_dimension = dim.TURBULENCE_ENERGY_DISSIPATION_RATE
    
    def set(self, value: float) -> ts.TurbulenceEnergyDissipationRateSetter:
        """Create a setter for this quantity."""
        ...
    

class VelocityAngular(TypedQuantity):
    """Type-safe velocity, angular quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VelocityAngularSetter
    _expected_dimension = dim.VELOCITY_ANGULAR
    
    def set(self, value: float) -> ts.VelocityAngularSetter:
        """Create a setter for this quantity."""
        ...
    

class VelocityLinear(TypedQuantity):
    """Type-safe velocity, linear quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VelocityLinearSetter
    _expected_dimension = dim.VELOCITY_LINEAR
    
    def set(self, value: float) -> ts.VelocityLinearSetter:
        """Create a setter for this quantity."""
        ...
    

class ViscosityDynamic(TypedQuantity):
    """Type-safe viscosity, dynamic quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ViscosityDynamicSetter
    _expected_dimension = dim.VISCOSITY_DYNAMIC
    
    def set(self, value: float) -> ts.ViscosityDynamicSetter:
        """Create a setter for this quantity."""
        ...
    

class ViscosityKinematic(TypedQuantity):
    """Type-safe viscosity, kinematic quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ViscosityKinematicSetter
    _expected_dimension = dim.VISCOSITY_KINEMATIC
    
    def set(self, value: float) -> ts.ViscosityKinematicSetter:
        """Create a setter for this quantity."""
        ...
    

class Volume(TypedQuantity):
    """Type-safe volume quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumeSetter
    _expected_dimension = dim.VOLUME
    
    def set(self, value: float) -> ts.VolumeSetter:
        """Create a setter for this quantity."""
        ...
    

class VolumeFractionOfI(TypedQuantity):
    """Type-safe volume fraction of "i" quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumeFractionOfISetter
    _expected_dimension = dim.VOLUME_FRACTION_OF_I
    
    def set(self, value: float) -> ts.VolumeFractionOfISetter:
        """Create a setter for this quantity."""
        ...
    

class VolumetricCalorificHeatingValue(TypedQuantity):
    """Type-safe volumetric calorific (heating) value quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricCalorificHeatingValueSetter
    _expected_dimension = dim.VOLUMETRIC_CALORIFIC_HEATING_VALUE
    
    def set(self, value: float) -> ts.VolumetricCalorificHeatingValueSetter:
        """Create a setter for this quantity."""
        ...
    

class VolumetricCoefficientOfExpansion(TypedQuantity):
    """Type-safe volumetric coefficient of expansion quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricCoefficientOfExpansionSetter
    _expected_dimension = dim.VOLUMETRIC_COEFFICIENT_OF_EXPANSION
    
    def set(self, value: float) -> ts.VolumetricCoefficientOfExpansionSetter:
        """Create a setter for this quantity."""
        ...
    

class VolumetricFlowRate(TypedQuantity):
    """Type-safe volumetric flow rate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricFlowRateSetter
    _expected_dimension = dim.VOLUMETRIC_FLOW_RATE
    
    def set(self, value: float) -> ts.VolumetricFlowRateSetter:
        """Create a setter for this quantity."""
        ...
    

class VolumetricFlux(TypedQuantity):
    """Type-safe volumetric flux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricFluxSetter
    _expected_dimension = dim.VOLUMETRIC_FLUX
    
    def set(self, value: float) -> ts.VolumetricFluxSetter:
        """Create a setter for this quantity."""
        ...
    

class VolumetricMassFlowRate(TypedQuantity):
    """Type-safe volumetric mass flow rate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricMassFlowRateSetter
    _expected_dimension = dim.VOLUMETRIC_MASS_FLOW_RATE
    
    def set(self, value: float) -> ts.VolumetricMassFlowRateSetter:
        """Create a setter for this quantity."""
        ...
    

class Wavenumber(TypedQuantity):
    """Type-safe wavenumber quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.WavenumberSetter
    _expected_dimension = dim.WAVENUMBER
    
    def set(self, value: float) -> ts.WavenumberSetter:
        """Create a setter for this quantity."""
        ...
    

# All quantity classes are defined above
# Setter classes are defined in setters.pyi
