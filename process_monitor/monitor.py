from __future__ import annotations

import psutil
from datetime import datetime
from typing import Any
from .analyzer import ProcessInfo


class ProcessMonitor:
    """Collects and retrieves running process information from the system.
    
    Uses psutil to gather detailed process metrics including CPU usage, memory
    consumption, file handles, and network connections. Handles permission errors
    gracefully for processes that cannot be accessed.
    """

    def collect(self) -> list[ProcessInfo]:
        """Collect information about all running processes.
        
        Returns:
            List of ProcessInfo objects sorted by CPU usage (descending)
        """
        processes: list[ProcessInfo] = []

        for proc in psutil.process_iter(["pid", "name", "username", "cpu_percent", "memory_percent", "status", "create_time"]):
            try:
                info = proc.info
                start_time = self._format_timestamp(info.get("create_time"))
                processes.append(
                    ProcessInfo(
                        pid=info.get("pid", 0),
                        name=info.get("name") or "<unknown>",
                        user=info.get("username") or "<system>",
                        cpu_percent=float(info.get("cpu_percent") or 0.0),
                        memory_percent=float(info.get("memory_percent") or 0.0),
                        status=info.get("status") or "unknown",
                        start_time=start_time,
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
                continue

        return sorted(processes, key=lambda proc: proc.cpu_percent, reverse=True)

    @staticmethod
    def _format_timestamp(timestamp: float | None) -> str:
        """Format Unix timestamp to readable datetime string."""
        if timestamp is None:
            return "N/A"
        try:
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        except (OSError, ValueError):
            return "N/A"

    def get_process_details(self, pid: int) -> dict[str, Any]:
        """Get detailed information about a specific process by PID.
        
        Retrieves comprehensive process information including command line,
        working directory, resource usage, open files, and network connections.
        Gracefully handles access denied and zombie process errors.
        
        Args:
            pid: The process ID to retrieve details for
            
        Returns:
            Dictionary containing process details
            
        Raises:
            ValueError: If process not found or is a zombie process
        """
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            raise ValueError(f"No running process was found with PID {pid}.")
        except psutil.ZombieProcess:
            raise ValueError(f"PID {pid} belongs to a zombie process and cannot be inspected.")

        details = {"pid": pid, "error": None}

        # Basic info
        try:
            details["name"] = proc.name()
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["name"] = "<unknown>"

        try:
            details["ppid"] = proc.ppid()
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["ppid"] = "N/A"

        try:
            details["user"] = proc.username()
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["user"] = "<unknown>"

        try:
            details["cmdline"] = " ".join(proc.cmdline()) or "<no command>"
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["cmdline"] = "<access denied>"

        try:
            details["cwd"] = proc.cwd()
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["cwd"] = "<access denied>"

        try:
            details["status"] = proc.status()
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["status"] = "<unknown>"

        try:
            details["cpu_percent"] = proc.cpu_percent(interval=0.1)
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["cpu_percent"] = 0.0

        try:
            mem_info = proc.memory_info()
            details["memory_percent"] = proc.memory_percent()
            details["memory_rss"] = mem_info.rss / (1024 * 1024)
            details["memory_vms"] = mem_info.vms / (1024 * 1024)
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["memory_percent"] = 0.0
            details["memory_rss"] = 0.0
            details["memory_vms"] = 0.0

        try:
            details["create_time"] = self._format_timestamp(proc.create_time())
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["create_time"] = "N/A"

        try:
            open_files = proc.open_files()
            details["open_files_count"] = len(open_files)
            details["open_files"] = [f.path for f in open_files[:10]]
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            details["open_files_count"] = 0
            details["open_files"] = []

        try:
            connections = proc.net_connections(kind="inet")
            details["connections_count"] = len(connections)
            details["connections"] = [
                f"{c.laddr.ip}:{c.laddr.port} -> {c.raddr.ip if c.raddr else 'N/A'}:{c.raddr.port if c.raddr else 'N/A'} ({c.status})"
                for c in connections[:5]
            ]
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess, OSError):
            details["connections_count"] = 0
            details["connections"] = []

        return details
