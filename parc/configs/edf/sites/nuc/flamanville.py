from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

FLAMANVILLE = Site(
    name="Flamanville",
    units=[
        FrenchNuclearUnit(name="fla1", design=FrenchNuclearUnitDesign.P4),
        FrenchNuclearUnit(name="fla2", design=FrenchNuclearUnitDesign.P4),
        FrenchNuclearUnit(name="fla3", design=FrenchNuclearUnitDesign.EPR),
    ],
)
