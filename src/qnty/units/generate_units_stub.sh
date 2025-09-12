#!/bin/bash
# Generate units.pyi stub file

cd "$(dirname "$0")/src/qnty/units"
python -c "from qnty.units.core import write_units_stub; write_units_stub('units.pyi'); print('✓ Generated units.pyi successfully')"