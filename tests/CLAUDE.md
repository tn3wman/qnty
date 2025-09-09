# Pytest Test Authoring Rules

## Global goals**

- Use `pytest` with clear Arrange-Act-Assert sections.
- Prefer table-driven tests via `pytest.mark.parametrize`.
- Expected values must be **hard-coded** or sourced from **independent references**, never computed by the function or module under test.
- Keep tests deterministic: control randomness, time, environment.

---

## 1) Hard-coded oracle rule (non-negotiable)

- **DO** write expected values as literals (numbers/tuples/strings/dicts) in the test file.
- **DO** cite the origin (comment) if derived from an external reference (standard, spreadsheet, manual calc).
- **DON’T** compute expected values by calling:
  - the function under test,
  - helpers from the same module,
  - the same algorithm re-implemented inline.
- **DON’T** “prove identity” by comparing a thing to itself (e.g., calling the function twice).

### Bad

```python
expected = mymod.f(x)        # ❌ same function
```

### Good

```python
# From design doc example (section 3.2) and hand calc checked 2025-09-09
expected = 42.75
```

---

## 2) Parametrized, table-driven tests

- Use `@pytest.mark.parametrize` with a compact table of `inputs -> expected`.
- For floats, compare with `math.isclose` or `pytest.approx`.

### Example

```python
import math
import pytest

from mypkg.mymod import area_of_ring

@pytest.mark.parametrize(
    "ro, ri, expected",
    [
        (5.0, 3.0, math.pi * (5.0**2 - 3.0**2)),  # Derived from definition
        (2.0, 1.0, 3 * math.pi),                  # Literal
        (10.0, 0.0, 100 * math.pi),
    ],
)
def test_area_of_ring(ro, ri, expected):
    got = area_of_ring(ro, ri)
    assert got == pytest.approx(expected, rel=1e-12, abs=1e-12)
```

---

## 3) Clear naming and structure

- File: `tests/test_<module>_<topic>.py`
- Test names: `test_<function>_<case>`
- Keep one assertion per behavioral aspect; multiple asserts are fine if they check **distinct** facets.

---

## 4) Floating-point comparisons

Use tight, explicit tolerances:

```python
assert got == pytest.approx(expected, rel=1e-9, abs=1e-12)
```

- Prefer **small** tolerances. Widen only with justification.

---

## 5) Edge cases & error behavior

Always include:

- Smallest/zero/negative inputs (where defined),
- Boundary values,
- Non-finite values (NaN/inf) if supported,
- Invalid inputs raising errors:

```python
with pytest.raises(ValueError, match="radius must be positive"):
    circle_area(-1)
```

---

## 6) Determinism (randomness, time, env)

- Random: set seed **inside** test or fixture.

```python
import random
random.seed(1234)
```

- Time: freeze/patch time or inject clock dependency.
- Env: use `monkeypatch`.

---

## 7) I/O and filesystem

- Use `tmp_path` or `tmp_path_factory`.
- Validate both **content** and **metadata** you care about.

---

## 8) Fixtures

- Keep fixtures **small and explicit**.
- Store golden files under `tests/data/`.
- Document provenance for goldens.

---

## 9) Property checks (optional add-on)

- Light property assertions are OK **in addition** to hard-coded cases.
- Still include at least 3–5 literal examples first.

---

## 10) Regression tests

When a bug is found:

- Add a minimal failing input with a **hard-coded expected value**.
- Reference the issue ID or root cause in a comment.

---

## 11) Coverage of API surface

For each public function/class:

- Happy path examples (2–5 cases),
- Edge/boundary cases,
- Error behavior,
- Type variations (ints vs floats, etc.).

---

## 12) Prohibited patterns (auto-reject)

- Calling the function under test to compute `expected`.
- Snapshotting outputs without external justification.
- Broad excepts or vague truthiness checks.
- Hidden global state reliance.

---

## 13) Minimal boilerplate templates

### Numeric function

```python
import math
import pytest
from mypkg.mymod import bernoulli_pressure

@pytest.mark.parametrize(
    "p1, v1, rho, expected",
    [
        # Hand-calc (sheet “Bernoulli-A”, checked 2025-09-09)
        (101325.0, 3.0, 1.225, 101325.0 + 0.5 * 1.225 * (3.0**2)),
        (200000.0, 0.0, 1.225, 200000.0),
    ],
)
def test_bernoulli_pressure_basic(p1, v1, rho, expected):
    got = bernoulli_pressure(p1, v1, rho)
    assert got == pytest.approx(expected, rel=1e-10, abs=1e-12)
```

### Error paths

```python
import pytest
from mypkg.mymod import safe_sqrt

@pytest.mark.parametrize("x", [-1.0, -0.0 - 1e-15])
def test_safe_sqrt_raises_on_negative(x):
    with pytest.raises(ValueError, match="nonnegative"):
        safe_sqrt(x)
```

### Filesystem

```python
def test_write_report_creates_expected_file(tmp_path):
    out = tmp_path / "report.txt"
    write_report(["a", "b"], out)
    assert out.exists()
    assert out.read_text(encoding="utf-8") == "a\nb\n"
```

---

## 14) Docstring examples

If the docstring has examples with outputs:

- Add them as tests with **exact inputs and outputs**.

---

## 15) Style & speed

- Tests must run in seconds.
- Prefer clarity over cleverness.

---

### Final checklist for each test PR

- [ ] Expected values are hard-coded or from independent source.
- [ ] No calls to the implementation for expected values.
- [ ] Deterministic (seed/time/env controlled).
- [ ] Includes happy path, edges, and errors.
- [ ] Explicit tolerances for floats.
- [ ] Uses tmp paths for I/O.
- [ ] Names and comments make intent obvious.
