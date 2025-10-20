"""
Debug script for FlangeDesign problem - adds comprehensive logging to understand solving failures.
"""
import logging
import sys
from pathlib import Path

# Add the src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent / "tests" / "asme" / "section_viii" / "division_ii"))

# Configure comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)-8s [%(name)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('flange_debug.log', mode='w')
    ]
)

# Create specific loggers for different components
logger = logging.getLogger('DEBUG')
solver_logger = logging.getLogger('qnty.solving')
problem_logger = logging.getLogger('qnty.problems')
equation_logger = logging.getLogger('qnty.algebra')

# Set all to DEBUG level
for log in [solver_logger, problem_logger, equation_logger]:
    log.setLevel(logging.DEBUG)

def debug_problem_state(problem):
    """Print detailed problem state for debugging."""
    logger.info("="*80)
    logger.info("PROBLEM STATE ANALYSIS")
    logger.info("="*80)

    # Variables
    logger.info(f"\nTotal Variables: {len(problem.variables)}")
    known_vars = problem.get_known_variables()
    unknown_vars = problem.get_unknown_variables()

    logger.info(f"\nKnown Variables ({len(known_vars)}):")
    for symbol, var in known_vars.items():
        logger.info(f"  {symbol:20} = {var.value:20} {var.dim} (preferred: {var.preferred})")

    logger.info(f"\nUnknown Variables ({len(unknown_vars)}):")
    for symbol, var in unknown_vars.items():
        logger.info(f"  {symbol:20} (dim: {var.dim})")

    # Equations
    logger.info(f"\nTotal Equations: {len(problem.equations)}")
    for i, eq in enumerate(problem.equations, 1):
        logger.info(f"\n  Equation {i}: {eq.name}")
        try:
            eq_vars = eq.get_all_variables()
            logger.info(f"    Variables: {eq_vars}")
            logger.info(f"    LHS: {eq.lhs}")
            logger.info(f"    RHS: {eq.rhs}")
        except Exception as e:
            logger.error(f"    Error analyzing equation: {e}")

    # System analysis
    logger.info("\n" + "="*80)
    logger.info("SYSTEM ANALYSIS")
    logger.info("="*80)
    try:
        analysis = problem.analyze_system()
        for key, value in analysis.items():
            logger.info(f"  {key}: {value}")
    except Exception as e:
        logger.error(f"  Error in system analysis: {e}")

    logger.info("="*80)

def debug_equation_details(problem):
    """Print detailed equation information."""
    logger.info("\n" + "="*80)
    logger.info("DETAILED EQUATION ANALYSIS")
    logger.info("="*80)

    for i, eq in enumerate(problem.equations, 1):
        logger.info(f"\nEquation {i}: {eq.name}")
        logger.info(f"  Type: {type(eq)}")
        logger.info(f"  LHS type: {type(eq.lhs)}")
        logger.info(f"  RHS type: {type(eq.rhs)}")

        # Try to get equation variables
        try:
            eq_vars = eq.get_all_variables()
            logger.info(f"  Variables used: {eq_vars}")

            # Check which are known vs unknown
            known = [v for v in eq_vars if v in problem.variables and problem.variables[v].is_known]
            unknown = [v for v in eq_vars if v in problem.variables and not problem.variables[v].is_known]
            missing = [v for v in eq_vars if v not in problem.variables]

            logger.info(f"  Known vars: {known}")
            logger.info(f"  Unknown vars: {unknown}")
            if missing:
                logger.error(f"  MISSING vars: {missing}")

            # Try to evaluate if possible
            if len(unknown) == 1 and not missing:
                logger.info(f"  --> Can potentially solve for: {unknown[0]}")

        except Exception as e:
            logger.error(f"  Error analyzing equation variables: {e}")
            import traceback
            logger.error(traceback.format_exc())

    logger.info("="*80)

def debug_solving_attempt(problem):
    """Monitor the solving attempt with detailed logging."""
    logger.info("\n" + "="*80)
    logger.info("SOLVING ATTEMPT")
    logger.info("="*80)

    try:
        # Add hooks to track solver progress
        original_solve = problem.solver_manager.solve

        def wrapped_solve(*args, **kwargs):
            logger.info("Solver manager called with:")
            logger.info(f"  Equations: {len(args[0]) if args else 'N/A'}")
            logger.info(f"  Variables: {len(args[1]) if len(args) > 1 else 'N/A'}")
            logger.info(f"  Max iterations: {kwargs.get('max_iterations', 'default')}")
            logger.info(f"  Tolerance: {kwargs.get('tolerance', 'default')}")

            result = original_solve(*args, **kwargs)

            logger.info(f"\nSolver result:")
            logger.info(f"  Success: {result.success}")
            logger.info(f"  Message: {result.message}")
            logger.info(f"  Method: {result.method}")
            logger.info(f"  Iterations: {getattr(result, 'iterations', 'N/A')}")
            logger.info(f"  Steps: {len(result.steps)}")

            return result

        problem.solver_manager.solve = wrapped_solve

        # Attempt to solve
        logger.info("\nCalling problem.solve()...")
        solution = problem.solve()

        logger.info("\n" + "="*80)
        logger.info("SOLVE COMPLETED SUCCESSFULLY")
        logger.info("="*80)

        # Print solution
        logger.info("\nSolution:")
        for symbol, var in solution.items():
            if var.value is not None:
                logger.info(f"  {symbol:20} = {var.value:20} (dim: {var.dim})")

        return True, solution

    except Exception as e:
        logger.error("\n" + "="*80)
        logger.error("SOLVE FAILED")
        logger.error("="*80)
        logger.error(f"Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False, None

def main():
    """Main debug function."""
    logger.info("="*80)
    logger.info("FLANGE DESIGN DEBUG SCRIPT")
    logger.info("="*80)

    # Import the test module
    try:
        from test_flange_design import FlangeDesign, create_flange_design
        logger.info("Successfully imported FlangeDesign")
    except Exception as e:
        logger.error(f"Failed to import: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return

    # Create the problem
    logger.info("\nCreating FlangeDesign problem...")
    try:
        problem = create_flange_design()
        logger.info("Problem created successfully")
    except Exception as e:
        logger.error(f"Failed to create problem: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return

    # Debug problem state before solving
    debug_problem_state(problem)

    # Detailed equation analysis
    debug_equation_details(problem)

    # Attempt to solve with monitoring
    success, solution = debug_solving_attempt(problem)

    # Final summary
    logger.info("\n" + "="*80)
    logger.info("DEBUG SUMMARY")
    logger.info("="*80)
    if success:
        logger.info("✓ Problem solved successfully")
    else:
        logger.info("✗ Problem failed to solve")
        logger.info("\nCheck flange_debug.log for detailed analysis")
    logger.info("="*80)

if __name__ == "__main__":
    main()
