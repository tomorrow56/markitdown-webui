#!/usr/bin/env bash
# Permanently remove auto-start (deletes the launch agent) and stop the server.
# The repo, .venv, and logs are left untouched.
set -euo pipefail
LABEL="com.$(id -un).markitdown-webui"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
DOMAIN="gui/$(id -u)"

launchctl bootout "${DOMAIN}/${LABEL}" 2>/dev/null || true
rm -f "${PLIST}"
echo "🗑  Auto-start removed and server stopped."
echo "   Re-enable any time with: ./install.sh"
