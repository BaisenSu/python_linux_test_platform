from __future__ import annotations
from rich.console import Console
from rich.table import Table
from .test_runner import run_smoke_tests

def main():
    console = Console()
    console.rule("[bold cyan]Python Linux Test Platform — Showcase (Mock)")

    rpt, ok, out_dir = run_smoke_tests(mode="mock", uut_id="DEMO-123")

    table = Table(title="Run Summary", show_lines=True)
    table.add_column("Step", style="bold")
    table.add_column("Status")
    table.add_column("Output")
    table.add_column("Error")

    for r in rpt.records:
        table.add_row(r["name"], r["status"], str(r["output"]), str(r["error"]))

    console.print(table)
    console.print(f"[green]Overall OK:[/green] {ok}")
    console.print(f"[yellow]Artifacts:[/yellow] {out_dir}")