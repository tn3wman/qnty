


from qnty.quantities.core import Acceleration

a = Acceleration("Acceleration, a").set(25).meter_per_square_second # This should also mark the variable as known
print(a) # Should print "25 m/s²"
print(a.is_known)  # Should print True

# b = Acceleration("Acceleration, b").set(9.81, "m/s²")
# print(b.is_known)  # True

# c = Acceleration("Acceleration, c")
# print(c.is_known)  # False

# a.to_unit.foot_per_second_squared # Converts and returns new Acceleration in ft/s²
# a.to_unit("ft/s²") # Converts and returns new Acceleration in ft/s²

# a.as_unit.foot_per_second_squared # Keeps same value, but changes unit to ft/s²
# a.as_unit("ft/s²") # Keeps same value, but changes unit to ft/s²





