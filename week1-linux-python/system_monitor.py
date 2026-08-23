import json
import shutil
import sys
from datetime import datetime, timezone
import psutil

# Operational alert thresholds
CPU_THRESHOLD_PERCENT = 80.0
MEMORY_THRESHOLD_PERCENT = 85.0
DISK_THRESHOLD_PERCENT = 90.0

def collect_metrics() -> dict:
    # CPU usage over a 1-second sample window
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory metrics
    mem = psutil.virtual_memory()
    memory_total_gb = round(mem.total / (1024 ** 3), 2)
    memory_used_gb = round(mem.used / (1024 ** 3), 2)
    memory_percent = mem.percent
    
    # Root filesystem disk metrics
    disk = shutil.disk_usage("/")
    disk_total_gb = round(disk.total / (1024 ** 3), 2)
    disk_used_gb = round(disk.used / (1024 ** 3), 2)
    disk_percent = round((disk.used / disk.total) * 100, 2)
    
    # Threshold evaluations
    alerts = []
    if cpu_percent > CPU_THRESHOLD_PERCENT:
        alerts.append(f"HIGH_CPU_USAGE: {cpu_percent}% > {CPU_THRESHOLD_PERCENT}%")
    if memory_percent > MEMORY_THRESHOLD_PERCENT:
        alerts.append(f"HIGH_MEMORY_USAGE: {memory_percent}% > {MEMORY_THRESHOLD_PERCENT}%")
    if disk_percent > DISK_THRESHOLD_PERCENT:
        alerts.append(f"HIGH_DISK_USAGE: {disk_percent}% > {DISK_THRESHOLD_PERCENT}%")
        
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "CRITICAL" if alerts else "HEALTHY",
        "alerts": alerts,
        "metrics": {
            "cpu_percent": cpu_percent,
            "memory": {
                "total_gb": memory_total_gb,
                "used_gb": memory_used_gb,
                "percent_used": memory_percent
            },
            "disk": {
                "total_gb": disk_total_gb,
                "used_gb": disk_used_gb,
                "percent_used": disk_percent
            }
        }
    }

if __name__ == "__main__":
    report = collect_metrics()
    print(json.dumps(report, indent=2))
    
    # Non-zero exit code on critical state (enables automated alerting in CI/CD or cron)
    if report["status"] == "CRITICAL":
        sys.exit(2)