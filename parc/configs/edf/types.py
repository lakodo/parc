from typing import Optional, Union

from parc.technologies.nuc import NuclearUnit
from parc.types.unit import Unit

from .constants import FRENCH_LEVEL_DEFAULT_POWER_MAPPING, FrenchNuclearUnitDesign


def _is_of_power(unit: Unit, power: int):
    """
    Private method of this module to check if a unit is of a specific power
    """
    if isinstance(unit, FrenchNuclearUnit):
        return unit.power == power
    return False


def _is_of_design(unit: Unit, design: Union[FrenchNuclearUnitDesign, list[FrenchNuclearUnitDesign]]):
    """
    Private method of this module to check if a unit is of a specific design
    """
    if isinstance(unit, FrenchNuclearUnit):
        if isinstance(design, list):
            return unit.design in design
        else:
            return unit.design == design
    return False


class FrenchNuclearUnit(NuclearUnit):
    design: FrenchNuclearUnitDesign
    power: int

    def __init__(
        self,
        *,
        design: FrenchNuclearUnitDesign,
        name: str,
        electricity_producer: bool = True,
        power: Optional[int] = None,
    ):
        super().__init__(name=name, electricity_producer=electricity_producer)
        self.design = design
        self.power = power or FRENCH_LEVEL_DEFAULT_POWER_MAPPING[design]

    def __repr__(self) -> str:
        return f"<☢️ {self.design} ({self.power}): {self.name} >"

    @classmethod
    def get_900(cls):
        return cls.list_all(lambda u: _is_of_power(u, 900))

    @classmethod
    def get_1300(cls):
        return cls.list_all(lambda u: _is_of_power(u, 1300))

    @classmethod
    def get_1450(cls):
        return cls.list_all(lambda u: _is_of_power(u, 1450))

    @classmethod
    def get_1600(cls):
        return cls.list_all(lambda u: _is_of_power(u, 1600))

    @classmethod
    def get_CP0(cls):
        return cls.list_all(lambda u: _is_of_design(u, FrenchNuclearUnitDesign.CP0))

    @classmethod
    def get_of_design(cls, design: Union[FrenchNuclearUnitDesign, list[FrenchNuclearUnitDesign]]):
        return cls.list_all(lambda u: _is_of_design(u, design))
