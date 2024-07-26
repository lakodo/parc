from .unit import Unit
import typing


class Site(object):
    """
    units: only use
    """

    name: str
    units: typing.List[Unit]

    def __init__(self, *, name: str, units: typing.List[Unit]):
        self.name = name
        self.units = units

    def __repr__(self) -> str:
        return '<site: "' + self.name + '" (' + str(len(self.units)) + " units)>"
