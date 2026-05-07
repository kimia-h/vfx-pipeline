import click
from rich.console import Console
from rich.table import Table
from rich import box
from .ingest import ingest_directory
from .validator import validate_filename
from .versioning import lock_asset, get_version_history
from .report import generate_report

console = Console()


@click.group()
def main():
    """VFX Asset Pipeline CLI — validate, ingest, and track studio assets."""
    pass


@main.command()
@click.argument("directory")
def ingest(directory):
    """Ingest all assets from a directory into the pipeline registry."""
    console.print(f"\n[bold]Ingesting assets from:[/bold] {directory}\n")

    try:
        results = ingest_directory(directory)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if results["passed"]:
        table = Table(title="Passed", box=box.SIMPLE, show_header=True)
        table.add_column("Filename", style="green")
        table.add_column("Shot")
        table.add_column("Type")
        table.add_column("Version")
        for a in results["passed"]:
            p = a["parsed"]
            table.add_row(
                a["filename"],
                f"{p['sequence']}_{p['shot']}",
                p["asset_type"],
                p["version"]
            )
        console.print(table)

    if results["failed"]:
        table = Table(title="Failed", box=box.SIMPLE, show_header=True)
        table.add_column("Filename", style="red")
        table.add_column("Error")
        for f in results["failed"]:
            table.add_row(f["filename"], f["error"])
        console.print(table)

    if results["skipped"]:
        table = Table(title="Skipped", box=box.SIMPLE, show_header=True)
        table.add_column("Filename", style="yellow")
        table.add_column("Reason")
        for s in results["skipped"]:
            table.add_row(s["filename"], s["reason"])
        console.print(table)

    console.print(
        f"\n[green]✓ {len(results['passed'])} ingested[/green]  "
        f"[red]✗ {len(results['failed'])} failed[/red]  "
        f"[yellow]⊘ {len(results['skipped'])} skipped[/yellow]\n"
    )


@main.command()
@click.argument("filename")
def validate(filename):
    """Validate a single filename against pipeline naming conventions."""
    result = validate_filename(filename)
    if result.valid:
        console.print(f"\n[green]✓ Valid[/green] — {filename}\n")
        for k, v in result.parsed.items():
            console.print(f"  {k:15} {v}")
    else:
        console.print(f"\n[red]✗ Invalid[/red] — {filename}")
        console.print(f"  [red]{result.error}[/red]\n")


@main.command()
def report():
    """Print a pipeline status report."""
    data = generate_report()

    console.print(f"\n[bold]Pipeline Status Report[/bold]")
    console.print(f"Generated: {data['generated_at']}\n")

    summary = Table(box=box.SIMPLE, show_header=False)
    summary.add_column("Metric", style="bold")
    summary.add_column("Value")
    summary.add_row("Total assets", str(data["total_assets"]))
    summary.add_row("Locked", str(data["locked"]))
    summary.add_row("Unlocked", str(data["unlocked"]))
    console.print(summary)

    if data["by_type"]:
        type_table = Table(title="By asset type", box=box.SIMPLE)
        type_table.add_column("Type")
        type_table.add_column("Count")
        for t, c in data["by_type"].items():
            type_table.add_row(t, str(c))
        console.print(type_table)

    if data["by_shot"]:
        shot_table = Table(title="By shot", box=box.SIMPLE)
        shot_table.add_column("Shot")
        shot_table.add_column("Count")
        for s, c in data["by_shot"].items():
            shot_table.add_row(s, str(c))
        console.print(shot_table)


@main.command()
@click.argument("filepath")
def lock(filepath):
    """Lock an asset version to prevent overwriting."""
    try:
        lock_asset(filepath)
        console.print(f"\n[green]✓ Locked:[/green] {filepath}\n")
    except ValueError as e:
        console.print(f"\n[red]Error:[/red] {e}\n")


@main.command()
@click.argument("filepath")
def history(filepath):
    """Show version history for an asset."""
    rows = get_version_history(filepath)
    if not rows:
        console.print(f"\n[yellow]No history found for:[/yellow] {filepath}\n")
        return
    table = Table(title="Version history", box=box.SIMPLE)
    table.add_column("Version")
    table.add_column("Checksum")
    table.add_column("Created at")
    for r in rows:
        table.add_row(r["version"], r["checksum"], r["created_at"])
    console.print(table)