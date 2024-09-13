from typing import Optional

from .site import Site


class Grid:
    """A grid is just a list of units"""

    sites: list[Site]
    name: str

    def __init__(self, *, name: str = "grid", sites: Optional[list[Site]] = None):
        if sites is None:
            sites = []
        self.name = name
        self.sites = sites
