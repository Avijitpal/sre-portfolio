import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone

# Regex matching: IP - - [timestamp] "METHOD /path HTTP/1.1" status response_time_ms
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<endpoint>\S+) \S+" (?P<status>\d{3}) (?P<latency>\d+)'
)

def analyze_logs(file_path: str) -> dict:
    total_requests = 0
    status_counts = Counter()
    endpoint_hits = Counter()
    endpoint_latency = {}
    error_5xx_count = 0

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = LOG_PATTERN.match(line.strip())
                if not match:
                    continue

                total_requests += 1
                data = match.groupdict()
                status = int(data["status"])
                endpoint = data["endpoint"]
                latency = int(data["latency"])

                status_counts[status] += 1
                endpoint_hits[endpoint] += 1

                if endpoint not in endpoint_latency:
                    endpoint_latency[endpoint] = []
                endpoint_latency[endpoint].append(latency)

                if 500 <= status <= 599:
                    error_5xx_count += 1

    except FileNotFoundError:
        print(f"Error: Log file '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    if total_requests == 0:
        return {"error": "No valid log entries found"}

    error_rate = (error_5xx_count / total_requests) * 100
    avg_latencies = {
        ep: round(sum(lats) / len(lats), 2)
        for ep, lats in endpoint_latency.items()
    }

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_requests": total_requests,
        "error_rate_percentage": round(error_rate, 2),
        "status_distribution": dict(status_counts),
        "endpoint_traffic": dict(endpoint_hits.most_common(5)),
        "avg_latency_ms": avg_latencies,
        "alert_sla_breach": error_rate > 5.0
    }

if __name__ == "__main__":
    log_file = sys.argv[1] if len(sys.argv) > 1 else "access.log"
    report = analyze_logs(log_file)
    print(json.dumps(report, indent=2))