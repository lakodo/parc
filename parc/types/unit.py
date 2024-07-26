import typing
from parc.constants import UnitTechnology
from parc.types.errors import UniqueUnitError


class Unit(object):
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
            raise UniqueUnitError(_ALL_UNITS[self._unique_key])
        _ALL_UNITS[self._unique_key] = self

    def __repr__(self) -> str:
        return "<unit(" + self.technology + "): " + self.name + ">"


_ALL_UNITS: typing.Dict[str, Unit] = {}
