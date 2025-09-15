#!/usr/bin/env python3

"""Debug script to investigate the variable canonicalization issue."""

from tests.test_composed_problem import create_welded_branch_connection

def debug_variable_issue():
    problem = create_welded_branch_connection()

    # For system
    problem.P.set(2068000).pascal

    # For header
    problem.header.D.set(219.1).millimeter
    problem.header.T_bar.set(8.18).millimeter
    problem.header.U_m.set(0.125).dimensionless
    problem.header.c.set(2.5).millimeter
    problem.header.S.set(110000000).pascal # 110 MPa
    problem.header.E.set(1).dimensionless
    problem.header.W.set(1).dimensionless
    problem.header.Y.set(0.4).dimensionless

    # For run
    problem.branch.D.set(114.3).millimeter
    problem.branch.T_bar.set(6.02).millimeter
    problem.branch.U_m.set(0.125).dimensionless
    problem.branch.c.set(2.5).millimeter
    problem.branch.S.set(110000000).pascal
    problem.branch.E.set(1).dimensionless
    problem.branch.W.set(1).dimensionless
    problem.branch.Y.set(0.4).dimensionless

    print(f"T_bar_r.name: '{problem.T_bar_r.name}'")
    print(f"T_bar_r.value: {problem.T_bar_r.value}")
    print(f"header.c.name: '{problem.header.c.name}'")
    print(f"header.c.value: {problem.header.c.value}")
    print(f"T_bar_r id: {id(problem.T_bar_r)}")
    print(f"header.c id: {id(problem.header.c)}")

    # Check if the names look similar or could be confused
    print(f"\nName comparison:")
    print(f"T_bar_r name == header.c name: {problem.T_bar_r.name == problem.header.c.name}")
    print(f"'c' in T_bar_r name: {'c' in problem.T_bar_r.name.lower()}")
    print(f"'c' in header.c name: {'c' in problem.header.c.name.lower()}")

    # Check all variables in the problem for any that have 'c' in the name
    print(f"\nAll variables with 'c' in name:")
    for attr_name in dir(problem):
        if not attr_name.startswith('_'):
            attr_value = getattr(problem, attr_name, None)
            if (attr_value and hasattr(attr_value, 'name') and hasattr(attr_value, 'value') and
                'c' in attr_value.name.lower()):
                print(f"  {attr_name}: '{attr_value.name}' = {attr_value.value}")

            # Also check sub-problem attributes
            if hasattr(attr_value, '__dict__'):
                for sub_attr_name in dir(attr_value):
                    if not sub_attr_name.startswith('_'):
                        try:
                            sub_attr_value = getattr(attr_value, sub_attr_name, None)
                            if (sub_attr_value and hasattr(sub_attr_value, 'name') and
                                hasattr(sub_attr_value, 'value') and
                                'c' in sub_attr_value.name.lower()):
                                print(f"  {attr_name}.{sub_attr_name}: '{sub_attr_value.name}' = {sub_attr_value.value}")
                        except (AttributeError, TypeError):
                            continue

    # Find the t_c_r_eqn equation
    t_c_r_eqn = None
    for eq in problem.equations:
        if eq.name == "t_c_r_eqn":
            t_c_r_eqn = eq
            break

    if t_c_r_eqn:
        print(f"\nOriginal equation: {t_c_r_eqn}")
        print(f"LHS: {t_c_r_eqn.lhs}")
        print(f"RHS: {t_c_r_eqn.rhs}")

        # Examine the RHS components
        from qnty.algebra.nodes import BinaryOperation, VariableReference
        if isinstance(t_c_r_eqn.rhs, BinaryOperation):
            print(f"RHS operation: {t_c_r_eqn.rhs.operation}")
            print(f"RHS left: {t_c_r_eqn.rhs.left}")
            print(f"RHS right: {t_c_r_eqn.rhs.right}")

            if isinstance(t_c_r_eqn.rhs.right, VariableReference):
                var_ref = t_c_r_eqn.rhs.right.variable
                print(f"Variable referenced in RHS: {var_ref.name}")
                print(f"Variable id: {id(var_ref)}")
                print(f"Variable value: {var_ref.value}")

    problem.solve()

    print(f"\nAfter solving:")
    print(f"t_c_r.value: {problem.t_c_r.value}")
    print(f"A_w_r.value: {problem.A_w_r.value}")
    print(f"A_4.value: {problem.A_4.value}")

if __name__ == "__main__":
    debug_variable_issue()