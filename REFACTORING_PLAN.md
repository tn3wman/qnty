# Qnty Architecture Refactoring Plan

This document outlines a comprehensive strategy for refactoring the qnty library from its current mixed architecture to a well-structured, maintainable system while preserving performance and ensuring backward compatibility.

## Executive Summary

The qnty library has grown organically and now suffers from several architectural issues:

- Monolithic files (`problem.py` at 1,251 lines, `expression.py` at 683 lines)
- Inconsistent API surface with missing core exports
- Complex dependency chains requiring duck typing and defensive programming
- Mixed ownership between problem-solving engines and core functionality

This refactoring plan addresses these issues through a 4-phase approach over 6 weeks, decomposing monoliths into focused modules while maintaining backward compatibility.

## Current Architectural Issues

### 1. Monolithic Files

- **`problem.py` (1,251 lines)**: Contains variable management, equation processing, solving, validation, composition, and metaclass logic
- **`expression.py` (683 lines)**: Mixed expression nodes, functions, caching, and helper utilities

### 2. Inconsistent API Surface

- Current `__init__.py` imports 100+ generated variables but doesn't expose core classes like `Problem`
- Mix of facade modules (`quantity.py`) and direct imports
- Validation uses function name `validate` which conflicts with built-in Python function

### 3. Complex Dependencies

- Circular import chains through engines system
- Duck typing and `getattr()` usage indicates unresolved dependency issues
- `TYPE_CHECKING` guards throughout codebase

### 4. Unclear Module Ownership

- Engines system spans problem solving but ownership unclear
- Validation system disconnected from problem domain
- Generated code mixed with core implementations

## Proposed Target Architecture

```
qnty/
[ ]├── __init__.py                 # Curated public API facade
[ ]├── api.py                      # Optional explicit export mapping
[x]├── expressions/                # Decomposed expression system
[x]│   ├── __init__.py
[x]│   ├── nodes.py               # Core AST classes
[x]│   ├── functions.py           # Math helper functions
[x]│   └── cache.py              # Expression caching
[x]├── equations/                  # Clean equation system
[x]│   ├── __init__.py
[x]│   ├── equation.py           # Single equation logic
[x]│   └── system.py            # Multi-equation orchestration
[x]├── quantities/                 # Consolidated quantities
[x]│   ├── __init__.py           # Lazy facade replacing quantity.py
[x]│   ├── quantity.py      # FastQuantity core
[x]│   ├── expression_quantity.py           # TypeSafeVariable
[x]│   └── typed_quantity.py     # Domain-specific variables
[x]├── units/                     # Units system (existing structure maintained)
[x]├── problem/                   # Decomposed problem domain
[x]│   ├── __init__.py
[ ]│   ├── base.py              # Core Problem state/init
[ ]│   ├── variables.py         # Variable lifecycle management
[ ]│   ├── equations.py         # Equation processing
[ ]│   ├── solving.py           # High-level solve orchestration
[x]│   ├── composition.py       # Sub-problem integration
[x]│   ├── metaclass.py         # Class-level magic
[x]│   ├── reconstruction.py    # Equation reconstruction
[ ]│   └── validation.py        # Problem-validation integration
[x]├── solving/                   # Renamed from engines
[x]│   ├── __init__.py
[x]│   ├── order.py  # Dependency analysis
[x]│   ├── manager.py           # Solver strategy selection
[x]│   └── solvers/
[x]│       ├── __init__.py
[x]│       ├── base.py         # Abstract solver interface
[x]│       ├── iterative.py    # Iterative solver
[x]│       └── simultaneous.py # Simultaneous solver
[ ]├── validation/                # Proper validation system
[ ]│   ├── __init__.py
[ ]│   ├── rules.py            # Validation dataclass
[ ]│   └── registry.py         # Future extensibility
[ ]├── generated/                 # All auto-generated artifacts
[ ]│   ├── dimensions.py
[ ]│   ├── units.py
[ ]│   ├── quantities.py
[ ]│   └── setters.py
[x]├── codegen/                   # Structured code generation
[x]│   ├── __init__.py
[ ]│   ├── cli.py              # Unified command-line interface
[x]│   └── generators/
[x]│       ├── dimensions.py
[x]│       ├── units.py
[x]│       ├── setters.py
[x]│       ├── quantities.py
[x]│       └── stubs.py
[ ]└── utils/
[ ]    ├── __init__.py
[ ]    └── logging.py
```

## Implementation Plan

### Phase 1: Foundation & Expression System (Week 1-2)

**Priority: High - Establishes clean foundation**

#### 1.1 Split `expression.py` into Modular System

**Current Issues:**

- 683 lines mixing AST nodes, helper functions, and caching
- Global cache variables scattered throughout
- Performance-critical code mixed with utilities

**Implementation Steps:**

1. **Create `expressions/nodes.py`:**
   - Move core AST classes: `Expression`, `VariableReference`, `Constant`, `BinaryOperation`, `UnaryFunction`, `ConditionalExpression`
   - Keep evaluation protocol and simplification logic
   - Remove global cache implementation (interface only)

2. **Create `expressions/functions.py`:**
   - Move functional helpers: `sin`, `cos`, `tan`, `sqrt`, `ln`, `log10`, `exp`, `abs_expr`, `min_expr`, `max_expr`, `cond_expr`
   - Thin wrappers returning node instances
   - No heavy evaluation logic

3. **Create `expressions/cache.py`:**
   - Extract global caches: `_CACHED_DIMENSIONLESS_QUANTITIES`, `_EXPRESSION_RESULT_CACHE`
   - Encapsulate with clear eviction strategies
   - Add instrumentation and debug counters
   - Provide reset utilities for tests

4. **Create `expressions/__init__.py`:**
   - Curated re-exports maintaining backward compatibility
   - Lazy imports where beneficial for startup performance

**Success Criteria:**

- All existing tests pass without modification
- No performance regression in expression evaluation
- Clean separation of concerns

#### 1.2 Create Clean Equation System

**Current Issues:**

- `equation.py` contains both single equation and system logic
- Mixed concerns between equation representation and solving

**Implementation Steps:**

1. **Split into `equations/equation.py` and `equations/system.py`:**
   - Single equation logic remains in `equation.py`
   - Multi-equation orchestration moves to `system.py`
   - Clear interface between the two

2. **Maintain backward compatibility:**
   - `equations/__init__.py` exports both `Equation` and `EquationSystem`
   - Existing imports continue to work

#### 1.3 Consolidate Quantities System

**Current Issues:**

- Facade module `quantity.py` provides unclear value
- `quantities/` directory has scattered responsibilities

**Implementation Steps:**

1. **Restructure `quantities/` directory:**
   - `fast_quantity.py`: Pure `FastQuantity` implementation
   - `variable.py`: `TypeSafeVariable` and core variable logic
   - `typed_variable.py`: Domain-specific variable extensions
   - `__init__.py`: Replaces `quantity.py` facade with lazy imports

2. **Deprecate `quantity.py`:**
   - Add deprecation warning
   - Redirect imports to new structure
   - Plan removal for next major version

**Dependencies:**

- `expressions/` must be completed first
- Coordinate with generated code in `generated/quantities.py`

### Phase 2: Problem Domain Decomposition (Week 3-4)

**Priority: High - Breaks apart the monolith**

#### 2.1 Decompose `problem.py` Monolith

**Current Issues:**

- Single 1,251-line file with mixed responsibilities
- Variable management, equation processing, solving, validation, and composition all mixed
- Difficult to test, maintain, and understand

**Implementation Strategy:**

1. **Create Problem Module Structure:**

   ```
   problem/
   ├── __init__.py          # Reassemble Problem class
   ├── base.py             # Core state, initialization, caching
   ├── variables.py        # Variable lifecycle (add/get/placeholder)
   ├── equations.py        # Equation processing pipeline
   ├── solving.py          # High-level solve orchestration
   ├── composition.py      # Sub-problem integration
   ├── metaclass.py        # Class-level magic (moved from engines)
   ├── reconstruction.py   # Equation reconstruction
   └── validation.py       # Problem-validation hooks
   ```

2. **Decomposition Process:**

   **Step 2.1.1: Create `problem/base.py`**
   - Move core `Problem` class definition
   - Initialization logic (`__init__`)
   - State management (`_invalidate_caches`, `copy`)
   - Logging and representation methods

   **Step 2.1.2: Create `problem/variables.py`**
   - Variable lifecycle: `add_variable`, `add_variables`, `get_variable`
   - Placeholder creation: `_create_placeholder_variable`
   - Variable validation and caching logic
   - Known/unknown variable subset management

   **Step 2.1.3: Create `problem/equations.py`**
   - Equation processing pipeline: `_process_equation`
   - Missing variable handling
   - Equation validation and self-reference checks
   - Reconstruction triggers

   **Step 2.1.4: Create `problem/solving.py`**
   - High-level `solve()` method
   - Dependency graph building: `_build_dependency_graph`
   - Solution verification: `verify_solution`
   - Integration with solver system

   **Step 2.1.5: Move `engines/problem/composition.py` to `problem/composition.py`**
   - Sub-problem namespace handling
   - Variable cloning for composition
   - Composite equation synthesis (min/max operations)

   **Step 2.1.6: Move `engines/problem/metaclass.py` to `problem/metaclass.py`**
   - Class-level variable/equation collection
   - `ProblemMeta` implementation
   - Integration with class definition process

   **Step 2.1.7: Create `problem/reconstruction.py`**
   - Move from `engines/problem/equation_reconstruction.py`
   - Equation reconstruction heuristics
   - Delayed expression resolution

   **Step 2.1.8: Create `problem/validation.py`**
   - Integration between Problem and validation system
   - Validation check execution
   - Result collection and reporting

3. **Reassembly in `problem/__init__.py`:**
   - Import all components
   - Reassemble into single `Problem` class using mixins or composition
   - Maintain identical external interface

**Migration Strategy:**

- Use mixin classes or composition to reassemble functionality
- Maintain identical public interface
- All existing tests must pass without modification
- Gradual migration with feature flags if needed

#### 2.2 Rename Engines to Solving System

**Current Issues:**

- "Engines" is unclear terminology
- Mixed ownership between problem domain and solving algorithms

**Implementation Steps:**

1. **Create new `solving/` directory structure:**

   ```
   solving/
   ├── __init__.py
   ├── dependency_graph.py  # From engines/problem/
   ├── manager.py          # From engines/solver/
   └── solvers/
       ├── __init__.py
       ├── base.py         # From engines/solver/
       ├── iterative.py    # From engines/solver/
       └── simultaneous.py # From engines/solver/
   ```

2. **Move files with minimal changes:**
   - `engines/problem/dependency_graph.py` → `solving/dependency_graph.py`
   - `engines/solver/manager.py` → `solving/manager.py`
   - `engines/solver/*.py` → `solving/solvers/*.py`

3. **Update imports throughout codebase:**
   - Use systematic find/replace for import statements
   - Maintain backward compatibility with deprecation warnings

4. **Keep `engines/` directory temporarily:**
   - Add deprecation warnings to all imports
   - Plan removal after one release cycle

### Phase 3: Validation & API Cleanup (Week 5)

**Priority: Medium - API consistency and user experience**

#### 3.1 Create Proper Validation System

**Current Issues:**

- Single `validation.py` file with unclear integration
- Function name `validate` conflicts with Python built-in
- Validation system disconnected from problem domain

**Implementation Steps:**

1. **Create `validation/` directory:**

   ```
   validation/
   ├── __init__.py          # Export rule factory, Validation class
   ├── rules.py            # Validation dataclass (renamed)
   └── registry.py         # Future extensibility
   ```

2. **Rename `validation.py` → `validation/rules.py`:**
   - Move `Validation` dataclass to `rules.py`
   - Rename `validate()` → `rule()` function
   - Maintain backward compatibility with deprecation warning

3. **Update `validation/__init__.py`:**
   - Export `rule` as primary function name
   - Export `Validation` class for advanced usage
   - Add `validate` as deprecated alias

4. **Create `validation/registry.py`:**
   - Future extensibility for custom validation categories
   - Plugin system for domain-specific validation rules

#### 3.2 Fix API Naming and Surface

**Current Issues:**

- `Problem` class not exported in `__init__.py`
- Inconsistent import patterns
- Missing convenient aliases

**Implementation Steps:**

1. **Update `qnty/__init__.py`:**

   ```python
   # Core classes - newly exported
   from .problem import Problem
   from .equation import Equation, EquationSystem
   
   # Convenient aliases
   from .quantities import FastQuantity as Quantity
   from .quantities import TypeSafeVariable as Variable
   
   # Validation
   from .validation import rule
   
   # Expression helpers
   from .expressions.functions import min_expr, max_expr, cond_expr
   
   # Generated variables (existing imports maintained)
   from .generated.quantities import (
       Length, Pressure, Temperature, Mass, Volume, Area, Force,
       # ... all other generated variables
   )
   
   # Public API definition
   __all__ = [
       'Problem', 'Equation', 'EquationSystem',
       'Variable', 'Quantity',
       'rule',
       'min_expr', 'max_expr', 'cond_expr',
       # Generated variables
       'Length', 'Pressure', 'Temperature', # ... etc
   ]
   ```

2. **Create optional `qnty/api.py`:**
   - Central definition of public API surface
   - Prevents circular import issues
   - Documents intended stability levels

3. **Add deprecation warnings:**
   - `from qnty.validation import validate` → warning + redirect to `rule`
   - `import qnty.quantity` → warning + redirect to `qnty.quantities`

### Phase 4: Code Generation Restructure (Week 6)

**Priority: Low - Developer experience improvement**

#### 4.1 Restructure Generation System

**Current Issues:**

- Numbered script files in `scripts/` directory
- No unified command-line interface
- Mixed concerns between generation logic and CLI

**Implementation Steps:**

1. **Create `codegen/` directory structure:**

   ```
   codegen/
   ├── __init__.py
   ├── cli.py              # Unified command-line interface
   └── generators/
       ├── __init__.py
       ├── dimensions.py   # From scripts/_1_generate_dimensions.py
       ├── units.py       # From scripts/_2_generate_units.py
       ├── variables.py   # From scripts/_3_generate_variables.py
       └── stubs.py       # From scripts/_4_generate_variable_pyi.py
   ```

2. **Create unified CLI in `codegen/cli.py`:**

   ```python
   def main():
       """Unified code generation CLI."""
       parser = argparse.ArgumentParser(description="Qnty code generator")
       parser.add_argument('target', choices=['dimensions', 'units', 'variables', 'stubs', 'all'])
       # ... argument parsing
       
   if __name__ == "__main__":
       main()
   ```

3. **Maintain backward compatibility:**
   - Keep existing `scripts/` directory with shim files
   - Add deprecation warnings
   - Update documentation to use new CLI

4. **Update generation commands:**

   ```bash
   # Old (deprecated)
   python scripts/_1_generate_dimensions.py
   
   # New
   python -m qnty.codegen dimensions
   # or
   qnty-codegen dimensions  # if console script added
   ```

## Migration Strategy

### Backward Compatibility Approach

1. **Dual Import Paths (1 release cycle):**

   ```python
   # Old import (deprecated with warning)
   from qnty.validation import validate
   
   # New import
   from qnty.validation import rule
   ```

2. **Facade Modules with Warnings:**

   ```python
   # qnty/quantity.py (deprecated)
   import warnings
   warnings.warn(
       "qnty.quantity is deprecated, use qnty.quantities", 
       DeprecationWarning, 
       stacklevel=2
   )
   from .quantities import *
   ```

3. **Preserve Public API Surface:**
   - Keep all generated variable imports in `__init__.py`
   - Add missing `Problem` class to public exports
   - Maintain import compatibility for core classes

### Development Process

1. **Feature Flag Approach:**
   - Implement new structure alongside existing
   - Use environment variable `QNTY_USE_NEW_STRUCTURE` during development
   - Gradual migration with comprehensive testing

2. **Test-First Migration:**
   - Migrate tests first to establish expected behavior
   - Use existing test suite as regression validation
   - Add integration tests for new module boundaries

3. **Continuous Integration:**
   - Run both old and new structures in CI
   - Performance benchmarking after each phase
   - Automated backward compatibility testing

## Risk Mitigation

### Performance Regression Prevention

1. **Benchmarking Requirements:**
   - Run existing benchmarks before/after each phase
   - Profile critical paths: equation solving, unit conversion, expression evaluation
   - Maintain or improve existing 18-25x performance advantage over Pint
   - Focus on import time improvements through lazy loading

2. **Critical Performance Paths:**
   - `FastQuantity` arithmetic operations
   - Unit conversion through registry
   - Expression tree evaluation
   - Equation solving algorithms

### Type Safety Preservation

1. **Dynamic Access Patterns:**
   - Maintain existing `hasattr()`/`getattr()` patterns during migration
   - Preserve defensive programming for dynamic attributes
   - Keep try/except blocks for safe attribute assignment

2. **Gradual Type Strengthening:**
   - Add stronger typing as architecture stabilizes
   - Use `TYPE_CHECKING` guards for complex forward references
   - Maintain compatibility with existing duck typing

### Generated Code Stability

1. **Generation Pipeline:**
   - Keep generation scripts working throughout refactor
   - Test generated code compatibility after each phase
   - Maintain all 100+ variable types and 800+ units
   - Ensure generated code passes all existing tests

2. **Template Consistency:**
   - Keep generated code templates stable
   - Test template changes against existing usage patterns
   - Verify IDE support (type hints, autocomplete) continues working

## Breaking Changes & Compatibility

### Minimal Breaking Changes

1. **Function Rename:**
   - `validate()` → `rule()` (with 1-release deprecation shim)
   - Clear migration path in documentation

2. **Import Path Changes (Internal Only):**
   - Most internal imports will change but public API remains stable
   - Generated variables continue to be importable from main package
   - Core classes gain consistent public imports

3. **Removed Facades:**
   - `qnty.quantity` module replaced by `qnty.quantities`
   - 1-release deprecation period with warnings

### Non-Breaking Enhancements

1. **Enhanced Public API:**

   ```python
   # New - Problem class finally exported publicly
   from qnty import Problem
   
   # New - Cleaner aliases for common classes
   from qnty import Variable, Quantity
   
   # Improved - Consistent validation interface
   from qnty import rule
   ```

2. **Better Error Messages:**
   - Clearer error context from focused modules
   - Better validation error reporting with source location
   - Improved debugging experience

3. **Development Experience:**
   - Cleaner internal architecture for contributors
   - Better separation of concerns
   - Simplified testing of individual components

## Success Criteria

### 1. Maintainability Metrics

- **File Size Limits:** No file over 500 lines
- **Module Responsibility:** Each module has single, clear responsibility
- **Dependency Direction:** Clean unidirectional dependency graph without cycles
- **Test Coverage:** Maintain or improve existing test coverage across all modules

### 2. Performance Requirements

- **Benchmark Maintenance:** All existing performance benchmarks must pass
- **Critical Path Performance:** No regression in equation solving, unit conversion, or expression evaluation
- **Startup Performance:** Improved or maintained import time through lazy loading
- **Memory Usage:** No increase in memory footprint for common operations

### 3. Developer Experience

- **Public API Clarity:** Logical, discoverable exports in main `__init__.py`
- **Error Messages:** Improved error context and debugging information
- **Documentation:** Clear migration guide and updated architecture documentation
- **Testing:** Easier to test individual components in isolation

### 4. Backward Compatibility

- **User Code Compatibility:** All existing user code continues working without changes
- **Deprecation Process:** Clear 1-release deprecation warnings for changed APIs
- **Migration Support:** Documentation and tooling to help users migrate deprecated usage

### 5. Code Quality

- **Type Safety:** Improved type hints and better IDE support
- **Code Reuse:** Elimination of duplicated logic across modules
- **Extension Points:** Clear interfaces for adding new solvers, expressions, or validation rules
- **Generated Code:** Stable, consistent generated code that integrates cleanly

## Implementation Timeline

### Week 1-2: Foundation & Expression System

- [x] Split `expression.py` into modular `expressions/` package
- [x] Create clean `equations/` system
- [ ] Consolidate `quantities/` with lazy loading
- [ ] Comprehensive testing of decomposed expression system

### Week 3-4: Problem Domain Decomposition

- [ ] Decompose 1,251-line `problem.py` into focused modules
- [ ] Rename `engines/` to `solving/` system
- [ ] Reassemble Problem class with identical interface
- [ ] Migration testing and performance validation

### Week 5: Validation & API Cleanup

- [ ] Create proper `validation/` system with `rule()` function
- [ ] Fix public API exports in `__init__.py`
- [ ] Add backward compatibility shims with deprecation warnings
- [ ] Update documentation and migration guide

### Week 6: Code Generation Restructure

- [ ] Restructure generation system to `codegen/` package
- [ ] Create unified CLI for code generation
- [ ] Maintain backward compatibility for generation scripts
- [ ] Final testing and documentation updates

## Post-Refactoring Benefits

### For Users

- **Cleaner Imports:** Logical public API with consistent exports
- **Better Performance:** Lazy loading reduces startup time
- **Improved Errors:** Clearer error messages with better context
- **Stable Interface:** Backward compatibility with deprecation guidance

### For Contributors

- **Maintainable Code:** Focused modules under 500 lines each
- **Clear Architecture:** Unidirectional dependencies and single responsibilities
- **Easier Testing:** Individual components can be tested in isolation
- **Better Tooling:** Improved IDE support and development experience

### For Library Evolution

- **Extension Points:** Clear interfaces for adding new functionality
- **Modular Growth:** New features can be added without touching core modules
- **Performance Optimization:** Individual components can be optimized independently
- **Technology Adoption:** Modern Python patterns and type system usage

This refactoring plan transforms qnty from its current mixed state into a well-structured, maintainable library while preserving its performance advantages and ensuring a smooth transition for all users.
