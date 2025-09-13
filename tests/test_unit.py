import cProfile
import json
import os
import pstats
import sys
import time
from pathlib import Path

from qnty.core import u
from qnty.core.dimension_catalog import dim
from qnty.core.unit import attach_composed, ureg


def test_base_units_and_dimensions():
    # Basic presence and dimensions
    assert u.meter.dim is dim.L
    assert u.second.dim is dim.T
    assert u.gram.dim is dim.M
    assert u.kg.dim is dim.M  # prefixed mass

    # Symbols
    assert u.meter.symbol == "m"
    assert u.second.symbol == "s"
    assert u.kg.symbol == "kg"


def test_us_customary_units_basic():
    # Pound mass
    assert u.pound.dim is dim.M
    assert u.lb.dim is dim.M
    assert abs(u.pound.si_factor - 0.45359237) < 1e-15
    assert u.pound.symbol == "lb"
    # Aliases resolve
    assert ureg.resolve("lbs") is u.pound
    assert ureg.resolve("lbm") is u.pound

    # Slug mass
    assert u.slug.dim is dim.M
    assert abs(u.slug.si_factor - 14.59390293720636) < 1e-12

    # Pound force
    assert u.pound_force.dim is dim.Force
    assert u.lbf.dim is dim.Force
    assert abs(u.pound_force.si_factor - 4.4482216152605) < 1e-12
    assert u.pound_force.symbol == "lbf"
    # Aliases resolve
    assert ureg.resolve("poundforce") is u.pound_force
    assert ureg.resolve("lbf") is u.pound_force


def test_composition_and_caching_identity():
    # Compose multiple times; symbol interning should return same object
    a1 = u.meter / u.second
    a2 = u.meter / u.second
    assert a1 is a2
    assert a1.symbol == "m/s"

    # Power caching by symbol
    b1 = u.meter ** 2
    b2 = u.meter ** 2
    assert b1 is b2
    assert b1.symbol in ("m²", "m^2")

    # Mixed compositions
    c1 = (u.meter ** 2) / (u.second ** 2)
    c2 = (u.meter ** 2) / (u.second ** 2)
    assert c1 is c2
    assert c1.dim == (dim.L ** 2) / (dim.T ** 2)


def test_attach_composed_reuse_and_resolve():
    # `meter_per_second` is defined in the catalog via attach_composed
    mps = u.meter_per_second
    # Re-attaching should return the existing named unit
    again = attach_composed(u.meter / u.second, name="meter_per_second", symbol="m/s")
    assert again is mps

    # Resolve by symbol and aliases
    assert ureg.resolve("m/s") is mps
    # Acceleration unit registered with aliases like m/s2
    mps2 = u.meter_per_square_second
    assert ureg.resolve("m/s2") is mps2


def test_prefix_exposure_and_preferred_units():
    # Prefixed exposure
    assert hasattr(u, "milli_meter")
    assert hasattr(u, "mm") or u.milli_meter.symbol == "mm"
    # Preferred for length should be meter
    preferred_L = ureg.preferred_for(dim.L)
    assert preferred_L is u.meter
    # SI unit for mass should be kilogram (factor 1.0)
    si_mass = ureg.si_unit_for(dim.M)
    assert si_mass is u.kg


def _run_unit_benchmark(iterations: int = 20000) -> dict:
    # Warmup
    warmup = max(1000, iterations // 10)
    for _ in range(warmup):
        _a = u.meter / u.second
        _b = u.meter ** 2
        _c = _a * _b
        _d = _b / (u.second ** 2)
        _ = (_d.dim == (dim.L ** 2) / (dim.T ** 2))

    def workload():
        res = 0
        obj = u.meter
        for _ in range(iterations):
            a = u.meter / u.second
            b = u.meter ** 2
            c = a * b
            d = b / (u.second ** 2)
            obj = c / a  # should be b
            # fold into res to avoid optimization
            res ^= hash((a.symbol, b.symbol, c.symbol, d.symbol, obj.symbol))
        return obj, res

    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    obj, res = workload()
    profiler.disable()
    end = time.perf_counter()

    # c/a should be equivalent to m^2 dimensionally (symbol may not simplify)
    assert obj.dim == (dim.L ** 2)
    assert abs(obj.si_factor - (u.meter ** 2).si_factor) < 1e-12
    assert isinstance(res, int)

    stats = pstats.Stats(profiler)
    total_calls = 0
    for (filename, _lineno, _funcname), stat in stats.stats.items():
        if os.path.sep + "core" + os.path.sep + "unit.py" in filename:
            total_calls += stat[1]  # ncalls

    total_time = end - start
    # count approx primitive ops per loop: 1 div, 1 pow, 1 mul, 1 div, 1 div = 5
    ops_per_loop = 5
    ops_total = iterations * ops_per_loop
    time_per_op_ns = (total_time / max(ops_total, 1)) * 1e9
    time_per_loop_ns = (total_time / max(iterations, 1)) * 1e9

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "python_version": sys.version.split()[0],
        "iterations": iterations,
        "ops_per_loop": ops_per_loop,
        "time_s": total_time,
        "time_per_loop_ns": time_per_loop_ns,
        "time_per_op_ns": time_per_op_ns,
        "unit_calls": total_calls,
    }


def _append_perf_log(record: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _read_last_record(path: Path) -> dict | None:
    if not path.exists():
        return None
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


def test_unit_performance_regression(tmp_path: Path):
    metrics = _run_unit_benchmark(iterations=20000)

    perf_dir = Path(__file__).parent / ".perf"
    log_path = perf_dir / "unit_performance.jsonl"

    last = _read_last_record(log_path)
    _append_perf_log(metrics, log_path)

    if last and last.get("ops_per_loop") == metrics["ops_per_loop"]:
        # No more than 2x slower
        prev_t = float(last.get("time_per_op_ns", 0) or 0)
        curr_t = float(metrics["time_per_op_ns"])
        if prev_t > 0:
            ratio = curr_t / prev_t
            assert ratio <= 2.0, (
                f"Unit ops slowed down {ratio:.2f}x (prev {prev_t:.1f} ns/op, now {curr_t:.1f} ns/op)"
            )

        # Function call budget: <= 25% more calls per iteration
        prev_calls = int(last.get("unit_calls", 0) or 0)
        curr_calls = int(metrics["unit_calls"])
        prev_norm = prev_calls / max(int(last.get("iterations", 1)), 1)
        curr_norm = curr_calls / max(int(metrics.get("iterations", 1)), 1)
        call_ratio = curr_norm / max(prev_norm, 1e-12)
        assert call_ratio <= 1.25, (
            f"Function call count increased {call_ratio:.2f}x per iteration (prev {prev_norm:.2f}, now {curr_norm:.2f})"
        )

