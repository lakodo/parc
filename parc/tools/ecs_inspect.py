"""CLI to inspect ECS references inside text or files."""

from __future__ import annotations

from pathlib import Path

import typer

from parc.naming import ecs

app = typer.Typer(help="Inspect ECS references in free text or files.")


def _emit_extract_report(text: str) -> int:
    detections = ecs.extract_references(text)
    for detection in detections:
        typer.echo(detection.canonical)
    return 0 if detections else 1


def _emit_validation_report(query: str, limit: int, *, list_only: bool = False) -> int:
    result = ecs.validate_rf(query, limit=limit)
    if list_only:
        for candidate in result.candidates:
            typer.echo(str(candidate))
        return 0 if result.candidates else 1

    typer.echo(f"Query: {result.query}")
    typer.echo(f"Normalized: {result.normalized_query}")
    typer.echo(f"Exact Match: {'yes' if result.is_exact_match else 'no'}")
    typer.echo(f"Candidates: {len(result.candidates)}")
    if result.truncated:
        typer.echo(f"Truncated: yes (limit={limit})")
    else:
        typer.echo("Truncated: no")
    typer.echo("")

    if not result.candidates:
        typer.echo("No RF candidate detected.")
        return 1

    for index, candidate in enumerate(result.candidates, start=1):
        typer.echo(f"Candidate {index}:")
        typer.echo(
            ecs.format_detection(
                ecs.DetectedReference(
                    kind="rf",
                    raw=str(candidate),
                    start=0,
                    end=len(str(candidate)),
                    parsed=candidate,
                )
            )
        )
        if index != len(result.candidates):
            typer.echo("")

    return 0


def _emit_reference_validation_report(query: str, limit: int, *, list_only: bool = False) -> int:
    result = ecs.validate_reference(query, limit=limit)
    if result.is_exact_match:
        detection = result.candidates[0]
        if list_only:
            typer.echo(detection.canonical)
            return 0
        typer.echo(f"Query: {query}")
        typer.echo(f"Normalized: {detection.canonical}")
        typer.echo("Exact Match: yes")
        typer.echo("Candidates: 1")
        typer.echo("Truncated: no")
        typer.echo("")
        typer.echo(ecs.format_detection(detection))
        return 0

    if list_only:
        for detection in result.candidates:
            typer.echo(detection.canonical)
        return 0 if result.candidates else 1

    typer.echo(f"Query: {result.query}")
    typer.echo(f"Normalized: {result.normalized_query}")
    typer.echo("Exact Match: no")
    typer.echo(f"Candidates: {len(result.candidates)}")
    if result.truncated:
        typer.echo(f"Truncated: yes (limit={limit})")
    else:
        typer.echo("Truncated: no")
    typer.echo("")

    if not result.candidates:
        typer.echo("No ECS candidate detected.")
        return 1

    for index, detection in enumerate(result.candidates, start=1):
        typer.echo(f"Candidate {index}:")
        typer.echo(ecs.format_detection(detection))
        if index != len(result.candidates):
            typer.echo("")

    return 0


@app.command("extract")
def extract_command(text: str) -> None:
    """Extract canonical ECS references from a raw text."""

    raise typer.Exit(_emit_extract_report(text))


@app.command("extract-file")
def extract_file_command(path: Path) -> None:
    """Extract canonical ECS references from a text file."""

    if not path.exists():
        typer.secho(f"File not found: {path}", err=True, fg=typer.colors.RED)
        raise typer.Exit(2)
    if not path.is_file():
        typer.secho(f"Not a file: {path}", err=True, fg=typer.colors.RED)
        raise typer.Exit(2)

    text = path.read_text(encoding="utf-8")
    raise typer.Exit(_emit_extract_report(text))


@app.command("validate")
def validate_command(query: str, limit: int = 10, list_only: bool = False) -> None:
    """Validate an ECS reference of any supported type, with RF fallback."""

    raise typer.Exit(_emit_reference_validation_report(query, limit, list_only=list_only))


if __name__ == "__main__":
    app()
