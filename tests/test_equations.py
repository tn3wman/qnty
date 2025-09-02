"""Tests for the qnty equation system."""

import pytest

from src.qnty.equation import Equation
from src.qnty.expression import BinaryOperation, Expression, VariableReference
from src.qnty.variable import TypeSafeVariable
from src.qnty.variables import Dimensionless, Length, Pressure


class TestEquationCreation:
    """Test equation creation using the fluent API."""
    
    def test_basic_equation_creation(self):
        """Test creating equations using the .equals() method."""
        T = Length("Wall Thickness", is_known=False)
        T_bar = Length(0.147, "inch", "Nominal Wall Thickness")
        U_m = Dimensionless(0.125, "Mill Undertolerance")
        
        # Create equation: T = T_bar * (1 - U_m)
        T_eqn = T.equals(T_bar * (1 - U_m))
        
        assert isinstance(T_eqn, Equation)
        assert T_eqn.name == "Wall Thickness_eq"
        assert isinstance(T_eqn.lhs, VariableReference)
        assert T_eqn.lhs.name == "Wall Thickness"
        assert isinstance(T_eqn.rhs, BinaryOperation)
    
    def test_equation_variable_collection(self):
        """Test that equations correctly identify all variables."""
        P = Pressure(90, "psi", "Design Pressure")
        D = Length(0.84, "inch", "Outside Diameter")
        S = Pressure(20000, "psi", "Allowable Stress")
        E = Dimensionless(0.8, "Quality Factor")
        W = Dimensionless(1, "Weld Joint Strength Reduction Factor")
        Y = Dimensionless(0.4, "Y Coefficient")
        
        # Create equation: t = (P * D) / (2 * (S * E * W + P * Y))
        t = Length("Pressure Design Thickness", is_known=False)
        t_eqn = t.equals((P * D) / (2 * (S * E * W + P * Y)))
        
        expected_vars = {"Pressure Design Thickness", "Design Pressure", "Outside Diameter",
                        "Allowable Stress", "Quality Factor", "Weld Joint Strength Reduction Factor",
                        "Y Coefficient"}
        assert t_eqn.get_all_variables() == expected_vars
    
    def test_equation_string_representation(self):
        """Test string representation of equations."""
        T = Length("T", is_known=False)
        T_bar = Length(0.147, "inch", "T_bar")
        
        eqn = T.equals(T_bar * 0.875)
        eqn_str = str(eqn)
        
        assert "T" in eqn_str
        assert "=" in eqn_str
        assert "T_bar" in eqn_str


class TestArithmeticOperations:
    """Test arithmetic operations between variables."""
    
    def test_variable_addition(self):
        """Test addition between variables creates expressions."""
        a = Length(5, "meter", "Length A")
        b = Length(3, "meter", "Length B")
        
        result = a + b
        assert isinstance(result, Expression)
        
        # Test that the expression can be used in equations
        c = Length("Length C", is_known=False)
        eqn = c.equals(a + b)
        assert isinstance(eqn, Equation)
    
    def test_variable_multiplication(self):
        """Test multiplication between variables."""
        width = Length(10, "meter", "Width")
        height = Length(5, "meter", "Height")
        
        result = width * height
        assert isinstance(result, Expression)
        
        # Use in equation
        area = Length("Area", is_known=False)  # This should be Area type, but Length works for test
        eqn = area.equals(width * height)
        assert isinstance(eqn, Equation)
    
    def test_complex_expression(self):
        """Test complex arithmetic expressions."""
        P = Pressure(90, "psi", "P")
        D = Length(0.84, "inch", "D")
        S = Pressure(20000, "psi", "S")
        E = Dimensionless(0.8, "E")
        
        # Complex expression: (P * D) / (2 * S * E)
        expr = (P * D) / (2 * S * E)
        assert isinstance(expr, Expression)
        
        # Use in equation
        t = Length("t", is_known=False)
        eqn = t.equals(expr)
        assert isinstance(eqn, Equation)
        assert len(eqn.get_all_variables()) == 5  # P, D, S, E, t
    
    def test_arithmetic_with_constants(self):
        """Test arithmetic operations with numeric constants."""
        var = Pressure(100, "psi", "Test")
        
        # Test with numbers
        expr1 = var * 2
        expr2 = var + 50
        expr3 = var / 2.5
        expr4 = var - 25
        
        assert all(isinstance(expr, Expression) for expr in [expr1, expr2, expr3, expr4])
    
    def test_reverse_operations(self):
        """Test reverse arithmetic operations."""
        var = Pressure(100, "psi", "Test")
        
        # Test reverse operations
        expr1 = 2 * var
        expr2 = 150 - var
        expr3 = 200 / var
        
        assert all(isinstance(expr, Expression) for expr in [expr1, expr2, expr3])


class TestEquationSolving:
    """Test equation solving capabilities."""
    
    def test_simple_equation_solving(self):
        """Test solving simple direct assignment equations."""
        # Known variables
        T_bar = Length(0.147, "inch", "T_bar")
        U_m = Dimensionless(0.125, "U_m")
        
        # Unknown variable
        T = Length("T", is_known=False)
        
        # Create equation: T = T_bar * (1 - U_m)
        T_eqn = T.equals(T_bar * (1 - U_m))
        
        # Create variable dictionary
        variables = {"T_bar": T_bar, "U_m": U_m, "T": T}
        
        # Check if we can solve for T
        known_vars = {"T_bar", "U_m"}
        assert T_eqn.can_solve_for("T", known_vars)
        
        # Solve for T
        result = T_eqn.solve_for("T", variables)
        assert result is T  # Should return the same variable object
        assert T.is_known is True  # Should be marked as known
        assert T.quantity is not None  # Should have a value
        
        # Verify the calculation - result will be in the unit system's base unit
        expected_value = 0.147 * (1 - 0.125)  # 0.147 * 0.875 = 0.128625
        # Convert to expected unit for comparison
        if T.quantity.unit.name == "millimeter":
            # Convert inch to millimeters: 0.128625 inch * 25.4 mm/inch = 3.267075 mm
            expected_value_mm = expected_value * 25.4
            assert abs(T.quantity.value - expected_value_mm) < 1e-6
        else:
            assert abs(T.quantity.value - expected_value) < 1e-6
    
    def test_equation_residual_check(self):
        """Test checking if equations are satisfied."""
        # Set up variables with known values
        a = Length(5, "meter", "a")
        b = Length(3, "meter", "b")
        c = Length(8, "meter", "c")  # 5 + 3 = 8
        
        # Create equation: c = a + b
        eqn = c.equals(a + b)
        
        variables: dict[str, TypeSafeVariable] = {"a": a, "b": b, "c": c}
        
        # Should be satisfied
        assert eqn.check_residual(variables) is True
        
        # Change c to wrong value
        assert c.quantity is not None
        c.quantity.value = 9  # Wrong value
        assert eqn.check_residual(variables) is False
    
    def test_unknown_variable_detection(self):
        """Test detection of unknown variables in equations."""
        P = Pressure(90, "psi", "P")  # Known
        D = Length(0.84, "inch", "D")  # Known
        t = Length("t", is_known=False)  # Unknown
        S = Pressure("S", is_known=False)  # Unknown
        
        eqn = t.equals(P * D / (2 * S))
        
        known_vars = {"P", "D"}
        unknown_vars = eqn.get_unknown_variables(known_vars)
        
        assert unknown_vars == {"t", "S"}
        assert eqn.get_known_variables(known_vars) == {"P", "D"}


class TestExpressionEvaluation:
    """Test expression evaluation with variables."""
    
    def test_expression_evaluation(self):
        """Test evaluating expressions with variable values."""
        # Create variables without initial quantities to force expression creation
        a = Length("a", is_known=False)
        b = Length("b", is_known=False)
        
        # Create expression before setting values
        from qnty.expression import Expression
        expr: Expression = a + b
        
        # Now set values for the variables that will be used in evaluation
        a_eval = Length(5, "meter", "a")
        b_eval = Length(3, "meter", "b")
        variables: dict[str, TypeSafeVariable] = {"a": a_eval, "b": b_eval}
        
        result = expr.evaluate(variables)
        assert result.value == 8.0  # 5 + 3
        assert result.unit.name == "meter"  # Should preserve units
    
    def test_complex_expression_evaluation(self):
        """Test evaluating complex expressions."""
        # Create variables without initial quantities to force expression creation
        P = Pressure("P", is_known=False)
        D = Length("D", is_known=False)
        
        # Create expression before setting values
        from qnty.expression import Expression
        expr: Expression = P * D * 2  # 90 * 1 * 2 = 180
        
        # Set values for the variables that will be used in evaluation
        P_eval = Pressure(90, "psi", "P")
        D_eval = Length(1, "inch", "D")  # Simplified for easier math
        variables: dict[str, TypeSafeVariable] = {"P": P_eval, "D": D_eval}
        
        result = expr.evaluate(variables)
        # Result will be in some combined unit, just check it evaluates
        assert result.value > 0
    
    def test_expression_with_constants(self):
        """Test expressions containing constants."""
        # Create variable without initial quantity to force expression creation
        var = Pressure("var", is_known=False)
        
        # Create expression before setting values
        from qnty.expression import Expression
        expr: Expression = var * 2  # 100 * 2 = 200
        
        # Set value for the variable that will be used in evaluation
        var_eval = Pressure(100, "psi", "var")
        variables: dict[str, TypeSafeVariable] = {"var": var_eval}
        
        result = expr.evaluate(variables)
        # The actual value depends on unit conversions, but should be computable
        assert result.value > 0
        # Should be roughly double the original value
        original_pascals = 100 * 6894.757  # psi to pascals
        expected_result = original_pascals * 2
        assert abs(result.value - expected_result) < 10  # Allow some tolerance for floating point precision


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_equation_with_unknown_variables(self):
        """Test equations cannot solve when too many unknowns."""
        x = Length("x", is_known=False)
        y = Length("y", is_known=False)
        
        eqn = x.equals(y + 5)
        
        # Cannot solve for x when y is also unknown
        known_vars = set()  # No known variables
        assert not eqn.can_solve_for("x", known_vars)
    
    def test_invalid_solve_target(self):
        """Test error when trying to solve for non-existent variable."""
        a = Length(5, "meter", "a")
        b = Length("b", is_known=False)
        
        eqn = b.equals(a * 2)
        variables: dict[str, TypeSafeVariable] = {"a": a, "b": b}
        
        with pytest.raises(ValueError, match="Variable 'nonexistent' not found"):
            eqn.solve_for("nonexistent", variables)
    
    def test_expression_string_representation(self):
        """Test string representations of expressions."""
        a = Length(5, "meter", "a")
        b = Length(3, "meter", "b")
        
        expr = a + b
        expr_str = str(expr)
        
        assert "a" in expr_str
        assert "b" in expr_str
        assert "+" in expr_str
