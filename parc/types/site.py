from .unit import Unit


class Site:
    """
    units: only use
    """

    name: str
    name_full: str | None
    units: list[Unit]

    def __init__(self, *, name: str, name_full: str | None = None, units: list[Unit]):
        self.name = name
        self.name_full = name_full
        self.units = units

    def __repr__(self) -> str:
        return '<site: "' + self.name + '" (' + str(len(self.units)) + " units)>"
