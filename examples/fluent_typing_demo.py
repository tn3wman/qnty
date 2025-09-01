"""
Demonstration of fluent typing with consolidated variables.

This file shows how the .pyi stub file provides rich IDE autocomplete
and type checking for the dynamically generated setter properties.
"""

from qnty.variables import Area, Length, Pressure


def demo_fluent_typing():
    """Demonstrate fluent API with full type safety."""
    
    # ========== PRESSURE EXAMPLE ==========
    # When you type `pressure.set(15).` the IDE will show ONLY pressure units:
    pressure = Pressure("working_pressure")
    
    # All these have full IDE autocomplete and type checking:
    pressure.set(15).bar        # ✓ Pressure unit
    pressure.set(101.325).kilogram_force_per_square_meter  # ✓ Pressure unit
    pressure.set(14.7).bar            # ✓ Pressure unit
    pressure.set(1.013).bar           # ✓ Pressure unit
    pressure.set(760).torr            # ✓ Pressure unit
    
    # The IDE will NOT suggest length or area units here - compile-time safety!
    # pressure.set(15).meters          # ✗ Would be a type error
    # pressure.set(15).square_meters   # ✗ Would be a type error
    
    print(f"Pressure: {pressure.quantity}")
    
    
    # ========== LENGTH EXAMPLE ==========
    # When you type `length.set(100).` the IDE will show ONLY length units:
    length = Length("beam_length")
    
    # All these have full IDE autocomplete and type checking:
    length.set(100).meter      # ✓ Length unit
    length.set(5.5).meter             # ✓ Length unit
    length.set(12).inch              # ✓ Length unit (with alias support)
    length.set(3).foot                 # ✓ Length unit
    length.set(1000).kilometer        # ✓ Length unit

    print(f"Length: {length.quantity}")
    
    
    # ========== AREA EXAMPLE ==========
    # When you type `area.set(50).` the IDE will show ONLY area units:
    area = Area("surface_area")
    
    # All these have full IDE autocomplete and type checking:
    area.set(50).square_meter        # ✓ Area unit
    area.set(100).square_foot         # ✓ Area unit (note: auto-pluralized)
    area.set(2.5).hectare             # ✓ Area unit
    area.set(1000).square_millimeter  # ✓ Area unit
    
    print(f"Area: {area.quantity}")


def demo_type_safety():
    """Show compile-time type safety benefits."""
    
    pressure = Pressure("system_pressure")
    length = Length("pipe_length")
    
    # The setter is properly typed - IDE knows it's PressureSetter
    pressure_setter = pressure.set(15)
    print(f"Pressure setter type: {type(pressure_setter).__name__}")
    
    # The setter is properly typed - IDE knows it's LengthSetter
    length_setter = length.set(100)
    print(f"Length setter type: {type(length_setter).__name__}")
    
    # Type checking prevents dimensional errors at development time
    # This ensures you can't accidentally mix up units from different dimensions


if __name__ == "__main__":
    print("=== Fluent Typing Demo ===")
    demo_fluent_typing()
    
    print("\n=== Type Safety Demo ===")
    demo_type_safety()
    
    print("""
=== IDE Benefits ===

With the .pyi stub file, your IDE now provides:

1. ✅ Full autocomplete for dimension-specific units
2. ✅ Type checking prevents mixing units from different dimensions
3. ✅ IntelliSense shows only valid unit properties
4. ✅ Compile-time error detection for invalid units
5. ✅ Rich tooltips with unit descriptions

Try typing in your IDE:
- pressure.set(15).    <- Shows ONLY pressure units
- length.set(100).     <- Shows ONLY length units
- area.set(50).        <- Shows ONLY area units

This provides the same excellent developer experience as the original
non-optimized implementation, but with much better performance!
    """)
