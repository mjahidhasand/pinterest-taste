#!/bin/sh
set -eu
mkdir -p /state/thumbs /state/profile
rm -f /tmp/.X99-lock

Xvfb :99 -screen 0 1440x900x24 -nolisten tcp &
sleep 1
fluxbox >/dev/null 2>&1 &

# VNC is only published on the VM's 127.0.0.1 (docker-compose.yml), and is
# password-protected when VNC_PASSWORD is set.
if [ -n "${VNC_PASSWORD:-}" ]; then
  x11vnc -storepasswd "$VNC_PASSWORD" /tmp/vncpass >/dev/null
  x11vnc -display :99 -forever -shared -rfbauth /tmp/vncpass -rfbport 5900 -quiet &
else
  x11vnc -display :99 -forever -shared -nopw -localhost -rfbport 5900 -quiet &
fi
websockify --web /usr/share/novnc 6080 localhost:5900 >/dev/null 2>&1 &

exec python3 -u /app/collector.py
