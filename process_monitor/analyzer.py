from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class ProcessInfo:
    """Container for process information and risk analysis data."""
    pid: int
    name: str
    user: str
    cpu_percent: float
    memory_percent: float
    status: str
    start_time: str = ""
    suspicious: bool = False
    risk_score: int = 0
    risk_level: str = "LOW"
    risk_reason: str = ""


class Analyzer:
    """Analyzes process metrics and calculates security risk scores."""

    cpu_threshold = 50.0
    memory_threshold = 50.0

    def flag_suspicious_processes(self, processes: Iterable[ProcessInfo]) -> list[ProcessInfo]:
        """Mark processes as suspicious based on resource usage patterns.
        
        Args:
            processes: Iterable of process information
            
        Returns:
            List of ProcessInfo objects with suspicious flags set
        """
        results: list[ProcessInfo] = []

        for process in processes:
            suspicious = self._has_suspicious_resource_usage(process)
            results.append(ProcessInfo(**{**process.__dict__, "suspicious": suspicious}))

        return results

    def _has_suspicious_resource_usage(self, process: ProcessInfo) -> bool:
        """Determine if a process should be flagged as suspicious.
        
        Args:
            process: Process information to evaluate
            
        Returns:
            True if process exhibits suspicious behavior, False otherwise
        """
        if process.cpu_percent >= self.cpu_threshold:
            return True
        if process.memory_percent >= self.memory_threshold:
            return True
        return False

    def sort_processes(self, processes: list[ProcessInfo], sort_by: str = "cpu") -> list[ProcessInfo]:
        """Sort processes by given criteria (cpu, memory, pid, name)."""
        sort_by_lower = sort_by.lower()

        if sort_by_lower == "cpu":
            return sorted(processes, key=lambda p: p.cpu_percent, reverse=True)
        elif sort_by_lower in ("memory", "mem"):
            return sorted(processes, key=lambda p: p.memory_percent, reverse=True)
        elif sort_by_lower == "pid":
            return sorted(processes, key=lambda p: p.pid)
        elif sort_by_lower == "name":
            return sorted(processes, key=lambda p: p.name)
        else:
            raise ValueError(f"'{sort_by}' is not a supported sort field. Use one of: cpu, memory, pid, name.")

    def assess_process_risks(self, processes: list[ProcessInfo]) -> list[ProcessInfo]:
        """Analyze processes for security risks and calculate risk scores."""
        results: list[ProcessInfo] = []

        for process in processes:
            score, level, reason = self._calculate_risk(process)
            results.append(
                ProcessInfo(
                    **{**process.__dict__, "risk_score": score, "risk_level": level, "risk_reason": reason}
                )
            )

        return sorted(results, key=lambda p: p.risk_score, reverse=True)

    def _calculate_risk(self, process: ProcessInfo) -> tuple[int, str, str]:
        """Calculate risk score and level for a single process."""
        score = 0
        reasons = []

        # CPU usage rule
        if process.cpu_percent >= 80.0:
            score += 30
            reasons.append(f"High CPU usage ({process.cpu_percent:.1f}%)")

        # Memory usage rule
        if process.memory_percent >= 50.0:
            score += 25
            reasons.append(f"High memory usage ({process.memory_percent:.1f}%)")

        # Unknown process rule
        if not process.name or process.name == "<unknown>":
            score += 20
            reasons.append("Unknown process name")

        # Root user rule
        if process.user == "root":
            score += 10
            reasons.append("Running as root")

        # Suspicious keywords rule
        suspicious_keywords = {"miner", "crypto", "payload", "reverse", "backdoor", "nc", "netcat"}
        name_lower = process.name.lower()
        for keyword in suspicious_keywords:
            if keyword in name_lower:
                score += 40
                reasons.append(f"Suspicious keyword: {keyword}")
                break

        # Determine risk level
        if score < 30:
            level = "LOW"
        elif score < 60:
            level = "MEDIUM"
        else:
            level = "HIGH"

        reason_text = "; ".join(reasons) if reasons else "No issues detected"
        return min(score, 100), level, reason_text
