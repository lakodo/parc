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


_ALL_UNITS: dict[str, Unit] = {}
