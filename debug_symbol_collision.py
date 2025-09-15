#!/usr/bin/env python3

"""Debug to check if T_bar_r and header.c have the same symbol."""

import os
import sys
sys.path.insert(0, os.getcwd())

from qnty import Length, Problem
from qnty.algebra import equation
from tests.test_composed_problem import create_straight_pipe_internal

class SymbolTest(Problem):
    # Create a sub-problem first
    header = create_straight_pipe_internal()

    # Define our variables
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    t_c_r = Length("Weld Throat, Reinforcement")

    # Create equation
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

def test_symbols():
    print("=== SYMBOL COLLISION TEST ===")

    problem = SymbolTest()

    print(f"T_bar_r.symbol: '{problem.T_bar_r.symbol}'")
    print(f"T_bar_r.name: '{problem.T_bar_r.name}'")
    print(f"T_bar_r ID: {id(problem.T_bar_r)}")

    print(f"\nheader.c.symbol: '{problem.header.c.symbol}'")
    print(f"header.c.name: '{problem.header.c.name}'")
    print(f"header.c ID: {id(problem.header.c)}")

    print(f"\nSymbol collision: {problem.T_bar_r.symbol == problem.header.c.symbol}")
    print(f"Name collision: {problem.T_bar_r.name == problem.header.c.name}")

    # Check all variables in the problem for symbol collisions
    print(f"\n=== ALL VARIABLES SYMBOL CHECK ===")
    symbol_map = {}

    for var_name in dir(problem):
        if not var_name.startswith('_'):
            var = getattr(problem, var_name, None)
            if hasattr(var, 'symbol') and hasattr(var, 'name'):
                symbol = var.symbol
                if symbol in symbol_map:
                    print(f"COLLISION FOUND!")
                    print(f"  Variable 1: {symbol_map[symbol]['name']} -> symbol='{symbol}', name='{symbol_map[symbol]['display_name']}'")
                    print(f"  Variable 2: {var_name} -> symbol='{symbol}', name='{var.name}'")
                else:
                    symbol_map[symbol] = {
                        'name': var_name,
                        'display_name': var.name,
                        'id': id(var)
                    }

    # Also check sub-problem variables
    for sub_name in dir(problem):
        if not sub_name.startswith('_'):
            sub_obj = getattr(problem, sub_name, None)
            if hasattr(sub_obj, '__dict__'):
                for sub_var_name in dir(sub_obj):
                    if not sub_var_name.startswith('_'):
                        sub_var = getattr(sub_obj, sub_var_name, None)
                        if hasattr(sub_var, 'symbol') and hasattr(sub_var, 'name'):
                            symbol = sub_var.symbol
                            full_name = f"{sub_name}.{sub_var_name}"
                            if symbol in symbol_map:
                                print(f"COLLISION FOUND!")
                                print(f"  Variable 1: {symbol_map[symbol]['name']} -> symbol='{symbol}', name='{symbol_map[symbol]['display_name']}'")
                                print(f"  Variable 2: {full_name} -> symbol='{symbol}', name='{sub_var.name}'")
                            else:
                                symbol_map[symbol] = {
                                    'name': full_name,
                                    'display_name': sub_var.name,
                                    'id': id(sub_var)
                                }

    if len(symbol_map) > 0:
        print(f"\nNo symbol collisions found among {len(symbol_map)} variables")

    # Check the context that gets passed to resolve
    print(f"\n=== CONTEXT CHECK ===")
    if hasattr(problem, 'variables'):
        print(f"Problem has {len(problem.variables)} variables in context:")
        for symbol, var in problem.variables.items():
            if hasattr(var, 'name'):
                print(f"  '{symbol}' -> '{var.name}' (ID: {id(var)})")
                if 'c' in symbol.lower() or 'thickness' in var.name.lower() or 'reinforcement' in var.name.lower():
                    print(f"    *** RELEVANT ***")

if __name__ == "__main__":
    test_symbols()