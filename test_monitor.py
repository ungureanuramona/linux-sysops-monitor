import subprocess
import unittest
from unittest.mock import patch

from monitor import get_status, check_service


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


if __name__ == "__main__":
    unittest.main()
