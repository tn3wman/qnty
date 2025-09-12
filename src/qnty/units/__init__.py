# /units/__init__.py
from __future__ import annotations

from .core import (
    add_unit,
    attach_composed,
    seal_units,
    u,  # namespace + registry
    ureg,
    Unit,
)

from .unit_catalog_base import *
from .unit_catalog_tert import *
from .unit_catalog_sec import *

# from .pressure import *   # add more catalogs here
# from .dimensionless import *

# --- Optionally: set preferred display units here (try/except avoids order issues) ---
# try:
#     ureg.set_preferred(u.meter)
#     ureg.set_preferred(u.second)
#     # If your catalogs define these:
#     # ureg.set_preferred(u.newton)
#     # ureg.set_preferred(u.pascal)
# except Exception:
#     pass

# --- Optionally: auto-generate stubs in a build/init step (comment out in production) ---
# write_dimensions_stub("dimensions.pyi")
# write_units_stub("core.pyi")                 # or "__init__.pyi" if you stub this package
# write_unit_namespaces_stub("unit_namespaces.pyi", ForceUnits, DimensionlessUnits)

# --- Optionally: seal to prevent mutations after import (uncomment when stable) ---
# seal_dimensions()
# seal_units()

__all__ = [
    "u", "ureg",
    "add_unit", "attach_composed",
    "seal_units",
]

