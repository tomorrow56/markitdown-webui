#!/usr/bin/env bash
# One-click START for MarkItDown Web UI (managed by launchd).
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL="com.$(id -un).markitdown-webui"
DOMAIN="gui/$(id -u)"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
URL="http://localhost:${PORT:-5001}"

if [ ! -f "$PLIST" ]; then
    echo "Launch agent not installed. Run ./install.sh first." >&2
    exit 1
fi

if launchctl print "${DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    echo "Already loaded — restarting..."
    launchctl kickstart -k "${DOMAIN}/${LABEL}"
else
    echo "Loading launch agent..."
    launchctl bootstrap "${DOMAIN}" "${PLIST}"
fi

for _ in $(seq 1 20); do
    if curl -s -o /dev/null "${URL}/" 2>/dev/null; then
        echo "✅ MarkItDown Web UI is up: ${URL}"
        exit 0
    fi
    sleep 0.5
done
echo "⚠️  Started but not responding yet — check ${DIR}/logs/webui.log"
exit 1
