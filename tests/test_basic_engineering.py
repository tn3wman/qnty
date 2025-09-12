import pytest

import qnty as qt


def _create_problem_1():
    """Create the honey problem variables."""
    mu = qt.ViscosityDynamic("Honey_viscosity").set(1000).poise
    rho = qt.MassDensity("Honey_density").set(0.05).oz_mL
    nu = qt.ViscosityKinematic("Honey_kinematic_viscosity")
    return mu, rho, nu

def _create_problem_2():
    D_1 = qt.Length("D_1").set(1.049).inch
    D_1_5 = qt.Length("D_1_5").set(1.610).inch
    D_2_5 = qt.Length("D_2_5").set(2.469).inch

    V_1 = qt.VelocityLinear("V_1")
    V_1_5 = qt.VelocityLinear("V_1_5").set(4).ft_s
    V_2_5 = qt.VelocityLinear("V_2_5")

    Q_1 = qt.VolumetricFlowRate("Q_1")
    Q_1_5 = qt.VolumetricFlowRate("Q_1_5")
    Q_2_5 = qt.VolumetricFlowRate("Q_2_5").set(50).gpm

    A_1 = qt.Area("A_1")
    A_1_5 = qt.Area("A_1_5")
    A_2_5 = qt.Area("A_2_5")

    return D_1, D_1_5, D_2_5, V_1, V_1_5, V_2_5, Q_1, Q_1_5, Q_2_5, A_1, A_1_5, A_2_5

def _solve_problem_1(method):
    """Helper to solve honey viscosity problem using different methods."""
    
    if method == "problem_class":
        # For Problem class, define it with class attributes
        class Problem(qt.Problem):
            mu, rho, nu = _create_problem_1()
            nu_eqn = nu.equals(mu / rho)
        
        problem = Problem()
        problem.solve()
        return {"mu": problem.mu, "rho": problem.rho, "nu": problem.nu}
    
    # For non-Problem methods, create variables normally
    mu, rho, nu = _create_problem_1()
    
    if method == "solve_from":
        nu.solve_from(mu / rho)
    elif method == "equation":
        _nu_eqn = nu.equals(mu / rho)
        nu.solve()
    
    return {"mu": mu, "rho": rho, "nu": nu}

def _solve_problem_2(method):

    if method == "problem_class":
        # For Problem class, define it with class attributes
        class Problem(qt.Problem):
            D_1, D_1_5, D_2_5, V_1, V_1_5, V_2_5, Q_1, Q_1_5, Q_2_5, A_1, A_1_5, A_2_5 = _create_problem_2()

            A_1_eqn = A_1.equals(3.14 * (D_1 / 2) ** 2)
            A_1_5_eqn = A_1_5.equals(3.14 * (D_1_5 / 2) ** 2)
            A_2_5_eqn = A_2_5.equals(3.14 * (D_2_5 / 2) ** 2)

            # V_1_eqn = V_1.equals(Q_1 / A_1)
            # V_1_5_eqn = V_1_5.equals(Q_1_5 / A_1_5)
            # V_2_5_eqn = V_2_5.equals(Q_2_5 / A_2_5)

            Q_1_eqn = Q_1.equals(V_1 * A_1)
            Q_1_5_eqn = Q_1_5.equals(V_1_5 * A_1_5)
            Q_2_5_eqn = Q_2_5.equals(V_2_5 * A_2_5)

            Q = Q_2_5.equals(Q_1_5 + Q_1)

        problem = Problem()
        problem.solve()
        return {
            "D_1": problem.D_1,
            "D_1_5": problem.D_1_5,
            "D_2_5": problem.D_2_5,
            "V_1": problem.V_1,
            "V_1_5": problem.V_1_5,
            "V_2_5": problem.V_2_5,
            "Q_1": problem.Q_1,
            "Q_1_5": problem.Q_1_5,
            "Q_2_5": problem.Q_2_5,
            "A_1": problem.A_1,
            "A_1_5": problem.A_1_5,
            "A_2_5": problem.A_2_5,
        }
    
    # For non-Problem methods, create variables normally
    D_1, D_1_5, D_2_5, V_1, V_1_5, V_2_5, Q_1, Q_1_5, Q_2_5, A_1, A_1_5, A_2_5 = _create_problem_2()

    if method == "solve_from":
        A_1.solve_from(3.14 * (D_1 / 2) ** 2)
        A_1_5.solve_from(3.14 * (D_1_5 / 2) ** 2)
        A_2_5.solve_from(3.14 * (D_2_5 / 2) ** 2)

        Q_1_5.solve_from(A_1_5 * V_1_5)
        Q_1.solve_from(Q_2_5 - Q_1_5)

        V_1.solve_from(Q_1 / A_1)
        V_2_5.solve_from(Q_2_5 / A_2_5)

    elif method == "equation":
        _A_1_eqn = A_1.equals(3.14 * (D_1 / 2) ** 2)
        _A_1_5_eqn = A_1_5.equals(3.14 * (D_1_5 / 2) ** 2)
        _A_2_5_eqn = A_2_5.equals(3.14 * (D_2_5 / 2) ** 2)

        _Q_1_5_eqn = Q_1_5.equals(A_1_5 * V_1_5)
        _Q_1_eqn = Q_1.equals(Q_2_5 - Q_1_5)

        _V_1_eqn = V_1.equals(Q_1 / A_1)
        _V_2_5_eqn = V_2_5.equals(Q_2_5 / A_2_5)

        A_1.solve()
        A_1_5.solve()
        A_2_5.solve()
        Q_1_5.solve()
        Q_1.solve()
        V_1.solve()
        V_2_5.solve()

    return {
        "D_1": D_1,
        "D_1_5": D_1_5,
        "D_2_5": D_2_5,
        "V_1": V_1,
        "V_1_5": V_1_5,
        "V_2_5": V_2_5,
        "Q_1": Q_1,
        "Q_1_5": Q_1_5,
        "Q_2_5": Q_2_5,
        "A_1": A_1,
        "A_1_5": A_1_5,
        "A_2_5": A_2_5,
    }



@pytest.mark.parametrize("solving_method", [
    "solve_from",
    "equation",
    "problem_class"
])
def test_problem_1(solving_method, capsys):
    """Test honey viscosity problem using three different solving approaches."""
    
    # Expected values (from reference calculation)
    expected = {
        "mu": 2.09,  # lb_f*s/ft^2
        "rho": 88.4,  # lb/ft^3
        "nu": 0.76,  # ft^2/s
    }
    
    # Target units for conversion
    target_units = {
        "mu": "lb_f_s_ft_2",
        "rho": "lb_cu_ft",
        "nu": "mathrm_ft_2_mathrm_s",
    }
    
    # Solve using the specified method
    variables = _solve_problem_1(solving_method)
    
    # Convert to target units and assert
    actuals = {}
    for name, var in variables.items():
        actuals[name] = var.to_unit(target_units[name])
        assert pytest.approx(actuals[name].value, 0.01) == expected[name]
    
    with capsys.disabled():
        print(f"\n{solving_method} method results:")
        for name in ["mu", "rho", "nu"]:
            print(f"  {actuals[name]}")


@pytest.mark.parametrize("solving_method", [
    "solve_from",
    "equation",
    "problem_class"
])
def test_problem_2(solving_method, capsys):
    """Test pipe flow problem using three different solving approaches."""
    
    # Expected values (from reference calculation)
    expected = {
        "D_1": 1.049,  # inch
        "D_1_5": 1.610,  # inch
        "D_2_5": 2.469,  # inch
        "V_1": 9.17,  # ft/s
        "V_1_5": 4.0,  # ft/s
        "V_2_5": 3.35,  # ft/s
        "Q_1": 3.29,  # ft^3/min
        "Q_1_5": 3.39,  # ft^3/min
        "Q_2_5": 6.68,  # ft^3/min
        "A_1": 0.005999,  # ft^2
        "A_1_5": 0.01413,  # ft^2
        "A_2_5": 0.03323,  # ft^2
    }
    
    # Target units for conversion
    target_units = {
        "D_1": "inch",
        "D_1_5": "inch",
        "D_2_5": "inch",
        "V_1": "ft_s",
        "V_1_5": "ft_s",
        "V_2_5": "ft_s",
        "Q_1": "ft_3_min",
        "Q_1_5": "ft_3_min",
        "Q_2_5": "ft_3_min",
        "A_1": "ft_2",
        "A_1_5": "ft_2",
        "A_2_5": "ft_2",
    }
    
    # Solve using the specified method
    variables = _solve_problem_2(solving_method)
    
    # Convert to target units and assert
    actuals = {}
    for name, var in variables.items():
        actuals[name] = var.to_unit(target_units[name])
        assert pytest.approx(actuals[name].value, 0.01) == expected[name]

    with capsys.disabled():
        print(f"\n{solving_method} method results:")
        for name in ["D_1", "D_1_5", "D_2_5", "V_1", "V_1_5", "V_2_5", "Q_1", "Q_1_5", "Q_2_5", "A_1", "A_1_5", "A_2_5"]:
            print(f"  {actuals[name]}")

