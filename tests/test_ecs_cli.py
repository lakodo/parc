from pathlib import Path

from typer.testing import CliRunner

from parc.tools.ecs_inspect import app

runner = CliRunner()


def test_extract_command_returns_canonical_matches() -> None:
    result = runner.invoke(app, ["extract", "foo 1EAS1003VA- bar HRA0503ZL baz"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["1EAS1003VA-", "HRA0503ZL-"]


def test_extract_command_ignores_ambiguous_non_exact_candidates() -> None:
    result = runner.invoke(app, ["extract", "... RCP001PO ... RCC001PO ..."])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["RCP001PO-"]


def test_extract_command_accepts_unique_wildcard_candidates() -> None:
    result = runner.invoke(app, ["extract", "... HRA0503ZL? ..."])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["HRA0503ZL-"]


def test_extract_command_keeps_ambiguous_wildcard_candidates_as_patterns() -> None:
    result = runner.invoke(app, ["extract", "... ASG00?PO ..."])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["ASG00?PO"]


def test_extract_command_keeps_large_wildcard_patterns() -> None:
    result = runner.invoke(app, ["extract", "je veux travailler sur RCV*"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["RCV*"]


def test_extract_command_handles_mixed_exact_and_broad_patterns_quickly() -> None:
    result = runner.invoke(app, ["extract", "I'm looking for something about HDM0220PBA0025 et BKI00?PO- et 0*PO"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["HDM0220PBA0025", "BKI00?PO-"]


def test_extract_file_command(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    path.write_text("LHA0824JC and HLA0732CDF", encoding="utf-8")

    result = runner.invoke(app, ["extract-file", str(path)])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["LHA0824JC-", "HLA0732CDF"]


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


def test_validate_command_on_exact_location() -> None:
    result = runner.invoke(app, ["validate", "1HRA0503ZL-"])

    assert result.exit_code == 0
    assert "Exact Match: yes" in result.stdout
    assert "type: location" in result.stdout
    assert "building_label: Bâtiment réacteur" in result.stdout
    assert "local_kind_label: Local (pièce)" in result.stdout


def test_validate_command_on_exact_location_without_tranche() -> None:
    result = runner.invoke(app, ["validate", "HRA0503ZL-"])

    assert result.exit_code == 0
    assert "Exact Match: yes" in result.stdout
    assert "type: location" in result.stdout
    assert "canonical: HRA0503ZL-" in result.stdout
    assert "tranche_segment: <absent> -> Tranche non précisée" in result.stdout


def test_validate_command_with_location_wildcard() -> None:
    result = runner.invoke(app, ["validate", "1HRA0503ZL?"])

    assert result.exit_code == 0
    assert "Exact Match: no" in result.stdout
    assert "Candidates: 1" in result.stdout
    assert "type: location" in result.stdout
    assert "canonical: 1HRA0503ZL-" in result.stdout


def test_validate_command_with_location_wildcard_without_tranche() -> None:
    result = runner.invoke(app, ["validate", "HRA0503ZL?"])

    assert result.exit_code == 0
    assert "Exact Match: no" in result.stdout
    assert "Candidates: 1" in result.stdout
    assert "canonical: HRA0503ZL-" in result.stdout


def test_validate_command_with_location_wildcard_list_only() -> None:
    result = runner.invoke(app, ["validate", "1HRA0503ZL?", "--list-only"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["1HRA0503ZL-"]


def test_validate_command_with_location_wildcard_without_tranche_list_only() -> None:
    result = runner.invoke(app, ["validate", "HRA0503ZL?", "--list-only"])

    assert result.exit_code == 0
    assert result.stdout.splitlines() == ["HRA0503ZL-"]


def test_validate_command_accepts_zero_instead_of_o() -> None:
    result = runner.invoke(app, ["validate", "RCV002P0", "--limit", "1"])

    assert result.exit_code == 0
    assert "Query: RCV002P0" in result.stdout
    assert "Normalized: RCV002PO" in result.stdout
    assert "Exact Match: no" in result.stdout
    assert "Candidates: 1" in result.stdout
    assert "canonical: RCV002PO-" in result.stdout


def test_validate_command_accepts_zero_instead_of_o_exact() -> None:
    result = runner.invoke(app, ["validate", "RCV002P0-"])

    assert result.exit_code == 0
    assert "Query: RCV002P0-" in result.stdout
    assert "Normalized: RCV002PO-" in result.stdout
    assert "Exact Match: yes" in result.stdout
