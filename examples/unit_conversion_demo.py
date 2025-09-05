import qnty as qt

# Demonstrate unit conversion and manipulation
# TODO: Not implemented yet
L = qt.Length(5, "m", "Length")
A = qt.Area(1, "square_meter", "Area", is_known=False)

A.solve_from(L**2)

print(f"L = {L}")
print(f"A = {A}")
