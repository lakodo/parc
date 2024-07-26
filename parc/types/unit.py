from parc.constants import UnitTechnology


class Unit(object):
    """

    electricity_producer: can be false for common buildings (storage, control rooms...)
    """

    name: str
    technology: UnitTechnology
    electricity_producer: bool

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

    def __repr__(self) -> str:
        return "<unit(" + self.technology + "): " + self.name + ">"
