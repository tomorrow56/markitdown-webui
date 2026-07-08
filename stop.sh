#!/usr/bin/env bash
# One-click STOP for MarkItDown Web UI.
# Stops the server now. It will still auto-start again at next login.
# (To remove auto-start permanently, run ./uninstall.sh)
set -euo pipefail
LABEL="com.$(id -un).markitdown-webui"
DOMAIN="gui/$(id -u)"

if launchctl print "${DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    launchctl bootout "${DOMAIN}/${LABEL}" 2>/dev/null || true
    echo "🛑 Stopped. (Auto-starts again at next login; run ./start.sh to start now.)"
else
    echo "Not running."
fi
