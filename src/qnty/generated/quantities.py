"""
Quantity Classes Module - Static Edition
========================================

Static quantity class definitions for maximum import performance.
Uses static class generation instead of dynamic type() calls.
Auto-generated from unit_data.json.
"""

from ..quantities.typed_quantity import TypedQuantity
from . import dimensions as dim
from . import setters as ts


# ===== QUANTITY CLASSES =====
# Static quantity class definitions with __slots__ optimization

class AbsorbedDose(TypedQuantity):
    """Type-safe absorbeddose quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AbsorbedDoseSetter
    _expected_dimension = dim.ABSORBED_DOSE
    
    def set(self, value: float) -> ts.AbsorbedDoseSetter:
        """Create a setter for this quantity."""
        return ts.AbsorbedDoseSetter(self, value)
    

class Acceleration(TypedQuantity):
    """Type-safe acceleration quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AccelerationSetter
    _expected_dimension = dim.ACCELERATION
    
    def set(self, value: float) -> ts.AccelerationSetter:
        """Create a setter for this quantity."""
        return ts.AccelerationSetter(self, value)
    

class ActivationEnergy(TypedQuantity):
    """Type-safe activationenergy quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ActivationEnergySetter
    _expected_dimension = dim.ACTIVATION_ENERGY
    
    def set(self, value: float) -> ts.ActivationEnergySetter:
        """Create a setter for this quantity."""
        return ts.ActivationEnergySetter(self, value)
    

class AmountOfSubstance(TypedQuantity):
    """Type-safe amountofsubstance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AmountOfSubstanceSetter
    _expected_dimension = dim.AMOUNT_OF_SUBSTANCE
    
    def set(self, value: float) -> ts.AmountOfSubstanceSetter:
        """Create a setter for this quantity."""
        return ts.AmountOfSubstanceSetter(self, value)
    

class AnglePlane(TypedQuantity):
    """Type-safe angleplane quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AnglePlaneSetter
    _expected_dimension = dim.ANGLE_PLANE
    
    def set(self, value: float) -> ts.AnglePlaneSetter:
        """Create a setter for this quantity."""
        return ts.AnglePlaneSetter(self, value)
    

class AngleSolid(TypedQuantity):
    """Type-safe anglesolid quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AngleSolidSetter
    _expected_dimension = dim.ANGLE_SOLID
    
    def set(self, value: float) -> ts.AngleSolidSetter:
        """Create a setter for this quantity."""
        return ts.AngleSolidSetter(self, value)
    

class AngularAcceleration(TypedQuantity):
    """Type-safe angularacceleration quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AngularAccelerationSetter
    _expected_dimension = dim.ANGULAR_ACCELERATION
    
    def set(self, value: float) -> ts.AngularAccelerationSetter:
        """Create a setter for this quantity."""
        return ts.AngularAccelerationSetter(self, value)
    

class AngularMomentum(TypedQuantity):
    """Type-safe angularmomentum quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AngularMomentumSetter
    _expected_dimension = dim.ANGULAR_MOMENTUM
    
    def set(self, value: float) -> ts.AngularMomentumSetter:
        """Create a setter for this quantity."""
        return ts.AngularMomentumSetter(self, value)
    

class Area(TypedQuantity):
    """Type-safe area quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AreaSetter
    _expected_dimension = dim.AREA
    
    def set(self, value: float) -> ts.AreaSetter:
        """Create a setter for this quantity."""
        return ts.AreaSetter(self, value)
    

class AreaPerUnitVolume(TypedQuantity):
    """Type-safe areaperunitvolume quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AreaPerUnitVolumeSetter
    _expected_dimension = dim.AREA_PER_UNIT_VOLUME
    
    def set(self, value: float) -> ts.AreaPerUnitVolumeSetter:
        """Create a setter for this quantity."""
        return ts.AreaPerUnitVolumeSetter(self, value)
    

class AtomicWeight(TypedQuantity):
    """Type-safe atomicweight quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.AtomicWeightSetter
    _expected_dimension = dim.ATOMIC_WEIGHT
    
    def set(self, value: float) -> ts.AtomicWeightSetter:
        """Create a setter for this quantity."""
        return ts.AtomicWeightSetter(self, value)
    

class Concentration(TypedQuantity):
    """Type-safe concentration quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ConcentrationSetter
    _expected_dimension = dim.CONCENTRATION
    
    def set(self, value: float) -> ts.ConcentrationSetter:
        """Create a setter for this quantity."""
        return ts.ConcentrationSetter(self, value)
    

class Dimensionless(TypedQuantity):
    """Type-safe dimensionless quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.DimensionlessSetter
    _expected_dimension = dim.DIMENSIONLESS
    
    def set(self, value: float) -> ts.DimensionlessSetter:
        """Create a setter for this quantity."""
        return ts.DimensionlessSetter(self, value)
    

class DynamicFluidity(TypedQuantity):
    """Type-safe dynamicfluidity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.DynamicFluiditySetter
    _expected_dimension = dim.DYNAMIC_FLUIDITY
    
    def set(self, value: float) -> ts.DynamicFluiditySetter:
        """Create a setter for this quantity."""
        return ts.DynamicFluiditySetter(self, value)
    

class ElectricCapacitance(TypedQuantity):
    """Type-safe electriccapacitance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricCapacitanceSetter
    _expected_dimension = dim.ELECTRIC_CAPACITANCE
    
    def set(self, value: float) -> ts.ElectricCapacitanceSetter:
        """Create a setter for this quantity."""
        return ts.ElectricCapacitanceSetter(self, value)
    

class ElectricCharge(TypedQuantity):
    """Type-safe electriccharge quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricChargeSetter
    _expected_dimension = dim.ELECTRIC_CHARGE
    
    def set(self, value: float) -> ts.ElectricChargeSetter:
        """Create a setter for this quantity."""
        return ts.ElectricChargeSetter(self, value)
    

class ElectricCurrentIntensity(TypedQuantity):
    """Type-safe electriccurrentintensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricCurrentIntensitySetter
    _expected_dimension = dim.ELECTRIC_CURRENT_INTENSITY
    
    def set(self, value: float) -> ts.ElectricCurrentIntensitySetter:
        """Create a setter for this quantity."""
        return ts.ElectricCurrentIntensitySetter(self, value)
    

class ElectricDipoleMoment(TypedQuantity):
    """Type-safe electricdipolemoment quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricDipoleMomentSetter
    _expected_dimension = dim.ELECTRIC_DIPOLE_MOMENT
    
    def set(self, value: float) -> ts.ElectricDipoleMomentSetter:
        """Create a setter for this quantity."""
        return ts.ElectricDipoleMomentSetter(self, value)
    

class ElectricFieldStrength(TypedQuantity):
    """Type-safe electricfieldstrength quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricFieldStrengthSetter
    _expected_dimension = dim.ELECTRIC_FIELD_STRENGTH
    
    def set(self, value: float) -> ts.ElectricFieldStrengthSetter:
        """Create a setter for this quantity."""
        return ts.ElectricFieldStrengthSetter(self, value)
    

class ElectricInductance(TypedQuantity):
    """Type-safe electricinductance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricInductanceSetter
    _expected_dimension = dim.ELECTRIC_INDUCTANCE
    
    def set(self, value: float) -> ts.ElectricInductanceSetter:
        """Create a setter for this quantity."""
        return ts.ElectricInductanceSetter(self, value)
    

class ElectricPotential(TypedQuantity):
    """Type-safe electricpotential quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricPotentialSetter
    _expected_dimension = dim.ELECTRIC_POTENTIAL
    
    def set(self, value: float) -> ts.ElectricPotentialSetter:
        """Create a setter for this quantity."""
        return ts.ElectricPotentialSetter(self, value)
    

class ElectricResistance(TypedQuantity):
    """Type-safe electricresistance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricResistanceSetter
    _expected_dimension = dim.ELECTRIC_RESISTANCE
    
    def set(self, value: float) -> ts.ElectricResistanceSetter:
        """Create a setter for this quantity."""
        return ts.ElectricResistanceSetter(self, value)
    

class ElectricalConductance(TypedQuantity):
    """Type-safe electricalconductance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricalConductanceSetter
    _expected_dimension = dim.ELECTRICAL_CONDUCTANCE
    
    def set(self, value: float) -> ts.ElectricalConductanceSetter:
        """Create a setter for this quantity."""
        return ts.ElectricalConductanceSetter(self, value)
    

class ElectricalPermittivity(TypedQuantity):
    """Type-safe electricalpermittivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricalPermittivitySetter
    _expected_dimension = dim.ELECTRICAL_PERMITTIVITY
    
    def set(self, value: float) -> ts.ElectricalPermittivitySetter:
        """Create a setter for this quantity."""
        return ts.ElectricalPermittivitySetter(self, value)
    

class ElectricalResistivity(TypedQuantity):
    """Type-safe electricalresistivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ElectricalResistivitySetter
    _expected_dimension = dim.ELECTRICAL_RESISTIVITY
    
    def set(self, value: float) -> ts.ElectricalResistivitySetter:
        """Create a setter for this quantity."""
        return ts.ElectricalResistivitySetter(self, value)
    

class EnergyFlux(TypedQuantity):
    """Type-safe energyflux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.EnergyFluxSetter
    _expected_dimension = dim.ENERGY_FLUX
    
    def set(self, value: float) -> ts.EnergyFluxSetter:
        """Create a setter for this quantity."""
        return ts.EnergyFluxSetter(self, value)
    

class EnergyHeatWork(TypedQuantity):
    """Type-safe energyheatwork quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.EnergyHeatWorkSetter
    _expected_dimension = dim.ENERGY_HEAT_WORK
    
    def set(self, value: float) -> ts.EnergyHeatWorkSetter:
        """Create a setter for this quantity."""
        return ts.EnergyHeatWorkSetter(self, value)
    

class EnergyPerUnitArea(TypedQuantity):
    """Type-safe energyperunitarea quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.EnergyPerUnitAreaSetter
    _expected_dimension = dim.ENERGY_PER_UNIT_AREA
    
    def set(self, value: float) -> ts.EnergyPerUnitAreaSetter:
        """Create a setter for this quantity."""
        return ts.EnergyPerUnitAreaSetter(self, value)
    

class Force(TypedQuantity):
    """Type-safe force quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ForceSetter
    _expected_dimension = dim.FORCE
    
    def set(self, value: float) -> ts.ForceSetter:
        """Create a setter for this quantity."""
        return ts.ForceSetter(self, value)
    

class ForceBody(TypedQuantity):
    """Type-safe forcebody quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ForceBodySetter
    _expected_dimension = dim.FORCE_BODY
    
    def set(self, value: float) -> ts.ForceBodySetter:
        """Create a setter for this quantity."""
        return ts.ForceBodySetter(self, value)
    

class ForcePerUnitMass(TypedQuantity):
    """Type-safe forceperunitmass quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ForcePerUnitMassSetter
    _expected_dimension = dim.FORCE_PER_UNIT_MASS
    
    def set(self, value: float) -> ts.ForcePerUnitMassSetter:
        """Create a setter for this quantity."""
        return ts.ForcePerUnitMassSetter(self, value)
    

class FrequencyVoltageRatio(TypedQuantity):
    """Type-safe frequencyvoltageratio quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.FrequencyVoltageRatioSetter
    _expected_dimension = dim.FREQUENCY_VOLTAGE_RATIO
    
    def set(self, value: float) -> ts.FrequencyVoltageRatioSetter:
        """Create a setter for this quantity."""
        return ts.FrequencyVoltageRatioSetter(self, value)
    

class FuelConsumption(TypedQuantity):
    """Type-safe fuelconsumption quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.FuelConsumptionSetter
    _expected_dimension = dim.FUEL_CONSUMPTION
    
    def set(self, value: float) -> ts.FuelConsumptionSetter:
        """Create a setter for this quantity."""
        return ts.FuelConsumptionSetter(self, value)
    

class HeatOfCombustion(TypedQuantity):
    """Type-safe heatofcombustion quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatOfCombustionSetter
    _expected_dimension = dim.HEAT_OF_COMBUSTION
    
    def set(self, value: float) -> ts.HeatOfCombustionSetter:
        """Create a setter for this quantity."""
        return ts.HeatOfCombustionSetter(self, value)
    

class HeatOfFusion(TypedQuantity):
    """Type-safe heatoffusion quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatOfFusionSetter
    _expected_dimension = dim.HEAT_OF_FUSION
    
    def set(self, value: float) -> ts.HeatOfFusionSetter:
        """Create a setter for this quantity."""
        return ts.HeatOfFusionSetter(self, value)
    

class HeatOfVaporization(TypedQuantity):
    """Type-safe heatofvaporization quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatOfVaporizationSetter
    _expected_dimension = dim.HEAT_OF_VAPORIZATION
    
    def set(self, value: float) -> ts.HeatOfVaporizationSetter:
        """Create a setter for this quantity."""
        return ts.HeatOfVaporizationSetter(self, value)
    

class HeatTransferCoefficient(TypedQuantity):
    """Type-safe heattransfercoefficient quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.HeatTransferCoefficientSetter
    _expected_dimension = dim.HEAT_TRANSFER_COEFFICIENT
    
    def set(self, value: float) -> ts.HeatTransferCoefficientSetter:
        """Create a setter for this quantity."""
        return ts.HeatTransferCoefficientSetter(self, value)
    

class Illuminance(TypedQuantity):
    """Type-safe illuminance quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.IlluminanceSetter
    _expected_dimension = dim.ILLUMINANCE
    
    def set(self, value: float) -> ts.IlluminanceSetter:
        """Create a setter for this quantity."""
        return ts.IlluminanceSetter(self, value)
    

class KineticEnergyOfTurbulence(TypedQuantity):
    """Type-safe kineticenergyofturbulence quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.KineticEnergyOfTurbulenceSetter
    _expected_dimension = dim.KINETIC_ENERGY_OF_TURBULENCE
    
    def set(self, value: float) -> ts.KineticEnergyOfTurbulenceSetter:
        """Create a setter for this quantity."""
        return ts.KineticEnergyOfTurbulenceSetter(self, value)
    

class Length(TypedQuantity):
    """Type-safe length quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LengthSetter
    _expected_dimension = dim.LENGTH
    
    def set(self, value: float) -> ts.LengthSetter:
        """Create a setter for this quantity."""
        return ts.LengthSetter(self, value)
    

class LinearMassDensity(TypedQuantity):
    """Type-safe linearmassdensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LinearMassDensitySetter
    _expected_dimension = dim.LINEAR_MASS_DENSITY
    
    def set(self, value: float) -> ts.LinearMassDensitySetter:
        """Create a setter for this quantity."""
        return ts.LinearMassDensitySetter(self, value)
    

class LinearMomentum(TypedQuantity):
    """Type-safe linearmomentum quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LinearMomentumSetter
    _expected_dimension = dim.LINEAR_MOMENTUM
    
    def set(self, value: float) -> ts.LinearMomentumSetter:
        """Create a setter for this quantity."""
        return ts.LinearMomentumSetter(self, value)
    

class LuminanceSelf(TypedQuantity):
    """Type-safe luminanceself quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LuminanceSelfSetter
    _expected_dimension = dim.LUMINANCE_SELF
    
    def set(self, value: float) -> ts.LuminanceSelfSetter:
        """Create a setter for this quantity."""
        return ts.LuminanceSelfSetter(self, value)
    

class LuminousFlux(TypedQuantity):
    """Type-safe luminousflux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LuminousFluxSetter
    _expected_dimension = dim.LUMINOUS_FLUX
    
    def set(self, value: float) -> ts.LuminousFluxSetter:
        """Create a setter for this quantity."""
        return ts.LuminousFluxSetter(self, value)
    

class LuminousIntensity(TypedQuantity):
    """Type-safe luminousintensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.LuminousIntensitySetter
    _expected_dimension = dim.LUMINOUS_INTENSITY
    
    def set(self, value: float) -> ts.LuminousIntensitySetter:
        """Create a setter for this quantity."""
        return ts.LuminousIntensitySetter(self, value)
    

class MagneticField(TypedQuantity):
    """Type-safe magneticfield quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticFieldSetter
    _expected_dimension = dim.MAGNETIC_FIELD
    
    def set(self, value: float) -> ts.MagneticFieldSetter:
        """Create a setter for this quantity."""
        return ts.MagneticFieldSetter(self, value)
    

class MagneticFlux(TypedQuantity):
    """Type-safe magneticflux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticFluxSetter
    _expected_dimension = dim.MAGNETIC_FLUX
    
    def set(self, value: float) -> ts.MagneticFluxSetter:
        """Create a setter for this quantity."""
        return ts.MagneticFluxSetter(self, value)
    

class MagneticInductionFieldStrength(TypedQuantity):
    """Type-safe magneticinductionfieldstrength quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticInductionFieldStrengthSetter
    _expected_dimension = dim.MAGNETIC_INDUCTION_FIELD_STRENGTH
    
    def set(self, value: float) -> ts.MagneticInductionFieldStrengthSetter:
        """Create a setter for this quantity."""
        return ts.MagneticInductionFieldStrengthSetter(self, value)
    

class MagneticMoment(TypedQuantity):
    """Type-safe magneticmoment quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticMomentSetter
    _expected_dimension = dim.MAGNETIC_MOMENT
    
    def set(self, value: float) -> ts.MagneticMomentSetter:
        """Create a setter for this quantity."""
        return ts.MagneticMomentSetter(self, value)
    

class MagneticPermeability(TypedQuantity):
    """Type-safe magneticpermeability quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagneticPermeabilitySetter
    _expected_dimension = dim.MAGNETIC_PERMEABILITY
    
    def set(self, value: float) -> ts.MagneticPermeabilitySetter:
        """Create a setter for this quantity."""
        return ts.MagneticPermeabilitySetter(self, value)
    

class MagnetomotiveForce(TypedQuantity):
    """Type-safe magnetomotiveforce quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MagnetomotiveForceSetter
    _expected_dimension = dim.MAGNETOMOTIVE_FORCE
    
    def set(self, value: float) -> ts.MagnetomotiveForceSetter:
        """Create a setter for this quantity."""
        return ts.MagnetomotiveForceSetter(self, value)
    

class Mass(TypedQuantity):
    """Type-safe mass quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassSetter
    _expected_dimension = dim.MASS
    
    def set(self, value: float) -> ts.MassSetter:
        """Create a setter for this quantity."""
        return ts.MassSetter(self, value)
    

class MassDensity(TypedQuantity):
    """Type-safe massdensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassDensitySetter
    _expected_dimension = dim.MASS_DENSITY
    
    def set(self, value: float) -> ts.MassDensitySetter:
        """Create a setter for this quantity."""
        return ts.MassDensitySetter(self, value)
    

class MassFlowRate(TypedQuantity):
    """Type-safe massflowrate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassFlowRateSetter
    _expected_dimension = dim.MASS_FLOW_RATE
    
    def set(self, value: float) -> ts.MassFlowRateSetter:
        """Create a setter for this quantity."""
        return ts.MassFlowRateSetter(self, value)
    

class MassFlux(TypedQuantity):
    """Type-safe massflux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassFluxSetter
    _expected_dimension = dim.MASS_FLUX
    
    def set(self, value: float) -> ts.MassFluxSetter:
        """Create a setter for this quantity."""
        return ts.MassFluxSetter(self, value)
    

class MassFractionOfI(TypedQuantity):
    """Type-safe massfractionofi quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassFractionOfISetter
    _expected_dimension = dim.MASS_FRACTION_OF_I
    
    def set(self, value: float) -> ts.MassFractionOfISetter:
        """Create a setter for this quantity."""
        return ts.MassFractionOfISetter(self, value)
    

class MassTransferCoefficient(TypedQuantity):
    """Type-safe masstransfercoefficient quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MassTransferCoefficientSetter
    _expected_dimension = dim.MASS_TRANSFER_COEFFICIENT
    
    def set(self, value: float) -> ts.MassTransferCoefficientSetter:
        """Create a setter for this quantity."""
        return ts.MassTransferCoefficientSetter(self, value)
    

class MolalityOfSoluteI(TypedQuantity):
    """Type-safe molalityofsolutei quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolalityOfSoluteISetter
    _expected_dimension = dim.MOLALITY_OF_SOLUTE_I
    
    def set(self, value: float) -> ts.MolalityOfSoluteISetter:
        """Create a setter for this quantity."""
        return ts.MolalityOfSoluteISetter(self, value)
    

class MolarConcentrationByMass(TypedQuantity):
    """Type-safe molarconcentrationbymass quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarConcentrationByMassSetter
    _expected_dimension = dim.MOLAR_CONCENTRATION_BY_MASS
    
    def set(self, value: float) -> ts.MolarConcentrationByMassSetter:
        """Create a setter for this quantity."""
        return ts.MolarConcentrationByMassSetter(self, value)
    

class MolarFlowRate(TypedQuantity):
    """Type-safe molarflowrate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarFlowRateSetter
    _expected_dimension = dim.MOLAR_FLOW_RATE
    
    def set(self, value: float) -> ts.MolarFlowRateSetter:
        """Create a setter for this quantity."""
        return ts.MolarFlowRateSetter(self, value)
    

class MolarFlux(TypedQuantity):
    """Type-safe molarflux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarFluxSetter
    _expected_dimension = dim.MOLAR_FLUX
    
    def set(self, value: float) -> ts.MolarFluxSetter:
        """Create a setter for this quantity."""
        return ts.MolarFluxSetter(self, value)
    

class MolarHeatCapacity(TypedQuantity):
    """Type-safe molarheatcapacity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarHeatCapacitySetter
    _expected_dimension = dim.MOLAR_HEAT_CAPACITY
    
    def set(self, value: float) -> ts.MolarHeatCapacitySetter:
        """Create a setter for this quantity."""
        return ts.MolarHeatCapacitySetter(self, value)
    

class MolarityOfI(TypedQuantity):
    """Type-safe molarityofi quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MolarityOfISetter
    _expected_dimension = dim.MOLARITY_OF_I
    
    def set(self, value: float) -> ts.MolarityOfISetter:
        """Create a setter for this quantity."""
        return ts.MolarityOfISetter(self, value)
    

class MoleFractionOfI(TypedQuantity):
    """Type-safe molefractionofi quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MoleFractionOfISetter
    _expected_dimension = dim.MOLE_FRACTION_OF_I
    
    def set(self, value: float) -> ts.MoleFractionOfISetter:
        """Create a setter for this quantity."""
        return ts.MoleFractionOfISetter(self, value)
    

class MomentOfInertia(TypedQuantity):
    """Type-safe momentofinertia quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MomentOfInertiaSetter
    _expected_dimension = dim.MOMENT_OF_INERTIA
    
    def set(self, value: float) -> ts.MomentOfInertiaSetter:
        """Create a setter for this quantity."""
        return ts.MomentOfInertiaSetter(self, value)
    

class MomentumFlowRate(TypedQuantity):
    """Type-safe momentumflowrate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MomentumFlowRateSetter
    _expected_dimension = dim.MOMENTUM_FLOW_RATE
    
    def set(self, value: float) -> ts.MomentumFlowRateSetter:
        """Create a setter for this quantity."""
        return ts.MomentumFlowRateSetter(self, value)
    

class MomentumFlux(TypedQuantity):
    """Type-safe momentumflux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.MomentumFluxSetter
    _expected_dimension = dim.MOMENTUM_FLUX
    
    def set(self, value: float) -> ts.MomentumFluxSetter:
        """Create a setter for this quantity."""
        return ts.MomentumFluxSetter(self, value)
    

class NormalityOfSolution(TypedQuantity):
    """Type-safe normalityofsolution quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.NormalityOfSolutionSetter
    _expected_dimension = dim.NORMALITY_OF_SOLUTION
    
    def set(self, value: float) -> ts.NormalityOfSolutionSetter:
        """Create a setter for this quantity."""
        return ts.NormalityOfSolutionSetter(self, value)
    

class ParticleDensity(TypedQuantity):
    """Type-safe particledensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ParticleDensitySetter
    _expected_dimension = dim.PARTICLE_DENSITY
    
    def set(self, value: float) -> ts.ParticleDensitySetter:
        """Create a setter for this quantity."""
        return ts.ParticleDensitySetter(self, value)
    

class Percent(TypedQuantity):
    """Type-safe percent quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PercentSetter
    _expected_dimension = dim.PERCENT
    
    def set(self, value: float) -> ts.PercentSetter:
        """Create a setter for this quantity."""
        return ts.PercentSetter(self, value)
    

class Permeability(TypedQuantity):
    """Type-safe permeability quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PermeabilitySetter
    _expected_dimension = dim.PERMEABILITY
    
    def set(self, value: float) -> ts.PermeabilitySetter:
        """Create a setter for this quantity."""
        return ts.PermeabilitySetter(self, value)
    

class PhotonEmissionRate(TypedQuantity):
    """Type-safe photonemissionrate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PhotonEmissionRateSetter
    _expected_dimension = dim.PHOTON_EMISSION_RATE
    
    def set(self, value: float) -> ts.PhotonEmissionRateSetter:
        """Create a setter for this quantity."""
        return ts.PhotonEmissionRateSetter(self, value)
    

class PowerPerUnitMass(TypedQuantity):
    """Type-safe powerperunitmass quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PowerPerUnitMassSetter
    _expected_dimension = dim.POWER_PER_UNIT_MASS
    
    def set(self, value: float) -> ts.PowerPerUnitMassSetter:
        """Create a setter for this quantity."""
        return ts.PowerPerUnitMassSetter(self, value)
    

class PowerPerUnitVolume(TypedQuantity):
    """Type-safe powerperunitvolume quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PowerPerUnitVolumeSetter
    _expected_dimension = dim.POWER_PER_UNIT_VOLUME
    
    def set(self, value: float) -> ts.PowerPerUnitVolumeSetter:
        """Create a setter for this quantity."""
        return ts.PowerPerUnitVolumeSetter(self, value)
    

class PowerThermalDuty(TypedQuantity):
    """Type-safe powerthermalduty quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PowerThermalDutySetter
    _expected_dimension = dim.POWER_THERMAL_DUTY
    
    def set(self, value: float) -> ts.PowerThermalDutySetter:
        """Create a setter for this quantity."""
        return ts.PowerThermalDutySetter(self, value)
    

class Pressure(TypedQuantity):
    """Type-safe pressure quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.PressureSetter
    _expected_dimension = dim.PRESSURE
    
    def set(self, value: float) -> ts.PressureSetter:
        """Create a setter for this quantity."""
        return ts.PressureSetter(self, value)
    

class RadiationDoseEquivalent(TypedQuantity):
    """Type-safe radiationdoseequivalent quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.RadiationDoseEquivalentSetter
    _expected_dimension = dim.RADIATION_DOSE_EQUIVALENT
    
    def set(self, value: float) -> ts.RadiationDoseEquivalentSetter:
        """Create a setter for this quantity."""
        return ts.RadiationDoseEquivalentSetter(self, value)
    

class RadiationExposure(TypedQuantity):
    """Type-safe radiationexposure quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.RadiationExposureSetter
    _expected_dimension = dim.RADIATION_EXPOSURE
    
    def set(self, value: float) -> ts.RadiationExposureSetter:
        """Create a setter for this quantity."""
        return ts.RadiationExposureSetter(self, value)
    

class Radioactivity(TypedQuantity):
    """Type-safe radioactivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.RadioactivitySetter
    _expected_dimension = dim.RADIOACTIVITY
    
    def set(self, value: float) -> ts.RadioactivitySetter:
        """Create a setter for this quantity."""
        return ts.RadioactivitySetter(self, value)
    

class SecondMomentOfArea(TypedQuantity):
    """Type-safe secondmomentofarea quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SecondMomentOfAreaSetter
    _expected_dimension = dim.SECOND_MOMENT_OF_AREA
    
    def set(self, value: float) -> ts.SecondMomentOfAreaSetter:
        """Create a setter for this quantity."""
        return ts.SecondMomentOfAreaSetter(self, value)
    

class SecondRadiationConstantPlanck(TypedQuantity):
    """Type-safe secondradiationconstantplanck quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SecondRadiationConstantPlanckSetter
    _expected_dimension = dim.SECOND_RADIATION_CONSTANT_PLANCK
    
    def set(self, value: float) -> ts.SecondRadiationConstantPlanckSetter:
        """Create a setter for this quantity."""
        return ts.SecondRadiationConstantPlanckSetter(self, value)
    

class SpecificEnthalpy(TypedQuantity):
    """Type-safe specificenthalpy quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificEnthalpySetter
    _expected_dimension = dim.SPECIFIC_ENTHALPY
    
    def set(self, value: float) -> ts.SpecificEnthalpySetter:
        """Create a setter for this quantity."""
        return ts.SpecificEnthalpySetter(self, value)
    

class SpecificGravity(TypedQuantity):
    """Type-safe specificgravity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificGravitySetter
    _expected_dimension = dim.SPECIFIC_GRAVITY
    
    def set(self, value: float) -> ts.SpecificGravitySetter:
        """Create a setter for this quantity."""
        return ts.SpecificGravitySetter(self, value)
    

class SpecificHeatCapacityConstantPressure(TypedQuantity):
    """Type-safe specificheatcapacityconstantpressure quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificHeatCapacityConstantPressureSetter
    _expected_dimension = dim.SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE
    
    def set(self, value: float) -> ts.SpecificHeatCapacityConstantPressureSetter:
        """Create a setter for this quantity."""
        return ts.SpecificHeatCapacityConstantPressureSetter(self, value)
    

class SpecificLength(TypedQuantity):
    """Type-safe specificlength quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificLengthSetter
    _expected_dimension = dim.SPECIFIC_LENGTH
    
    def set(self, value: float) -> ts.SpecificLengthSetter:
        """Create a setter for this quantity."""
        return ts.SpecificLengthSetter(self, value)
    

class SpecificSurface(TypedQuantity):
    """Type-safe specificsurface quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificSurfaceSetter
    _expected_dimension = dim.SPECIFIC_SURFACE
    
    def set(self, value: float) -> ts.SpecificSurfaceSetter:
        """Create a setter for this quantity."""
        return ts.SpecificSurfaceSetter(self, value)
    

class SpecificVolume(TypedQuantity):
    """Type-safe specificvolume quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SpecificVolumeSetter
    _expected_dimension = dim.SPECIFIC_VOLUME
    
    def set(self, value: float) -> ts.SpecificVolumeSetter:
        """Create a setter for this quantity."""
        return ts.SpecificVolumeSetter(self, value)
    

class Stress(TypedQuantity):
    """Type-safe stress quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.StressSetter
    _expected_dimension = dim.STRESS
    
    def set(self, value: float) -> ts.StressSetter:
        """Create a setter for this quantity."""
        return ts.StressSetter(self, value)
    

class SurfaceMassDensity(TypedQuantity):
    """Type-safe surfacemassdensity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SurfaceMassDensitySetter
    _expected_dimension = dim.SURFACE_MASS_DENSITY
    
    def set(self, value: float) -> ts.SurfaceMassDensitySetter:
        """Create a setter for this quantity."""
        return ts.SurfaceMassDensitySetter(self, value)
    

class SurfaceTension(TypedQuantity):
    """Type-safe surfacetension quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.SurfaceTensionSetter
    _expected_dimension = dim.SURFACE_TENSION
    
    def set(self, value: float) -> ts.SurfaceTensionSetter:
        """Create a setter for this quantity."""
        return ts.SurfaceTensionSetter(self, value)
    

class Temperature(TypedQuantity):
    """Type-safe temperature quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TemperatureSetter
    _expected_dimension = dim.TEMPERATURE
    
    def set(self, value: float) -> ts.TemperatureSetter:
        """Create a setter for this quantity."""
        return ts.TemperatureSetter(self, value)
    

class ThermalConductivity(TypedQuantity):
    """Type-safe thermalconductivity quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ThermalConductivitySetter
    _expected_dimension = dim.THERMAL_CONDUCTIVITY
    
    def set(self, value: float) -> ts.ThermalConductivitySetter:
        """Create a setter for this quantity."""
        return ts.ThermalConductivitySetter(self, value)
    

class Time(TypedQuantity):
    """Type-safe time quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TimeSetter
    _expected_dimension = dim.TIME
    
    def set(self, value: float) -> ts.TimeSetter:
        """Create a setter for this quantity."""
        return ts.TimeSetter(self, value)
    

class Torque(TypedQuantity):
    """Type-safe torque quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TorqueSetter
    _expected_dimension = dim.TORQUE
    
    def set(self, value: float) -> ts.TorqueSetter:
        """Create a setter for this quantity."""
        return ts.TorqueSetter(self, value)
    

class TurbulenceEnergyDissipationRate(TypedQuantity):
    """Type-safe turbulenceenergydissipationrate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.TurbulenceEnergyDissipationRateSetter
    _expected_dimension = dim.TURBULENCE_ENERGY_DISSIPATION_RATE
    
    def set(self, value: float) -> ts.TurbulenceEnergyDissipationRateSetter:
        """Create a setter for this quantity."""
        return ts.TurbulenceEnergyDissipationRateSetter(self, value)
    

class VelocityAngular(TypedQuantity):
    """Type-safe velocityangular quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VelocityAngularSetter
    _expected_dimension = dim.VELOCITY_ANGULAR
    
    def set(self, value: float) -> ts.VelocityAngularSetter:
        """Create a setter for this quantity."""
        return ts.VelocityAngularSetter(self, value)
    

class VelocityLinear(TypedQuantity):
    """Type-safe velocitylinear quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VelocityLinearSetter
    _expected_dimension = dim.VELOCITY_LINEAR
    
    def set(self, value: float) -> ts.VelocityLinearSetter:
        """Create a setter for this quantity."""
        return ts.VelocityLinearSetter(self, value)
    

class ViscosityDynamic(TypedQuantity):
    """Type-safe viscositydynamic quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ViscosityDynamicSetter
    _expected_dimension = dim.VISCOSITY_DYNAMIC
    
    def set(self, value: float) -> ts.ViscosityDynamicSetter:
        """Create a setter for this quantity."""
        return ts.ViscosityDynamicSetter(self, value)
    

class ViscosityKinematic(TypedQuantity):
    """Type-safe viscositykinematic quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.ViscosityKinematicSetter
    _expected_dimension = dim.VISCOSITY_KINEMATIC
    
    def set(self, value: float) -> ts.ViscosityKinematicSetter:
        """Create a setter for this quantity."""
        return ts.ViscosityKinematicSetter(self, value)
    

class Volume(TypedQuantity):
    """Type-safe volume quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumeSetter
    _expected_dimension = dim.VOLUME
    
    def set(self, value: float) -> ts.VolumeSetter:
        """Create a setter for this quantity."""
        return ts.VolumeSetter(self, value)
    

class VolumeFractionOfI(TypedQuantity):
    """Type-safe volumefractionofi quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumeFractionOfISetter
    _expected_dimension = dim.VOLUME_FRACTION_OF_I
    
    def set(self, value: float) -> ts.VolumeFractionOfISetter:
        """Create a setter for this quantity."""
        return ts.VolumeFractionOfISetter(self, value)
    

class VolumetricCalorificHeatingValue(TypedQuantity):
    """Type-safe volumetriccalorificheatingvalue quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricCalorificHeatingValueSetter
    _expected_dimension = dim.VOLUMETRIC_CALORIFIC_HEATING_VALUE
    
    def set(self, value: float) -> ts.VolumetricCalorificHeatingValueSetter:
        """Create a setter for this quantity."""
        return ts.VolumetricCalorificHeatingValueSetter(self, value)
    

class VolumetricCoefficientOfExpansion(TypedQuantity):
    """Type-safe volumetriccoefficientofexpansion quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricCoefficientOfExpansionSetter
    _expected_dimension = dim.VOLUMETRIC_COEFFICIENT_OF_EXPANSION
    
    def set(self, value: float) -> ts.VolumetricCoefficientOfExpansionSetter:
        """Create a setter for this quantity."""
        return ts.VolumetricCoefficientOfExpansionSetter(self, value)
    

class VolumetricFlowRate(TypedQuantity):
    """Type-safe volumetricflowrate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricFlowRateSetter
    _expected_dimension = dim.VOLUMETRIC_FLOW_RATE
    
    def set(self, value: float) -> ts.VolumetricFlowRateSetter:
        """Create a setter for this quantity."""
        return ts.VolumetricFlowRateSetter(self, value)
    

class VolumetricFlux(TypedQuantity):
    """Type-safe volumetricflux quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricFluxSetter
    _expected_dimension = dim.VOLUMETRIC_FLUX
    
    def set(self, value: float) -> ts.VolumetricFluxSetter:
        """Create a setter for this quantity."""
        return ts.VolumetricFluxSetter(self, value)
    

class VolumetricMassFlowRate(TypedQuantity):
    """Type-safe volumetricmassflowrate quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.VolumetricMassFlowRateSetter
    _expected_dimension = dim.VOLUMETRIC_MASS_FLOW_RATE
    
    def set(self, value: float) -> ts.VolumetricMassFlowRateSetter:
        """Create a setter for this quantity."""
        return ts.VolumetricMassFlowRateSetter(self, value)
    

class Wavenumber(TypedQuantity):
    """Type-safe wavenumber quantity with expression capabilities."""
    __slots__ = ()
    _setter_class = ts.WavenumberSetter
    _expected_dimension = dim.WAVENUMBER
    
    def set(self, value: float) -> ts.WavenumberSetter:
        """Create a setter for this quantity."""
        return ts.WavenumberSetter(self, value)
    

