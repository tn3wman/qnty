# Qnty Package File Structure Analysis & Rename Suggestions

## Current vs Proposed Structure

Based on analysis of file contents, sizes, and purposes, here are the suggested improvements:

## Files Requiring Rename

### **Major Directory Renames**

| Current Path | Proposed Path | Reason | 
|--------------|---------------|--------|
| `qnty/unit_system/` | `qnty/units/` | Remove "system" suffix, cleaner |
| `qnty/variable_system/` | `qnty/variables/` | Remove "system" suffix, cleaner |
| `qnty/solver_system/` | `qnty/solver/` | Remove "system" suffix, cleaner |
| `qnty/problem_system/` | `qnty/problem_internals/` | More descriptive of hidden complexity |

### **File Conflicts & Renames**

| Current Path | Proposed Path | Reason | Lines |
|--------------|---------------|--------|-------|
| `qnty/units.py` | `qnty/unit_constants.py` | Avoid conflict with `units/` directory | 8,119 |
| `qnty/variables.py` | `qnty/variable_types.py` | Avoid conflict with `variables/` directory | 10,725 |
| `qnty/unit_system/core.py` | `qnty/units/registry.py` | Describes actual purpose (unit registry) | 190 |
| `qnty/variable_system/core.py` | `qnty/variables/quantities.py` | Describes content (FastQuantity, TypeSafeVariable) | 426 |

### **System Directory Consolidation**

| Current Path | Proposed Path | Reason | Lines |
|--------------|---------------|--------|-------|
| `qnty/equation_system/equation.py` | `qnty/equation.py` | Single file doesn't need directory | 379 |
| `qnty/logging_system/logging.py` | `qnty/logging.py` | Single file doesn't need directory | 41 |
| `qnty/problem_system/checks.py` | `qnty/checks.py` | Extract public functionality | 158 |

### **Descriptive Renames**

| Current Path | Proposed Path | Reason | Lines |
|--------------|---------------|--------|-------|
| `qnty/problem_system/metaclass.py` | `qnty/problem_internals/composition_meta.py` | More descriptive | 294 |
| `qnty/solver_system/base.py` | `qnty/solver/solver_base.py` | Avoid generic "base" | 89 |
| `qnty/unit_system/base.py` | `qnty/units/module_base.py` | More specific | 54 |
| `qnty/variable_system/base.py` | `qnty/variables/module_base.py` | More specific | 64 |

## **Proposed Complete Structure**

```
qnty/
├── __init__.py                              # PUBLIC API (127 lines)
│
├── # === PUBLIC MODULES ===
├── variable_types.py                        # All variable types (10,725 lines) [RENAMED from variables.py]
├── problem.py                              # Problem class (1,244 lines)
├── expression.py                           # Expression utilities (683 lines)
├── checks.py                               # add_check function (158 lines) [MOVED]
│
├── # === INTERNAL MODULES ===
├── equation.py                             # Equation system (379 lines) [MOVED]
├── logging.py                              # Logging utilities (41 lines) [MOVED]
├── unit_constants.py                       # Unit constant classes (8,119 lines) [RENAMED from units.py]
│
├── # === INTERNAL DIRECTORIES ===
├── units/                                  # Unit system [RENAMED from unit_system/]
│   ├── __init__.py                        # (0 lines)
│   ├── registry.py                        # Unit registry & definitions (190 lines) [RENAMED from core.py]
│   ├── dimension.py                       # Dimensional analysis (349 lines)
│   ├── prefixes.py                        # SI prefixes (250 lines)
│   └── module_base.py                     # Abstract base class (54 lines) [RENAMED from base.py]
│
├── variables/                              # Variable system [RENAMED from variable_system/]
│   ├── __init__.py                        # (6 lines)
│   ├── quantities.py                      # FastQuantity, TypeSafeVariable (426 lines) [RENAMED from core.py]
│   ├── typed_variable.py                  # Typed implementations (215 lines)
│   ├── expression_variable.py             # Mathematical operations (314 lines)
│   └── module_base.py                     # Abstract base class (64 lines) [RENAMED from base.py]
│
├── solver/                                 # Solver system [RENAMED from solver_system/]
│   ├── __init__.py                        # (19 lines)
│   ├── solver_base.py                     # Base solver class (89 lines) [RENAMED from base.py]
│   ├── manager.py                         # Solver manager (88 lines)
│   ├── iterative.py                       # Iterative solver (182 lines)
│   └── simultaneous.py                    # Simultaneous solver (516 lines)
│
└── problem_internals/                      # Problem internals [RENAMED from problem_system/]
    ├── __init__.py                        # (0 lines)
    ├── composition_meta.py                # Composition metaclass (294 lines) [RENAMED from metaclass.py]
    ├── dependency_graph.py                # Dependency analysis (354 lines)
    ├── equation_reconstruction.py         # Equation reconstruction (1,037 lines)
    └── composition.py                     # Problem composition (337 lines)
```

## **Import Path Changes**

### **Public API (Updated)**
```python
# NEW public imports
from qnty.variable_types import Length, Pressure  # Changed from qnty.variables
from qnty.problem import Problem
from qnty.expression import cond_expr
from qnty.checks import add_check  # New location
```

### **Internal Imports (Need Updates)**
```python
# OLD → NEW
from qnty.units import LengthUnits → from qnty.unit_constants import LengthUnits
from qnty.variables import Length → from qnty.variable_types import Length
from qnty.unit_system.core import registry → from qnty.units.registry import registry
from qnty.variable_system.core import FastQuantity → from qnty.variables.quantities import FastQuantity
from qnty.equation_system.equation import Equation → from qnty.equation import Equation
from qnty.logging_system.logging import get_logger → from qnty.logging import get_logger
from qnty.solver_system.manager import SolverManager → from qnty.solver.manager import SolverManager
from qnty.problem_system.checks import add_check → from qnty.checks import add_check
```

## **Alternative: Keep Public Files, Rename Directories Only**

If you prefer to keep `variables.py` and `units.py` as the public interface:

```
qnty/
├── variables.py                            # PUBLIC: All variable types (keep name)
├── units.py                                # INTERNAL: Unit constants (keep name) 
├── problem.py                              # PUBLIC: Problem class
├── expression.py                           # PUBLIC: Expression utilities
├── checks.py                               # PUBLIC: add_check function
├── equation.py                             # INTERNAL: Equation system
├── logging.py                              # INTERNAL: Logging utilities
│
├── unit_internals/                         # INTERNAL [RENAMED from unit_system/]
├── variable_internals/                     # INTERNAL [RENAMED from variable_system/]  
├── solver/                                 # INTERNAL [RENAMED from solver_system/]
└── problem_internals/                      # INTERNAL [RENAMED from problem_system/]
```

## **Recommended Approach**

**Option A: Full Rename** (variable_types.py, unit_constants.py)
- Most consistent with directory names
- Clear separation between public files and internal directories
- Requires updating import paths

**Option B: Directory Rename Only** (keep variables.py, units.py)
- Less disruptive to existing code
- Still achieves clean directory structure
- May cause some confusion with similar names

Which approach do you prefer?