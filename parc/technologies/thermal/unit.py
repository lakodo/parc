import typing
from parc.types import Unit, Site


class ThermalPowerUnit(Unit):
    pass


class ThermalPowerStation(Site):
    def __init__(self, *, name: str, units: typing.List[str]):
        super().__init__(name=name, units=units)
