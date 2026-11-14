FROM node:22-bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Pinned to the version on the VM; bump deliberately, not by auto-update.
RUN npm install -g @anthropic-ai/claude-code@2.1.322 && npm cache clean --force

COPY analyst/analyst.py /app/analyst.py
COPY analyst/prompts /app/prompts
COPY analyst/claude-settings.json /app/claude-settings.json
COPY common /app/common
RUN mkdir -p /home/node/.claude && chown node:node /home/node/.claude

# node user is uid 1000, same as the VM user that owns the repo checkout.
USER node
ENV HOME=/home/node \
    DISABLE_AUTOUPDATER=1 \
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
    PYTHONPATH=/app/common
WORKDIR /app
ENTRYPOINT ["python3", "-u", "/app/analyst.py"]
