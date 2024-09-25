from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

CHINON = Site(
    name="Chinon",
    units=[
        CHI1 := FrenchNuclearUnit(name="chi1", design=FrenchNuclearUnitDesign.CP1),
        CHI2 := FrenchNuclearUnit(name="chi2", design=FrenchNuclearUnitDesign.CP1),
        CHI3 := FrenchNuclearUnit(name="chi3", design=FrenchNuclearUnitDesign.CP1),
        CHI4 := FrenchNuclearUnit(name="chi4", design=FrenchNuclearUnitDesign.CP1),
    ],
)
