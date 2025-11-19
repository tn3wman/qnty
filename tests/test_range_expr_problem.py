"""Test range_expr integration with Problem class."""

import pytest

from qnty import Dimensionless
from qnty.algebra import When, equation, range_expr
from qnty.problems import Problem


class RangeExprProblem(Problem):
    """Test problem using range_expr in Problem class context."""

    X_h = Dimensionless("X_h").set(0.3).dimensionless  # Default value, will be overridden
    V = Dimensionless("V")

    # V depends on X_h ranges
    V_eqn = equation(
        V,
        range_expr(
            X_h,
            When.between(0.1, 0.5).then(100),
            When.gt(0.5).and_leq(2.0).then(200),
            otherwise=999
        )
    )


def test_range_expr_in_problem_class_first_range():
    """Test range_expr in Problem class with value in first range."""
    problem = RangeExprProblem()
    problem.X_h.set(0.3).dimensionless
    problem.solve()

    assert problem.V.value == pytest.approx(100)


def test_range_expr_in_problem_class_second_range():
    """Test range_expr in Problem class with value in second range."""
    problem = RangeExprProblem()
    problem.X_h.set(1.0).dimensionless
    problem.solve()

    assert problem.V.value == pytest.approx(200)


def test_range_expr_in_problem_class_boundary():
    """Test range_expr in Problem class at boundary."""
    problem = RangeExprProblem()
    problem.X_h.set(0.5).dimensionless
    problem.solve()

    # 0.5 should be in first range (inclusive upper bound)
    assert problem.V.value == pytest.approx(100)


def test_range_expr_in_problem_class_otherwise():
    """Test range_expr in Problem class with value triggering otherwise."""
    problem = RangeExprProblem()
    problem.X_h.set(2.5).dimensionless
    problem.solve()

    assert problem.V.value == pytest.approx(999)


class MultiRangeExprProblem(Problem):
    """Test problem using range_expr with 4 ranges."""

    X = Dimensionless("X").set(0.2).dimensionless  # Default value, will be overridden
    Result = Dimensionless("Result")

    # Result depends on X ranges
    Result_eqn = equation(
        Result,
        range_expr(
            X,
            When.between(0.1, 0.25).then(10),
            When.gt(0.25).and_leq(0.5).then(20),
            When.gt(0.5).and_leq(1.0).then(30),
            When.gt(1.0).and_leq(2.0).then(40),
            otherwise=0
        )
    )


def test_multi_range_expr_in_problem_class():
    """Test range_expr with multiple ranges in Problem class."""
    # Test first range
    problem = MultiRangeExprProblem()
    problem.X.set(0.2).dimensionless
    problem.solve()
    assert problem.Result.value == pytest.approx(10)

    # Test second range
    problem = MultiRangeExprProblem()
    problem.X.set(0.4).dimensionless
    problem.solve()
    assert problem.Result.value == pytest.approx(20)

    # Test third range
    problem = MultiRangeExprProblem()
    problem.X.set(0.75).dimensionless
    problem.solve()
    assert problem.Result.value == pytest.approx(30)

    # Test fourth range
    problem = MultiRangeExprProblem()
    problem.X.set(1.5).dimensionless
    problem.solve()
    assert problem.Result.value == pytest.approx(40)

    # Test otherwise
    problem = MultiRangeExprProblem()
    problem.X.set(2.5).dimensionless
    problem.solve()
    assert problem.Result.value == pytest.approx(0)
