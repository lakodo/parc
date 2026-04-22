from pathlib import Path

from typer.testing import CliRunner

from parc.tools.ecs_inspect import app

runner = CliRunner()


def test_analyze_command() -> None:
    result = runner.invoke(app, ["analyze", "foo 1EAS1003VA- bar 1HLD0317ZL- baz"])

    assert result.exit_code == 0
    assert "Detected: 2" in result.stdout
    assert "type: rf" in result.stdout
    assert "type: location" in result.stdout
    assert "system_label: Aspersion - recirculation de l'aspersion" in result.stdout
    assert "building_label: Bâtiments électriques et des auxiliaires de sauvegarde" in result.stdout


def test_analyze_compact_command() -> None:
    result = runner.invoke(app, ["analyze", "... RCP001PO- ... RCC001PO- ..."])

    assert result.exit_code == 0
    assert "Detected: 1" in result.stdout
    assert "canonical: RCP001PO-" in result.stdout
    assert "system_label: Circuit primaire" in result.stdout
    assert "decomposition:" in result.stdout
    assert "system_segment: RCP -> Circuit primaire" in result.stdout
    assert "system_letter_1: R -> Réacteur" in result.stdout
    assert "system_letters_2_3: CP -> Partie spécifique du trigramme système" in result.stdout
    assert "identification_digits_2_3: 01 -> Ordre 1" in result.stdout
    assert "material_bigram: PO -> Pompe" in result.stdout
    assert "RCC001PO-" not in result.stdout


def test_analyze_file_command(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("1LHA0824JC- and 1HDM0220PBA0025", encoding="utf-8")

    result = runner.invoke(app, ["analyze-file", str(path)])

    assert result.exit_code == 0
    assert "Detected: 2" in result.stdout
    assert "type: electrical-supply" in result.stdout
    assert "type: rg" in result.stdout
    assert "support_kind: tableau" in result.stdout
    assert "structure_meanings: Poteau, Béton, Ancrage à sceller (Halfen)" in result.stdout


def test_validate_command_rf_fallback() -> None:
    result = runner.invoke(app, ["validate", "ASG00?PO", "--limit", "3"])

    assert result.exit_code == 0
    assert "Query: ASG00?PO" in result.stdout
    assert "Exact Match: no" in result.stdout
    assert "Candidates: 3" in result.stdout
    assert "Truncated: yes" in result.stdout
    assert "Candidate 1:" in result.stdout
    assert "canonical: ASG000PO-" in result.stdout
    assert "Candidate 2:" in result.stdout
    assert "canonical: ASG001PO-" in result.stdout


def test_validate_list_only_command_rf_fallback() -> None:
    result = runner.invoke(app, ["validate", "ASG00?PO", "--limit", "3", "--list-only"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["ASG000PO-", "ASG001PO-", "ASG002PO-"]


def test_validate_reference_command_on_exact_location() -> None:
    result = runner.invoke(app, ["validate", "1HRA0503ZL-"])

    assert result.exit_code == 0
    assert "Exact Match: yes" in result.stdout
    assert "type: location" in result.stdout
    assert "building_label: Bâtiment réacteur" in result.stdout
    assert "local_kind_label: Local (pièce)" in result.stdout


def test_validate_reference_command_on_exact_location_without_tranche() -> None:
    result = runner.invoke(app, ["validate", "HRA0503ZL-"])

    assert result.exit_code == 0
    assert "Exact Match: yes" in result.stdout
    assert "type: location" in result.stdout
    assert "canonical: HRA0503ZL-" in result.stdout
    assert "tranche_segment: <absent> -> Tranche non précisée" in result.stdout


def test_validate_reference_command_rf_fallback_and_list_only() -> None:
    result = runner.invoke(app, ["validate", "ASG00?PO", "--limit", "3", "--list-only"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["ASG000PO-", "ASG001PO-", "ASG002PO-"]


def test_validate_reference_command_with_location_wildcard() -> None:
    result = runner.invoke(app, ["validate", "1HRA0503ZL?"])

    assert result.exit_code == 0
    assert "Exact Match: no" in result.stdout
    assert "Candidates: 1" in result.stdout
    assert "type: location" in result.stdout
    assert "canonical: 1HRA0503ZL-" in result.stdout


def test_validate_reference_command_with_location_wildcard_without_tranche() -> None:
    result = runner.invoke(app, ["validate", "HRA0503ZL?"])

    assert result.exit_code == 0
    assert "Exact Match: no" in result.stdout
    assert "Candidates: 1" in result.stdout
    assert "canonical: HRA0503ZL-" in result.stdout


def test_validate_reference_command_with_location_wildcard_list_only() -> None:
    result = runner.invoke(app, ["validate", "1HRA0503ZL?", "--list-only"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["1HRA0503ZL-"]


def test_validate_reference_command_with_location_wildcard_without_tranche_list_only() -> None:
    result = runner.invoke(app, ["validate", "HRA0503ZL?", "--list-only"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["HRA0503ZL-"]
