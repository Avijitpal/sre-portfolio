## Week 3: Cloud Foundations & Infrastructure as Code (Terraform)

### Architecture Overview
Automated provisioning of an isolated Virtual Private Cloud (VPC) network architecture using modular Terraform (HCL):
- **VPC Boundary:** Parameterized `10.0.0.0/16` CIDR with DNS hostnames and resolution enabled.
- **Network Tiering:**
  - **Public Subnet (`10.0.1.0/24`):** Direct egress/ingress via Internet Gateway for external load balancers and ingress controllers.
  - **Private Subnet (`10.0.2.0/24`):** Fully isolated compute tier for microservice Pods and databases.
- **Traffic Routing:** Route tables associating default outbound routes (`0.0.0.0/0`) through the provisioned Internet Gateway.
- **Firewall & Security Groups:** Least-privilege ingress rules permitting HTTP (80) and HTTPS (443), with full egress monitoring.

### Terraform Files
- `versions.tf`: Provider lock constraints and AWS provider block.
- `variables.tf`: Parameterized inputs for multi-environment deployments.
- `main.tf`: Core cloud resource declarations.
- `outputs.tf`: Exported infrastructure attributes for downstream CI/CD consumption.

### Execution Workflow
```bash
terraform init -upgrade
terraform validate
terraform plan


## Week 4: Production Containerization & Orchestration (Docker)

### Architectural Overview
Hardened, production-grade microservice packaging using modern containerization standards:
- **Multi-Stage Build (`Dockerfile`):** Utilizes an intermediate `builder` stage to install dependencies, copying only release artifacts into a minimal Alpine Linux `runner` stage to eliminate build tools and reduce image attack surface.
- **Principle of Least Privilege:** Drops root privileges explicitly, executing runtime processes under the unprivileged `USER node` (UID 1000).
- **Proactive Health Probes:** Exposes an HTTP `/healthz` endpoint integrated directly into native container runtime health checks (`HEALTHCHECK`).
- **POSIX Signal Handling (`SIGTERM`/`SIGINT`):** Implements graceful connection draining and process termination hooks to guarantee zero-downtime rolling deploys.
- **Service Orchestration (`docker-compose.yml`):** Deploys microservices alongside backing persistence (MongoDB) with deterministic dependency startup (`condition: service_healthy`), isolated bridge networking, and persistent volume mounting.

### Verification Commands
```bash
# Build & audit image size
docker build -t sre-service:v1.0.0 .
docker images | grep sre-service

# Run multi-container stack
docker compose up -d
docker compose ps
curl -i http://localhost:3000/healthz

# Teardown
docker compose down