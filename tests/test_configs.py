from parc.configs import edf
from parc.configs.edf import types
from parc.configs.edf.constants import FrenchNuclearUnitLevel


def test_edf_french_grid():
    print(edf.FRENCH_GRID)


def test_edf_types():
    french_nuclear_unit = types.FrenchNuclearUnit(level=FrenchNuclearUnitLevel.CP0, name="some_french_nuclear_unit")
    str(french_nuclear_unit)
