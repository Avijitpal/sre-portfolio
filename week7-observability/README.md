# Week 7: Observability & Alerting (Prometheus & Grafana)

## Overview
Implemented production-grade observability and Golden Signals monitoring for a Kubernetes-hosted microservice using Prometheus and Grafana.

## Key Implementations
- **Telemetry Instrumentation**: Integrated `prom-client` exposing `/metrics` with HTTP request duration histograms, request totals with status codes, and process saturation gauges.
- **Prometheus Pipeline**: Scrapes `sre-service:80/metrics` every 2s/5s intervals with alert rule evaluation.
- **Alert Rules**: Configured and validated SLO alert rules (`HighErrorRate` and `HighLatencyP99`), verified full state transitions (`Inactive` -> `Pending` -> `Firing`).
- **Grafana Visualization**: Built an SRE Golden Signals dashboard monitoring Traffic, Latency (p50/p99), Errors, and Memory.
