from parc.types import Site, Unit


class ThermalPowerUnit(Unit):
    pass


class ThermalPowerStation(Site):
    def __init__(self, *, name: str, units: list[Unit]):
        super().__init__(name=name, units=units)
