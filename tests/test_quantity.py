import cProfile
import json
import os
import pstats
import sys
import time
from pathlib import Path

import pytest

from qnty.core.dimension_catalog import dim
from qnty.core.quantity import Q, Quantity
from qnty.core.unit import ureg
from qnty.core.unit_catalog import LengthUnits


def test_quantity_construction_and_str():
    q_m = Q(2.5, LengthUnits)
    assert isinstance(q_m, Quantity)
    assert q_m.dim == dim.L
    # Default preferred is preferred unit of LengthUnits (meter)
    s = str(q_m)
    assert "m" in s and ("2.5" in s or "2.500" in s)

    # From_value factory (resolve explicit unit object)
    unit_m = ureg.resolve("meter") or ureg.resolve("m")
    assert unit_m is not None
    q2 = Quantity.from_value(100, unit_m, name="len")
    assert q2.dim == dim.L and q2.is_known
    # Round-trip conversion via to()
    q2_in_m = q2.to("meter")
    assert q2_in_m.value is not None and abs(q2_in_m.value - 100) < 1e-12


def test_quantity_set_and_unit_changers():
    q = Quantity.unknown("L", dim.L)
    q1 = q.set(1.0).meter
    assert isinstance(q1, Quantity) and q1.is_known
    assert q1.to("meter").value == pytest.approx(1.0)

    # .to and .as_unit helpers
    q_m = Q(1.0, LengthUnits)
    q_mm = q_m.to_unit.millimeter
    assert q_mm.preferred is not None and q_mm.preferred.symbol in ("mm", "millimeter")
    # as_unit keeps the numeric display (value changes internally)
    q_as_m = q_mm.as_unit.meter
    assert q_as_m.preferred is not None and q_as_m.preferred.symbol == "m"


def test_quantity_arithmetic_and_comparisons():
    a = Q(10.0, LengthUnits)
    b = Q(5.0, LengthUnits)
    c = a + b
    assert c.dim == dim.L and c.value == pytest.approx(10.0 + 5.0)

    d = a - b
    assert d.dim == dim.L and d.value == pytest.approx(10.0 - 5.0)

    e = a * b
    assert e.dim == (dim.L * dim.L)

    f = a / b
    assert f.dim == (dim.L / dim.L)

    # power
    g = a ** 2
    assert g.dim == (dim.L ** 2)

    # comparisons
    a2 = Q(10.0, LengthUnits)
    b2 = Q(10.0, LengthUnits)
    c2 = Q(9.0, LengthUnits)
    assert a2 == b2
    assert a2 != c2
    assert c2 < a2
    assert a2 > c2
    assert c2 <= a2
    assert a2 >= c2

    # numeric + dimensionless
    dless = Q(2.0, "dimensionless")
    assert float(dless) == pytest.approx(2.0)
    assert (3 + dless).value == pytest.approx(5.0)
    assert (3 - dless).value == pytest.approx(1.0)
    assert (3 * dless).value == pytest.approx(6.0)
    assert (3 / dless).dim == (dim.D ** -1)  # 1/dimensionless


def _run_quantity_benchmark(iterations: int = 20000) -> dict:
    # use string-based conversions to avoid dynamic-attr typing issues
    # Warmup
    warmup = max(1000, iterations // 10)
    for _ in range(warmup):
        q = Q(100.0, LengthUnits)
        _ = q.to_unit.millimeter
        _ = q.to("meter")
        _ = (q * q)
        _ = (q / q)
        _ = (q ** 2)

    def workload():
        res = 0
        q = Q(100.0, LengthUnits)
        for _ in range(iterations):
            q_mm = q.to_unit.millimeter
            q_back = q_mm.to("meter")
            a = q * q_back
            b = q / q_back
            c = q ** 2
            # comparisons
            _cmp = (q_back == q)
            # values are guaranteed non-None for arithmetic results; assert to aid type checkers
            assert a.value is not None and b.value is not None and c.value is not None
            res ^= hash((int(_cmp), int(a.value), int(b.value), int(c.value)))
        return res

    profiler = cProfile.Profile()
    start = time.perf_counter()
    profiler.enable()
    res = workload()
    profiler.disable()
    end = time.perf_counter()

    assert isinstance(res, int)

    stats = pstats.Stats(profiler)
    total_calls = 0
    raw_stats = getattr(stats, "stats", {})
    for (filename, _lineno, _funcname), stat in raw_stats.items():
        if os.path.sep + "core" + os.path.sep + "quantity.py" in filename:
            total_calls += stat[1]

    total_time = end - start
    # per loop ops we count: 1 conv (.to_unit), 1 conv (.to()), 1 mul, 1 div, 1 pow, 1 cmp = 6
    ops_per_loop = 6
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
        "quantity_calls": total_calls,
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


def test_quantity_performance_regression(tmp_path: Path):
    metrics = _run_quantity_benchmark(iterations=20000)

    perf_dir = Path(__file__).parent / ".perf"
    log_path = perf_dir / "quantity_performance.jsonl"

    last = _read_last_record(log_path)
    _append_perf_log(metrics, log_path)

    if last and last.get("ops_per_loop") == metrics["ops_per_loop"]:
        # Time guardrail: ≤ 2x slower
        prev_t = float(last.get("time_per_op_ns", 0) or 0)
        curr_t = float(metrics["time_per_op_ns"])
        if prev_t > 0:
            ratio = curr_t / prev_t
            assert ratio <= 2.0, (
                f"Quantity ops slowed {ratio:.2f}x (prev {prev_t:.1f} ns/op, now {curr_t:.1f} ns/op)"
            )

        # Function call budget: ≤ 25% more per iteration
        prev_calls = int(last.get("quantity_calls", 0) or 0)
        curr_calls = int(metrics["quantity_calls"])
        prev_norm = prev_calls / max(int(last.get("iterations", 1)), 1)
        curr_norm = curr_calls / max(int(metrics.get("iterations", 1)), 1)
        call_ratio = curr_norm / max(prev_norm, 1e-12)
        assert call_ratio <= 1.25, (
            f"Function call count increased {call_ratio:.2f}x per iteration (prev {prev_norm:.2f}, now {curr_norm:.2f})"
        )

