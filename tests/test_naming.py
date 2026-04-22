from parc.naming import ecs, kks


def test_namings():
    assert ecs.ElementarySystems["A"].value == "Alimentation en eau - poste d'eau"
    assert ecs.describe_ecs_code("ASG") == "Alimentation auxiliaire de secours des GV"
    assert ecs.describe_ecs_code("DA *") == "Ascenseurs et monte-charges"
    assert ecs.describe_ecs_code("LH#") == "Courant alternatif > ou = à 5,5 kV secouru"
    assert ecs.describe_ecs_code("YGV") == "Dispositif d'instrumentation GV"
    assert ecs.describe_ecs_code("ZZZ") is None
    assert len(ecs.ELEMENTARY_SYSTEM_CODES) > 150
    assert kks is not None
