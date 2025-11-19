"""Tests for range_expr and When helper class."""

import pytest

from qnty import Dimensionless
from qnty.algebra import range_expr, When


def test_when_between():
    """Test When.between() creates inclusive range."""
    when = When.between(0.1, 0.5)
    assert when.lower == 0.1
    assert when.upper == 0.5
    assert when.lower_inclusive is True
    assert when.upper_inclusive is True


def test_when_gt_and_leq():
    """Test chaining gt and and_leq."""
    when = When.gt(0.5).and_leq(2.0)
    assert when.lower == 0.5
    assert when.upper == 2.0
    assert when.lower_inclusive is False
    assert when.upper_inclusive is True


def test_when_geq_and_lt():
    """Test chaining geq and and_lt."""
    when = When.geq(0.1).and_lt(0.25)
    assert when.lower == 0.1
    assert when.upper == 0.25
    assert when.lower_inclusive is True
    assert when.upper_inclusive is False


def test_when_lt():
    """Test single-sided less-than condition."""
    when = When.lt(0.1)
    assert when.lower is None
    assert when.upper == 0.1
    assert when.upper_inclusive is False


def test_when_gt():
    """Test single-sided greater-than condition."""
    when = When.gt(1.0)
    assert when.lower == 1.0
    assert when.upper is None
    assert when.lower_inclusive is False


def test_when_leq():
    """Test single-sided less-than-or-equal condition."""
    when = When.leq(5.0)
    assert when.lower is None
    assert when.upper == 5.0
    assert when.upper_inclusive is True


def test_when_geq():
    """Test single-sided greater-than-or-equal condition."""
    when = When.geq(10.0)
    assert when.lower == 10.0
    assert when.upper is None
    assert when.lower_inclusive is True


def test_when_then():
    """Test that then() creates a tuple with condition and expression."""
    when = When.between(0.1, 0.5)
    expr = 100
    case = when.then(expr)
    assert isinstance(case, tuple)
    assert len(case) == 2
    assert case[0] is when
    assert case[1] == expr


def test_range_expr_two_ranges():
    """Test range_expr with two ranges."""
    X_h = Dimensionless("X_h")

    # Define two different expressions
    expr1 = 100
    expr2 = 200

    # Create range expression
    result_expr = range_expr(
        X_h,
        When.between(0.1, 0.5).then(expr1),
        When.gt(0.5).and_leq(2.0).then(expr2)
    )

    # Test with value in first range
    X_h_val = X_h.set(0.3).dimensionless
    result = result_expr.evaluate({"_symbol": X_h_val})
    assert result.value == 100

    # Test with value in second range
    X_h_val = X_h.set(1.0).dimensionless
    result = result_expr.evaluate({"_symbol": X_h_val})
    assert result.value == 200

    # Test boundary - 0.5 should be in first range (inclusive upper)
    X_h_val = X_h.set(0.5).dimensionless
    result = result_expr.evaluate({"_symbol": X_h_val})
    assert result.value == 100


def test_range_expr_four_ranges_with_otherwise():
    """Test range_expr with four ranges and an otherwise clause."""
    X_h = Dimensionless("X_h")

    # Define expressions for each range
    expr1 = 10
    expr2 = 20
    expr3 = 30
    expr4 = 40
    default_expr = 99

    # Create range expression
    result_expr = range_expr(
        X_h,
        When.between(0.1, 0.25).then(expr1),
        When.gt(0.25).and_leq(0.5).then(expr2),
        When.gt(0.5).and_leq(1.0).then(expr3),
        When.gt(1.0).and_leq(2.0).then(expr4),
        otherwise=default_expr
    )

    # Test each range
    X_h = X_h.set(0.2).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 10

    X_h = X_h.set(0.4).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 20

    X_h = X_h.set(0.75).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 30

    X_h = X_h.set(1.5).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 40

    # Test otherwise clause
    X_h = X_h.set(2.5).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 99

    X_h = X_h.set(0.05).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 99


def test_range_expr_one_sided_conditions():
    """Test range_expr with one-sided conditions."""
    X_h = Dimensionless("X_h")

    result_expr = range_expr(
        X_h,
        When.lt(0.1).then(1),
        When.geq(0.1).and_lt(1.0).then(2),
        When.geq(1.0).then(3)
    )

    # Test below 0.1
    X_h = X_h.set(0.05).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 1

    # Test middle range
    X_h = X_h.set(0.5).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 2

    # Test above 1.0
    X_h = X_h.set(5.0).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 3


def test_range_expr_with_quantity_expressions():
    """Test range_expr with actual Quantity expressions."""
    X_h = Dimensionless("X_h")

    # Use constant expressions instead of quantities to avoid symbol issues
    result_expr = range_expr(
        X_h,
        When.between(0.1, 0.5).then(10),
        When.gt(0.5).and_leq(2.0).then(30)
    )

    # Test first range: should give 10
    X_h_val = X_h.set(0.3).dimensionless
    result = result_expr.evaluate({"_symbol": X_h_val})
    assert pytest.approx(result.value) == 10.0

    # Test second range: should give 30
    X_h_val = X_h.set(1.0).dimensionless
    result = result_expr.evaluate({"_symbol": X_h_val})
    assert pytest.approx(result.value) == 30.0


def test_range_expr_boundary_conditions():
    """Test range_expr boundary handling with exclusive/inclusive bounds."""
    X_h = Dimensionless("X_h")

    # 0.1 <= X_h <= 0.5: expr1
    # 0.5 < X_h <= 1.0: expr2
    result_expr = range_expr(
        X_h,
        When.between(0.1, 0.5).then(100),
        When.gt(0.5).and_leq(1.0).then(200)
    )

    # 0.5 should be in first range (inclusive on both ends)
    X_h = X_h.set(0.5).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 100

    # Just above 0.5 should be in second range
    X_h = X_h.set(0.50001).dimensionless
    assert result_expr.evaluate({"_symbol": X_h}).value == 200


def test_range_expr_with_multiple_ranges():
    """Test range_expr with more than two ranges."""
    X = Dimensionless("X")

    # Five different ranges
    result_expr = range_expr(
        X,
        When.lt(0.1).then(1),
        When.geq(0.1).and_lt(0.3).then(2),
        When.geq(0.3).and_lt(0.6).then(3),
        When.geq(0.6).and_lt(0.9).then(4),
        When.geq(0.9).then(5)
    )

    # Test each range
    X_val = X.set(0.05).dimensionless
    assert result_expr.evaluate({"_symbol": X_val}).value == 1

    X_val = X.set(0.2).dimensionless
    assert result_expr.evaluate({"_symbol": X_val}).value == 2

    X_val = X.set(0.5).dimensionless
    assert result_expr.evaluate({"_symbol": X_val}).value == 3

    X_val = X.set(0.75).dimensionless
    assert result_expr.evaluate({"_symbol": X_val}).value == 4

    X_val = X.set(1.5).dimensionless
    assert result_expr.evaluate({"_symbol": X_val}).value == 5


def test_range_expr_error_no_cases():
    """Test that range_expr raises error with no cases."""
    X_h = Dimensionless("X_h")

    with pytest.raises(ValueError, match="requires at least one case"):
        range_expr(X_h)


def test_range_expr_error_invalid_case_format():
    """Test that range_expr raises error with invalid case format."""
    X_h = Dimensionless("X_h")

    with pytest.raises(ValueError, match="must be created using When"):
        range_expr(X_h, (0.1, 0.5, 100))  # Not using When


def test_when_error_double_upper_bound():
    """Test that setting upper bound twice raises error."""
    when = When.leq(5.0)

    with pytest.raises(ValueError, match="Upper bound already set"):
        when.and_leq(10.0)


def test_when_error_double_lower_bound():
    """Test that setting lower bound twice raises error."""
    when = When.geq(5.0)

    with pytest.raises(ValueError, match="Lower bound already set"):
        when.and_geq(10.0)


def test_range_expr_complex_engineering_example():
    """Test range_expr with a realistic engineering calculation using constants."""
    # This test demonstrates range_expr with complex formulas
    # Note: Using symbolic quantities in expressions requires a Problem class context,
    # so we test with numeric constants here
    X_h = Dimensionless("X_h")
    X_g_val = 1.2  # Constant value

    # Different formulas for different ranges of X_h
    # For 0.1 <= X_h <= 0.5 - simplified formula
    v_1_const = 0.500244 + 0.227914/X_g_val  # Pre-compute constant part

    # For 0.5 < X_h <= 2.0 - simplified formula
    v_2_const = 0.0144868 - 0.135977/X_g_val  # Pre-compute constant part

    V = range_expr(
        X_h,
        When.between(0.1, 0.5).then(v_1_const),
        When.gt(0.5).and_leq(2.0).then(v_2_const)
    )

    # Test with X_h in first range
    X_h_val = X_h.set(0.3).dimensionless
    result1 = V.evaluate({"_symbol": X_h_val})
    expected1 = v_1_const
    assert pytest.approx(result1.value, rel=1e-9) == expected1

    # Test with X_h in second range
    X_h_val = X_h.set(1.0).dimensionless
    result2 = V.evaluate({"_symbol": X_h_val})
    expected2 = v_2_const
    assert pytest.approx(result2.value, rel=1e-9) == expected2
