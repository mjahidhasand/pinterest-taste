FROM mcr.microsoft.com/playwright/python:v1.65.2-noble

# Virtual display + VNC + browser-based VNC client, so you can log in to
# Pinterest once from your PC (see README, "Log in").
RUN apt-get update \
 && apt-get install -y --no-install-recommends xvfb x11vnc novnc websockify fluxbox \
 && rm -rf /var/lib/apt/lists/*
# The image ships browsers only; the Python package must match their version.
RUN pip install --no-cache-dir --break-system-packages playwright==1.65.2

COPY collector/entrypoint.sh /app/entrypoint.sh
COPY collector/collector.py /app/collector.py
COPY common /app/common
RUN chmod 755 /app/entrypoint.sh \
 && mkdir -p /state/thumbs /state/profile && chown -R 1000:1000 /state

USER 1000:1000
ENV HOME=/tmp DISPLAY=:99
ENTRYPOINT ["/app/entrypoint.sh"]
