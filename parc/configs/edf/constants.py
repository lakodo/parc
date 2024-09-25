from parc.utils.types import StrEnum


class FrenchNuclearUnitLevel(StrEnum):
    """List of the different level of French nuclear plant owned by EDF"""

    CP0 = "CP0"
    CP1 = "CP1"
    CP2 = "CP2"
    P4 = "P4"
    PP4 = "P'4"
    N4 = "N4"
    EPR = "EPR"
