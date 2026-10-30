import tempfile
import unittest
from pathlib import Path

from monitor import get_status, load_config


class TestConfiguration(unittest.TestCase):

    def load_yaml(self, content):
        with tempfile.TemporaryDirectory() as directory:
            config_file = Path(directory) / "config.yaml"
            config_file.write_text(content, encoding="utf-8")
            return load_config(config_file)

    def test_valid_configuration(self):
        config = self.load_yaml("""
thresholds:
  warning: 80
  critical: 95
services:
  - cron.service
  - rsyslog.service
""")
        self.assertEqual(config["thresholds"]["warning"], 80)
        self.assertEqual(config["thresholds"]["critical"], 95)
        self.assertEqual(len(config["services"]), 2)

    def test_invalid_threshold_order(self):
        with self.assertRaises(ValueError):
            self.load_yaml("""
thresholds:
  warning: 95
  critical: 80
services:
  - cron.service
""")

    def test_empty_services(self):
        with self.assertRaises(ValueError):
            self.load_yaml("""
thresholds:
  warning: 80
  critical: 95
services: []
""")

    def test_invalid_yaml_structure(self):
        with self.assertRaises(ValueError):
            self.load_yaml("""
- warning
- critical
""")

    def test_custom_thresholds(self):
        self.assertEqual(
            get_status(75, warning=70, critical=90),
            "WARNING",
        )
        self.assertEqual(
            get_status(92, warning=70, critical=90),
            "CRITICAL",
        )


if __name__ == "__main__":
    unittest.main()
