
# Week 6: CI/CD Automation & Shift-Left Security with GitHub Actions

## Overview
This module implements a production-grade Continuous Integration and Continuous Delivery (CI/CD) pipeline using **GitHub Actions**. It enforces automated testing, shift-left vulnerability scanning, Kubernetes manifest linting, and immutable artifact delivery to the **GitHub Container Registry (GHCR)**.

---

## Architectural Pipeline Flow
+-----------------------------------------------------------------------------------+
|                              Git Push (main/master)                               |
+-----------------------------------------------------------------------------------+
|
v
+------------------------------------------+
|        Job 1: Node.js Test Suite         |
|        - Sets up Node.js 20              |
|        - Executes automated smoke tests  |
+------------------------------------------+
|
+--------------------+--------------------+
|                                         |
v                                         v
+------------------------------------------+  +------------------------------------------+
|      Job 2: Docker Build & Trivy Scan    |  | Job 3: Kubeconform Manifest Validation   |
|  - Builds multi-stage production image   |  |  - Validates declarative k8s manifests   |
|  - Scans for HIGH & CRITICAL CVEs        |  |  - Enforces strict official spec schemas |
+------------------------------------------+  +------------------------------------------+
|                                         |
+--------------------+--------------------+
| (On Success)
v
+------------------------------------------+
|    Job 4: Publish Container to GHCR      |
|  - Authenticates via GITHUB_TOKEN        |
|  - Tags image with immutable Git SHA     |
|  - Publishes to ghcr.io registry         |
+------------------------------------------+


---

## Key SRE Patterns Implemented

1. **Shift-Left Security (Trivy):**
   - Vulnerability detection is integrated directly into the pull-request and push gates.
   - Prevents unpatched or vulnerable dependencies (`HIGH`/`CRITICAL` CVEs) from ever reaching staging or production clusters.

2. **Schema Enforcement Before Runtime (Kubeconform):**
   - Validates all Kubernetes manifests (`deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`) against Kubernetes OpenAPI schemas prior to cluster application.
   - Eliminates runtime deployment failures caused by deprecated APIs or malformed syntax.

3. **Immutable Artifact Versioning:**
   - Artifacts are pushed to `ghcr.io` tagged with the exact Git commit SHA (`${{ github.sha }}`) alongside `latest`.
   - Enables zero-ambiguity rollbacks and precise audit trails linking production images back to source code.

---

## Verification & Workflow Status

* Workflow definition: `.github/workflows/ci.yml`
* Published registry artifact: `ghcr.io/avijitpal/sre-service`
* Execution triggers: Push, Pull Request, and manual dispatch (`workflow_dispatch`).
