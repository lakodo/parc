from parc.types import Grid
from .sites.nuc import FRENCH_NUCLEAR_SITES

FRENCH_GRID = Grid(
    name="France",
    sites=[
        *FRENCH_NUCLEAR_SITES,
    ],
)

