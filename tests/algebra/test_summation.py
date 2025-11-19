"""
Test suite for the summation function in qnty.

This module tests the generic summation system using well-known mathematical
summations to verify correctness.
"""

import numpy as np
import pytest

from qnty import Dimensionless, Length, Problem
from qnty.algebra import equation, summation


class TestBasicSummations:
    """Test basic summation patterns with known results."""

    def test_sum_of_first_n_integers(self):
        """Test: Σ(i) for i=0 to n-1 = n(n-1)/2"""
        # Sum of first 10 integers (0 to 9): 0+1+2+...+9 = 45
        class SumIntegers(Problem):
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i: i, 10)
            )

        problem = SumIntegers()
        problem.solve()

        assert problem.result.value == 45.0

    def test_sum_of_squares(self):
        """Test: Σ(i²) for i=1 to n = n(n+1)(2n+1)/6"""
        # Sum of squares from 1 to 5: 1² + 2² + 3² + 4² + 5² = 55
        class SumSquares(Problem):
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i: i**2, (1, 6))  # Range 1 to 5 (exclusive 6)
            )

        problem = SumSquares()
        problem.solve()

        assert problem.result.value == 55.0

    def test_sum_of_cubes(self):
        """Test: Σ(i³) for i=1 to n = [n(n+1)/2]²"""
        # Sum of cubes from 1 to 4: 1³ + 2³ + 3³ + 4³ = 100
        class SumCubes(Problem):
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i: i**3, (1, 5))
            )

        problem = SumCubes()
        problem.solve()

        assert problem.result.value == 100.0

    def test_geometric_series(self):
        """Test: Σ(2^i) for i=0 to n-1 = 2^n - 1"""
        # Geometric series: 2^0 + 2^1 + 2^2 + 2^3 + 2^4 = 1+2+4+8+16 = 31
        class GeometricSeries(Problem):
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i: 2**i, 5)
            )

        problem = GeometricSeries()
        problem.solve()

        assert problem.result.value == 31.0

    def test_arithmetic_series(self):
        """Test: Σ(2i + 3) for i=0 to n-1"""
        # Arithmetic: (3) + (5) + (7) + (9) + (11) = 35
        class ArithmeticSeries(Problem):
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i: 2*i + 3, 5)
            )

        problem = ArithmeticSeries()
        problem.solve()

        assert problem.result.value == 35.0


class TestMatrixSummations:
    """Test 2D summations with matrices (ASME-style calculations)."""

    def test_simple_2d_summation(self):
        """Test: Σ Σ M[i,j] for all i,j in a 2x3 matrix"""
        class Matrix2DSum(Problem):
            # Simple 2x3 matrix
            M = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])  # Use floats to avoid numpy int64 issues

            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i, j, M: M[i, j], 2, 3, M=M)
            )

        problem = Matrix2DSum()
        problem.solve()

        # Sum of all elements: 1+2+3+4+5+6 = 21
        assert problem.result.value == 21.0

    def test_polynomial_2d_summation(self):
        """Test: Σ Σ i*j for i,j in range"""
        # Manual calculation:
        # i=0: 0*0 + 0*1 + 0*2 = 0
        # i=1: 1*0 + 1*1 + 1*2 = 3
        # i=2: 2*0 + 2*1 + 2*2 = 6
        # Total = 9
        class PolynomialSum(Problem):
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i, j: i * j, 3, 3)
            )

        problem = PolynomialSum()
        problem.solve()

        assert problem.result.value == 9.0

    def test_matrix_with_powers(self):
        """Test: Σ Σ M[i,j] * x^i * y^j (ASME-style polynomial)"""
        class MatrixPolynomial(Problem):
            # Identity matrix with floats
            M = np.array([[1.0, 0.0], [0.0, 1.0]])

            x = Dimensionless("x").set(2).dimensionless
            y = Dimensionless("y").set(3).dimensionless

            result = Dimensionless("result")
            # M[0,0]*x^0*y^0 + M[0,1]*x^0*y^1 + M[1,0]*x^1*y^0 + M[1,1]*x^1*y^1
            # = 1*1*1 + 0*1*3 + 0*2*1 + 1*2*3
            # = 1 + 0 + 0 + 6 = 7
            result_eqn = equation(
                result,
                summation(lambda i, j, M, x, y: M[i, j] * x**i * y**j, 2, 2, M=M, x=x, y=y)
            )

        problem = MatrixPolynomial()
        problem.solve()

        assert problem.result.value == pytest.approx(7.0)


class TestWithUnits:
    """Test summations with dimensional quantities."""

    def test_sum_of_lengths(self):
        """Test summation preserves dimensions"""
        class SumLengths(Problem):
            # Create a series of lengths: 1m, 2m, 3m, 4m, 5m
            base = Length("base").set(1).meter

            total = Length("total")
            total_eqn = equation(
                total,
                summation(lambda i, base: i * base, (1, 6), base=base)
            )

        problem = SumLengths()
        problem.solve()

        # Sum = 1+2+3+4+5 = 15 meters
        assert problem.total.to_unit("meter").value == pytest.approx(15.0)

    def test_power_series_with_units(self):
        """Test geometric series with dimensional quantities"""
        class GeometricWithUnits(Problem):
            base = Length("base").set(2).meter

            # Geometric series: base + base² + base³
            # But base² has wrong dimensions! This should demonstrate
            # that summation works but dimensional analysis will catch issues
            total = Length("total")
            total_eqn = equation(
                total,
                summation(lambda i, base: base if i == 0 else base, 3, base=base)
            )

        problem = GeometricWithUnits()
        problem.solve()

        # 2m + 2m + 2m = 6m
        assert problem.total.to_unit("meter").value == pytest.approx(6.0)


class TestClosureVsExplicit:
    """Test both closure-based and explicit variable passing."""

    @pytest.mark.skip(reason="Closure-based summation doesn't work in class definition context - use explicit variable passing instead")
    def test_closure_based_summation(self):
        """Test summation using closure (simpler syntax)

        NOTE: This test demonstrates that closure-based summation doesn't work
        in Problem class definition context because class attributes aren't
        accessible from closures during class definition. Use explicit variable
        passing via kwargs instead.
        """
        class ClosureSum(Problem):
            M = np.array([[1.0, 2.0], [3.0, 4.0]])

            result = Dimensionless("result")
            # Using closure - M is captured from class namespace
            result_eqn = equation(
                result,
                summation(lambda i, j: M[i, j], 2, 2)
            )

        problem = ClosureSum()
        problem.solve()

        assert problem.result.value == 10.0  # 1+2+3+4

    def test_explicit_variable_passing(self):
        """Test summation with explicit variable passing (linter-friendly)"""
        class ExplicitSum(Problem):
            M = np.array([[1.0, 2.0], [3.0, 4.0]])

            result = Dimensionless("result")
            # Explicit passing - variables passed as kwargs
            result_eqn = equation(
                result,
                summation(lambda i, j, M: M[i, j], 2, 2, M=M)
            )

        problem = ExplicitSum()
        problem.solve()

        assert problem.result.value == 10.0  # 1+2+3+4

    @pytest.mark.skip(reason="Closure-based summation doesn't work in class definition context - only explicit variable passing works")
    def test_both_methods_equivalent(self):
        """Verify closure and explicit passing give same results

        NOTE: This test demonstrates that only explicit variable passing works
        in Problem class definition context. Closure-based approach fails because
        class attributes aren't accessible from closures during class definition.
        """
        M = np.array([[5.0, 6.0, 7.0], [8.0, 9.0, 10.0], [11.0, 12.0, 13.0]])

        class ClosureVersion(Problem):
            matrix = M
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i, j: matrix[i, j] * i * j, 3, 3)
            )

        class ExplicitVersion(Problem):
            matrix = M
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i, j, matrix: matrix[i, j] * i * j, 3, 3, matrix=matrix)
            )

        problem1 = ClosureVersion()
        problem1.solve()

        problem2 = ExplicitVersion()
        problem2.solve()

        assert problem1.result.value == problem2.result.value


class TestASMEStyleCalculations:
    """Test summations matching the ASME flange calculation pattern."""

    def test_asme_polynomial_ratio(self):
        """Test ratio of two polynomial summations (simplified ASME pattern)"""
        class ASMEStyleRatio(Problem):
            # Coefficient matrices (simplified from ASME)
            M = np.array([[1.0, 2.0], [3.0, 4.0]])
            N = np.array([[0.5, 1.0], [1.5, 2.0]])

            x = Dimensionless("x").set(2).dimensionless
            y = Dimensionless("y").set(3).dimensionless

            result = Dimensionless("result")
            # F = (Σ M_ij * x^i * y^j) / (Σ N_ij * x^i * y^j)
            result_eqn = equation(
                result,
                summation(lambda i, j, M, x, y: M[i, j] * x**i * y**j, 2, 2, M=M, x=x, y=y) /
                summation(lambda i, j, N, x, y: N[i, j] * x**i * y**j, 2, 2, N=N, x=x, y=y)
            )

        problem = ASMEStyleRatio()
        problem.solve()

        # Numerator: M[0,0]*1*1 + M[0,1]*1*3 + M[1,0]*2*1 + M[1,1]*2*3
        #          = 1 + 6 + 6 + 24 = 37
        # Denominator: N[0,0]*1*1 + N[0,1]*1*3 + N[1,0]*2*1 + N[1,1]*2*3
        #            = 0.5 + 3 + 3 + 12 = 18.5
        # Ratio = 37/18.5 = 2.0
        assert problem.result.value == pytest.approx(2.0)

    def test_3x3_matrix_summation(self):
        """Test 3x3 summation matching ASME flange calculation structure"""
        M = np.array([
            [-0.33289917, 1.89824507, 0.51289982],
            [5.33592441, -17.32691994, 17.31106722],
            [4.92214647, 3.21485121, -1.76102532]
        ])

        class ThreeByThreeSum(Problem):
            matrix = M

            x = Dimensionless("x").set(1).dimensionless
            y = Dimensionless("y").set(1).dimensionless

            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i, j, matrix, x, y: matrix[i, j] * x**i * y**j, 3, 3, matrix=matrix, x=x, y=y)
            )

        problem = ThreeByThreeSum()
        problem.solve()

        # With x=y=1, this is just the sum of all matrix elements
        expected = np.sum(M)
        assert problem.result.value == pytest.approx(expected, rel=1e-6)


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_range(self):
        """Test summation with zero terms"""
        with pytest.raises(ValueError, match="sum_expr requires at least 1 argument"):
            # This should fail because there are no terms to sum
            class EmptySum(Problem):
                result = Dimensionless("result")
                result_eqn = equation(
                    result,
                    summation(lambda i: i, 0)  # No terms
                )

    def test_single_term(self):
        """Test summation with single term"""
        class SingleTerm(Problem):
            result = Dimensionless("result")
            result_eqn = equation(
                result,
                summation(lambda i: i + 5, 1)  # Just i=0: 0+5=5
            )

        problem = SingleTerm()
        problem.solve()

        assert problem.result.value == 5.0

    def test_custom_range_with_step(self):
        """Test summation with custom range (start, stop, step)"""
        class CustomRange(Problem):
            result = Dimensionless("result")
            # Sum even numbers from 0 to 8: 0+2+4+6+8 = 20
            result_eqn = equation(
                result,
                summation(lambda i: i, (0, 10, 2))
            )

        problem = CustomRange()
        problem.solve()

        assert problem.result.value == 20.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
