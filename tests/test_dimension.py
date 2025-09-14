import cProfile
import json
import os
import pstats
import sys
import time
from pathlib import Path

from qnty.core.dimension import BACKEND, Dimension, dimensions_map, write_dimensions_stub
from qnty.core.dimension_catalog import dim  # pre-populated registry


def test_basic_dimension_arithmetic():
    # dimensionless
    dless = dim.D
    assert isinstance(dless, Dimension)
    assert dless.is_dimensionless()
    assert dless.code == (1, 1)
    assert dless.exps == (0, 0, 0, 0, 0, 0, 0)

    # basic bases should compose and cancel
    L = dim.L
    M = dim.M
    T = dim.T

    length = L
    mass = M

    assert (length * mass) / mass == length
    assert length**3 == Dimension((3, 0, 0, 0, 0, 0, 0), BACKEND.pow(L.code, 3))
    assert (length / length).is_dimensionless()
    assert (length**0).is_dimensionless()

    # mixed derived: acceleration = L / T^2 (from catalog)
    acceleration = dim.ACCELERATION
    assert acceleration == (L / (T**2))


def test_dimension_equality_and_hashing():
    L = dim.L
    M = dim.M
    # Equal codes => equal dimensions
    a = L * M / M
    b = L**1
    assert a == b
    # Hash based on code, usable as dict/set keys
    s = {a, b}
    assert len(s) == 1
    assert a in s and b in s


def test_aliases_and_registry_and_stub(tmp_path: Path):
    # Aliases map to the same Dimension objects
    assert dim.LENGTH is dim.L
    assert dim.TIME is dim.T

    # Registry exposes only canonical names
    reg = dimensions_map()
    assert "L" in reg and "M" in reg and "T" in reg
    assert "LENGTH" not in reg  # aliases excluded
    assert reg["L"] is dim.L

    # Stub generation contains canonical names and alias comments
    out_file = tmp_path / "dimension_stub_test.pyi"
    write_dimensions_stub(str(out_file))
    data = out_file.read_text(encoding="utf-8")
    assert "class Dimensions:" in data
    # spot-check canonical and alias comment presence
    assert "L: Final[Dimension]" in data
    assert "alias for L" in data


def test_backend_prime_code_properties():
    # For base axes, numerator should be prime power and denominator 1
    for name in ("L", "M", "T", "A", "Θ", "N", "J"):
        d = getattr(dim, name)
        num, den = d.code
        assert den == 1
        assert isinstance(num, int)
        assert num > 1  # base is not dimensionless

    # Derived examples
    area = dim.Area
    num, den = area.code
    assert den == 1 and num > 1

    # dimensionless is exactly (1,1)
    assert dim.D.code == (1, 1)


def _run_dimension_benchmark(iterations: int = 20000) -> dict:
    """Run a micro-benchmark of core Dimension ops and return metrics + cProfile stats."""
    L = dim.L
    M = dim.M
    T = dim.T

    # Warmup to stabilize caches and JITs (if any)
    warmup = max(1000, iterations // 10)
    for _ in range(warmup):
        _x = (L * M) / M
        _y = L**3
        _z = _y / (L**2)
        _ = _z == L
        _ = hash(_z)
        # Use _x to avoid unused variable warning
        _ = _x

    def workload():
        x = L
        res = 0
        for _ in range(iterations):
            a = (L * M) / M
            b = L**3
            c = b / (L**2)
            res ^= hash(c)
            res ^= int(a == L)
            x = a * c / (T**0)  # include trivial ops; T**0 is dless
        return x, res

    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    x, res = workload()
    profiler.disable()
    end = time.perf_counter()

    # Basic sanity so Python doesn't optimize away
    assert isinstance(x, Dimension)
    assert isinstance(res, int)

    stats = pstats.Stats(profiler)
    total_calls = 0
    reduce_calls = 0
    stats_dict = getattr(stats, "stats", {})
    for (filename, lineno, funcname), stat in stats_dict.items():
        # Use lineno to avoid unused variable warning
        _ = lineno
        if os.path.sep + "core" + os.path.sep + "dimension.py" in filename:
            ncalls = stat[1]  # ncalls
            total_calls += ncalls
            if funcname == "_reduce":
                reduce_calls += ncalls

    total_time = end - start
    ops_per_loop = 7  # approx primitive ops we count per loop
    ops_total = iterations * ops_per_loop
    time_per_op_ns = (total_time / max(ops_total, 1)) * 1e9
    time_per_loop_ns = (total_time / max(iterations, 1)) * 1e9

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "python_version": sys.version.split()[0],
        "backend": type(BACKEND).__name__,
        "iterations": iterations,
        "ops_per_loop": ops_per_loop,
        "time_s": total_time,
        "time_per_loop_ns": time_per_loop_ns,
        "time_per_op_ns": time_per_op_ns,
        "dimension_calls": total_calls,
        "reduce_calls": reduce_calls,
    }


def _append_perf_log(record: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _read_last_record(path: Path) -> dict | None:
    if not path.exists():
        return None
    # Read last non-empty line
    last = None
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            last = line
    if last is None:
        return None
    try:
        return json.loads(last)
    except json.JSONDecodeError:
        return None


def test_dimension_performance_regression():
    # Run benchmark and capture metrics
    metrics = _run_dimension_benchmark(iterations=20000)

    # Persist metrics under tests/.perf
    perf_dir = Path(__file__).parent / ".perf"
    log_path = perf_dir / "dimension_performance.jsonl"

    last = _read_last_record(log_path)

    # Append first, so we always log even on assertion failure (best-effort)
    _append_perf_log(metrics, log_path)

    # Compare with previous, if compatible
    if last and last.get("backend") == metrics["backend"]:
        # Ensure configuration matches for fair comparison
        if last.get("ops_per_loop") == metrics["ops_per_loop"]:
            # Time regression guardrail: no more than 2x slower
            prev_t = float(last.get("time_per_op_ns", 0) or 0)
            curr_t = float(metrics["time_per_op_ns"])
            if prev_t > 0:
                ratio = curr_t / prev_t
                assert ratio <= 2.0, f"Dimension ops slowed down {ratio:.2f}x (prev {prev_t:.1f} ns/op, now {curr_t:.1f} ns/op)"

            # Function call budget: <= 25% more calls per run (scale by iterations)
            prev_calls = int(last.get("dimension_calls", 0) or 0)
            curr_calls = int(metrics["dimension_calls"])
            # Normalize by iterations to make comparable
            prev_norm = prev_calls / max(int(last.get("iterations", 1)), 1)
            curr_norm = curr_calls / max(int(metrics.get("iterations", 1)), 1)
            call_ratio = curr_norm / max(prev_norm, 1e-12)
            assert call_ratio <= 1.25, f"Function call count increased {call_ratio:.2f}x per iteration (prev {prev_norm:.2f}, now {curr_norm:.2f})"
