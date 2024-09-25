from parc.utils.types import StrEnum


class FrenchNuclearUnitDesign(StrEnum):
    """List of the different design of French nuclear plant owned by EDF"""

    CP0 = "CP0"
    CP1 = "CP1"  #  CPY
    CP2 = "CP2"  # CPY
    P4 = "P4"
    PP4 = "P'4"
    N4 = "N4"
    EPR = "EPR"

    @property
    def power(self):
        return FRENCH_LEVEL_DEFAULT_POWER_MAPPING[self]

    def __repr__(self) -> str:
        return f"{self.value}"

    def __str__(self) -> str:
        return self.__repr__()


FRENCH_LEVEL_DEFAULT_POWER_MAPPING = {
    FrenchNuclearUnitDesign.CP0: 900,
    FrenchNuclearUnitDesign.CP1: 900,
    FrenchNuclearUnitDesign.CP2: 900,
    FrenchNuclearUnitDesign.P4: 1300,
    FrenchNuclearUnitDesign.PP4: 1300,
    FrenchNuclearUnitDesign.N4: 1450,
    FrenchNuclearUnitDesign.EPR: 1600,
}


if __name__ == "__main__":
    for design in FrenchNuclearUnitDesign:
        print(design, design.power)
