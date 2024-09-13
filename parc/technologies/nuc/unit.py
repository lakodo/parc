from parc.constants import UnitTechnology
from parc.types import Unit


class NuclearUnit(Unit):
    def __init__(
        self,
        *,
        name: str,
        electricity_producer: bool = True,
    ):
        super().__init__(name=name, electricity_producer=electricity_producer, technology=UnitTechnology.NUCLEAR)
