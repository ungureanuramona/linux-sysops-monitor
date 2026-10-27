
# Linux SysOps Monitor
![Linux SysOps Monitor CI](https://github.com/ungureanuramona/linux-sysops-monitor/actions/workflows/tests.yml/badge.svg)
A lightweight Linux monitoring tool built with Python for system health checks, service availability monitoring, and incident logging.

## Features

- Monitor CPU, memory, and disk utilization
- Detect WARNING and CRITICAL resource thresholds
- Check Linux systemd service availability
- Log incidents with timestamps and severity levels
- Run automated unit tests using unittest
- Execute tests automatically with GitHub Actions

## Technologies

- Python 3.14
- Ubuntu Linux / WSL2
- psutil
- systemd / systemctl
- Python unittest and unittest.mock
- GitHub Actions

## Monitoring Thresholds

| Usage | Status |
|---|---|
| Below 80% | OK |
| 80% to below 95% | WARNING |
| 95% or higher | CRITICAL |

## Installation

Clone the repository:

```bash
git clone https://github.com/ungureanuramona/linux-sysops-monitor.git
cd linux-sysops-monitor
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the monitor:

```bash
python monitor.py
```

Example output:

```text
Linux SysOps Monitor
-----------------------------------

SYSTEM RESOURCES
-----------------------------------
CPU: 0.0% [OK]
Memory: 6.7% [OK]
Disk: 0.2% [OK]

SYSTEM SERVICES
-----------------------------------
systemd-journald.service: [OK] active
cron.service: [OK] active
rsyslog.service: [OK] active
```

## Incident Detection

The monitor identifies inactive Linux services and reports them as CRITICAL.

Example simulated incident:

```text
nonexistent-demo.service: [CRITICAL] inactive
```

Incident log example:

```text
2026-10-27 12:52:51,845 | CRITICAL | Service nonexistent-demo.service is not healthy: inactive
```

Alerts are written to `monitor.log`, which is excluded from version control.

## Automated Tests

Run all tests:

```bash
python -m unittest discover -v
```

Six unit tests cover resource alert thresholds and active, inactive, and unknown service states.

## CI/CD

GitHub Actions automatically installs dependencies and runs the unit test suite on pushes and pull requests.

## Skills Demonstrated

Linux system administration, system monitoring, service health checks, incident detection, troubleshooting, Python scripting, automated testing, and CI/CD.

## Future Improvements

- JSON-formatted monitoring reports
- Configurable service lists and thresholds
- Scheduled monitoring
- Prometheus and Grafana integration
- Alert notifications
