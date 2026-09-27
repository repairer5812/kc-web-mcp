FROM cloudflare/cloudflared:2026.9.3 AS tunnel
FROM node:22-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git python3 python3-venv ripgrep bash tini \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/kc-mcp
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts && \
    ln -s /opt/kc-mcp/node_modules/@starlove7/spacedock/npm/bin/spacedock.js /usr/local/bin/spacedock
COPY --from=tunnel /usr/local/bin/cloudflared /usr/local/bin/cloudflared
COPY scripts /opt/kc-mcp/scripts
COPY LICENSE THIRD_PARTY_NOTICES.md /opt/kc-mcp/
COPY licenses /opt/kc-mcp/licenses
RUN mkdir -p /state /workspace && chown node:node /state /workspace && \
    chmod 755 /opt/kc-mcp/scripts/entrypoint.sh
ENV HOME=/state PYTHONDONTWRITEBYTECODE=1
USER node
WORKDIR /workspace
ENTRYPOINT ["/usr/bin/tini", "--", "/opt/kc-mcp/scripts/entrypoint.sh"]
