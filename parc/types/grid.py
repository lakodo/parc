import typing
from .site import Site


class Grid(object):
    """A grid is just a list of units"""

    sites: typing.List[Site]
    name: str

    def __init__(self, *, name: str = "grid", sites: typing.List[Site] = []):
        self.name = name
        self.sites = sites
