
import json
import logging
import subprocess
from datetime import datetime

import psutil


# Alert thresholds
WARNING_THRESHOLD = 80
CRITICAL_THRESHOLD = 95


# Linux services to monitor
SERVICES = [
    "systemd-journald.service",
    "cron.service",
    "rsyslog.service",
]


# Logging configuration
logging.basicConfig(
    filename="monitor.log",
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def get_system_metrics():
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }


def get_status(value):
    if value >= CRITICAL_THRESHOLD:
        return "CRITICAL"
    elif value >= WARNING_THRESHOLD:
        return "WARNING"
    return "OK"


def check_service(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )

    state = result.stdout.strip() or "unknown"

    status = (
        "OK"
        if result.returncode == 0 and state == "active"
        else "CRITICAL"
    )

    return status, state


def save_json_report(metrics, services):
    report = {
        "timestamp": metrics["timestamp"],
        "resources": {
            "cpu": {
                "usage_percent": metrics["cpu_percent"],
                "status": get_status(metrics["cpu_percent"]),
            },
            "memory": {
                "usage_percent": metrics["memory_percent"],
                "status": get_status(metrics["memory_percent"]),
            },
            "disk": {
                "usage_percent": metrics["disk_percent"],
                "status": get_status(metrics["disk_percent"]),
            },
        },
        "services": services,
    }

    with open("metrics.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def main():
    metrics = get_system_metrics()

    print("\nLinux SysOps Monitor")
    print("-" * 35)
    print(f"Timestamp: {metrics['timestamp']}")

    # System resource monitoring
    resources = {
        "CPU": metrics["cpu_percent"],
        "Memory": metrics["memory_percent"],
        "Disk": metrics["disk_percent"],
    }

    print("\nSYSTEM RESOURCES")
    print("-" * 35)

    for name, usage in resources.items():
        status = get_status(usage)

        print(f"{name}: {usage:.1f}% [{status}]")

        if status == "WARNING":
            logging.warning(
                "%s usage is high: %.1f%%",
                name,
                usage,
            )

        elif status == "CRITICAL":
            logging.critical(
                "%s usage is critical: %.1f%%",
                name,
                usage,
            )

    # Linux service monitoring
    print("\nSYSTEM SERVICES")
    print("-" * 35)

    services_report = {}

    for service in SERVICES:
        try:
            status, state = check_service(service)

            print(f"{service}: [{status}] {state}")

            services_report[service] = {
                "status": status,
                "state": state,
            }

            if status == "CRITICAL":
                logging.critical(
                    "Service %s is not healthy: %s",
                    service,
                    state,
                )

        except subprocess.TimeoutExpired:
            print(f"{service}: [CRITICAL] timeout")

            services_report[service] = {
                "status": "CRITICAL",
                "state": "timeout",
            }

            logging.critical(
                "Service %s check timed out",
                service,
            )

        except OSError as error:
            print(f"{service}: [CRITICAL] {error}")

            services_report[service] = {
                "status": "CRITICAL",
                "state": "error",
                "message": str(error),
            }

            logging.critical(
                "Service %s check failed: %s",
                service,
                error,
            )

    # Save monitoring results as JSON
    save_json_report(metrics, services_report)

    print("\nJSON report saved to metrics.json")


if __name__ == "__main__":
    main()
