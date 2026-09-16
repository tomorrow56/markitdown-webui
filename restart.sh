#!/usr/bin/env bash
# One-click RESTART for MarkItDown Web UI.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL="com.$(id -un).markitdown-webui"
DOMAIN="gui/$(id -u)"

if launchctl print "${DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    launchctl kickstart -k "${DOMAIN}/${LABEL}"
    echo "🔄 Restarted: http://localhost:${PORT:-5001}"
else
    exec "${DIR}/start.sh"
fi
