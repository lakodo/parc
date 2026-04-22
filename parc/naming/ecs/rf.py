"""Helpers to parse and manipulate ECS repères fonctionnels (RF)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .ecs import describe_ecs_code, normalize_ecs_code
from .materials import MaterialCodeDescription, describe_extension, describe_material_code

RF_REGEX = (
    r"(?P<tranche>[0-9])"
    r"(?P<system>[A-Z]{3})"
    r"(?P<identification>[0-9]{4})"
    r"(?P<material_bigram>[A-Z]{2})"
    r"(?P<material_qualifier>[A-Z0-9-])"
    r"(?P<extension>[A-Z0-9]{0,4})"
)
RF_PATTERN = re.compile(f"^{RF_REGEX}$")
RF_FINDER_PATTERN = re.compile(rf"(?<![A-Z0-9])(?P<rf>{RF_REGEX})(?![A-Z0-9])")


@dataclass(frozen=True)
class IdentificationSection:
    """Section 2 of an RF."""

    raw: str

    @property
    def sub_function(self) -> int:
        return int(self.raw[0])

    @property
    def base_function(self) -> int:
        return int(self.raw[1])

    @property
    def order(self) -> int:
        return int(self.raw[2:])


@dataclass(frozen=True)
class MaterialSection:
    """Section 3 of an RF."""

    bigram: str
    qualifier: str

    @property
    def code(self) -> str:
        return f"{self.bigram}{self.qualifier}"

    @property
    def description(self) -> MaterialCodeDescription:
        return describe_material_code(self.code)

    @property
    def labels(self) -> tuple[str, ...]:
        return self.description.labels

    @property
    def qualifier_meanings(self) -> tuple[str, ...]:
        return self.description.qualifier_meanings


@dataclass(frozen=True)
class FunctionalReference:
    """Parsed ECS repère fonctionnel."""

    tranche: str
    system: str
    identification: IdentificationSection
    material: MaterialSection
    extension: str = ""

    @property
    def system_label(self) -> str | None:
        return describe_ecs_code(self.system)

    @property
    def canonical(self) -> str:
        return (
            f"{self.tranche}"
            f"{self.system}"
            f"{self.identification.raw}"
            f"{self.material.code}"
            f"{self.extension}"
        )

    @property
    def extension_meanings(self) -> tuple[str, ...]:
        return describe_extension(self.material.code, self.extension)

    def with_extension(self, extension: str) -> FunctionalReference:
        return FunctionalReference(
            tranche=self.tranche,
            system=self.system,
            identification=self.identification,
            material=self.material,
            extension=normalize_rf_token(extension),
        )

    def __str__(self) -> str:
        return self.canonical


def normalize_rf_token(value: str) -> str:
    """Normalize a single RF token."""

    return value.strip().upper().replace(" ", "")


def normalize_rf(value: str) -> str:
    """Normalize a full RF while preserving ECS semantics."""

    return normalize_rf_token(value)


def parse_rf(value: str) -> FunctionalReference:
    """Parse an ECS repère fonctionnel."""

    normalized = normalize_rf(value)
    match = RF_PATTERN.fullmatch(normalized)
    if not match:
        msg = f"Invalid ECS RF: {value!r}"
        raise ValueError(msg)

    groups = match.groupdict()
    return FunctionalReference(
        tranche=groups["tranche"],
        system=normalize_ecs_code(groups["system"]),
        identification=IdentificationSection(groups["identification"]),
        material=MaterialSection(groups["material_bigram"], groups["material_qualifier"]),
        extension=groups["extension"],
    )


def is_rf(value: str) -> bool:
    """Return ``True`` if ``value`` is a valid ECS RF."""

    try:
        parse_rf(value)
    except ValueError:
        return False
    return True


def build_rf(
    *,
    tranche: str | int,
    system: str,
    identification: str | int,
    material: str,
    extension: str = "",
) -> FunctionalReference:
    """Build an RF from explicit sections."""

    tranche_str = str(tranche)
    identification_str = f"{int(identification):04d}" if isinstance(identification, int) else str(identification)
    material_code = normalize_rf_token(material)
    if len(material_code) == 2:
        material_code = f"{material_code}-"
    return parse_rf(f"{tranche_str}{normalize_ecs_code(system)}{identification_str}{material_code}{extension}")


def build_rf_regex(
    *,
    tranche: str | None = None,
    system: str | None = None,
    identification: str | None = None,
    material: str | None = None,
    extension: str | None = None,
    anchored: bool = True,
) -> re.Pattern[str]:
    """Build a regex for RF matching from exact section values."""

    material = normalize_rf_token(material) if material else None
    if material and len(material) == 2:
        material = f"{material}-"

    pattern = (
        (re.escape(str(tranche)) if tranche is not None else r"[0-9]")
        + (re.escape(normalize_ecs_code(system)) if system is not None else r"[A-Z]{3}")
        + (re.escape(str(identification)) if identification is not None else r"[0-9]{4}")
        + (re.escape(material[:2]) if material is not None else r"[A-Z]{2}")
        + (re.escape(material[2]) if material is not None else r"[A-Z0-9-]")
        + (re.escape(normalize_rf_token(extension)) if extension is not None else r"[A-Z0-9]{0,4}")
    )
    if anchored:
        pattern = f"^{pattern}$"
    return re.compile(pattern)


def find_rfs(text: str) -> list[FunctionalReference]:
    """Extract every canonical RF found in a block of text."""

    found: list[FunctionalReference] = []
    for match in RF_FINDER_PATTERN.finditer(text.upper()):
        found.append(parse_rf(match.group("rf")))
    return found
