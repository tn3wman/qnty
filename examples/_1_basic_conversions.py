from binascii import crc_hqx
from calendar import c
from qnty.core import Acceleration, Dimensionless, Length, Q
from qnty.core import unit_catalog as uc


def basic_quantity_usage():
    """Demonstrates basic usage of the Q function and unit conversions."""
    # Using a basic acceleration quantity
    print()
    print("Using a basic acceleration quantity")
    print("-----------------------------------")
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
    print("Using the unit catalog")
    print("----------------------")
    b_quantity = Q(25, uc.AccelerationUnits)
    print(f"b_quantity in preferred units: {b_quantity}")
    b_quantity = b_quantity.to_unit("ft/s²")
    print(f"b_quantity in ft/s²: {b_quantity}")
    b_quantity = b_quantity.as_unit("m/s²")
    print(f"b_quantity as m/s²: {b_quantity}")
    b_quantity = b_quantity.to_unit.feet_per_square_second
    print(f"b_quantity in ft/s²: {b_quantity}")
    print()

    # Using a field quantity
    print()
    print("Using a field quantity")
    print("----------------------")
    c_quantity = Acceleration("c_quantity").set(25).foot_per_square_second
    print(f"c_quantity in ft/s²: {c_quantity}")
    c_quantity = c_quantity.to_unit.meter_per_square_second
    print(f"c_quantity in m/s²: {c_quantity}")
    c_quantity = c_quantity.as_unit.foot_per_square_second
    print(f"c_quantity as ft/s²: {c_quantity}")
    c_quantity = c_quantity.to_unit.meter_per_square_second
    print(f"c_quantity in m/s²: {c_quantity}")
    print()


if __name__ == "__main__":
    basic_quantity_usage()