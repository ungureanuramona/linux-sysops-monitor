
# Linux SysOps Monitor

![Linux SysOps Monitor CI](https://github.com/ungureanuramona/linux-sysops-monitor/actions/workflows/tests.yml/badge.svg)

A Python-based Linux monitoring project focused on system reliability, service health checks, incident detection, and operational automation.

Built as a hands-on SysOps and Site Reliability Engineering (SRE) portfolio project.

## Features

- Monitor CPU, memory, and disk utilization
- Classify resource usage as OK, WARNING, or CRITICAL
- Monitor Linux systemd service availability
- Detect and log unhealthy services
- Generate structured JSON health reports
- Support scheduled execution through Linux cron
- Run automated unit tests
- Validate changes using GitHub Actions CI

## Technology Stack

- Python 3.14
- Ubuntu Linux / WSL2
- psutil
- systemd / systemctl
- Linux cron
- Python logging and JSON
- unittest / unittest.mock
- Git and GitHub Actions

## Monitoring Thresholds

| Resource usage | Health status |
|---|---|
| Below 80% | OK |
| 80% to below 95% | WARNING |
| 95% or higher | CRITICAL |

These thresholds currently apply to CPU, memory, and disk utilization.

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

## Running the Monitor

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
Memory: 7.1% [OK]
Disk: 0.2% [OK]

SYSTEM SERVICES
-----------------------------------
systemd-journald.service: [OK] active
cron.service: [OK] active
rsyslog.service: [OK] active

JSON report saved to metrics.json
```

## JSON Health Reports

Each execution generates a `metrics.json` report containing:

- Monitoring timestamp
- CPU, memory, and disk utilization
- Health status for each resource
- Service availability and health status

Example:

```json
{
    "timestamp": "2026-10-27T13:00:00",
    "resources": {
        "cpu": {
            "usage_percent": 25.0,
            "status": "OK"
        },
        "memory": {
            "usage_percent": 85.0,
            "status": "WARNING"
        },
        "disk": {
            "usage_percent": 96.0,
            "status": "CRITICAL"
        }
    },
    "services": {
        "cron.service": {
            "status": "OK",
            "state": "active"
        }
    }
}
```

The JSON report is excluded from version control.

## Incident Detection and Logging

The monitor detects resource threshold violations and unhealthy Linux services.

Example simulated incident:

```text
nonexistent-demo.service: [CRITICAL] inactive
```

Example log entry:

```text
2026-10-27 12:52:51,845 | CRITICAL | Service nonexistent-demo.service is not healthy: inactive
```

Incidents are written to `monitor.log`.

The current implementation records incidents locally. External notifications are planned as a future improvement.

## Scheduled Monitoring with Cron

The monitor has been tested with a cron schedule running every five minutes.

Example crontab entry:

```cron
*/5 * * * * cd /path/to/linux-sysops-monitor && /path/to/linux-sysops-monitor/.venv/bin/python monitor.py >> cron.log 2>&1
```

Replace the example paths with your own installation paths.

The cron job is configured separately on each machine and is not installed automatically when cloning the repository.

Note: Under WSL2, the Linux distribution must be running for cron jobs to execute.

## Automated Tests

Run the test suite:

```bash
python -m unittest discover -v
```

Seven automated unit tests cover:

- OK, WARNING, and CRITICAL resource thresholds
- Active, inactive, and unknown systemd services
- JSON report generation and health status classification

## Continuous Integration

GitHub Actions automatically runs the unit tests on pushes and pull requests.

The CI workflow installs Python dependencies and executes the test suite to help detect regressions.

## SRE and SysOps Skills Demonstrated

- Linux system monitoring
- Systemd service health checks
- Incident detection and log analysis
- Operational automation with cron
- Structured monitoring data
- Python scripting and unit testing
- Git version control
- CI/CD with GitHub Actions

## Future Improvements

- YAML-based configuration for monitored services and thresholds
- Automatic incident notifications
- Additional automated tests and failure scenarios
- Incident response runbook and postmortem documentation
- Prometheus and Grafana integration
```
