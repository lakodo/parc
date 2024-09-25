from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

BLAYAIS = Site(
    name="Blayais",
    units=[
        BLA1 := FrenchNuclearUnit(name="bla1", design=FrenchNuclearUnitDesign.CP1),
        BLA2 := FrenchNuclearUnit(name="bla2", design=FrenchNuclearUnitDesign.CP1),
        BLA3 := FrenchNuclearUnit(name="bla3", design=FrenchNuclearUnitDesign.CP1),
        BLA4 := FrenchNuclearUnit(name="bla4", design=FrenchNuclearUnitDesign.CP1),
    ],
)
