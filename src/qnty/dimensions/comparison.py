# Create and run a quantity-arithmetic perf comparing prime vs tuple 7D modules.
import importlib.util, sys, time

prime_path = "src/qnty/dimensions/prime_encoding_demo_7d.py"
tuple_path = "src/qnty/dimensions/tuple_encoding_demo_7d.py"

def load_module_from_path(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

prime_mod = load_module_from_path(prime_path, "prime7d")
tuple_mod = load_module_from_path(tuple_path, "tuple7d")

def perf_quantity_ops(mod, n=100_000):
    # Pull symbols
    Q = getattr(mod, "Q")
    Unit = getattr(mod, "Unit")
    meter = getattr(mod, "meter")
    kilogram = getattr(mod, "kilogram")
    second = getattr(mod, "second")
    newton = getattr(mod, "newton")
    pascal = getattr(mod, "pascal")
    foot = getattr(mod, "foot")
    psi = getattr(mod, "psi")
    L = getattr(mod, "L")
    T = getattr(mod, "T")
    Force = getattr(mod, "Force")
    Pressure = getattr(mod, "Pressure")

    # Set up representative quantities
    length = Q(3.0, meter)
    mass   = Q(70.0, kilogram)
    time1  = Q(2.0, second)
    vel    = length / time1
    accel  = length / (time1**2)
    force  = mass * accel
    area   = (Q(8.0, foot) * Q(12.0, foot))
    press  = force / area

    # 1) mul/div loop on quantities (same-dim operations where needed)
    t0 = time.perf_counter()
    acc = Q(1.0, foot)  # use a length for dimension
    for _ in range(n):
        acc = (acc * length) / length
    t1 = time.perf_counter()
    muldiv_len = t1 - t0

    # 2) add/sub loop (same-dimension)
    t0 = time.perf_counter()
    acc = Q(20, foot)
    for _ in range(n):
        acc = acc + length - length
    t1 = time.perf_counter()
    addsub_len = t1 - t0

    # 3) mixed physics chain (force/area -> pressure), repeated
    t0 = time.perf_counter()
    accp = press
    for _ in range(n):
        # recompute simple chain but keep same dims
        accp = (force / area)  # pressure
    t1 = time.perf_counter()
    mixed_chain = t1 - t0

    # 4) conversions (to unit) loop
    t0 = time.perf_counter()
    s = 0.0
    for _ in range(n):
        s += press.to(pascal)
    t1 = time.perf_counter()
    convert_pa = t1 - t0

    t0 = time.perf_counter()
    s2 = 0.0
    for _ in range(n):
        s2 += press.to(psi)
    t1 = time.perf_counter()
    convert_psi = t1 - t0

    return {
        "muldiv_length_s": muldiv_len,
        "addsub_length_s": addsub_len,
        "pressure_chain_s": mixed_chain,
        "convert_pa_s": convert_pa,
        "convert_psi_s": convert_psi,
        "check_sum": float(s + s2)  # avoid optimizing away
    }

# Run with a modest iteration count to keep runtime reasonable here.
results = {
    "tuple_7d": perf_quantity_ops(tuple_mod, n=80_000),
    "prime_7d": perf_quantity_ops(prime_mod, n=80_000),
}

# Printing
import pprint
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(results)
