from typing import Any, Optional

from .unit import Unit


class Site:
    """
    units: only use
    """

    name: str
    name_full: Optional[str]
    units: list[Unit[Any]]

    def __init__(self, *, name: str, name_full: Optional[str] = None, units: list[Unit[Any]]):
        self.name = name
        self.name_full = name_full
        self.units = units

    def __repr__(self) -> str:
        return '<site: "' + self.name + '" (' + str(len(self.units)) + " units)>"
