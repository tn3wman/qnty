
from math import acos, acosh, asin, asinh, atan, atan2, atanh, cos, cosh, exp, log, log10, sin, sinh, sqrt, tan, tanh
from re import L

from qnty.core import Acceleration, Dimensionless, Length, Q
from qnty.core import unit_catalog as uc


def basic_quantity_usage():
    """Demonstrates basic usage of the Q function and unit conversions."""
    # Using a basic acceleration quantity
    print()
    print("Using a basic acceleration quantity")
    print("--------------------------------")
    a_quantity = Q(25, "ft/s²")
    print(f"a_quantity in ft/s²: {a_quantity}")
    a_quantity = a_quantity.to_unit("m/s²")
    print(f"a_quantity in m/s²: {a_quantity}")
    a_quantity = a_quantity.as_unit("ft/s²")
    print(f"a_quantity as ft/s²: {a_quantity}")
    a_quantity = a_quantity.to_unit("m/s²")
    print(f"a_quantity in m/s²: {a_quantity}")

    # Using the unit catalog directly (default preferred units)
    print()
    print("Using the unit catalog directly (default preferred units)")
    print("----------------------------------------------------")
    b_quantity = Q(25, uc.AccelerationUnits)
    print(f"b_quantity in preferred units: {b_quantity}")
    b_quantity = b_quantity.to_unit("ft/s²")
    print(f"b_quantity in ft/s²: {b_quantity}")
    b_quantity = b_quantity.as_unit("m/s²")
    print(f"b_quantity as m/s²: {b_quantity}")
    b_quantity = b_quantity.to_unit.feet_per_square_second
    print(f"b_quantity in ft/s²: {b_quantity}")
    print()

def field_quantity_usage():
    """Demonstrates usage of quantities as fields in classes."""
    x = Length("x").set(3).meter
    y = Length("y").set(4).meter
    z = Length("z").set(5).meter

    area = x * y

    print()
    print(f"Area = {area}")

    volume = x * y * z

    print()
    print(f"Volume = {volume}")

def other_stuff():
    d = Dimensionless("d").set(0.01).dimensionless

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

    z = a + a

    q = a * a

    print(q)

    # Now this works! Addition returns a Quantity with .to_unit method
    print(z.to_unit.feet_per_square_second)  # Should print the sum in ft/s²

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


if __name__ == "__main__":
    # basic_quantity_usage()
    field_quantity_usage()


