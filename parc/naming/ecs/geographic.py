"""Parser for ECS repères géographiques (RG)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .buildings import (
    STRUCTURE_ELEMENT_CODES,
    describe_structure_code,
    describe_structure_extension,
    level_altitude_range,
    parse_building_trigram,
)

RG_REGEX = (
    r"(?P<tranche>[0-9])?"
    r"(?P<building>H[A-Z]{2})"
    r"(?P<identification>[0-9]{4})"
    r"(?P<structure>[BCDEFJLMNPVX][A-Z][A-Z0-9-])"
    r"(?P<extension>[A-Z0-9]{0,4})"
)
RG_PATTERN = re.compile(f"^{RG_REGEX}$")
RG_FINDER_PATTERN = re.compile(rf"(?<![A-Z0-9])(?P<value>{RG_REGEX})(?![A-Z0-9])")


def normalize_rg(value: str) -> str:
    """Normalize a geographic reference."""

    return value.strip().upper().replace(" ", "")


@dataclass(frozen=True)
class GeographicIdentification:
    """Section 2 of an RG."""

    raw: str

    @property
    def level(self) -> str:
        return self.raw[:2]

    @property
    def order(self) -> str:
        return self.raw[2:]

    @property
    def altitude_range(self) -> tuple[float, float] | None:
        return level_altitude_range(self.level)


@dataclass(frozen=True)
class GeographicReference:
    """Parsed ECS repère géographique."""

    tranche: str | None
    building: str
    identification: GeographicIdentification
    structure: str
    extension: str = ""

    @property
    def code(self) -> str:
        return f"{self.tranche or ''}{self.building}{self.identification.raw}{self.structure}{self.extension}"

    @property
    def building_label(self) -> str | None:
        return parse_building_trigram(self.building).family_label

    @property
    def structure_meanings(self) -> tuple[str, ...]:
        return describe_structure_code(self.structure)

    @property
    def extension_meanings(self) -> tuple[str, ...]:
        return describe_structure_extension(self.structure, self.extension)

    def __str__(self) -> str:
        return self.code


def parse_rg(value: str) -> GeographicReference:
    """Parse an ECS repère géographique."""

    normalized = normalize_rg(value)
    match = RG_PATTERN.fullmatch(normalized)
    if not match:
        msg = f"Invalid ECS geographic reference: {value!r}"
        raise ValueError(msg)
    groups = match.groupdict()
    if groups["structure"][0] not in STRUCTURE_ELEMENT_CODES:
        msg = f"Invalid ECS geographic reference: {value!r}"
        raise ValueError(msg)
    return GeographicReference(
        tranche=groups["tranche"],
        building=parse_building_trigram(groups["building"]).code,
        identification=GeographicIdentification(groups["identification"]),
        structure=groups["structure"],
        extension=groups["extension"],
    )


def is_rg(value: str) -> bool:
    """Return ``True`` if ``value`` is a valid ECS RG."""

    try:
        parse_rg(value)
    except ValueError:
        return False
    return True


def build_rg_regex(
    *, tranche: str | None = None, building: str | None = None, structure: str | None = None
) -> re.Pattern[str]:
    """Build a regex for geographic references."""

    pattern = (
        (re.escape(str(tranche)) if tranche is not None else r"[0-9]?")
        + (re.escape(normalize_rg(building)) if building is not None else r"H[A-Z]{2}")
        + r"[0-9]{4}"
        + (re.escape(normalize_rg(structure)) if structure is not None else r"[A-Z]{2}[A-Z0-9-]")
        + r"[A-Z0-9]{0,4}"
    )
    return re.compile(f"^{pattern}$")


def find_rgs(text: str) -> list[GeographicReference]:
    """Extract geographic references from text."""

    return [parse_rg(match.group("value")) for match in RG_FINDER_PATTERN.finditer(text.upper())]
