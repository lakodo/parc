from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

DAMPIERRE = Site(
    name="Dampierre",
    units=[
        FrenchNuclearUnit(
            name="dam" + str(i + 1),
            design=FrenchNuclearUnitDesign.CP1,
        )
        for i in range(4)
    ],
)
