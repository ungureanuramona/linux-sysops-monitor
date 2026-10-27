
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from monitor import check_service, get_status, save_json_report


class TestMonitorAlerts(unittest.TestCase):

    def test_ok(self):
        self.assertEqual(get_status(25), "OK")
        self.assertEqual(get_status(79.9), "OK")

    def test_warning(self):
        self.assertEqual(get_status(80), "WARNING")
        self.assertEqual(get_status(90), "WARNING")
        self.assertEqual(get_status(94.9), "WARNING")

    def test_critical(self):
        self.assertEqual(get_status(95), "CRITICAL")
        self.assertEqual(get_status(100), "CRITICAL")


class TestServiceMonitoring(unittest.TestCase):

    @patch("monitor.subprocess.run")
    def test_active_service(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["systemctl", "is-active", "cron.service"],
            returncode=0,
            stdout="active\n",
            stderr="",
        )

        status, state = check_service("cron.service")

        self.assertEqual(status, "OK")
        self.assertEqual(state, "active")

    @patch("monitor.subprocess.run")
    def test_inactive_service(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["systemctl", "is-active", "demo.service"],
            returncode=3,
            stdout="inactive\n",
            stderr="",
        )

        status, state = check_service("demo.service")

        self.assertEqual(status, "CRITICAL")
        self.assertEqual(state, "inactive")

    @patch("monitor.subprocess.run")
    def test_unknown_service(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["systemctl", "is-active", "missing.service"],
            returncode=4,
            stdout="unknown\n",
            stderr="",
        )

        status, state = check_service("missing.service")

        self.assertEqual(status, "CRITICAL")
        self.assertEqual(state, "unknown")


class TestJsonReport(unittest.TestCase):

    def test_json_report(self):
        metrics = {
            "timestamp": "2026-10-27T13:00:00",
            "cpu_percent": 25.0,
            "memory_percent": 85.0,
            "disk_percent": 96.0,
        }

        services = {
            "cron.service": {
                "status": "OK",
                "state": "active",
            }
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "metrics.json"

            with patch("monitor.open", create=True) as mocked_open:
                import builtins

                mocked_open.side_effect = (
                    lambda filename, *args, **kwargs:
                    builtins.open(output_file, *args, **kwargs)
                )

                save_json_report(metrics, services)

            with output_file.open(encoding="utf-8") as file:
                report = json.load(file)

        self.assertEqual(
            report["timestamp"],
            "2026-10-27T13:00:00",
        )

        self.assertEqual(
            report["resources"]["cpu"]["status"],
            "OK",
        )

        self.assertEqual(
            report["resources"]["memory"]["status"],
            "WARNING",
        )

        self.assertEqual(
            report["resources"]["disk"]["status"],
            "CRITICAL",
        )

        self.assertEqual(
            report["services"]["cron.service"]["state"],
            "active",
        )


if __name__ == "__main__":
    unittest.main()
