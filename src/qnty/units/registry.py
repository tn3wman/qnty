import re
from collections.abc import Iterable
from dataclasses import dataclass

from ..dimensions import Dimension


# ---------- Unit + Registry ----------
@dataclass(frozen=True)
class Unit:
    name: str                 # canonical Python-safe name (e.g., "erg_per_gram")
    symbol: str               # display symbol (e.g., "erg/g")
    dimension: Dimension
    si_factor: float          # SI_value = value * si_factor + si_offset
    si_offset: float = 0.0
    aliases: tuple[str, ...] = ()   # optional extra aliases

_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹·", "0123456789.")

# Common unit aliases mapping
_ALIASES: dict[str, str] = {
    # Add common unit aliases here as needed
    "metre": "meter",
    "metres": "meter",
    "litre": "liter",
    "litres": "liter",
}

def _norm_token(s: str) -> str:
    s = s.strip().casefold()
    s = s.translate(_SUP).replace("^", "")
    s = s.replace("·","*")
    for ch in [" ","_","-"]:
        s = s.replace(ch, "")
    s = _ALIASES.get(s, s)
    if s.endswith("s") and len(s) > 1:
        s = s[:-1]
    return s

# token like 'm2', 'm^2', 'm²', 'cm2', 'N', 'ft2'
_EXTRACT = re.compile(r"(?P<unit>[a-zµΩ]+)(?P<exp>[0-9]+)?", re.IGNORECASE)  # Ω example if you add electrical units


class UnitRegistry:
    def __init__(self):
        self._by_key: dict[str, Unit] = {}
        self._preferred: dict[Dimension, Unit] = {}

    @staticmethod
    def _norm(s: str) -> str:
        return s.strip().casefold().replace(" ", "").replace("_","").replace("-","").replace("^","")

    def register(self, unit: Unit, aliases: Iterable[str] = ()):
        # Always include canonical name and symbol
        names = set(aliases) | {unit.name, unit.symbol}
        for a in names:
            key = self._norm(a)
            # Skip empty or minimal symbols to avoid collisions
            if not key:
                continue
            prev = self._by_key.get(key)
            if prev and prev is not unit:
                # Only raise collision error if same dimension, different SI factor, AND same unit name
                # (identical units with different conversions = real collision)
                # Allow different units with same dimension and symbol but different SI factors
                if (prev.dimension == unit.dimension and 
                    prev.si_factor != unit.si_factor and 
                    prev.name == unit.name):
                    raise ValueError(f"Alias collision: {a!r} - same dimension '{prev.dimension}' and name '{prev.name}' but different SI factors ({prev.si_factor} vs {unit.si_factor}). Units: '{prev.name}' vs '{unit.name}'")
            self._by_key[key] = unit

    def set_preferred(self, unit: Unit):
        self._preferred[unit.dimension] = unit

    def preferred_for(self, dim: Dimension) -> Unit | None:
        return self._preferred.get(dim)

    def get(self, alias: str) -> Unit:
        key = self._norm(alias)
        if key not in self._by_key:
            raise KeyError(f"Unknown unit alias: {alias!r}")
        return self._by_key[key]

# Global registry instance
ureg = UnitRegistry()

# ---------- UnitNamespace metaclass ----------
class UnitNamespaceMeta(type):
    """
    On class creation:
      • find all Unit instances
      • register each to the global registry under (name, symbol, attribute-name, and Unit.aliases)
      • if __preferred__ is set to attribute name(s), mark those as preferred for their dimensions
      • freeze the class (attributes are constants)
    """
    def __new__(mcls, name, bases, ns, **kwargs):
        cls = super().__new__(mcls, name, bases, ns)
        # Collect Units in the class dict
        units: dict[str, Unit] = {k: v for k, v in ns.items() if isinstance(v, Unit)}
        # Register each unit. Also register by the attribute name.
        for attr, unit in units.items():
            # Include attribute name as an alias
            all_aliases = (unit.aliases or ()) + (attr,)
            # Also include symbol (registry.register already includes symbol and name)
            ureg.register(unit, aliases=all_aliases)

        # Handle preferred(s): allow a single name or an iterable of names
        preferred = ns.get("__preferred__", ())
        if isinstance(preferred, str):
            preferred = (preferred,)
        for pref_attr in preferred:
            if pref_attr in units:
                ureg.set_preferred(units[pref_attr])

        # Make attributes effectively read-only
        def _blocked_setattr(self, k, v):
            raise AttributeError(f"{name} is frozen; define units in the class body.")
        cls.__setattr__ = _blocked_setattr  # type: ignore
        return cls

class UnitNamespace(metaclass=UnitNamespaceMeta):
    __slots__ = ()
