from parc.configs.edf.constants import FrenchNuclearUnitDesign
from parc.configs.edf.types import FrenchNuclearUnit
from parc.types import Site

BUGEY = Site(
    name="Bugey",
    units=[
        BUG1 := FrenchNuclearUnit(name="bug1", design=FrenchNuclearUnitDesign.CP0),
        BUG2 := FrenchNuclearUnit(name="bug2", design=FrenchNuclearUnitDesign.CP0),
        BUG3 := FrenchNuclearUnit(name="bug3", design=FrenchNuclearUnitDesign.CP0),
        BUG4 := FrenchNuclearUnit(name="bug4", design=FrenchNuclearUnitDesign.CP0),
    ],
)
