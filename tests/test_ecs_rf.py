from parc.naming import ecs


def test_parse_basic_rf():
    rf = ecs.parse_rf("1EAS1003VA-")

    assert rf.tranche == "1"
    assert rf.system == "EAS"
    assert rf.system_label == "Aspersion - recirculation de l'aspersion"
    assert rf.identification.raw == "1003"
    assert rf.identification.sub_function == 1
    assert rf.identification.base_function == 0
    assert rf.identification.order == 3
    assert rf.material.code == "VA-"
    assert rf.material.labels == ("Vanne d'air",)
    assert str(rf) == "1EAS1003VA-"


def test_parse_state_and_extension_examples_from_pdf():
    state_rf = ecs.parse_rf("1EAS1003VA 3")
    support_rf = ecs.parse_rf("1EAS2055TY- S001")
    card_rf = ecs.parse_rf("1KCO1072ARCAB19")
    bottle_rf = ecs.parse_rf("1EAS1011BA N0003")

    assert state_rf.material.code == "VA3"
    assert any("ouverte" in meaning for meaning in state_rf.material.qualifier_meanings)

    assert support_rf.material.code == "TY-"
    assert support_rf.extension == "S001"
    assert support_rf.extension_meanings == ("Point de supportage ou de fixation n°001",)

    assert card_rf.material.code == "ARC"
    assert card_rf.extension_meanings == ("Carte en rack AB, position 19",)

    assert bottle_rf.material.code == "BAN"
    assert "Bouteille de niveau" in bottle_rf.material.qualifier_meanings
    assert bottle_rf.extension == "0003"


def test_material_lookup_helpers():
    cable = ecs.describe_material_code("CAA")
    local_sensor = ecs.describe_material_code("MTL")

    assert cable.labels == ("Câble",)
    assert cable.qualifier_meanings == ("Câble moyenne tension",)
    assert local_sensor.labels == ("Mesure de température",)
    assert "Capteur local" in local_sensor.qualifier_meanings


def test_rf_build_and_regex_helpers():
    built = ecs.build_rf(tranche=1, system="eas", identification=1003, material="va")
    pattern = ecs.build_rf_regex(system="EAS", material="VA-")

    assert str(built) == "1EAS1003VA-"
    assert pattern.fullmatch("1EAS1003VA-")
    assert not pattern.fullmatch("1RCP1003VA-")


def test_find_rfs_in_text():
    refs = ecs.find_rfs("foo 1EAS1003VA- bar 1KAC0012RXC baz")

    assert [str(ref) for ref in refs] == ["1EAS1003VA-", "1KAC0012RXC"]
