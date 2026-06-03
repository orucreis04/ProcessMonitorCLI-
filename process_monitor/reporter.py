from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.text import Text
from .analyzer import ProcessInfo

console = Console()


class Reporter:
    """Displays process data on the command line and exports to JSON format."""

    def display(self, processes: list[ProcessInfo], analysis: list[ProcessInfo], snapshot: int, total: int) -> None:
        """Display process metrics as a formatted table.
        
        Args:
            processes: List of process information objects
            analysis: Analyzed process data with suspicious flags
            snapshot: Current snapshot number
            total: Total snapshots to collect
        """
        table = Table(title=f"Process Monitor Snapshot {snapshot}/{total}")
        table.add_column("PID", justify="right", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("User", style="green")
        table.add_column("CPU %", justify="right")
        table.add_column("MEM %", justify="right")
        table.add_column("Status")
        table.add_column("Flag", justify="center")

        for process in analysis[:20]:
            flag = Text("OK", style="green")
            if process.suspicious:
                flag = Text("SUSPICIOUS", style="bold red")

            table.add_row(
                str(process.pid),
                process.name,
                process.user,
                f"{process.cpu_percent:.1f}",
                f"{process.memory_percent:.1f}",
                process.status,
                flag,
            )

        console.print(table)

    def list_processes(self, processes: list[ProcessInfo], limit: int = 50) -> None:
        """Display all processes in a table format."""
        table = Table(title=f"Running Processes ({len(processes)} total)")
        table.add_column("PID", justify="right", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("User", style="green")
        table.add_column("CPU %", justify="right")
        table.add_column("MEM %", justify="right")
        table.add_column("Status", style="yellow")
        table.add_column("Start Time", style="blue")

        for process in processes[:limit]:
            table.add_row(
                str(process.pid),
                process.name,
                process.user,
                f"{process.cpu_percent:.1f}",
                f"{process.memory_percent:.1f}",
                process.status,
                process.start_time,
            )

        console.print(table)
        if len(processes) > limit:
            console.print(f"\n[yellow]Showing {limit} of {len(processes)} processes[/yellow]")

    def report_risks(self, processes: list[ProcessInfo], limit: int = 20) -> None:
        """Display process security risk analysis in table format."""
        high_risk = [p for p in processes if p.risk_level == "HIGH"]
        medium_risk = [p for p in processes if p.risk_level == "MEDIUM"]
        
        table = Table(title=f"Security Risk Analysis ({len(processes)} total processes)")
        table.add_column("PID", justify="right", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("User", style="green")
        table.add_column("CPU %", justify="right")
        table.add_column("MEM %", justify="right")
        table.add_column("Risk Score", justify="right", style="yellow")
        table.add_column("Risk Level", justify="center")
        table.add_column("Reason", style="dim")

        for process in processes[:limit]:
            level_style = "red"
            if process.risk_level == "MEDIUM":
                level_style = "yellow"
            elif process.risk_level == "LOW":
                level_style = "green"

            level_text = Text(process.risk_level, style=f"bold {level_style}")

            table.add_row(
                str(process.pid),
                process.name,
                process.user,
                f"{process.cpu_percent:.1f}",
                f"{process.memory_percent:.1f}",
                str(process.risk_score),
                level_text,
                process.risk_reason,
            )

        console.print(table)
        
        if high_risk:
            console.print(f"\n[bold red]HIGH RISK: {len(high_risk)} process(es) detected[/bold red]")
        if medium_risk:
            console.print(f"[bold yellow]MEDIUM RISK: {len(medium_risk)} process(es) detected[/bold yellow]")
        
        if len(processes) > limit:
            console.print(f"\n[yellow]Showing {limit} of {len(processes)} processes[/yellow]")

    def show_process_details(self, details: dict[str, Any]) -> None:
        """Display detailed information about a specific process."""
        from rich.panel import Panel

        basic_info = f"""[cyan]PID:[/cyan] {details.get('pid', 'N/A')}
[cyan]PPID:[/cyan] {details.get('ppid', 'N/A')}
[cyan]Name:[/cyan] {details.get('name', '<unknown>')}
[cyan]User:[/cyan] {details.get('user', '<unknown>')}
[cyan]Status:[/cyan] {details.get('status', '<unknown>')}
[cyan]Created:[/cyan] {details.get('create_time', 'N/A')}
        """
        console.print(Panel(basic_info.strip(), title="Basic Information", expand=False))

        cmd_info = f"""[cyan]Command:[/cyan] {details.get('cmdline', '<access denied>')}
[cyan]Working Dir:[/cyan] {details.get('cwd', '<access denied>')}
        """
        console.print(Panel(cmd_info.strip(), title="Execution Information", expand=False))

        resource_info = f"""[cyan]CPU Usage:[/cyan] {details.get('cpu_percent', 0.0):.1f}%
[cyan]Memory Usage:[/cyan] {details.get('memory_percent', 0.0):.1f}%
[cyan]Memory (RSS):[/cyan] {details.get('memory_rss', 0.0):.1f} MB
[cyan]Memory (VMS):[/cyan] {details.get('memory_vms', 0.0):.1f} MB
        """
        console.print(Panel(resource_info.strip(), title="Resource Usage", expand=False))

        open_files = details.get("open_files", [])
        files_count = details.get("open_files_count", 0)
        if open_files:
            files_text = "\n".join([f"  - {f}" for f in open_files])
            if files_count > 10:
                files_text += f"\n  ... and {files_count - 10} more"
            files_info = f"[cyan]Total:[/cyan] {files_count}\n\n{files_text}"
        else:
            files_info = f"[cyan]Total:[/cyan] {files_count}\n[dim]No open files[/dim]"
        console.print(Panel(files_info, title="Open Files", expand=False))

        connections = details.get("connections", [])
        conn_count = details.get("connections_count", 0)
        if connections:
            conn_text = "\n".join([f"  - {c}" for c in connections])
            if conn_count > 5:
                conn_text += f"\n  ... and {conn_count - 5} more"
            conn_info = f"[cyan]Total:[/cyan] {conn_count}\n\n{conn_text}"
        else:
            conn_info = f"[cyan]Total:[/cyan] {conn_count}\n[dim]No network connections[/dim]"
        console.print(Panel(conn_info, title="Network Connections", expand=False))

    def export_json(self, processes: list[ProcessInfo], filename: str) -> Path:
        """Export process list to JSON file."""
        try:
            data = {
                "timestamp": self._get_timestamp(),
                "total_processes": len(processes),
                "processes": [
                    {
                        "pid": p.pid,
                        "name": p.name,
                        "user": p.user,
                        "cpu_percent": p.cpu_percent,
                        "memory_percent": p.memory_percent,
                        "status": p.status,
                        "start_time": p.start_time,
                        "suspicious": p.suspicious,
                        "risk_score": p.risk_score,
                        "risk_level": p.risk_level,
                        "risk_reason": p.risk_reason,
                    }
                    for p in processes
                ],
            }

            file_path = Path(filename)
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return file_path.absolute()
        except (IOError, OSError) as e:
            raise ValueError(f"Could not write JSON report to '{filename}': {e}") from e
        except Exception as e:
            raise ValueError(f"Could not export JSON report: {e}") from e

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
