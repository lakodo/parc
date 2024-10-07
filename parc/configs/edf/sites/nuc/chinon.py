from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

CHINON = Site(
    name="Chinon",
    units=[
        CHI1 := FrenchNuclearUnit(name="chb1", design=FrenchNuclearUnitDesign.CP2),
        CHI2 := FrenchNuclearUnit(name="chb2", design=FrenchNuclearUnitDesign.CP2),
        CHI3 := FrenchNuclearUnit(name="chb3", design=FrenchNuclearUnitDesign.CP2),
        CHI4 := FrenchNuclearUnit(name="chb4", design=FrenchNuclearUnitDesign.CP2),
    ],
)
