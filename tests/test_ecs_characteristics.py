from parc.naming import ecs


def test_parse_location_reference():
    ref = ecs.parse_location_reference("1HLD0317ZL-")

    assert ref.building == "HLD"
    assert ref.building_label == "Bâtiments électriques et des auxiliaires de sauvegarde"
    assert ref.identification.level == "03"
    assert ref.local_number == "17"
    assert ref.local_kind_label == "Local (pièce)"
    assert ref.identification.altitude_range == (-7.0, -6.01)
    assert str(ref) == "1HLD0317ZL-"


def test_parse_fire_sector_reference():
    ref = ecs.parse_fire_sector_reference("1HLD0502SFI")

    assert ref.building == "HLD"
    assert ref.identification.level == "05"
    assert ref.sector_number == "02"
    assert ref.kind_label == "Secteur"
    assert ref.criterion_label == "Limitation et indisponibilité"
    assert ref.rank == 1
    assert str(ref) == "1HLD0502SFI"


def test_parse_electrical_supply_reference():
    tableau = ecs.parse_electrical_supply_reference("1LHA0824JC-")
    armoire = ecs.parse_electrical_supply_reference("LKA2922JC-".join(["1", ""]))  # 1LKA2922JC-

    assert tableau.system == "LHA"
    assert tableau.support_kind == "tableau"
    assert tableau.enclosure_number is None
    assert (tableau.column, tableau.row, tableau.subcolumn) == ("8", "2", "4")

    assert armoire.system == "LKA"
    assert armoire.support_kind == "armoire"
    assert armoire.enclosure_number == "2"
    assert (armoire.column, armoire.row, armoire.subcolumn) == ("9", "2", "2")


def test_parse_rg_examples():
    structure = ecs.parse_rg("1HMA0510EM-")
    component = ecs.parse_rg("1HDM0220PBA0025")
    cable_tray = ecs.parse_rg("1HLA0732CDF")

    assert structure.structure_meanings == ("Cage d'escalier et d'ascenseur", "Métal")
    assert component.structure_meanings == ("Poteau", "Béton", "Ancrage à sceller (Halfen)")
    assert component.extension_meanings == ("Identifiant composant 0025",)
    assert cable_tray.structure_meanings == ("Chemin de câbles", "Voie électrique D", "Tablette F")


def test_find_other_ecs_references_in_text():
    text = "1HLD0317ZL- 1HLD0301ZFI 1LHA0824JC- 1HDM0220PBA0025"

    assert [str(ref) for ref in ecs.find_location_references(text)] == ["1HLD0317ZL-"]
    assert [str(ref) for ref in ecs.find_fire_sector_references(text)] == ["1HLD0301ZFI"]
    assert [str(ref) for ref in ecs.find_electrical_supply_references(text)] == ["1LHA0824JC-"]
    assert [str(ref) for ref in ecs.find_rgs(text)] == ["1HDM0220PBA0025"]
