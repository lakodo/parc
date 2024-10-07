from typing import Callable

from parc.constants import UnitTechnology
from parc.types.errors import UniqueUnitError


class MetaUnit(type):
    def list_all(cls, fn: Callable[["Unit"], bool] = lambda _: True, include_other_units: bool = False) -> list["Unit"]:
        """List all created `Unit`.

        An optional filtering function can be set.
        This method is mainly intended to be use with a getter like this:
        ```python
        @property
        def get_900(cls):
            return cls.filter(lambda u: u.<whatever_property> == <something>)
        """

        units = sorted(_ALL_UNITS.values(), key=lambda u: u.name)

        if not include_other_units:
            # remove unit of different class (can be different after inheritance)
            units = [unit for unit in _ALL_UNITS.values() if isinstance(unit, cls)]
        return list(filter(fn, units))


class Unit(metaclass=MetaUnit):
    """
    electricity_producer: can be false for common buildings (storage, control rooms...)
    """

    name: str
    technology: UnitTechnology
    electricity_producer: bool
    _unique_key: str

    def __init__(
        self,
        *,
        technology: UnitTechnology,
        name: str,
        electricity_producer: bool = True,
    ):
        self.name = name
        self.technology = technology
        self.electricity_producer = electricity_producer
        self._unique_key = name + technology + str(electricity_producer)
        if self._unique_key in _ALL_UNITS:
            # a unit must be unique
            raise UniqueUnitError(_ALL_UNITS[self._unique_key])
        _ALL_UNITS[self._unique_key] = self

    def __repr__(self) -> str:
        return "<unit(" + self.technology + "): " + self.name + ">"


_ALL_UNITS: dict[str, Unit] = {}
