"""
Debug script to investigate why _b_0_cond is not recognized as known.
"""
import logging
import sys
from pathlib import Path

# Add the src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s: %(message)s')
logger = logging.getLogger('DEBUG')

from qnty import Length

# Test 1: Create variable exactly as in test file
logger.info("="*80)
logger.info("TEST 1: Variable creation as in test file")
logger.info("="*80)

_b_0_cond = Length("Condition for b_0").set(6).millimeter

logger.info(f"Variable name: {_b_0_cond.name}")
logger.info(f"Variable symbol: {_b_0_cond._symbol}")
logger.info(f"Variable value: {_b_0_cond.value}")
logger.info(f"Variable is_known: {_b_0_cond.is_known}")
logger.info(f"Variable preferred: {_b_0_cond.preferred}")
logger.info(f"Variable dim: {_b_0_cond.dim}")

# Test 2: Check variable without the .set() chain
logger.info("\n" + "="*80)
logger.info("TEST 2: Variable without .set() chain")
logger.info("="*80)

_b_0_cond_no_set = Length("Condition for b_0")

logger.info(f"No-set variable name: {_b_0_cond_no_set.name}")
logger.info(f"No-set variable value: {_b_0_cond_no_set.value}")
logger.info(f"No-set variable is_known: {_b_0_cond_no_set.is_known}")
logger.info(f"No-set variable dim: {_b_0_cond_no_set.dim}")

# Test 3: Check what happens during Problem initialization
logger.info("\n" + "="*80)
logger.info("TEST 3: Check variable extraction in Problem class")
logger.info("="*80)

from qnty import Problem

class TestProblem(Problem):
    name = "Test Problem"

    test_var = Length("Test Variable").set(5).meter
    _test_hidden = Length("Hidden Variable").set(6).millimeter

problem = TestProblem()

logger.info(f"Variables in problem: {list(problem.variables.keys())}")
logger.info("\nVariable details:")
for var_name, var in problem.variables.items():
    logger.info(f"  {var_name}:")
    logger.info(f"    is_known: {var.is_known}")
    logger.info(f"    value: {var.value}")
    logger.info(f"    symbol: {var._symbol if hasattr(var, '_symbol') else 'N/A'}")

# Test 4: Check if underscore prefix affects extraction
logger.info("\n" + "="*80)
logger.info("TEST 4: Does underscore prefix matter for variable extraction?")
logger.info("="*80)

logger.info(f"test_var in variables: {'test_var' in problem.variables}")
logger.info(f"_test_hidden in variables: {'_test_hidden' in problem.variables}")

# Test 5: Direct check of the FlangeDesign problem
logger.info("\n" + "="*80)
logger.info("TEST 5: Check _b_0_cond in actual FlangeDesign problem")
logger.info("="*80)

sys.path.insert(0, str(Path(__file__).parent / "tests" / "asme" / "section_viii" / "division_ii"))
from test_flange_design import create_flange_design

problem = create_flange_design()

if "_b_0_cond" in problem.variables:
    var = problem.variables["_b_0_cond"]
    logger.info(f"_b_0_cond found in variables")
    logger.info(f"  is_known: {var.is_known}")
    logger.info(f"  value: {var.value}")
    logger.info(f"  dim: {var.dim}")
else:
    logger.error("_b_0_cond NOT found in variables!")
    logger.info(f"Available variables starting with underscore:")
    for name in problem.variables.keys():
        if name.startswith("_"):
            logger.info(f"  {name}")
