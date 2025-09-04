# qnty Architecture Structure

This document captures the current (simplified) vs proposed refactored package structure, plus a migration mapping.

## Legend

- (new) newly introduced file/package
- (move) file moved (same name)
- (rename) renamed for clarity
- (split) file contents split across multiple modules
- (facade) public re-export surface
- (deprecate) temporary shim maintained one release cycle

---

## Current (condensed) Structure

```text
qnty/
  __init__.py
  quantity.py               (facade to generated quantities)
  quantity.pyi
  equation.py               (Equation + EquationSystem)
  expression.py             (all expression nodes + helpers + caches)
  problem.py                (Problem monolith: variables, equations, solving, composition, validation glue)
  validation.py             (Validation dataclass + validate())
  generated/
    quantities.py
    units.py
    dimensions.py
    setters.py
  quantities/
    __init__.py (FastQuantity, TypeSafeVariable re-export)
    base.py
    core.py
    expression_variable.py
    typed_variable.py
  units/
    __init__.py
    base.py
    core.py
    prefixes.py
  engines/
    problem/
      composition.py
      dependency_graph.py
      equation_reconstruction.py
      metaclass.py
    solver/
      base.py
      iterative.py
      manager.py
      simultaneous.py
  utils/
    logging.py
scripts/ (code generation numbered scripts)
```

---

## Proposed Target Structure

```text
qnty/
  __init__.py                 (facade: curated public API)
  api.py                      (optional explicit export map) (new)

  expressions/                (split expression system)
    __init__.py               (exports Expression, nodes, helpers) (new)
    nodes.py                  (Expression, VariableReference, Constant, BinaryOperation, UnaryFunction, ConditionalExpression) (split)
    functions.py              (sin, cos, tan, sqrt, abs_expr, ln, log10, exp, min_expr, max_expr, cond_expr) (split)
    cache.py                  (dimensionless + expression result caches) (new)

  equations/
    __init__.py               (exports Equation, EquationSystem) (new)
    equation.py               (moved from equation.py) (move)
    system.py                 (EquationSystem split out) (split)

  quantities/
    __init__.py               (lazy facade replaces quantity.py) (rename+move)
    fast_quantity.py          (FastQuantity) (split)
    variable.py               (TypeSafeVariable + related logic) (split)
    typed_variable.py         (from typed_variable.py) (move)
    base.py                   (if still needed) (move)

  units/
    __init__.py               (public unit constructors, high-level aliases)
    base.py                   (abstract unit + dimension base classes)
    core.py                   (concrete fundamental & derived unit definitions, conversion logic)
    prefixes.py               (metric/system prefixes & application helpers)

  problem/
    __init__.py               (exports Problem)
    base.py                   (core Problem state & init) (split)
    variables.py              (add/get/placeholder logic) (split)
    equations.py              (equation processing, reconstruction hooks) (split)
    composition.py            (sub-problem integration + composites) (move)
    solving.py                (solve(), verify, dependency graph build) (split)
    validation.py             (Problem-side hook integration) (new)
    reconstruction.py         (from equation_reconstruction.py) (rename)
    metaclass.py              (move from engines/problem) (move)

  solving/                    (renamed engines + solver infra)
    __init__.py
    dependency_graph.py       (move)
    manager.py                (from engines/solver/manager.py) (move)
    reconstruction.py         (optionally co-locate generic reconstruction helpers) (optional)
    solvers/
      __init__.py
      base.py                 (move)
      iterative.py            (move)
      simultaneous.py         (move)

  validation/
    __init__.py               (exports Validation, rule) (new)
    rules.py                  (Validation dataclass + rule factory) (rename from validation.py)
    registry.py               (future extensibility) (new)

  generated/                  (all auto-generated artifacts; single regeneration target)
    units.py                  (auto-generated unit symbols & category groupings)
    dimensions.py             (auto-generated dimension signatures/objects)
    quantities.py             (auto-generated quantity class/type registry)
    setters.py                (auto-generated setter helpers / dynamic property glue)

  utils/
    __init__.py
    logging.py

  codegen/                    (scripts → structured codegen API) (rename)
    __init__.py
    cli.py                    (unified entry point) (new)
    generators/
      dimensions.py           (from scripts)
      units.py
      variables.py
      stubs.py                (variable_pyi logic)

  docs/                       (documentation set) (new)
    architecture.md
    migration.md
```

---

## Current → Proposed Mapping (Selective)

| Current                                 | Proposed                                       | Notes |
|-----------------------------------------|------------------------------------------------|-------|
| expression.py                           | expressions/nodes.py + functions.py + cache.py | Split for clarity |
| equation.py                             | equations/equation.py & equations/system.py     | Separate system logic |
| problem.py                              | problem/*.py (base, variables, equations, etc.) | Decompose monolith |
| engines/problem/metaclass.py            | problem/metaclass.py                            | Move closer to Problem |
| engines/problem/equation_reconstruction.py | problem/reconstruction.py                     | Rename clearer scope |
| engines/problem/dependency_graph.py     | solving/dependency_graph.py                     | Lives with solving infra |
| engines/solver/*.py                     | solving/solvers/*.py & solving/manager.py       | Rename package |
| validation.py (validate())              | validation/rules.py (rule())                    | Avoid name collision |
| quantity.py facade                      | quantities/__init__.py                          | Consolidate API |
| scripts/_N_generate_*.py                | codegen/generators/*.py + codegen/cli.py        | Structured CLI |
| generated/units.py, dimensions.py       | generated/units.py, generated/dimensions.py     | Keep consolidated generated root |

---

## Public API (Intended)

```python
from qnty import (
  Problem,
  Variable,            # alias of TypeSafeVariable
  Quantity,            # alias of FastQuantity
  Equation,
  rule,                # validation rule factory
  min_expr, max_expr, cond_expr,
  units, prefixes
)
```

Internal modules (not imported from top-level) considered unstable / subject to change.

---

## Migration Phases (Abbrev.)

1. Introduce new packages + copies (dual path), add shim re-exports.
2. Split `problem.py`, move solver infra to `solving/`.
3. Replace `validate()` with `rule()`; keep deprecated alias one release.
4. Consolidate facade (`quantity.py` → `quantities/__init__.py`).
5. Move generated units under `units/generated/` & refactor codegen.
6. Remove shims & deprecated names after deprecation window.

---

## Notes

- Keep backward compatibility via re-export modules emitting DeprecationWarning.
- Add `docs/migration.md` detailing one-release deprecation policy.
- Consider introducing enums for severity levels in validation (future).
- Ensure unidirectional dependency: expressions → equations → problem → solving → validation (no reverse imports).

---
Generated: 2025-09-03

---

## Detailed File Responsibilities (Proposed Structure)

This section defines authoritative intent for every file/directory in the proposed layout. Use it as a checklist when refactoring. Each entry lists: Purpose, Core Contents, Excludes (explicit non-goals), Dependencies (allowed inbound), and Stability target.

### Top-Level

`qnty/__init__.py`

- Purpose: Single public facade. Re-export stable API (Problem, Variable, Quantity, Equation, rule, expression helpers, unit namespace).
- Core Contents: `__all__`, import proxies, optional version metadata, deprecation shims.
- Excludes: Business logic, heavy imports at module import time (lazy where possible), experimental symbols.
- Depends On: `api.py` (optional), underlying packages.
- Stability: High.

`qnty/api.py` (optional but recommended)

- Purpose: Central definition of public surface; prevents cyclical imports in `__init__`.
- Core Contents: Imports + mapping dictionaries (e.g. `PUBLIC_SYMBOLS`), helper `def export()` if needed.
- Excludes: Execution logic, side effects.
- Depends On: All implementation modules (read-only).
- Stability: High (but internal).

### Expression System (`expressions/`)

`expressions/__init__.py`

- Purpose: Curated exports: `Expression`, node classes, helper constructors (min_expr), enabling `from qnty.expressions import Expression`.
- Core Contents: Lightweight re-export; MAY implement lazy imports.
- Excludes: Node implementations.
- Depends On: `.nodes`, `.functions`.
- Stability: High.

`expressions/nodes.py`

- Purpose: Core AST node classes (`Expression`, `VariableReference`, `Constant`, `BinaryOperation`, `UnaryFunction`, `ConditionalExpression`).
- Core Contents: Class definitions, evaluation protocol, simplification, caching hooks (interfaces only), minimal internal helpers.
- Excludes: Math convenience wrappers, global caches implementation, domain-specific functions.
- Depends On: `quantities.fast_quantity` (for `FastQuantity`), `units` (dimensionless unit), _never_ on `equations` or `problem`.
- Stability: High after refactor; modifications need benchmark review.

`expressions/functions.py`

- Purpose: Functional helper API (sin, cos, tan, sqrt, ln, log10, exp, abs_expr, min_expr, max_expr, cond_expr).
- Core Contents: Thin wrappers returning node instances; no heavy logic.
- Excludes: Evaluation algorithm changes, caching.
- Depends On: `.nodes` only.
- Stability: Medium (easy to extend).

`expressions/cache.py`

- Purpose: Encapsulate caches (dimensionless constant pool, expression result cache, type-check caches) with clear eviction strategies.
- Core Contents: Cache containers, accessor functions, instrumentation (optional debug counters), reset utilities for tests.
- Excludes: Core node logic, problem solving logic.
- Depends On: Minimal primitive types; MAY import `FastQuantity`.
- Stability: Medium.

### Equations (`equations/`)

`equations/__init__.py`

- Purpose: Export `Equation`, `EquationSystem`.
- Core Contents: Re-exports.
- Stability: High.

`equations/equation.py`

- Purpose: Representation + logic for a single equation binding (lhs = rhs) with residual checking.
- Core Contents: `Equation` class, solving predicates (`can_solve_for`), direct-assignment solve path, residual check.
- Excludes: Multi-equation orchestration, dependency ordering, solver algorithms.
- Depends On: `expressions.nodes`, `quantities.variable`.
- Stability: High.

`equations/system.py`

- Purpose: Lightweight container orchestrating iterative direct-solve passes.
- Core Contents: `EquationSystem` class, known/unknown cache, solving order detection.
- Excludes: Advanced symbolic manipulation, graph algorithms (those move to `solving/`).
- Depends On: `equations.equation`.
- Stability: Medium-High.

### Quantities (`quantities/`)

`quantities/__init__.py`

- Purpose: Public quantity/variable facade & lazy loader for generated quantity classes if needed.
- Core Contents: Re-exports `FastQuantity`, `TypeSafeVariable`, optionally dynamic import of auto-generated quantity types.
- Excludes: Implementation details of arithmetic or variable semantics.
- Depends On: `fast_quantity.py`, `variable.py`, generated artifacts.
- Stability: High.

`quantities/fast_quantity.py`

- Purpose: High-performance numeric-with-unit container; core arithmetic & unit conversions.
- Core Contents: `FastQuantity` class, operator overloads, `.to()` conversion, dimensional signature storage.
- Excludes: Variable semantics, expression tree logic, solver logic.
- Depends On: `units` definitions.
- Stability: High; changes require perf tests.

`quantities/variable.py`

- Purpose: Type-safe variable abstraction bridging domain values and expression/equation references.
- Core Contents: `TypeSafeVariable`, properties (`symbol`, `name`, `quantity`, `is_known`), state mutation helpers (`mark_known`, `mark_unknown`), validation hook list.
- Excludes: Problem-scoped caching, solving order logic.
- Depends On: `fast_quantity.py`.
- Stability: High.

`quantities/typed_variable.py`

- Purpose: Specialized variable subclasses (if any) for domain-specific expectations (dimension-checking wrappers, typed constructors).
- Core Contents: Optional subclass definitions (e.g., `PressureVariable`).
- Excludes: Generic variable base implementation duplication.
- Depends On: `variable.py`.
- Stability: Medium.

`quantities/base.py`

- Purpose: Legacy or shared base components; consider deprecating if redundant.
- Core Contents: Common mixins (maybe dimension expectation enforcement), shared error types.
- Excludes: Arithmetic.
- Stability: Low (candidate for consolidation).

### Units & Dimensions (`units/` + `generated/`)

`units/__init__.py`

- Purpose: Provide user-friendly unit access (e.g. `from qnty.units import m, s, Pa`).
- Core Contents: Re-exports, maybe lazy resolution, group dictionaries.
- Excludes: Core classes.
- Depends On: `units/base.py`, `units/core.py`, generated units.
- Stability: High.

`units/base.py`

- Purpose: Abstract base classes / protocols for Unit, Dimension; hashing & equality semantics.
- Core Contents: ABCs, lightweight registry hooks, dimension signature utilities.
- Excludes: Concrete unit instantiation.
- Stability: High.

`units/core.py`

- Purpose: Concrete fundamental & derived unit definitions; unit registry assembly.
- Core Contents: Unit construction functions, canonical dimension definitions (if not generated), combination helpers.
- Excludes: Auto-generated enumerations (live in `generated/units.py`).
- Stability: Medium.

`units/prefixes.py`

- Purpose: Metric/binary prefix definitions and application helpers.
- Core Contents: Data tables, `apply_prefix()` utilities.
- Stability: High.

`generated/units.py`

- Purpose: Machine-generated list of unit instances & symbol maps.
- Core Contents: Constant definitions only; no logic.
- Excludes: Manual edits (regenerate via codegen).
- Stability: Regenerated (treat as derived artifact).

`generated/dimensions.py`

- Purpose: Generated dimension signatures & dimension objects.
- Core Contents: `Dimension` instances keyed by canonical names / signatures.
- Stability: Regenerated.

`generated/quantities.py`

- Purpose: Generated typed Quantity classes per dimension.
- Core Contents: Class definitions (e.g., `Pressure`, `Length`), linking to base `TypeSafeVariable` or convenience wrappers.
- Stability: Regenerated; public names stable.

`generated/setters.py`

- Purpose: Auto-created setter helpers / convenience assignment functions.
- Stability: Regenerated.

### Problem Domain (`problem/`)

`problem/__init__.py`

- Purpose: Export `Problem` after assembling from modular parts.
- Depends On: Local modules.

`problem/base.py`

- Purpose: Core `Problem` dataclass/state: initialization, storage dictionaries, logger, caches.
- Core Contents: `__init__`, `_invalidate_caches`, `copy`, repr/str.
- Excludes: Variable addition logic, solving.

`problem/variables.py`

- Purpose: Variable lifecycle management.
- Core Contents: `add_variable(s)`, `get_variable`, placeholder creation, caching of known/unknown subsets.
- Excludes: Equation logic.

`problem/equations.py`

- Purpose: Equation ingestion & normalization pipeline.
- Core Contents: `_process_equation`, missing variable handling, validation of self-references, reconstruction triggers.
- Excludes: Actual solving, dependency graphs.

`problem/composition.py`

- Purpose: Sub-problem namespace flattening and composite equation synthesis.
- Core Contents: Namespace variable cloning, auto min/max composites, alias mapping.
- Excludes: Generic equation parsing.

`problem/solving.py`

- Purpose: High-level solve orchestration calling into `solving/` layer.
- Core Contents: `solve()`, `_build_dependency_graph`, `verify_solution`, attribute synchronization.
- Excludes: Graph algorithm internals (delegated).

`problem/reconstruction.py`

- Purpose: Equation reconstruction / delayed expressions (formerly `equation_reconstruction`).
- Core Contents: Heuristics to transform composite variable references, delayed condition resolution.
- Excludes: Core equation evaluation.

`problem/metaclass.py`

- Purpose: Collect class-level variables/equations/checks into Problem subclass definitions at class creation time.
- Core Contents: `ProblemMeta` implementing `__new__` / `__init_subclass__` patterns.
- Excludes: Runtime solving operations.

`problem/validation.py`

- Purpose: Glue: attach validation rule objects to problems; integrate run pipeline.
- Excludes: Rule definitions (in `validation/rules.py`).

### Solving Layer (`solving/`)

`solving/__init__.py`

- Purpose: Export solver interfaces for advanced users.

`solving/dependency_graph.py`

- Purpose: Build and analyze variable dependency DAG from equations.
- Core Contents: Graph data structure, cycle detection, topological ordering, analysis summary.
- Excludes: Numeric solving algorithms.

`solving/manager.py`

- Purpose: Strategy coordinator; chooses solver (iterative vs simultaneous) based on heuristics.
- Core Contents: `SolverManager` with `solve()` dispatch producing `SolveResult`.
- Excludes: Actual algorithm implementation.

`solving/solvers/base.py`

- Purpose: Abstract solver interface + shared `SolveResult`, error types.

`solving/solvers/iterative.py`

- Purpose: Simple iterative direct-assignment pass with fallback loops.
- Core Contents: Convergence logic, iteration cap, tolerance checks.

`solving/solvers/simultaneous.py`

- Purpose: (Optional) Solve small coupled systems simultaneously (future expansion: linearization, numeric solver integration).

`solving/reconstruction.py` (optional)

- Purpose: Shared reconstruction utilities if reused across problem modules.

### Validation (`validation/`)

`validation/__init__.py`

- Purpose: Export `Validation`, `rule` (factory), optional severity Enum.

`validation/rules.py`

- Purpose: Rule dataclass & factory; evaluation context bridging expression to boolean.
- Core Contents: `Validation` dataclass, `rule()` (or `define_check()`), severity enumeration, error capturing.
- Excludes: Problem integration.

`validation/registry.py`

- Purpose: (Future) Central registration for pluggable rule sets or custom categories.

### Code Generation (`codegen/`)

`codegen/__init__.py`

- Purpose: Simple tag; MAY expose high-level generate() for programmatic use.

`codegen/cli.py`

- Purpose: Command-line interface bundling generation tasks.
- Core Contents: Argument parsing, selection of generator modules, concurrency handling.

`codegen/generators/dimensions.py`

- Purpose: Generate `generated/dimensions.py` from JSON or spec.
- Core Contents: Template writer, stable ordering.

`codegen/generators/units.py`

- Purpose: Generate `generated/units.py` mapping names → units.

`codegen/generators/variables.py`

- Purpose: Generate variable/quantity class skeletons (quantities.py) from dimension data.

`codegen/generators/stubs.py`

- Purpose: Generate `.pyi` typing stubs for IDE support (`quantity.pyi`).

### Utilities

`utils/logging.py`

- Purpose: Central logging configuration with env overrides.
- Excludes: Application logic.

### Testing Strategy (Not files, but mapping)

- Unit tests should mirror packages: `tests/expressions/test_nodes.py`, `tests/problem/test_solving.py`, etc.
- Generated artifacts: lightweight smoke tests verifying a sample of symbol presence and conversions.

### Dependency Direction Summary

`units` → `quantities` → `expressions` → `equations` → `problem` → `solving` → `validation`
Utilities & generated code are leaf/shared; no upward imports (avoid `problem` importing from `solving/validation` except via defined interfaces).

### Extension Points

- Add new solver: create `solving/solvers/<name>.py`, register in `manager.py` dispatch table.
- Add new function expression: add in `expressions/functions.py`; no edits to nodes unless structural.
- Add new validation category: extend enum in `validation/rules.py` and optional registry entry.

### Non-Goals Clarification

- No ORM / persistence layer in problem domain (keep pure computational model).
- No runtime reflection-based auto-solving beyond deterministic direct solve heuristics.
- No heavy symbolic algebra (delegate to external library if needed in future adapter module).

---
