from qnty.dimensions.core import add_derived, add_dimension, write_dimensions_stub

# Canonical dimensionless (all zeros) — prime code becomes (1, 1)
D = add_dimension(
    (0,0,0,0,0,0,0),
    aliases=("DIMENSIONLESS", "DLESS", "SCALAR")
)

# (L,M,T,I,Θ,N,J)

# Common bases (name and aliases are up to you)
L = add_dimension((1,0,0,0,0,0,0), aliases=("LENGTH",))
M = add_dimension((0,1,0,0,0,0,0), aliases=("MASS",))
T = add_dimension((0,0,1,0,0,0,0), aliases=("TIME",))
I = add_dimension((0,0,0,1,0,0,0), aliases=("CURRENT",)) # noqa: E741
Θ = add_dimension((0,0,0,0,1,0,0), aliases=("TEMPERATURE",))
N = add_dimension((0,0,0,0,0,1,0), aliases=("AMOUNT",))
J = add_dimension((0,0,0,0,0,0,1), aliases=("LUMINOUS_INTENSITY",))

ABSORBED_RADIATION_DOSE = add_derived(L**2 / (T**2), aliases=("AbsorbedRadiationDose",))
ACCELERATION = add_derived(L / (T**2), aliases=("Acceleration",))

# Common derived dimensions needed by units
Force = add_derived(M * L / (T**2), aliases=("FORCE",))
Area = add_derived(L**2, aliases=("AREA",))
Volume = add_derived(L**3, aliases=("VOLUME",))
Pressure = add_derived(M / (L * T**2), aliases=("PRESSURE",))
Energy = add_derived(M * L**2 / (T**2), aliases=("ENERGY",))
Power = add_derived(M * L**2 / (T**3), aliases=("POWER",))

if __name__ == "__main__":
    write_dimensions_stub("namespace.pyi")
