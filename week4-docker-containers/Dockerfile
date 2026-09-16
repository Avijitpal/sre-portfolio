# ==========================================
# STAGE 1: Builder
# ==========================================
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

COPY app/package*.json ./
RUN npm install --omit=dev

# ==========================================
# STAGE 2: Minimal Production Runtime
# ==========================================
FROM node:20-alpine AS runner

WORKDIR /usr/src/app

# SRE Best Practice: Install curl for health probes
RUN apk add --no-cache curl

# Copy assets from builder stage
COPY --from=builder /usr/src/app ./
COPY app/server.js ./

# SRE Best Practice: Run as built-in unprivileged non-root user (UID 1000)
USER node

# Expose microservice port
EXPOSE 3000

# SRE Best Practice: Native container health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/healthz || exit 1

# Execute node directly (not via npm) so it receives OS signals like SIGTERM
CMD ["node", "server.js"]
