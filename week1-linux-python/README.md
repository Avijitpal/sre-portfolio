# 🚀 Avijit's SRE & DevOps Engineering Portfolio

A practical collection of production-grade automation scripts, incident triage tools, and infrastructure configurations developed throughout an intensive 8-week SRE engineering track. This portfolio bridges enterprise middleware operations with modern Site Reliability Engineering and Product Engineering principles.

---

## 📂 Repository Structure

* `week1-linux-python/` - Linux operational tooling, rapid incident triage, and host telemetry.
* `week2-networking-probes/` - Synthetic API monitoring, SLA latency enforcement, and network diagnostics.

---

## 🛠️ Week 1: Linux Internals & Python Automation

### 1. Automated Access Log Incident Triage (`log_triage.py`)
Parses web access logs with regular expressions to compute real-time operational metrics and evaluate SLA breach thresholds.

* **SRE Use Case:** Production monitoring agents parse application traffic, calculating error rates (alerting if `5xx errors > 5%`) and computing per-endpoint latency metrics to catch performance regressions.
* **Usage:**
  ```bash
  python3 week1-linux-python/log_triage.py week1-linux-python/access.log