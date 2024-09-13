from .unit import Unit


class Site:
    """
    units: only use
    """

    name: str
    units: list[Unit]

    def __init__(self, *, name: str, units: list[Unit]):
        self.name = name
        self.units = units

    def __repr__(self) -> str:
        return '<site: "' + self.name + '" (' + str(len(self.units)) + " units)>"
