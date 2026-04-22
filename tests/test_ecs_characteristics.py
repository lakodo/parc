from parc.naming import ecs


def test_parse_location_reference():
    ref = ecs.parse_location_reference("1HLD0317ZL-")
    compact = ecs.parse_location_reference("HRA0503ZL-")

    assert ref.building == "HLD"
    assert ref.building_label == "Bâtiments électriques et des auxiliaires de sauvegarde"
    assert ref.identification.level == "03"
    assert ref.local_number == "17"
    assert ref.local_kind_label == "Local (pièce)"
    assert ref.identification.altitude_range == (-7.0, -6.01)
    assert str(ref) == "1HLD0317ZL-"
    assert compact.tranche is None
    assert compact.building == "HRA"
    assert str(compact) == "HRA0503ZL-"


def test_parse_fire_sector_reference():
    ref = ecs.parse_fire_sector_reference("1HLD0502SFI")
    compact = ecs.parse_fire_sector_reference("HLD0502SFI")

    assert ref.building == "HLD"
    assert ref.identification.level == "05"
    assert ref.sector_number == "02"
    assert ref.kind_label == "Secteur"
    assert ref.criterion_label == "Limitation et indisponibilité"
    assert ref.rank == 1
    assert str(ref) == "1HLD0502SFI"
    assert compact.tranche is None
    assert str(compact) == "HLD0502SFI"


def test_parse_electrical_supply_reference():
    tableau = ecs.parse_electrical_supply_reference("1LHA0824JC-")
    armoire = ecs.parse_electrical_supply_reference("LKA2922JC-".join(["1", ""]))  # 1LKA2922JC-
    compact = ecs.parse_electrical_supply_reference("LHA0824JC-")

    assert tableau.system == "LHA"
    assert tableau.support_kind == "tableau"
    assert tableau.enclosure_number is None
    assert (tableau.column, tableau.row, tableau.subcolumn) == ("8", "2", "4")

    assert armoire.system == "LKA"
    assert armoire.support_kind == "armoire"
    assert armoire.enclosure_number == "2"
    assert (armoire.column, armoire.row, armoire.subcolumn) == ("9", "2", "2")
    assert compact.tranche is None
    assert compact.system == "LHA"
    assert str(compact) == "LHA0824JC-"


def test_parse_rg_examples():
    structure = ecs.parse_rg("1HMA0510EM-")
    component = ecs.parse_rg("1HDM0220PBA0025")
    cable_tray = ecs.parse_rg("1HLA0732CDF")
    compact = ecs.parse_rg("HLA0732CDF")

    assert structure.structure_meanings == ("Cage d'escalier et d'ascenseur", "Métal")
    assert component.structure_meanings == ("Poteau", "Béton", "Ancrage à sceller (Halfen)")
    assert component.extension_meanings == ("Identifiant composant 0025",)
    assert cable_tray.structure_meanings == ("Chemin de câbles", "Voie électrique D", "Tablette F")
    assert compact.tranche is None
    assert str(compact) == "HLA0732CDF"


def test_find_other_ecs_references_in_text():
    text = "1HLD0317ZL- HRA0503ZL- 1HLD0301ZFI HLD0502SFI 1LHA0824JC- LHA0824JC- 1HDM0220PBA0025 HLA0732CDF"

    assert [str(ref) for ref in ecs.find_location_references(text)] == ["1HLD0317ZL-", "HRA0503ZL-"]
    assert [str(ref) for ref in ecs.find_fire_sector_references(text)] == ["1HLD0301ZFI", "HLD0502SFI"]
    assert [str(ref) for ref in ecs.find_electrical_supply_references(text)] == ["1LHA0824JC-", "LHA0824JC-"]
    assert [str(ref) for ref in ecs.find_rgs(text)] == ["1HDM0220PBA0025", "HLA0732CDF"]
