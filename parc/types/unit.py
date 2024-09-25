from typing import Callable

from parc.constants import UnitTechnology
from parc.types.errors import UniqueUnitError


class Unit:
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

    @classmethod
    def list_all(cls, fn: Callable[["Unit"], bool] = lambda _: True, include_other_units: bool = False):
        """List all created `Unit`.

        An optional filtering function can be set.
        This method is mainly intended to be use with a getter like this:
        ```python
        @property
        def get_900(cls):
            return cls.filter(lambda u: u.<whatever_property> == <something>)
        """
        if include_other_units:
            return filter(fn, _ALL_UNITS.values())
        return filter(fn, (unit for unit in _ALL_UNITS.values() if isinstance(unit, cls)))


_ALL_UNITS: dict[str, Unit] = {}
