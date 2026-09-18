# Week 5: Kubernetes Workload Orchestration & Reliability

## Overview
Deploys a hardened Node.js microservice (`sre-service:v1.0.0`) onto a local multi-node Kubernetes cluster (`k3d`) using declarative manifests configured for high availability, self-healing, and zero-downtime rolling updates.

## Architecture & Workloads
* **Cluster:** Multi-node `k3d` topology (1 control plane, 2 worker agent nodes).
* **Deployment (`k8s/deployment.yaml`):**
  * 3 replicas distributed across nodes.
  * Zero-downtime strategy: `RollingUpdate` with `maxSurge: 1` and `maxUnavailable: 0`.
  * Resource quotas: `requests` (50m CPU, 64Mi RAM) and `limits` (200m CPU, 128Mi RAM).
  * Native health probes targeting `/healthz`: `livenessProbe` (process restart) and `readinessProbe` (traffic routing).
* **Service (`k8s/service.yaml`):** `ClusterIP` load balancer routing internal traffic across pod endpoints on port 3000.
* **Config Decoupling (`k8s/configmap.yaml`, `k8s/secret.yaml`):** Twelve-Factor application principles applied via decoupled `ConfigMap` and `Secret` injected through `envFrom`.

## Verification & Resilience Tests
1. **Zero-Downtime Rollout:** Verified uninterrupted HTTP 200 responses during a `kubectl rollout restart`.
2. **Self-Healing:** Verified automatic pod reconciliation upon termination.
3. **Internal Routing:** Verified endpoint discovery and port-forwarded traffic.
