import pytest

import qnty as qt


def test_problem_1(capsys):
    mu = qt.ViscosityDynamic("Honey_viscosity").set(1000).poise
    rho = qt.MassDensity("Honey_density").set(0.05).oz_mL
    nu = qt.ViscosityKinematic("Honey_kinematic_viscosity")
    
    nu.solve_from(mu/rho)

    mu_actual = mu.to_unit("lb_f_s_ft_2")
    rho_actual = rho.to_unit("lb_cu_ft")
    nu_actual = nu.to_unit("mathrm_ft_2_mathrm_s")

    mu_expected = 2.09  # lb_f*s/ft^2
    rho_expected = 88.4  # lb/ft^3
    nu_expected = 0.76  # ft^2/s

    assert pytest.approx(mu_actual.value, 0.01) == mu_expected
    assert pytest.approx(rho_actual.value, 0.01) == rho_expected
    assert pytest.approx(nu_actual.value, 0.01) == nu_expected
    # assert mu_expected == pytest.approx(mu_actual.value, 0.01)
    # assert rho_expected == pytest.approx(rho_actual.value, 0.01)
    # assert nu_expected == pytest.approx(nu_actual.value, 0.01)

    with capsys.disabled():
        print(mu_actual)
        print(rho_actual)
        print(nu_actual)

def test_problem_1_eqn(capsys):
    mu = qt.ViscosityDynamic("Honey_viscosity").set(1000).poise
    rho = qt.MassDensity("Honey_density").set(0.05).oz_mL
    nu = qt.ViscosityKinematic("Honey_kinematic_viscosity")
    
    nu_eqn = nu.equals(mu/rho)

    mu_actual = mu.to_unit("lb_f_s_ft_2")
    rho_actual = rho.to_unit("lb_cu_ft")
    nu_actual = nu.solve().to_unit("mathrm_ft_2_mathrm_s")

    mu_expected = 2.09  # lb_f*s/ft^2
    rho_expected = 88.4  # lb/ft^3
    nu_expected = 0.76  # ft^2/s

    assert pytest.approx(mu_actual.value, 0.01) == mu_expected
    assert pytest.approx(rho_actual.value, 0.01) == rho_expected
    assert pytest.approx(nu_actual.value, 0.01) == nu_expected

    with capsys.disabled():
        print(mu_actual)
        print(rho_actual)
        print(nu_actual)





