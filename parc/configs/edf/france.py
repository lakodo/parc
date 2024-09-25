# configs/edf/france.py

"""Provide EDF plant details in France.


The module contains the following constant(s):

- `FRENCH_GRID` - All sites in France under EDF control.
"""

from parc.types import Grid

from .sites.nuc import FRENCH_NUCLEAR_SITES

FRENCH_GRID = Grid(
    name="France",
    sites=[
        *FRENCH_NUCLEAR_SITES,
    ],
)
