import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

TARGET_ENDPOINTS = [
    {"name": "GitHub Status API", "url": "https://www.githubstatus.com/api/v2/status.json", "expected_status": 200, "max_latency_ms": 1500},
    {"name": "Google Public Ping", "url": "https://www.google.com", "expected_status": 200, "max_latency_ms": 1000},
    {"name": "Simulated 404 Route", "url": "https://httpstat.us/404", "expected_status": 200, "max_latency_ms": 1000},
]

def probe_endpoint(endpoint: dict) -> dict:
    url = endpoint["url"]
    expected_status = endpoint["expected_status"]
    max_latency = endpoint["max_latency_ms"]

    start_time = time.perf_counter()
    status_code = None
    is_healthy = False
    error_message = None

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "SRE-Synthetic-Probe/1.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            is_healthy = (status_code == expected_status) and (latency_ms <= max_latency)
    except urllib.error.HTTPError as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        status_code = e.code
        error_message = f"HTTP error {e.code}"
    except Exception as e:
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        error_message = str(e)

    return {
        "name": endpoint["name"],
        "url": url,
        "status_code": status_code,
        "latency_ms": latency_ms,
        "healthy": is_healthy,
        "sla_latency_breached": latency_ms > max_latency,
        "error": error_message
    }

def run_probes() -> dict:
    results = [probe_endpoint(ep) for ep in TARGET_ENDPOINTS]
    total = len(results)
    healthy_count = sum(1 for r in results if r["healthy"])
    availability_pct = round((healthy_count / total) * 100, 2)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_probes": total,
        "healthy_probes": healthy_count,
        "system_availability_percentage": availability_pct,
        "status": "HEALTHY" if availability_pct == 100 else "DEGRADED",
        "results": results
    }

if __name__ == "__main__":
    report = run_probes()
    print(json.dumps(report, indent=2))
    
    if report["status"] != "HEALTHY":
        sys.exit(1)