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


def test_parse_compact_rf_without_tranche():
    rf = ecs.parse_rf("RCP001PO-")

    assert rf.tranche is None
    assert rf.system == "RCP"
    assert rf.system_label == "Circuit primaire"
    assert rf.identification.raw == "001"
    assert rf.identification.sub_function is None
    assert rf.identification.base_function == 0
    assert rf.identification.order == 1
    assert rf.material.code == "PO-"
    assert str(rf) == "RCP001PO-"
    assert ecs.is_rf("RCV001PO-")
    assert not ecs.is_rf("RCC001PO-")


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
    refs = ecs.find_rfs("foo 1EAS1003VA- bar 1KAC0012RXC baz RCP001PO-")

    assert [str(ref) for ref in refs] == ["1EAS1003VA-", "1KAC0012RXC", "RCP001PO-"]


def test_validate_exact_and_partial_rf_candidates():
    exact = ecs.validate_rf("RCP001PO-")
    partial = ecs.validate_rf("RCP001PO")

    assert exact.is_exact_match
    assert [str(candidate) for candidate in exact.candidates] == ["RCP001PO-"]

    assert not partial.is_exact_match
    assert partial.has_candidates
    assert str(partial.candidates[0]) == "RCP001PO-"


def test_validate_rf_with_minimatch_patterns():
    broad = ecs.validate_rf("RCV*", limit=3)
    precise = ecs.validate_rf("ASG00?PO", limit=5)
    invalid = ecs.validate_rf("RCC*", limit=3)

    assert not broad.is_exact_match
    assert broad.has_candidates
    assert broad.truncated
    assert all(candidate.system == "RCV" for candidate in broad.candidates)

    assert [str(candidate) for candidate in precise.candidates[:3]] == ["ASG000PO-", "ASG001PO-", "ASG002PO-"]
    assert not invalid.has_candidates


def test_validate_rf_accepts_zero_instead_of_o() -> None:
    result = ecs.validate_rf("RCV002P0", limit=5)

    assert not result.is_exact_match
    assert result.has_candidates
    assert result.normalized_query == "RCV002PO"
    assert any(str(c).startswith("RCV002PO") for c in result.candidates)


def test_validate_rf_zero_o_exact_correction() -> None:
    result = ecs.validate_rf("RCV002P0-")

    assert result.is_exact_match
    assert result.normalized_query == "RCV002PO-"
    assert str(result.candidates[0]) == "RCV002PO-"
