"""
Select Variable and Match Expression
====================================

Provides a typed enumeration-like system for select variables and match expressions,
useful for engineering calculations with multiple formula choices based on criteria.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from ..core.quantity import Quantity

# Type variable for the option type
T = TypeVar("T", bound="SelectOption")


@dataclass(frozen=True)
class SelectOption:
    """
    Base class for select options. Use as a frozen dataclass to create
    immutable option types for SelectVariable.

    Example:
        @dataclass(frozen=True)
        class GasketType(SelectOption):
            non_self_energized = "non_self_energized"
            self_energized = "self_energized"
    """

    pass


@dataclass
class SelectVariable(Generic[T]):
    """
    A variable that can be set to one of a predefined set of options.

    This is similar to an enum but integrates with the qnty algebra system
    and provides a way to enumerate all valid options for UI generation.

    Args:
        name: Human-readable name for this select variable
        options_class: The dataclass that defines valid options
        selected: The currently selected option (must be from options_class)

    Example:
        @dataclass(frozen=True)
        class GasketType(SelectOption):
            non_self_energized: str = "non_self_energized"
            self_energized: str = "self_energized"

        gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

        # Get all options for UI
        options = gasket_type.get_options()  # Returns list of option values

        # Change selection
        gasket_type.select(GasketType.self_energized)
    """

    name: str
    options_class: type[T]
    selected: Any = None
    _symbol: str | None = field(default=None, repr=False)

    def __post_init__(self):
        """Validate that selected option is valid."""
        if self.selected is not None:
            self._validate_option(self.selected)

    def _validate_option(self, option: Any) -> None:
        """Validate that an option is valid for this select variable."""
        valid_options = self.get_option_values()
        if option not in valid_options:
            raise ValueError(f"Invalid option '{option}' for {self.name}. Valid options: {valid_options}")

    def get_options(self) -> list[tuple[str, Any]]:
        """
        Get all valid options as a list of (name, value) tuples.

        This is useful for generating UI elements like select boxes or radio buttons.

        Returns:
            List of (option_name, option_value) tuples
        """
        options = []
        for attr_name in dir(self.options_class):
            # Skip private/magic attributes and methods
            if attr_name.startswith("_"):
                continue
            attr_value = getattr(self.options_class, attr_name)
            # Skip methods and callables
            if callable(attr_value):
                continue
            options.append((attr_name, attr_value))
        return options

    def get_option_values(self) -> list[Any]:
        """Get just the option values (not names)."""
        return [value for _, value in self.get_options()]

    def get_option_names(self) -> list[str]:
        """Get just the option names (not values)."""
        return [name for name, _ in self.get_options()]

    def select(self, option: Any) -> None:
        """
        Select an option from the valid options.

        Args:
            option: The option value to select (must be from options_class)

        Raises:
            ValueError: If option is not valid
        """
        self._validate_option(option)
        object.__setattr__(self, "selected", option)

    @property
    def symbol(self) -> str:
        """Get the symbol for this select variable (for use in expressions)."""
        if self._symbol is None:
            # Use name as symbol by default
            return self.name.replace(" ", "_")
        return self._symbol

    @property
    def value(self) -> Any:
        """Get the currently selected value."""
        return self.selected

    def __str__(self) -> str:
        if self.selected is None:
            return f"{self.name} (not selected)"
        return f"{self.name} = {self.selected}"

    def __repr__(self) -> str:
        return f"SelectVariable(name='{self.name}', selected={self.selected})"
