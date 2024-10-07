from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

FLAMANVILLE = Site(
    name="Flamanville",
    units=[
        FLA1 := FrenchNuclearUnit(name="fla1", design=FrenchNuclearUnitDesign.P4),
        FLA2 := FrenchNuclearUnit(name="fla2", design=FrenchNuclearUnitDesign.P4),
        FLA3 := FrenchNuclearUnit(name="fla3", design=FrenchNuclearUnitDesign.EPR),
    ],
)
