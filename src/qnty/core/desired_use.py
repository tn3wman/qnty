
from math import acos, acosh, asin, asinh, atan, atan2, atanh, cos, cosh, exp, log, log10, sin, sinh, sqrt, tan, tanh

from qnty.core import Acceleration, Dimensionless

# .set, .to_unit, .as_unit should all have proper auto completion and type checking and the units avaible for Acceleration should be available for auto completion and type checking as well

d = Dimensionless("d").set(3.14).dimensionless

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

a = acos(d)
b = acosh(d)
c = asin(d)
d = asinh(d)
e = atan(d)
f = atan2(d, d)
g = atanh(d)
h = cos(d)
i = cosh(d)
j = exp(d)
k = log(d)
l = log10(d)
m = sin(d)
n = sinh(d)
o = sqrt(d)
p = tan(d)
q = tanh(d)




