# syntax=docker/dockerfile:1

# ─── Stage 1: builder ────────────────────────────────────────────────────────
FROM node:18-alpine AS builder

WORKDIR /build

# Copy manifests first for better layer caching
COPY package.json package-lock.json ./

# Install production dependencies only — no devDependencies in final image
RUN npm ci --omit=dev


# ─── Stage 2: final ──────────────────────────────────────────────────────────
FROM node:18-alpine

WORKDIR /app

# Copy only the pruned node_modules and app source from builder
COPY --from=builder /build/node_modules ./node_modules

COPY app.js .
COPY views/ ./views/

# Create non-root user and hand over ownership
RUN adduser -D -u 1001 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) }).on('error', () => process.exit(1))"

CMD ["node", "app.js"]