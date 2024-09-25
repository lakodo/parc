from parc.configs.edf.sites.nuc.tricastin import TRICASTIN

from .belleville import BELLEVILLE
from .blayais import BLAYAIS
from .bugey import BUGEY
from .cattenom import CATTENOM
from .chinon import CHINON
from .chooz import CHOOZ
from .civaux import CIVAUX
from .cruas import CRUAS
from .dampierre import DAMPIERRE
from .flamanville import FLAMANVILLE
from .golfech import GOLFECH
from .gravelines import GRAVELINES
from .nogent import NOGENT
from .paluel import PALUEL
from .penly import PENLY
from .saint_alban import SAINT_ALBAN
from .saint_laurent import SAINT_LAURENT

FRENCH_NUCLEAR_SITES = [
    BELLEVILLE,
    BLAYAIS,
    BUGEY,
    CATTENOM,
    CHINON,
    CHOOZ,
    CIVAUX,
    CRUAS,
    DAMPIERRE,
    FLAMANVILLE,
    GOLFECH,
    GRAVELINES,
    NOGENT,
    PALUEL,
    PENLY,
    SAINT_ALBAN,
    SAINT_LAURENT,
    TRICASTIN,
]
FRENCH_NUCLEAR_UNITS = [unit for site in FRENCH_NUCLEAR_SITES for unit in site.units]
FRENCH_NUCLEAR_PRODUCING_UNITS = [
    unit for site in FRENCH_NUCLEAR_SITES for unit in site.units if unit.electricity_producer
]

__all__ = ["FRENCH_NUCLEAR_SITES", "FRENCH_NUCLEAR_UNITS", "FRENCH_NUCLEAR_PRODUCING_UNITS"]
