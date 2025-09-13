import qnty as qt

# Demonstrate unit conversion and manipulation
print("Unit Conversion Demo")
print("=" * 40)

# Create some variables
L = qt.Acceleration("Gravity").set(9.81).meter_per_square_second
W = qt.Length(3, "m", "Width")
A = qt.Area("Area")

# Demonstrate the new unit conversion API methods
print("Testing new unit conversion API:")

# L.set(5).mm - Set length to 5 millimeters
L.set(5).mm
print(f"After L.set(5).mm: {L}")

# Another way to set length to 5 millimeters - using constructor
L2 = qt.Length(5, "mm", "Length_Alt")
print(f"Alternative L2 = qt.Length(5, 'mm'): {L2}")

# L.to_unit.mm - Convert length to millimeters (L is already in mm, so no change)
L.to_unit.mm
print(f"After L.to_unit.mm: {L}")

# L.to_unit("mm") - Another way to convert length to millimeters
L.to_unit("mm")
print(f"After L.to_unit('mm'): {L}")

# L.as_unit.cm - Represent length in centimeters without changing the value
L_as_cm = L.as_unit.cm
print(f"L.as_unit.cm returns: {L_as_cm}")
print(f"Original L unchanged: {L}")

# L.as_unit("cm") - Another way to represent length in centimeters without changing the value
L_as_cm_alt = L.as_unit("cm")
print(f"L.as_unit('cm') returns: {L_as_cm_alt}")
print(f"Original L still unchanged: {L}")

print()

print(f"L = {L}")
print(f"W = {W}")
print(f"A = {A} (before)")

# Set arithmetic mode to quantity for direct calculation
L.set_arithmetic_mode('quantity')
W.set_arithmetic_mode('quantity')

# Calculate area
area_result = L * W
print(f"L * W = {area_result}")

# Manually set the area
A.quantity = area_result
A._is_known = True

print(f"A = {A} (after)")

# Show unit conversion
print()
print("Unit Conversion Examples:")
print(f"Length in meters: {L}")
print(f"Length in millimeters: {qt.Length(5000, 'mm', 'Length_mm')}")
print(f"Area: {A}")

print()
print("Unit conversion demo completed!")
