# Standard Unit Prefix Implementation Proposal for Qnty

## Current State Analysis

### How Units Are Currently Handled

1. **Unit Storage**: Each unit is explicitly defined in `parsed_units.json` with:
   - Full name (e.g., "millimeter", "kilometer")
   - SI conversion factor (e.g., 0.001 for millimeter, 1000 for kilometer)
   - Symbol/notation (e.g., "mm", "km")

2. **Unit Generation**: The scripts generate explicit unit definitions for each unit variant:
   - Some SI prefixed units exist (millimeter, centimeter, kilometer)
   - Each is treated as a completely separate unit
   - No systematic prefix handling

3. **Current Examples**:
   ```python
   # In units.py - each prefixed unit is defined separately
   millimeter = UnitDefinition("millimeter", "mm", LENGTH, 0.001)
   centimeter = UnitDefinition("centimeter", "cm", LENGTH, 0.01)
   kilometer = UnitDefinition("kilometer", "km", LENGTH, 1000.0)
   ```

## Proposed Implementation Approach

### 1. Define Standard SI Prefixes

Create a new module `src/qnty/prefixes.py`:

```python
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class SIPrefix:
    """Standard SI prefix definition."""
    name: str
    symbol: str
    factor: float
    
class StandardPrefixes(Enum):
    """Standard SI prefixes with their multiplication factors."""
    # Larger prefixes
    YOTTA = SIPrefix("yotta", "Y", 1e24)
    ZETTA = SIPrefix("zetta", "Z", 1e21)
    EXA = SIPrefix("exa", "E", 1e18)
    PETA = SIPrefix("peta", "P", 1e15)
    TERA = SIPrefix("tera", "T", 1e12)
    GIGA = SIPrefix("giga", "G", 1e9)
    MEGA = SIPrefix("mega", "M", 1e6)
    KILO = SIPrefix("kilo", "k", 1e3)
    HECTO = SIPrefix("hecto", "h", 1e2)
    DECA = SIPrefix("deca", "da", 1e1)
    
    # Base (no prefix)
    NONE = SIPrefix("", "", 1.0)
    
    # Smaller prefixes
    DECI = SIPrefix("deci", "d", 1e-1)
    CENTI = SIPrefix("centi", "c", 1e-2)
    MILLI = SIPrefix("milli", "m", 1e-3)
    MICRO = SIPrefix("micro", "μ", 1e-6)
    NANO = SIPrefix("nano", "n", 1e-9)
    PICO = SIPrefix("pico", "p", 1e-12)
    FEMTO = SIPrefix("femto", "f", 1e-15)
    ATTO = SIPrefix("atto", "a", 1e-18)
    ZEPTO = SIPrefix("zepto", "z", 1e-21)
    YOCTO = SIPrefix("yocto", "y", 1e-24)
```

### 2. Enhance UnitDefinition with Prefix Support

Update `src/qnty/unit.py`:

```python
@dataclass(frozen=True)
class UnitDefinition:
    """Immutable unit definition optimized for performance."""
    name: str
    symbol: str
    dimension: DimensionSignature
    si_factor: float
    si_offset: float = 0.0
    base_unit_name: str = None  # New: base unit without prefix
    prefix: SIPrefix = None      # New: SI prefix if applicable
    
    @classmethod
    def with_prefix(cls, base_def: 'UnitDefinition', prefix: SIPrefix) -> 'UnitDefinition':
        """Create a new unit definition with an SI prefix."""
        return cls(
            name=f"{prefix.name}{base_def.name}",
            symbol=f"{prefix.symbol}{base_def.symbol}",
            dimension=base_def.dimension,
            si_factor=base_def.si_factor * prefix.factor,
            si_offset=base_def.si_offset,
            base_unit_name=base_def.name,
            prefix=prefix
        )
```

### 3. Automatic Prefix Generation in Registry

Update `HighPerformanceRegistry` in `src/qnty/unit.py`:

```python
class HighPerformanceRegistry:
    """Ultra-fast registry with pre-computed conversion tables."""
    
    def __init__(self):
        self.units: dict[str, UnitDefinition] = {}
        self.conversion_table: dict[tuple[str, str], float] = {}
        self.base_units: dict[str, UnitDefinition] = {}  # New
        self.prefixable_units: set[str] = set()  # New
    
    def register_with_prefixes(self, unit_def: UnitDefinition, 
                              prefixes: list[SIPrefix] = None):
        """Register a unit and automatically generate prefixed variants."""
        # Register base unit
        self.register(unit_def)
        self.base_units[unit_def.name] = unit_def
        self.prefixable_units.add(unit_def.name)
        
        # Generate and register prefixed variants
        if prefixes is None:
            prefixes = [p.value for p in StandardPrefixes if p != StandardPrefixes.NONE]
        
        for prefix in prefixes:
            prefixed_unit = UnitDefinition.with_prefix(unit_def, prefix)
            self.register(prefixed_unit)
```

### 4. Update Generation Scripts

Modify `scripts/_2_generate_units.py` to:

1. Identify base SI units (meter, gram, second, etc.)
2. Automatically generate prefixed variants
3. Skip generating prefixed units that already exist in the data

```python
# In generate_units.py
SI_BASE_UNITS = {
    'meter': ['kilo', 'centi', 'milli', 'micro', 'nano'],
    'gram': ['kilo', 'milli', 'micro'],  # Note: kilogram is the SI base
    'second': ['milli', 'micro', 'nano', 'pico'],
    'ampere': ['milli', 'micro'],
    'kelvin': [],  # Usually no prefixes
    'mole': ['milli', 'micro'],
    'candela': [],  # Usually no prefixes
    'pascal': ['kilo', 'mega', 'giga'],
    'joule': ['kilo', 'mega', 'giga'],
    'watt': ['kilo', 'mega', 'giga', 'milli', 'micro'],
    'volt': ['kilo', 'milli', 'micro'],
    'ohm': ['kilo', 'mega', 'milli'],
    'farad': ['milli', 'micro', 'nano', 'pico'],
    'henry': ['milli', 'micro', 'nano'],
    'hertz': ['kilo', 'mega', 'giga'],
}
```

### 5. Fluent API Integration

Update the setter classes to support prefixed units:

```python
class LengthSetter(TypeSafeSetter):
    # Existing properties
    @property
    def meter(self) -> 'Length': ...
    
    # Auto-generated prefix properties
    @property
    def kilometer(self) -> 'Length': ...
    
    @property  
    def centimeter(self) -> 'Length': ...
    
    @property
    def millimeter(self) -> 'Length': ...
    
    @property
    def micrometer(self) -> 'Length': ...
    
    @property
    def nanometer(self) -> 'Length': ...
```

## Implementation Benefits

1. **Consistency**: All SI units will have standard prefixes available
2. **Reduced Redundancy**: No need to manually define each prefixed variant
3. **Performance**: Conversion factors are pre-computed at registration time
4. **Extensibility**: Easy to add new prefixes or customize per unit
5. **Type Safety**: Maintains full type checking with generated properties

## Implementation Steps

1. **Phase 1**: Create prefix module and update UnitDefinition
2. **Phase 2**: Update registry with prefix support
3. **Phase 3**: Modify generation scripts to use prefix system
4. **Phase 4**: Update type stubs (.pyi) generation
5. **Phase 5**: Add tests for prefix functionality

## Backward Compatibility

- Existing explicitly-defined prefixed units remain unchanged
- New prefix system supplements rather than replaces current units
- All current API remains functional

## Example Usage

```python
from qnty import Length

# All these would be automatically available
length = Length(5.0)
length.set(5.0).meters      # 5 m
length.set(5.0).kilometers   # 5 km = 5000 m  
length.set(5.0).millimeters  # 5 mm = 0.005 m
length.set(5.0).micrometers  # 5 μm = 0.000005 m
length.set(5.0).nanometers   # 5 nm = 0.000000005 m

# Conversion handled automatically
assert length.set(1.0).kilometers.value == length.set(1000.0).meters.value
```

## Testing Strategy

1. Unit tests for prefix multiplication
2. Integration tests for prefixed unit registration
3. Property generation verification
4. Conversion accuracy tests
5. Performance benchmarks

## Next Steps

1. Review and approve proposal
2. Create feature branch
3. Implement prefix module
4. Update unit system
5. Modify generation scripts
6. Add comprehensive tests
7. Update documentation