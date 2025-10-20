"""
Diagnostic script to find variables referenced in equations but missing their own defining equation.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent / "tests" / "asme" / "section_viii" / "division_ii"))

from test_flange_design import create_flange_design

problem = create_flange_design()

print("="*80)
print("EQUATION COVERAGE ANALYSIS")
print("="*80)

# Get all variables referenced in equations
all_referenced_vars = set()
for eq in problem.equations:
    all_referenced_vars.update(eq.get_all_variables())

# Get all variables that are LHS of an equation (i.e., have a defining equation)
defined_vars = set()
for eq in problem.equations:
    # Check if LHS is a VariableReference
    if hasattr(eq.lhs, 'symbol'):
        defined_vars.add(eq.lhs.symbol)

# Find variables that are referenced but not defined by any equation
unknown_vars = problem.get_unknown_symbols()
known_vars = problem.get_known_symbols()

# Variables that need equations (unknown and not defined)
missing_equations = unknown_vars - defined_vars

print(f"\nTotal variables: {len(problem.variables)}")
print(f"Known variables: {len(known_vars)}")
print(f"Unknown variables: {len(unknown_vars)}")
print(f"Variables with defining equations: {len(defined_vars)}")

if missing_equations:
    print(f"\n[X] CRITICAL: {len(missing_equations)} unknown variables are MISSING defining equations:")
    for var in sorted(missing_equations):
        print(f"  - {var}")
        # Find which equations reference this variable
        refs = []
        for i, eq in enumerate(problem.equations, 1):
            if var in eq.get_all_variables():
                refs.append(f"Eq{i}: {eq.name}")
        if refs:
            print(f"    Referenced in: {', '.join(refs[:3])}")
else:
    print("\n[OK] All unknown variables have defining equations")

# Check for duplicate equation definitions
print("\n" + "="*80)
print("DUPLICATE EQUATION CHECK")
print("="*80)

lhs_counts = {}
for eq in problem.equations:
    if hasattr(eq.lhs, 'symbol'):
        symbol = eq.lhs.symbol
        if symbol not in lhs_counts:
            lhs_counts[symbol] = []
        lhs_counts[symbol].append(eq.name)

duplicates = {k: v for k, v in lhs_counts.items() if len(v) > 1}
if duplicates:
    print(f"\n[!] WARNING: {len(duplicates)} variables have MULTIPLE defining equations:")
    for var, eqs in duplicates.items():
        print(f"  - {var}: {len(eqs)} equations")
        for eq_name in eqs:
            print(f"      - {eq_name}")
else:
    print("\n[OK] No duplicate equation definitions")

# Analyze the unsolvable variables
print("\n" + "="*80)
print("UNSOLVABLE VARIABLES ANALYSIS")
print("="*80)

analysis = problem.analyze_system()
unsolvable = analysis.get('unsolvable_variables', [])

if unsolvable:
    print(f"\n{len(unsolvable)} variables cannot be solved:")
    for var in unsolvable:
        print(f"\n  Variable: {var}")

        # Check if it has a defining equation
        if var in defined_vars:
            # Find the equation
            for eq in problem.equations:
                if hasattr(eq.lhs, 'symbol') and eq.lhs.symbol == var:
                    eq_vars = eq.get_all_variables()
                    eq_vars.remove(var)  # Remove LHS
                    unknown_deps = [v for v in eq_vars if v in unknown_vars]
                    print(f"    Has equation: {eq.name}")
                    print(f"    Depends on unknowns: {unknown_deps}")
                    break
        else:
            print(f"    [X] MISSING EQUATION - This is why it's unsolvable!")
else:
    print("\n[OK] All variables are solvable")

print("\n" + "="*80)
