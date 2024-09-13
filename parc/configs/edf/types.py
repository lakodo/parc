from parc.constants import UnitTechnology
from parc.technologies.nuc import NuclearUnit

from .constants import FrenchNuclearUnitLevel


class FrenchNuclearUnit(NuclearUnit):
    level: FrenchNuclearUnitLevel

    def __init__(
        self,
        *,
        level: FrenchNuclearUnitLevel,
        technology: UnitTechnology,
        name: str,
        electricity_producer: bool = True,
    ):
        super().__init__(technology=technology, name=name, electricity_producer=electricity_producer)
        self.level = level

    def __repr__(self) -> str:
        return "<☢️ " + self.level + ": " + self.name + ">"
