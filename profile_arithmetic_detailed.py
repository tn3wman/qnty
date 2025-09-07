#!/usr/bin/env python3
"""
Detailed Profiling of Multiplication and Division Operations

This script profiles multiplication and division operations to identify 
performance bottlenecks and optimization opportunities.
"""

import cProfile
import pstats
import time
from io import StringIO

# Import qnty components
from src.qnty import Length, Pressure, Area, Force, Volume, Mass, Temperature
from src.qnty.quantities.base_qnty import Quantity, ArithmeticOperations, _cache_manager
from src.qnty.units.field_units import LengthUnits, PressureUnits


class ArithmeticProfiler:
    """Comprehensive profiler for arithmetic operations."""
    
    def __init__(self):
        self.results = {}
        
    def time_operation(self, name: str, operation, iterations: int = 100000) -> float:
        """Time a specific operation."""
        start = time.perf_counter()
        for _ in range(iterations):
            operation()
        end = time.perf_counter()
        
        total_time = end - start
        per_op_time = total_time / iterations
        self.results[name] = {
            'total_time': total_time,
            'per_operation_us': per_op_time * 1_000_000,  # microseconds
            'operations_per_sec': iterations / total_time
        }
        return per_op_time
    
    def profile_multiplication_scenarios(self):
        """Profile different multiplication scenarios."""
        print("=== MULTIPLICATION PROFILING ===\n")
        
        # Setup test quantities
        length_10 = Length(10.0, LengthUnits.millimeter, "test_length")
        width_5 = Length(5.0, LengthUnits.millimeter, "test_width")
        pressure_100 = Pressure(100.0, PressureUnits.pascal, "test_pressure") 
        area_50 = Area(50.0, "mm²", "test_area")
        scalar_2 = 2.0
        scalar_int = 3
        
        # Clear caches for clean profiling
        _cache_manager.multiplication_cache.clear()
        _cache_manager.division_cache.clear()
        
        print("Multiplication Scenarios:")
        print("-" * 50)
        
        # 1. Scalar multiplication (should be fastest)
        self.time_operation("scalar_float_multiply", lambda: length_10 * scalar_2)
        self.time_operation("scalar_int_multiply", lambda: length_10 * scalar_int)
        
        # 2. Same dimension multiplication (Length × Length = Area)
        self.time_operation("length_x_length_uncached", lambda: length_10 * width_5)
        
        # Warm up cache
        for _ in range(10):
            length_10 * width_5
            
        self.time_operation("length_x_length_cached", lambda: length_10 * width_5)
        
        # 3. Different dimension multiplication (Pressure × Area = Force)
        _cache_manager.multiplication_cache.clear()
        _cache_manager.division_cache.clear()
        self.time_operation("pressure_x_area_uncached", lambda: pressure_100 * area_50)
        
        # Warm up cache
        for _ in range(10):
            pressure_100 * area_50
            
        self.time_operation("pressure_x_area_cached", lambda: pressure_100 * area_50)
        
        # 4. Mixed unit multiplication (different units, same dimension)
        length_mm = Length(10.0, LengthUnits.millimeter, "length_mm")
        length_m = Length(0.005, LengthUnits.meter, "length_m")
        
        _cache_manager.multiplication_cache.clear()
        _cache_manager.division_cache.clear()
        self.time_operation("mixed_units_uncached", lambda: length_mm * length_m)
        
        # Warm up cache
        for _ in range(10):
            length_mm * length_m
            
        self.time_operation("mixed_units_cached", lambda: length_mm * length_m)
        
        # Print results
        for name, stats in self.results.items():
            if 'multiply' in name:
                print(f"{name:30s}: {stats['per_operation_us']:8.3f} μs/op")
        
        print()
    
    def profile_division_scenarios(self):
        """Profile different division scenarios."""
        print("=== DIVISION PROFILING ===\n")
        
        # Setup test quantities
        area_100 = Area(100.0, "mm²", "test_area")
        length_10 = Length(10.0, LengthUnits.millimeter, "test_length")
        force_500 = Force(500.0, "N", "test_force")
        pressure_100 = Pressure(100.0, PressureUnits.pascal, "test_pressure")
        scalar_2 = 2.0
        scalar_int = 5
        
        # Clear caches for clean profiling
        _cache_manager.multiplication_cache.clear()
        _cache_manager.division_cache.clear()
        
        print("Division Scenarios:")
        print("-" * 50)
        
        # 1. Scalar division (should be fastest)  
        self.time_operation("scalar_float_divide", lambda: area_100 / scalar_2)
        self.time_operation("scalar_int_divide", lambda: area_100 / scalar_int)
        
        # 2. Same dimension division (Area ÷ Length = Length)
        self.time_operation("area_div_length_uncached", lambda: area_100 / length_10)
        
        # Warm up cache
        for _ in range(10):
            area_100 / length_10
            
        self.time_operation("area_div_length_cached", lambda: area_100 / length_10)
        
        # 3. Different dimension division (Force ÷ Area = Pressure)
        area_for_pressure = Area(5.0, "mm²", "area_for_pressure")
        _cache_manager.multiplication_cache.clear()
        _cache_manager.division_cache.clear()
        self.time_operation("force_div_area_uncached", lambda: force_500 / area_for_pressure)
        
        # Warm up cache
        for _ in range(10):
            force_500 / area_for_pressure
            
        self.time_operation("force_div_area_cached", lambda: force_500 / area_for_pressure)
        
        # 4. Dimensionless division
        dimensionless = Length(1.0, LengthUnits.meter, "dimensionless") / Length(1.0, LengthUnits.meter, "unit_length")
        self.time_operation("dimensionless_divide", lambda: area_100 / dimensionless)
        
        # Print results  
        print()
        for name, stats in self.results.items():
            if 'divide' in name:
                print(f"{name:30s}: {stats['per_operation_us']:8.3f} μs/op")
        
        print()
    
    def profile_with_cprofile(self):
        """Use cProfile to get detailed call statistics."""
        print("=== DETAILED CALL PROFILING ===\n")
        
        # Setup
        length_10 = Length(10.0, LengthUnits.millimeter, "test_length")
        width_5 = Length(5.0, LengthUnits.millimeter, "test_width") 
        area_100 = Area(100.0, "mm²", "test_area")
        
        def multiplication_workload():
            """Representative multiplication workload."""
            for _ in range(1000):
                # Mix of different operation types
                result1 = length_10 * width_5  # Length × Length
                result2 = length_10 * 2.0      # Scalar multiply
                result3 = length_10 * length_10  # Same variable multiply
        
        def division_workload():
            """Representative division workload."""
            for _ in range(1000):
                # Mix of different operation types
                result1 = area_100 / length_10  # Area ÷ Length
                result2 = area_100 / 2.0        # Scalar divide  
                result3 = area_100 / area_100   # Same variable divide
        
        # Profile multiplication
        print("Multiplication Call Profile:")
        print("-" * 40)
        pr = cProfile.Profile()
        pr.enable()
        multiplication_workload()
        pr.disable()
        
        s = StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.sort_stats('cumulative').print_stats(20)  # Top 20 functions
        print(s.getvalue())
        
        # Profile division
        print("\nDivision Call Profile:")
        print("-" * 40)
        pr = cProfile.Profile()
        pr.enable()
        division_workload()
        pr.disable()
        
        s = StringIO()
        ps = pstats.Stats(pr, stream=s)
        ps.sort_stats('cumulative').print_stats(20)  # Top 20 functions
        print(s.getvalue())
    
    def analyze_cache_performance(self):
        """Analyze cache hit/miss patterns."""
        print("=== CACHE PERFORMANCE ANALYSIS ===\n")
        
        # Setup
        length_vals = [Length(i, LengthUnits.millimeter, f"len_{i}") for i in range(1, 11)]
        
        # Clear cache and measure cold performance
        _cache_manager.multiplication_cache.clear()
        _cache_manager.division_cache.clear()
        
        cold_start = time.perf_counter()
        for i in range(10):
            for j in range(i+1, 10):
                result = length_vals[i] * length_vals[j]
        cold_end = time.perf_counter()
        
        # Measure warm cache performance
        warm_start = time.perf_counter()
        for i in range(10):
            for j in range(i+1, 10):
                result = length_vals[i] * length_vals[j]
        warm_end = time.perf_counter()
        
        cold_time = cold_end - cold_start
        warm_time = warm_end - warm_start
        
        print(f"Cold cache time: {cold_time*1000:.3f} ms")
        print(f"Warm cache time: {warm_time*1000:.3f} ms")
        print(f"Cache speedup:   {cold_time/warm_time:.2f}x")
        print()
        
        # Cache statistics
        print("Cache Statistics:")
        print(f"  multiplication_cache: {len(_cache_manager.multiplication_cache)} entries")
        print(f"  division_cache: {len(_cache_manager.division_cache)} entries")
        print(f"  multiplication_templates: {len(_cache_manager.multiplication_templates)} entries")
        print()
    
    def print_performance_summary(self):
        """Print a comprehensive performance summary."""
        print("=== PERFORMANCE SUMMARY ===\n")
        
        # Sort by performance (fastest first)
        sorted_results = sorted(self.results.items(), key=lambda x: x[1]['per_operation_us'])
        
        print(f"{'Operation':<30} {'Time (μs)':<12} {'Ops/sec':<15}")
        print("-" * 60)
        
        for name, stats in sorted_results:
            print(f"{name:<30} {stats['per_operation_us']:8.3f}    {stats['operations_per_sec']:12,.0f}")
        
        print()
        
        # Identify bottlenecks
        slowest = sorted_results[-3:]  # 3 slowest operations
        print("Performance Bottlenecks (slowest operations):")
        for name, stats in reversed(slowest):
            print(f"  {name}: {stats['per_operation_us']:.3f} μs/op")
        
        print()


def main():
    """Main profiling execution."""
    print("Qnty Library: Arithmetic Operations Performance Profiling")
    print("=" * 60)
    print()
    
    profiler = ArithmeticProfiler()
    
    # Run all profiling scenarios
    profiler.profile_multiplication_scenarios()
    profiler.profile_division_scenarios()
    profiler.analyze_cache_performance()
    profiler.profile_with_cprofile()
    profiler.print_performance_summary()
    
    print("Profiling complete.")


if __name__ == "__main__":
    main()