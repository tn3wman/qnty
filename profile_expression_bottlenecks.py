#!/usr/bin/env python3
"""
Detailed Expression System Performance Analysis

This script profiles the expression path to identify specific bottlenecks
in BinaryOperation creation, wrap_operand calls, and type checking.
"""

import cProfile
import pstats
import time
from io import StringIO
from typing import List, Dict, Any

from src.qnty import Length, Pressure, Area, Force, Volume, Mass, Temperature
from src.qnty.units.field_units import LengthUnits, PressureUnits
from src.qnty.expressions.nodes import BinaryOperation, wrap_operand
from src.qnty.expressions.nodes import _is_numeric_type, _is_expression_fast, _is_quantity_fast, _is_fieldqnty_fast


class ExpressionProfiler:
    """Detailed profiler for expression system components."""
    
    def __init__(self):
        self.results = {}
        
    def time_operation(self, name: str, operation, iterations: int = 50000) -> float:
        """Time a specific operation with more iterations for expression analysis."""
        start = time.perf_counter()
        for _ in range(iterations):
            operation()
        end = time.perf_counter()
        
        total_time = end - start
        per_op_time = total_time / iterations
        self.results[name] = {
            'total_time': total_time,
            'per_operation_us': per_op_time * 1_000_000,
            'operations_per_sec': iterations / total_time
        }
        return per_op_time
    
    def profile_wrap_operand_performance(self):
        """Profile wrap_operand function with different input types."""
        print("=== WRAP_OPERAND PERFORMANCE ANALYSIS ===\n")
        
        # Test data
        scalar_int = 5
        scalar_float = 5.0
        length_var = Length(10.0, LengthUnits.millimeter, "test_length")
        pressure_var = Pressure(100.0, PressureUnits.pascal, "test_pressure")
        
        # Already wrapped expression
        existing_expr = BinaryOperation("*", wrap_operand(length_var), wrap_operand(scalar_float))
        
        print("wrap_operand() Performance by Input Type:")
        print("-" * 50)
        
        # Profile different input types
        self.time_operation("wrap_operand_int", lambda: wrap_operand(scalar_int))
        self.time_operation("wrap_operand_float", lambda: wrap_operand(scalar_float))
        self.time_operation("wrap_operand_variable", lambda: wrap_operand(length_var))
        self.time_operation("wrap_operand_expression", lambda: wrap_operand(existing_expr))
        
        for name, stats in self.results.items():
            if 'wrap_operand' in name:
                print(f"{name:25s}: {stats['per_operation_us']:8.3f} μs/op")
        
        print()
    
    def profile_type_checking_functions(self):
        """Profile individual type checking functions."""
        print("=== TYPE CHECKING PERFORMANCE ANALYSIS ===\n")
        
        # Test data
        scalar_int = 5
        scalar_float = 5.0
        length_var = Length(10.0, LengthUnits.millimeter, "test_length")
        expression = BinaryOperation("*", wrap_operand(length_var), wrap_operand(scalar_float))
        quantity_obj = length_var.quantity
        
        print("Type Checking Function Performance:")
        print("-" * 50)
        
        # Profile type checking functions individually
        self.time_operation("is_numeric_int", lambda: _is_numeric_type(scalar_int))
        self.time_operation("is_numeric_float", lambda: _is_numeric_type(scalar_float))
        self.time_operation("is_numeric_variable", lambda: _is_numeric_type(length_var))
        self.time_operation("is_expression_fast", lambda: _is_expression_fast(expression))
        self.time_operation("is_quantity_fast", lambda: _is_quantity_fast(quantity_obj))
        self.time_operation("is_fieldqnty_fast", lambda: _is_fieldqnty_fast(length_var))
        
        for name, stats in self.results.items():
            if any(x in name for x in ['is_numeric', 'is_expression', 'is_quantity', 'is_fieldqnty']):
                print(f"{name:25s}: {stats['per_operation_us']:8.3f} μs/op")
        
        print()
    
    def profile_binary_operation_creation(self):
        """Profile BinaryOperation object creation overhead."""
        print("=== BINARY OPERATION CREATION ANALYSIS ===\n")
        
        # Pre-wrapped operands
        left_operand = wrap_operand(Length(10.0, LengthUnits.millimeter, "left"))
        right_operand = wrap_operand(Length(5.0, LengthUnits.millimeter, "right"))
        scalar_operand = wrap_operand(2.0)
        
        print("BinaryOperation Creation Performance:")
        print("-" * 50)
        
        # Profile different BinaryOperation creations
        self.time_operation("binop_multiply", lambda: BinaryOperation("*", left_operand, right_operand))
        self.time_operation("binop_divide", lambda: BinaryOperation("/", left_operand, right_operand))
        self.time_operation("binop_scalar_mult", lambda: BinaryOperation("*", left_operand, scalar_operand))
        self.time_operation("binop_add", lambda: BinaryOperation("+", left_operand, right_operand))
        
        for name, stats in self.results.items():
            if 'binop' in name:
                print(f"{name:25s}: {stats['per_operation_us']:8.3f} μs/op")
        
        print()
    
    def profile_full_expression_chain(self):
        """Profile complete expression creation chain."""
        print("=== FULL EXPRESSION CHAIN ANALYSIS ===\n")
        
        # Variables for chaining
        length_10 = Length(10.0, LengthUnits.millimeter, "test_length")
        width_5 = Length(5.0, LengthUnits.millimeter, "test_width")
        height_2 = Length(2.0, LengthUnits.millimeter, "test_height")
        
        print("Complete Expression Chain Performance:")
        print("-" * 50)
        
        # Profile complete operations as they would occur in real usage
        self.time_operation("expr_simple_mult", lambda: length_10 * width_5)
        self.time_operation("expr_scalar_mult", lambda: length_10 * 2.0)
        self.time_operation("expr_chain_mult", lambda: length_10 * width_5 * height_2)
        self.time_operation("expr_mixed_ops", lambda: (length_10 * width_5) / height_2)
        
        for name, stats in self.results.items():
            if 'expr_' in name:
                print(f"{name:25s}: {stats['per_operation_us']:8.3f} μs/op")
        
        print()
    
    def profile_expression_evaluation(self):
        """Profile expression evaluation performance."""
        print("=== EXPRESSION EVALUATION ANALYSIS ===\n")
        
        # Create expressions to evaluate
        length_10 = Length(10.0, LengthUnits.millimeter, "test_length")
        width_5 = Length(5.0, LengthUnits.millimeter, "test_width")
        
        simple_expr = length_10 * width_5
        scalar_expr = length_10 * 2.0
        complex_expr = (length_10 * width_5) / Length(2.0, LengthUnits.millimeter, "divisor")
        
        print("Expression Evaluation Performance:")
        print("-" * 50)
        
        # Profile evaluation methods (with empty variable dict for auto-evaluation)
        self.time_operation("eval_simple", lambda: simple_expr.evaluate({}))
        self.time_operation("eval_scalar", lambda: scalar_expr.evaluate({}))
        self.time_operation("eval_complex", lambda: complex_expr.evaluate({}))
        
        # Test string representation (often called)
        self.time_operation("str_simple", lambda: str(simple_expr))
        self.time_operation("str_complex", lambda: str(complex_expr))
        
        for name, stats in self.results.items():
            if any(x in name for x in ['eval_', 'str_']):
                print(f"{name:25s}: {stats['per_operation_us']:8.3f} μs/op")
        
        print()
    
    def profile_with_cprofile_detailed(self):
        """Use cProfile for detailed call analysis of expression operations."""
        print("=== DETAILED EXPRESSION CALL PROFILING ===\n")
        
        def expression_workload():
            """Representative expression workload for detailed profiling."""
            length_10 = Length(10.0, LengthUnits.millimeter, "test_length")
            width_5 = Length(5.0, LengthUnits.millimeter, "test_width")
            height_2 = Length(2.0, LengthUnits.millimeter, "test_height")
            
            for _ in range(500):  # Smaller count for detailed analysis
                # Various expression operations
                expr1 = length_10 * width_5
                expr2 = length_10 * 2.0
                expr3 = expr1 / height_2
                expr4 = expr1 + (width_5 * height_2)
                
                # Force evaluation
                _ = expr1.evaluate({})
                _ = expr3.evaluate({})
        
        print("Expression System Call Profile:")
        print("-" * 40)
        pr = cProfile.Profile()
        pr.enable()
        expression_workload()
        pr.disable()
        
        s = StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.sort_stats('cumulative').print_stats(30)  # Top 30 functions
        print(s.getvalue())
    
    def analyze_memory_usage(self):
        """Analyze memory usage patterns in expression creation."""
        print("=== EXPRESSION MEMORY USAGE ANALYSIS ===\n")
        
        import sys
        
        # Measure object sizes
        length_var = Length(10.0, LengthUnits.millimeter, "test")
        simple_expr = length_var * 2.0
        complex_expr = (length_var * 2.0) / Length(5.0, LengthUnits.millimeter, "divisor")
        
        print("Memory Usage by Object Type:")
        print("-" * 40)
        print(f"Length variable:     {sys.getsizeof(length_var):6d} bytes")
        print(f"Simple expression:   {sys.getsizeof(simple_expr):6d} bytes")
        print(f"Complex expression:  {sys.getsizeof(complex_expr):6d} bytes")
        
        # Measure creation overhead
        import tracemalloc
        
        tracemalloc.start()
        
        # Create many expressions to measure memory patterns
        expressions = []
        for i in range(100):
            length = Length(i, LengthUnits.millimeter, f"len_{i}")
            expr = length * 2.0
            expressions.append(expr)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\nMemory Usage for 100 Expressions:")
        print(f"Current usage:       {current / 1024:.1f} KB")
        print(f"Peak usage:          {peak / 1024:.1f} KB")
        print(f"Avg per expression:  {current / (100 * 1024):.2f} KB")
        print()
    
    def print_bottleneck_summary(self):
        """Identify and summarize the main bottlenecks."""
        print("=== EXPRESSION BOTTLENECK SUMMARY ===\n")
        
        # Sort all results by performance (slowest first for bottleneck identification)
        all_results = [(name, stats) for name, stats in self.results.items()]
        slowest_operations = sorted(all_results, key=lambda x: x[1]['per_operation_us'], reverse=True)
        
        print("Slowest Expression Operations:")
        print("-" * 60)
        print(f"{'Operation':<30} {'Time (μs)':<12} {'Category':<15}")
        print("-" * 60)
        
        for name, stats in slowest_operations[:15]:  # Top 15 slowest
            category = self._categorize_operation(name)
            print(f"{name:<30} {stats['per_operation_us']:8.3f}    {category:<15}")
        
        print()
        
        # Category analysis
        category_times = {}
        for name, stats in all_results:
            category = self._categorize_operation(name)
            if category not in category_times:
                category_times[category] = []
            category_times[category].append(stats['per_operation_us'])
        
        print("Average Time by Category:")
        print("-" * 40)
        for category, times in category_times.items():
            avg_time = sum(times) / len(times)
            print(f"{category:<20}: {avg_time:8.3f} μs/op")
        
        print()
    
    def _categorize_operation(self, operation_name: str) -> str:
        """Categorize operations for analysis."""
        if 'wrap_operand' in operation_name:
            return 'Type Wrapping'
        elif any(x in operation_name for x in ['is_numeric', 'is_expression', 'is_quantity', 'is_fieldqnty']):
            return 'Type Checking'
        elif 'binop' in operation_name:
            return 'Object Creation'
        elif 'expr_' in operation_name:
            return 'Full Expression'
        elif any(x in operation_name for x in ['eval_', 'str_']):
            return 'Evaluation'
        else:
            return 'Other'


def main():
    """Main profiling execution focused on expression system."""
    print("Qnty Expression System: Detailed Performance Analysis")
    print("=" * 60)
    print()
    
    profiler = ExpressionProfiler()
    
    # Run comprehensive expression profiling
    profiler.profile_type_checking_functions()
    profiler.profile_wrap_operand_performance()  
    profiler.profile_binary_operation_creation()
    profiler.profile_full_expression_chain()
    profiler.profile_expression_evaluation()
    profiler.analyze_memory_usage()
    profiler.profile_with_cprofile_detailed()
    profiler.print_bottleneck_summary()
    
    print("Expression system profiling complete.")


if __name__ == "__main__":
    main()