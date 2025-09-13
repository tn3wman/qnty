from qnty.algebra.nodes import wrap_operand, _get_dimensionless_quantity, _get_cached_dimensionless
from qnty.core.quantity import Quantity

# Test what _get_cached_dimensionless does
try:
    cached_unit = _get_cached_dimensionless()
    print(f"_get_cached_dimensionless() = {type(cached_unit)} : {cached_unit}")
except Exception as e:
    print(f"Error in _get_cached_dimensionless: {e}")

# Test direct Quantity creation
try:
    direct_qty = Quantity(1.0, cached_unit)
    print(f"Quantity(1.0, cached_unit) = {type(direct_qty)} : {direct_qty}")
    print(f"  direct_qty.value = {direct_qty.value}")
    print(f"  direct_qty.unit = {direct_qty.unit}")
except Exception as e:
    print(f"Error in direct Quantity creation: {e}")

# Test what _get_dimensionless_quantity does
try:
    dimless_qty = _get_dimensionless_quantity(1.0)
    print(f"_get_dimensionless_quantity(1.0) = {type(dimless_qty)} : {dimless_qty}")
    print(f"  dimless_qty.value = {dimless_qty.value}")
except Exception as e:
    print(f"Error in _get_dimensionless_quantity: {e}")