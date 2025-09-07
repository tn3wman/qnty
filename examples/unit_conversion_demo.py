import qnty as qt

# Demonstrate unit conversion and manipulation
print("Unit Conversion Demo")
print("=" * 40)

# Create some variables
L = qt.Length(5, "m", "Length")
W = qt.Length(3, "m", "Width") 
A = qt.Area("Area", is_known=False)

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
