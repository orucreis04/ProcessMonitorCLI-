"""CLI command definitions for Process Monitor."""

import time

import typer
from .monitor import ProcessMonitor
from .analyzer import Analyzer
from .reporter import Reporter
from .utils import validate_positive_integer, validate_refresh_interval

app = typer.Typer(help="Process Monitor CLI")


@app.command("monitor")
def monitor(
    refresh: int = typer.Option(5, "-r", "--refresh", help="Refresh interval in seconds.", show_default=True),
    count: int = typer.Option(1, "-n", "--count", help="Number of snapshots to collect.", show_default=True),
) -> None:
    """Collect and display process metrics.
    
    Shows a table of processes with their CPU usage, memory consumption, and status.
    Can collect multiple snapshots with specified intervals.
    
    Args:
        refresh: Interval in seconds between snapshots
        count: Number of snapshots to collect
    """
    refresh = validate_refresh_interval(refresh)
    count = validate_positive_integer(count, "Snapshot count")
    monitor_instance = ProcessMonitor()
    reporter = Reporter()
    analyzer = Analyzer()

    for index in range(count):
        processes = monitor_instance.collect()
        analysis = analyzer.flag_suspicious_processes(processes)
        reporter.display(processes, analysis, index + 1, count)
        if index < count - 1:
            typer.echo(f"Refreshing in {refresh} seconds...\n")
            time.sleep(refresh)


@app.command("list")
def list_processes(
    limit: int = typer.Option(20, "-l", "--limit", help="Maximum number of processes to display.", show_default=True),
    sort_by: str = typer.Option("cpu", "-s", "--sort", help="Sort by: cpu, memory, pid, name.", show_default=True),
    json_export: str = typer.Option(None, "--json", help="Export results to JSON file."),
) -> None:
    """List all running processes.
    
    Displays processes in a table format with sorting and filtering options.
    Can export results to JSON file for integration with other tools.
    
    Args:
        limit: Maximum number of processes to display
        sort_by: Column to sort by (cpu, memory, pid, or name)
        json_export: Optional JSON file path for exporting results
    """
    limit = validate_positive_integer(limit, "Process limit")
    monitor_instance = ProcessMonitor()
    reporter = Reporter()
    analyzer = Analyzer()

    processes = monitor_instance.collect()

    try:
        processes = analyzer.sort_processes(processes, sort_by=sort_by)
    except ValueError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    if json_export:
        try:
            exported_path = reporter.export_json(processes, json_export)
            typer.secho(f"JSON report written to {exported_path}", fg=typer.colors.GREEN)
        except ValueError as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
    else:
        reporter.list_processes(processes, limit=limit)


@app.command("scan")
def scan(
    limit: int = typer.Option(20, "-l", "--limit", help="Maximum number of processes to display.", show_default=True),
    json_export: str = typer.Option(None, "--json", help="Export results to JSON file."),
) -> None:
    """Analyze running processes for security risks.
    
    Evaluates processes against security rules to identify potential threats.
    Provides risk scoring with LOW, MEDIUM, and HIGH severity levels.
    
    Args:
        limit: Maximum number of processes to display
        json_export: Optional JSON file path for exporting results
    """
    limit = validate_positive_integer(limit, "Process limit")
    monitor_instance = ProcessMonitor()
    reporter = Reporter()
    analyzer = Analyzer()

    processes = monitor_instance.collect()
    processes = analyzer.assess_process_risks(processes)

    if json_export:
        try:
            exported_path = reporter.export_json(processes, json_export)
            typer.secho(f"JSON report written to {exported_path}", fg=typer.colors.GREEN)
        except ValueError as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1)
    else:
        reporter.report_risks(processes, limit=limit)


@app.command("detail")
def detail(
    pid: int = typer.Argument(..., help="Process ID to display details for."),
) -> None:
    """Display detailed information about a specific process.
    
    Shows comprehensive process information including:
    - Basic info (PID, PPID, name, user, status)
    - Execution details (command line, working directory)
    - Resource usage (CPU, memory breakdown)
    - Open files and network connections
    
    Args:
        pid: The process ID to get detailed information for
    """
    monitor_instance = ProcessMonitor()
    reporter = Reporter()

    try:
        details = monitor_instance.get_process_details(pid)
        reporter.show_process_details(details)
    except ValueError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
