"""EDF ECS building, level and structure helpers."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

BUILDING_CODE_LABELS = MappingProxyType(
    {
        "A": "Bâtiments et installations de site de l'aménagement",
        "B": "Bâtiment de site de l'exploitation",
        "C": "Rejets, réfrigérants",
        "D": "Bâtiments diesel",
        "E": "Poste d'interconnexion",
        "F": "Bâtiments à fioul / bâtiment électrique non classé",
        "G": "Galeries",
        "H": "Bâtiments d'entreposage et stockage provisoire G.V. usés",
        "I": "Chauffage central (production eau chaude)",
        "J": "Plate-forme transformateurs auxiliaires",
        "K": "Bâtiment combustible",
        "L": "Bâtiments électriques et des auxiliaires de sauvegarde",
        "M": "Salle des machines",
        "N": "Bâtiments des auxiliaires nucléaires",
        "O": "Bâtiment de stockage d'eau",
        "P": "Station de pompage et de filtration",
        "Q": "Bâtiment de traitement des effluents",
        "R": "Bâtiment réacteur",
        "S": "Environnement, site",
        "T": "Plate-forme transformateurs principaux",
        "U": "Protection site, poste d'accès principal",
        "V": "Bâtiments des auxiliaires généraux",
        "W": "Bâtiments périphériques des bâtiments réacteurs et bâtiments d'exploitation",
        "X": "Aire de stockage des effluents",
        "Y": "Bâtiment déminéralisation",
        "Z": "Bâtiment de stockage de gaz",
    }
)
SITE_BUILDING_SUBFUNCTIONS = MappingProxyType(
    {
        "0": "Chauffage, climatisation",
        "1": "Eclairage normal et de secours",
        "2": "Distribution électrique normale",
        "3": "Distribution électrique secourue",
        "4": "Détection incendie",
        "5": "Distribution eau incendie",
        "6": "Distribution eau potable",
    }
)
LOCAL_CODE_LABELS = MappingProxyType(
    {
        "A": "Zone de montage",
        "C": "Zone de circulation",
        "L": "Local (pièce)",
        "M": "Zone de manutention",
    }
)
FIRE_KIND_LABELS = MappingProxyType({"S": "Secteur", "Z": "Zone"})
FIRE_CRITERION_LABELS = MappingProxyType(
    {
        "C": "Confinement de matière radioactive",
        "I": "Limitation et indisponibilité",
        "S": "Sûreté",
    }
)
FIRE_CODE_ORDER = ("ZFI", "SFI", "ZFS", "SFS", "SFC")
STRUCTURE_ELEMENT_CODES = MappingProxyType(
    {
        "B": "Echelle",
        "C": "Chemin de câbles",
        "D": "Dalle",
        "E": "Cage d'escalier et d'ascenseur",
        "F": "Fondation, semelle",
        "J": "Joint",
        "L": "Levée",
        "M": "Massif",
        "N": "Nervure, poutre, longrine",
        "P": "Poteau",
        "V": "Voile",
        "X": "Faux plafond",
    }
)
STRUCTURE_CHARACTERISTIC_CODES = MappingProxyType(
    {
        "B": "Béton",
        "M": "Métal",
        "V": "Vide",
    }
)
STRUCTURE_COMPONENT_CODES = MappingProxyType(
    {
        "A": "Ancrage à sceller (Halfen)",
        "B": "Caniveaux",
        "C": "Cadre à sceller",
        "D": "Porte",
        "E": "Fer plat",
        "F": "Fourreau / chatière",
        "G": "Garde corps",
        "K": "Carottage",
        "L": "Palier / seuil",
        "N": "Portillon",
        "P": "Platine à sceller",
        "Q": "Console (cornière, ...)",
        "R": "Réservation",
        "S": "Divers à sceller",
        "T": "Trémie",
        "U": "Puisard",
        "V": "Volée",
        "W": "Supportage",
        "Y": "Pylône",
        "Z": "Ecran thermique pour les chemins de câble",
    }
)
TREMIE_EXTENSION_TYPES = MappingProxyType(
    {
        "D": "Trémie destinée à une porte",
        "E": "Trémie électrique",
        "F": "Trémie équipée (chatière, hublot, fenêtre...)",
        "K": "Trémie destinée à commande de vanne déportée",
        "L": "Trémie destinée à un passage libre / escalier / circulation",
        "M": "Trémie de manutention",
        "R": "Trémie de réserve",
        "T": "Trémie de tuyauterie",
        "V": "Trémie de ventilation",
        "W": "Trémie de transfert d'air",
        "X": "Trémie à destination multiple",
        "Z": "Trémie SAS du BR",
    }
)
JOINT_AND_CANIVEAU_COVERS = MappingProxyType(
    {
        "CB": "Couvre joint ou couvre caniveau béton",
        "CM": "Couvre joint ou couvre caniveau métallique",
    }
)


@dataclass(frozen=True)
class BuildingTrigram:
    """Structured view of a building trigram."""

    code: str

    @property
    def is_building(self) -> bool:
        return len(self.code) == 3 and self.code.startswith("H")

    @property
    def family(self) -> str:
        return self.code[1]

    @property
    def zone(self) -> str:
        return self.code[2]

    @property
    def family_label(self) -> str | None:
        return BUILDING_CODE_LABELS.get(self.family)


def normalize_building_code(code: str) -> str:
    """Normalize a building trigram."""

    return code.strip().upper().replace(" ", "")


def parse_building_trigram(code: str) -> BuildingTrigram:
    """Parse a building trigram."""

    normalized = normalize_building_code(code)
    if len(normalized) != 3 or not normalized.startswith("H"):
        msg = f"Invalid ECS building trigram: {code!r}"
        raise ValueError(msg)
    return BuildingTrigram(normalized)


def level_altitude_range(level: str | int) -> tuple[float, float] | None:
    """Return the nominal altitude range associated with a level number."""

    if isinstance(level, str):
        level = int(level)

    if level == 1:
        return (-10.0, -8.01)
    if 2 <= level <= 49:
        start = float(level - 10)
        return (start, start + 0.99)
    if 50 <= level <= 89:
        start = float((level - 50) * 2 + 40)
        return (start, start + 1.99)
    return None


def describe_structure_code(code: str) -> tuple[str, ...]:
    """Return the meaning of a structure code."""

    normalized = code.strip().upper().replace(" ", "")
    if len(normalized) != 3:
        msg = f"Invalid ECS structure code: {code!r}"
        raise ValueError(msg)

    if normalized[0] == "C":
        return ("Chemin de câbles", f"Voie électrique {normalized[1]}", f"Tablette {normalized[2]}")

    meanings = [STRUCTURE_ELEMENT_CODES.get(normalized[0], f"Elément {normalized[0]}")]
    meanings.append(STRUCTURE_CHARACTERISTIC_CODES.get(normalized[1], f"Caractéristique {normalized[1]}"))
    if normalized[2] != "-":
        meanings.append(STRUCTURE_COMPONENT_CODES.get(normalized[2], f"Composant {normalized[2]}"))
    return tuple(meanings)


def describe_structure_extension(structure_code: str, extension: str) -> tuple[str, ...]:
    """Return the known meaning of a structure extension."""

    structure_code = structure_code.strip().upper().replace(" ", "")
    extension = extension.strip().upper().replace(" ", "")
    if not extension:
        return ()

    meanings: list[str] = []
    if structure_code.endswith("T") and extension[0] in TREMIE_EXTENSION_TYPES:
        meanings.append(TREMIE_EXTENSION_TYPES[extension[0]])
        if extension[1:]:
            meanings.append(f"Identifiant composant {extension[1:]}")
    elif structure_code[0] in {"J"} or structure_code.endswith("B"):
        if len(extension) >= 2 and extension[:2] in JOINT_AND_CANIVEAU_COVERS:
            meanings.append(JOINT_AND_CANIVEAU_COVERS[extension[:2]])
            if extension[2:]:
                meanings.append(f"Identifiant composant {extension[2:]}")
    else:
        meanings.append(f"Identifiant composant {extension}")
    return tuple(meanings)
