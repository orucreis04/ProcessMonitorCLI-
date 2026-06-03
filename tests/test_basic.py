"""Basic unit tests for Process Monitor CLI."""

import unittest
from process_monitor.analyzer import Analyzer, ProcessInfo
from process_monitor.monitor import ProcessMonitor
from process_monitor.reporter import Reporter


class TestProcessMonitor(unittest.TestCase):
    """Test ProcessMonitor class."""

    def test_monitor_collects_processes(self) -> None:
        """Test that monitor can collect running processes."""
        monitor = ProcessMonitor()
        processes = monitor.collect()
        self.assertIsInstance(processes, list)
        self.assertGreater(len(processes), 0)
        self.assertTrue(all(hasattr(proc, "pid") for proc in processes))
        self.assertTrue(all(hasattr(proc, "name") for proc in processes))
        self.assertTrue(all(hasattr(proc, "user") for proc in processes))

    def test_monitor_process_attributes(self) -> None:
        """Test that collected processes have required attributes."""
        monitor = ProcessMonitor()
        processes = monitor.collect()
        
        for proc in processes[:5]:
            self.assertIsInstance(proc.pid, int)
            self.assertIsInstance(proc.name, str)
            self.assertIsInstance(proc.user, str)
            self.assertIsInstance(proc.cpu_percent, float)
            self.assertIsInstance(proc.memory_percent, float)
            self.assertIsInstance(proc.status, str)

    def test_format_timestamp_with_valid_value(self) -> None:
        """Test timestamp formatting with valid Unix timestamp."""
        monitor = ProcessMonitor()
        result = monitor._format_timestamp(1685894400.0)  # Valid Unix timestamp
        self.assertIsInstance(result, str)
        self.assertIn("-", result)  # Check YYYY-MM-DD format

    def test_format_timestamp_with_none(self) -> None:
        """Test timestamp formatting with None value."""
        monitor = ProcessMonitor()
        result = monitor._format_timestamp(None)
        self.assertEqual(result, "N/A")


class TestAnalyzer(unittest.TestCase):
    """Test Analyzer class."""

    def test_analyzer_flags_suspicious_processes(self) -> None:
        """Test process evaluation for suspicious activity."""
        analyzer = Analyzer()
        test_proc = ProcessInfo(
            pid=1, name="test", user="user", 
            cpu_percent=10.0, memory_percent=5.0,
            status="running", start_time="2026-06-03 10:00:00"
        )
        result = analyzer.flag_suspicious_processes([test_proc])
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0].suspicious, bool)

    def test_sort_by_cpu(self) -> None:
        """Test sorting processes by CPU usage."""
        analyzer = Analyzer()
        processes = [
            ProcessInfo(pid=1, name="proc1", user="user", cpu_percent=5.0, 
                       memory_percent=1.0, status="running", start_time=""),
            ProcessInfo(pid=2, name="proc2", user="user", cpu_percent=15.0, 
                       memory_percent=2.0, status="running", start_time=""),
            ProcessInfo(pid=3, name="proc3", user="user", cpu_percent=10.0, 
                       memory_percent=3.0, status="running", start_time=""),
        ]
        result = analyzer.sort_processes(processes, "cpu")
        self.assertEqual(result[0].cpu_percent, 15.0)
        self.assertEqual(result[1].cpu_percent, 10.0)
        self.assertEqual(result[2].cpu_percent, 5.0)

    def test_sort_by_memory(self) -> None:
        """Test sorting processes by memory usage."""
        analyzer = Analyzer()
        processes = [
            ProcessInfo(pid=1, name="proc1", user="user", cpu_percent=1.0, 
                       memory_percent=5.0, status="running", start_time=""),
            ProcessInfo(pid=2, name="proc2", user="user", cpu_percent=2.0, 
                       memory_percent=15.0, status="running", start_time=""),
            ProcessInfo(pid=3, name="proc3", user="user", cpu_percent=3.0, 
                       memory_percent=10.0, status="running", start_time=""),
        ]
        result = analyzer.sort_processes(processes, "memory")
        self.assertEqual(result[0].memory_percent, 15.0)
        self.assertEqual(result[1].memory_percent, 10.0)
        self.assertEqual(result[2].memory_percent, 5.0)

    def test_sort_by_pid(self) -> None:
        """Test sorting processes by PID."""
        analyzer = Analyzer()
        processes = [
            ProcessInfo(pid=3, name="proc3", user="user", cpu_percent=1.0, 
                       memory_percent=1.0, status="running", start_time=""),
            ProcessInfo(pid=1, name="proc1", user="user", cpu_percent=1.0, 
                       memory_percent=1.0, status="running", start_time=""),
            ProcessInfo(pid=2, name="proc2", user="user", cpu_percent=1.0, 
                       memory_percent=1.0, status="running", start_time=""),
        ]
        result = analyzer.sort_processes(processes, "pid")
        self.assertEqual(result[0].pid, 1)
        self.assertEqual(result[1].pid, 2)
        self.assertEqual(result[2].pid, 3)

    def test_sort_by_name(self) -> None:
        """Test sorting processes by name."""
        analyzer = Analyzer()
        processes = [
            ProcessInfo(pid=1, name="zebra", user="user", cpu_percent=1.0, 
                       memory_percent=1.0, status="running", start_time=""),
            ProcessInfo(pid=2, name="apple", user="user", cpu_percent=1.0, 
                       memory_percent=1.0, status="running", start_time=""),
            ProcessInfo(pid=3, name="banana", user="user", cpu_percent=1.0, 
                       memory_percent=1.0, status="running", start_time=""),
        ]
        result = analyzer.sort_processes(processes, "name")
        self.assertEqual(result[0].name, "apple")
        self.assertEqual(result[1].name, "banana")
        self.assertEqual(result[2].name, "zebra")

    def test_invalid_sort_option(self) -> None:
        """Test that invalid sort option raises ValueError."""
        analyzer = Analyzer()
        processes = [
            ProcessInfo(pid=1, name="test", user="user", cpu_percent=1.0, 
                       memory_percent=1.0, status="running", start_time=""),
        ]
        with self.assertRaises(ValueError):
            analyzer.sort_processes(processes, "invalid_sort")

    def test_assess_process_risks_low_risk(self) -> None:
        """Test risk analysis for low-risk process."""
        analyzer = Analyzer()
        test_proc = ProcessInfo(
            pid=1, name="normal_process", user="user",
            cpu_percent=10.0, memory_percent=5.0,
            status="running", start_time="2026-06-03 10:00:00"
        )
        result = analyzer.assess_process_risks([test_proc])
        self.assertEqual(result[0].risk_level, "LOW")
        self.assertLess(result[0].risk_score, 30)

    def test_assess_process_risks_high_cpu(self) -> None:
        """Test risk analysis for high CPU usage."""
        analyzer = Analyzer()
        test_proc = ProcessInfo(
            pid=1, name="cpu_hog", user="user",
            cpu_percent=90.0, memory_percent=5.0,
            status="running", start_time="2026-06-03 10:00:00"
        )
        result = analyzer.assess_process_risks([test_proc])
        self.assertGreater(result[0].risk_score, 0)
        self.assertIn("High CPU", result[0].risk_reason)

    def test_assess_process_risks_high_memory(self) -> None:
        """Test risk analysis for high memory usage."""
        analyzer = Analyzer()
        test_proc = ProcessInfo(
            pid=1, name="memory_hog", user="user",
            cpu_percent=10.0, memory_percent=60.0,
            status="running", start_time="2026-06-03 10:00:00"
        )
        result = analyzer.assess_process_risks([test_proc])
        self.assertGreater(result[0].risk_score, 0)
        self.assertIn("High memory", result[0].risk_reason)

    def test_assess_process_risks_suspicious_keyword(self) -> None:
        """Test risk analysis for suspicious keyword in process name."""
        analyzer = Analyzer()
        test_proc = ProcessInfo(
            pid=1, name="crypto_miner", user="user",
            cpu_percent=10.0, memory_percent=5.0,
            status="running", start_time="2026-06-03 10:00:00"
        )
        result = analyzer.assess_process_risks([test_proc])
        self.assertGreaterEqual(result[0].risk_score, 40)
        self.assertIn("Suspicious keyword", result[0].risk_reason)


class TestReporter(unittest.TestCase):
    """Test Reporter class."""

    def test_reporter_initialization(self) -> None:
        """Test reporter can be initialized."""
        reporter = Reporter()
        self.assertIsInstance(reporter, Reporter)

    def test_reporter_display_method_exists(self) -> None:
        """Test reporter has display method."""
        reporter = Reporter()
        self.assertTrue(hasattr(reporter, "display"))
        self.assertTrue(callable(reporter.display))

    def test_reporter_list_processes_method_exists(self) -> None:
        """Test reporter has list_processes method."""
        reporter = Reporter()
        self.assertTrue(hasattr(reporter, "list_processes"))
        self.assertTrue(callable(reporter.list_processes))

    def test_reporter_export_json_method_exists(self) -> None:
        """Test reporter has export_json method."""
        reporter = Reporter()
        self.assertTrue(hasattr(reporter, "export_json"))
        self.assertTrue(callable(reporter.export_json))


if __name__ == "__main__":
    unittest.main()
