# Qnty API Reference

Quick reference guide for the qnty library's public API.

## Quantity Types

Qnty provides 100+ engineering quantity types with dimensional safety and automatic unit conversion.

### Core Engineering Quantities

#### **Length**

```python
from qnty import Length
length = Length(10, "mm")
length = Length(1.5, "inch")
length = Length(100, "centimeter")
```

**Available units**: meter, millimeter, centimeter, kilometer, inch, foot, yard, mile, nautical_mile

#### **Pressure**

```python
from qnty import Pressure
pressure = Pressure(100, "kilopascal")
pressure = Pressure(14.7, "pound_force_per_square_inch")  # psi
pressure = Pressure(1, "bar")
```

**Available units**: pascal, kilopascal, megapascal, bar, pound_force_per_square_inch, atmosphere, torr

#### **Temperature**

```python
from qnty import Temperature
temp = Temperature(25, "celsius")
temp = Temperature(298.15, "kelvin")
temp = Temperature(77, "fahrenheit")
```

**Available units**: kelvin, celsius, fahrenheit, rankine

#### **Mass**

```python
from qnty import Mass
mass = Mass(10, "kilogram")
mass = Mass(22, "pound_mass")
mass = Mass(1000, "gram")
```

**Available units**: kilogram, gram, pound_mass, ounce_mass, ton_metric, ton_short

#### **Force**

```python
from qnty import Force
force = Force(100, "newton")
force = Force(50, "pound_force")
force = Force(10, "kilonewton")
```

**Available units**: newton, kilonewton, pound_force, dyne, kilogram_force

#### **Volume**

```python
from qnty import Volume
volume = Volume(1, "liter")
volume = Volume(0.001, "cubic_meter")
volume = Volume(1, "gallon_us")
```

**Available units**: cubic_meter, liter, gallon_us, gallon_imperial, cubic_foot, cubic_inch

#### **Area**

```python
from qnty import Area
area = Area(1, "square_meter")
area = Area(100, "square_centimeter")
area = Area(1550, "square_inch")
```

**Available units**: square_meter, square_centimeter, square_millimeter, square_foot, square_inch

### Electrical Quantities

#### **ElectricPotential** (Voltage)

```python
from qnty import ElectricPotential
voltage = ElectricPotential(120, "volt")
voltage = ElectricPotential(12, "kilovolt")
```

#### **ElectricCurrentIntensity** (Current)

```python
from qnty import ElectricCurrentIntensity
current = ElectricCurrentIntensity(10, "ampere")
current = ElectricCurrentIntensity(0.5, "milliampere")
```

#### **ElectricResistance**

```python
from qnty import ElectricResistance
resistance = ElectricResistance(100, "ohm")
resistance = ElectricResistance(2.2, "kiloohm")
```

#### **PowerThermalDuty** (Power)

```python
from qnty import PowerThermalDuty
power = PowerThermalDuty(1000, "watt")
power = PowerThermalDuty(1, "kilowatt")
power = PowerThermalDuty(750, "horsepower")
```

### Thermal Quantities

#### **ThermalConductivity**

```python
from qnty import ThermalConductivity
k = ThermalConductivity(401, "watt_per_meter_kelvin")  # Copper
```

#### **SpecificHeatCapacityConstantPressure**

```python
from qnty import SpecificHeatCapacityConstantPressure
cp = SpecificHeatCapacityConstantPressure(4186, "joule_per_kilogram_kelvin")  # Water
```

#### **HeatTransferCoefficient**

```python
from qnty import HeatTransferCoefficient
h = HeatTransferCoefficient(1000, "watt_per_square_meter_kelvin")
```

### Fluid Dynamics

#### **ViscosityDynamic**

```python
from qnty import ViscosityDynamic
mu = ViscosityDynamic(0.001, "pascal_second")  # Water at 20°C
```

#### **ViscosityKinematic**

```python
from qnty import ViscosityKinematic
nu = ViscosityKinematic(1e-6, "square_meter_per_second")  # Water at 20°C
```

#### **MassFlowRate**

```python
from qnty import MassFlowRate
flow = MassFlowRate(10, "kilogram_per_second")
```

#### **VolumetricFlowRate**

```python
from qnty import VolumetricFlowRate
flow = VolumetricFlowRate(0.1, "cubic_meter_per_second")
flow = VolumetricFlowRate(100, "gallon_per_minute")
```

### Motion and Time

#### **Time**

```python
from qnty import Time
time = Time(3600, "second")  # 1 hour
time = Time(1, "hour")
time = Time(0.5, "minute")
```

#### **VelocityLinear**

```python
from qnty import VelocityLinear
velocity = VelocityLinear(10, "meter_per_second")
velocity = VelocityLinear(60, "mile_per_hour")
```

#### **Acceleration**

```python
from qnty import Acceleration
accel = Acceleration(9.81, "meter_per_second_squared")  # Gravity
```

#### **VelocityAngular**

```python
from qnty import VelocityAngular
omega = VelocityAngular(100, "radian_per_second")
omega = VelocityAngular(1800, "revolution_per_minute")  # RPM
```

### Dimensionless Quantities

#### **Dimensionless**

```python
from qnty import Dimensionless
ratio = Dimensionless(0.8, "efficiency")
factor = Dimensionless(2.5, "safety_factor")
coefficient = Dimensionless(0.62, "discharge_coefficient")
```

#### **Percent**

```python
from qnty import Percent
efficiency = Percent(85, "percent")
```

### Complete Quantity Type List

**All Available Quantity Types:**

- **AbsorbedDose**
- **Acceleration**
- **ActivationEnergy**
- **AmountOfSubstance**
- **AnglePlane**
- **AngleSolid**
- **AngularAcceleration**
- **AngularMomentum**
- **Area**
- **AreaPerUnitVolume**
- **AtomicWeight**
- **Concentration**
- **Dimensionless**
- **DynamicFluidity**
- **ElectricalConductance**
- **ElectricalPermittivity**
- **ElectricalResistivity**
- **ElectricCapacitance**
- **ElectricCharge**
- **ElectricCurrentIntensity**
- **ElectricDipoleMoment**
- **ElectricFieldStrength**
- **ElectricInductance**
- **ElectricPotential**
- **ElectricResistance**
- **EnergyFlux**
- **EnergyHeatWork**
- **EnergyPerUnitArea**
- **Force**
- **ForceBody**
- **ForcePerUnitMass**
- **FrequencyVoltageRatio**
- **FuelConsumption**
- **HeatOfCombustion**
- **HeatOfFusion**
- **HeatOfVaporization**
- **HeatTransferCoefficient**
- **Illuminance**
- **KineticEnergyOfTurbulence**
- **Length**
- **LinearMassDensity**
- **LinearMomentum**
- **LuminanceSelf**
- **LuminousFlux**
- **LuminousIntensity**
- **MagneticField**
- **MagneticFlux**
- **MagneticInductionFieldStrength**
- **MagneticMoment**
- **MagneticPermeability**
- **MagnetomotiveForce**
- **Mass**
- **MassDensity**
- **MassFlowRate**
- **MassFlux**
- **MassFractionOfI**
- **MassTransferCoefficient**
- **MolalityOfSoluteI**
- **MolarConcentrationByMass**
- **MolarFlowRate**
- **MolarFlux**
- **MolarHeatCapacity**
- **MolarityOfI**
- **MoleFractionOfI**
- **MomentOfInertia**
- **MomentumFlowRate**
- **MomentumFlux**
- **NormalityOfSolution**
- **ParticleDensity**
- **Percent**
- **Permeability**
- **PhotonEmissionRate**
- **PowerPerUnitMass**
- **PowerPerUnitVolume**
- **PowerThermalDuty**
- **Pressure**
- **RadiationDoseEquivalent**
- **RadiationExposure**
- **Radioactivity**
- **SecondMomentOfArea**
- **SecondRadiationConstantPlanck**
- **SpecificEnthalpy**
- **SpecificGravity**
- **SpecificHeatCapacityConstantPressure**
- **SpecificLength**
- **SpecificSurface**
- **SpecificVolume**
- **Stress**
- **SurfaceMassDensity**
- **SurfaceTension**
- **Temperature**
- **ThermalConductivity**
- **Time**
- **Torque**
- **TurbulenceEnergyDissipationRate**
- **VelocityAngular**
- **VelocityLinear**
- **ViscosityDynamic**
- **ViscosityKinematic**
- **Volume**
- **VolumeFractionOfI**
- **VolumetricCalorificHeatingValue**
- **VolumetricCoefficientOfExpansion**
- **VolumetricFlowRate**
- **VolumetricFlux**
- **VolumetricMassFlowRate**
- **Wavenumber**

## Mathematical Functions

### Basic Functions

```python
from qnty import sin, cos, tan, sqrt, ln, log10, exp

# Trigonometric functions
angle = AnglePlane(45, "degree")
sin_val = sin(angle)  # Returns dimensionless
cos_val = cos(angle)
tan_val = tan(angle)

# Exponential and logarithmic
length = Length(100, "mm")
exp_val = exp(ln(length))  # Returns same as length
log_val = log10(length)    # Returns dimensionless
sqrt_val = sqrt(Area(4, "square_meter"))  # Returns Length(2, "meter")
```

### Expression Functions

```python
from qnty import abs_expr, min_expr, max_expr, cond_expr

# Absolute value
diff = abs_expr(length1 - length2)

# Min/Max
min_pressure = min_expr(p1, p2, p3)
max_temp = max_expr(t1, t2)

# Conditional expressions
thickness = cond_expr(
    pressure.gt(threshold),
    thick_wall,        # if pressure > threshold
    standard_wall      # else
)
```

## Variable Operations

### Creating Variables

```python
# Three ways to create variables:
length1 = Length(100, "mm", "Length 1")                           # With value and unit
length2 = Length(0, "mm", "beam_length", is_known=False)         # Unknown variable  
length3 = Length("pipe_diameter")                                # Named variable only
```

### Setting Values

```python
# Fluent API
length = Length("width")
length.set(50).millimeters   # Chainable setter
length.set(2).inches

# Direct assignment (advanced usage)
from qnty.quantities.quantity import Quantity
from qnty.generated.units import LengthUnits
length.quantity = Quantity(25.4, LengthUnits.millimeter)
```

### Mixed Unit Operations

```python
# Qnty automatically handles different units in operations
length_m = Length(1, "meter", "Length in meters")
length_mm = Length(500, "millimeter", "Length in mm")

# Operations automatically convert to compatible units
total = Length("total", is_known=False)
total.solve_from(length_m + length_mm)  # Automatic unit handling
print(f"Total: {total}")  # Result in consistent units
```

### Mathematical Operations

```python
# Arithmetic operations create expressions that need to be solved
width = Length(3, "meter", "Width")
height = Length(2, "meter", "Height")

# Method 1: solve_from() - creates equation and solves immediately
area = Area("area", is_known=False)
area.solve_from(width * height)
print(f"Area: {area}")  # Prints: Area: 6.0 m²

# Method 2: Create equations with .equals() and solve separately
perimeter = Length("perimeter", is_known=False)
perimeter_eq = perimeter.equals(2 * (width + height))
perimeter.solve()
print(f"Perimeter: {perimeter}")  # Prints: Perimeter: 10.0 m

# Method 3: Store equation and solve later
volume = Volume("volume", is_known=False)
depth = Length(1.5, "meter", "Depth")
volume_equation = volume.equals(area * depth)
# ... do other work ...
volume.solve()  # Solves using the stored equation
print(f"Volume: {volume}")

# Comparison operations return expressions that evaluate immediately
is_longer = length1.gt(length2)    # Method form
is_equal = length1 == length2       # Operator form  
is_greater = pressure1 > pressure2  # Automatic unit conversion
```

## Problem System

### Basic Problem Definition

```python
from qnty import Problem, Length, Pressure

class PipeAnalysis(Problem):
    # Known variables
    diameter = Length(0.5, "meter", "Pipe Diameter")
    pressure = Pressure(100, "kilopascal", "Operating Pressure")
    allowable_stress = Pressure(150000, "kilopascal", "Allowable Stress")
    
    # Unknown variable
    thickness = Length(0, "meter", "Wall Thickness", is_known=False)
    
    # Equation using .equals() method
    thickness_equation = thickness.equals(
        (pressure * diameter) / (2 * allowable_stress)
    )

# Use the problem
problem = PipeAnalysis()
problem.solve()
print(problem.thickness)  # Solved thickness value
```

### Programmatic Problem Creation

```python
problem = Problem("Dynamic Analysis")
problem.add_variable(diameter)
problem.add_variable(pressure)
problem.add_equation(thickness_equation)
problem.solve()
```

## Best Practices

### 1. **Always Specify Units**

```python
# Good
length = Length(100, "millimeter")

# Avoid - unclear units
length = Length(100)  # What unit?
```

### 2. **Use Descriptive Names**

```python
# Good
pipe_diameter = Length(0.5, "meter", "Main Pipe Diameter")

# Less clear  
d = Length(0.5, "meter")
```

### 3. **Check for None Before Accessing Quantity**

```python
if variable.quantity is not None:
    value = variable.quantity.value
    unit = variable.quantity.unit
```

### 4. **Leverage Type Safety**

```python
# This will raise an error at assignment - good!
try:
    length.set(100).pascal  # Wrong! Pressure unit on Length variable
except TypeError as e:
    print(f"Dimensional error caught: {e}")
```

### 5. **Use Comparison Methods for Engineering Logic**

```python
# Engineering decision based on comparison
if operating_pressure.gt(design_limit):
    wall_thickness = reinforced_thickness
else:
    wall_thickness = standard_thickness
```
