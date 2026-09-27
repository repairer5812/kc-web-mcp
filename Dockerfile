FROM cloudflare/cloudflared:2026.9.3 AS tunnel
FROM golang:1.27-bookworm AS branded-runtime
RUN apt-get update && apt-get install -y --no-install-recommends git python3 && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v0.1.6 https://github.com/starlove7/spacedock.git /src && \
    test "$(git -C /src rev-parse HEAD)" = '41df6ed1519242e742079c84989cd15b5a4e441b'
COPY scripts/customize.py /customize.py
COPY ui /ui
RUN python3 /customize.py /src /ui
WORKDIR /src
RUN go test ./internal/mcp && CGO_ENABLED=0 go build -trimpath -ldflags '-s -w -X github.com/starlove7/spacedock/internal/buildinfo.Version=0.1.6-webjjonku.1' -o /webjjonku ./cmd/spacedock
FROM node:22-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git python3 python3-venv ripgrep bash tini \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/kc-mcp
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY --from=branded-runtime /webjjonku /usr/local/bin/spacedock
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
