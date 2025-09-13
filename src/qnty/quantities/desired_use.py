
from qnty.quantities import Acceleration

a = Acceleration("Acceleration, a").set(25).meter_per_square_second # This should also mark the variable as known
a = a.as_unit.meter_per_square_second
print(a) # Should print "25 m/s²"
print(a.is_known)  # Should print True

b = Acceleration("Acceleration, b").set(9.81, "m/s²")
print(b)  # Should print "9.81 m/s²"
print(b.is_known)  # True

c = Acceleration("Acceleration, c")
print(c)  # Should print "Acceleration, c (unknown)"
print(c.is_known)  # False

a = a.to_unit.feet_per_square_second # Converts and returns new Acceleration in ft/s²
print(a)
a = a.to_unit("m/s²") # Converts and returns new Acceleration in m/s²
print(a)

a = a.as_unit.feet_per_second_squared # Keeps same value, but changes unit to ft/s²
a = a.as_unit("ft/s²") # Keeps same value, but changes unit to ft/s²
print(a)




