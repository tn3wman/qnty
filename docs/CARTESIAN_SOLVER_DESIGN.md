# Cartesian/Component Method Solver Design

## Overview
This document outlines the design for implementing a Cartesian/Component method solver for static force problems (problems 2-32 to 2-59 from the textbook).

## Engineering Mechanics Terminology

### Two Main Solution Methods

1. **Geometric/Trigonometric Method** (Problems 2-1 to 2-31)
   - Uses parallelogram law, triangle method
   - Law of cosines, law of sines
   - Works with magnitude and angle directly
   - Current implementation: `TriangleSolver` in `solving/triangle_solver.py`

2. **Component/Cartesian Method** (Problems 2-32 to 2-59)
   - Resolves forces into rectangular components (x, y, z)
   - Uses scalar/algebraic notation: ΣFx = 0, ΣFy = 0, ΣFz = 0
   - Cartesian vector notation: F = {Fx**i** + Fy**j** + Fz**k**}
   - Better for problems with many forces

## Proposed Architecture

### 1. Naming Convention Updates

**Current → Proposed:**
- `TrigSolver` → Keep name, but clarify it's the "Geometric/Trigonometric Solver"
- New: `ComponentSolver` or `CartesianSolver` for component method
- `VectorEquilibriumProblem` → Add `solver_method` parameter ('geometric' or 'component')

### 2. Component Solver Design

```python
class ComponentSolver:
    """
    Solves 2D/3D force equilibrium problems using the component/Cartesian method.

    Method:
    1. Resolve each force into components: Fx, Fy, (Fz)
    2. Sum components: ΣFx, ΣFy, (ΣFz)
    3. For equilibrium: ΣFx = 0, ΣFy = 0, (ΣFz = 0)
    4. For resultant: FR = √(ΣFx² + ΣFy² + ΣFz²)
    5. Direction: θx = cos⁻¹(ΣFx/FR), θy = cos⁻¹(ΣFy/FR), θz = cos⁻¹(ΣFz/FR)
    """

    def resolve_components(self, force: ForceVector) -> tuple[float, float, float]:
        """Convert force from magnitude/angle to x, y, z components."""
        pass

    def sum_components(self, forces: list[ForceVector]) -> tuple[float, float, float]:
        """Sum x, y, z components of all forces."""
        pass

    def calculate_resultant(self, sum_x, sum_y, sum_z) -> ForceVector:
        """Calculate resultant magnitude and direction from components."""
        pass

    def solve_equilibrium(self, known_forces, unknown_forces) -> dict:
        """Solve for unknowns using component equilibrium equations."""
        pass
```

### 3. Problem Types for Component Method

**Type 1: Find Resultant (Given all forces)**
- Example: Problem 2-32, 2-33, 2-40, 2-41
- Method: Sum components, calculate FR and θ

**Type 2: Express as Cartesian Vectors**
- Example: Problem 2-38, 2-42, 2-50
- Method: Resolve each force into components, express as {xi + yj + zk}

**Type 3: Find Components**
- Example: Problem 2-39
- Method: Given magnitude and angle, compute Fx and Fy

**Type 4: Find Unknown Force for Desired Resultant**
- Example: Problem 2-48, 2-57, 2-58
- Method: Set up component equations, solve for unknown magnitude and/or direction

### 4. Report Generator Design

The report should show:

1. **Force Decomposition**
   ```
   Force F1: 200 N at 45° from +x
     F1x = 200 sin(45°) = 141.4 N →
     F1y = 200 cos(45°) = 141.4 N ↑
   ```

2. **Component Summation**
   ```
   →+ ΣFx = F1x + F2x + F3x = 141.4 + (-130.0) + 0 = 11.4 N →
   ↑+ ΣFy = F1y + F2y + F3y = 141.4 + 75.0 + 0 = 216.4 N ↑
   ```

3. **Resultant Calculation**
   ```
   FR = √(ΣFx² + ΣFy²) = √(11.4² + 216.4²) = 216.7 N
   θ = tan⁻¹(ΣFy/ΣFx) = tan⁻¹(216.4/11.4) = 87.0°
   ```

4. **Cartesian Vector Form** (when requested)
   ```
   F1 = {141i + 141j} N
   F2 = {-130i + 75j} N
   FR = {11.4i + 216j} N
   ```

### 5. Integration with Existing Code

**ForceVector class:**
- Already stores both magnitude/angle AND x/y/z components
- Has `_vector` attribute with `Vector` class
- **No changes needed** - it's already designed to handle both methods!

**VectorEquilibriumProblem:**
- Add `solver_method` parameter: 'auto', 'geometric', or 'component'
- Auto-detect: Use geometric for ≤3 forces, component for >3 forces
- Route to appropriate solver

## Implementation Plan

1. ✅ Research and document terminology
2. ⏳ Create `ComponentSolver` class in `solving/component_solver.py`
3. ⏳ Add component method to `VectorEquilibriumProblem`
4. ⏳ Create `ComponentReportGenerator` in `reporting/`
5. ⏳ Add tests for problems 2-32 to 2-59
6. ⏳ Update documentation

## Notes

- The `ForceVector` class is well-designed and doesn't need changes
- Component method is actually simpler than geometric method for most cases
- The existing `Vector` class already handles component operations
- Main work is creating the solver logic and report formatting
