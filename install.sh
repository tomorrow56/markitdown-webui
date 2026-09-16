#!/usr/bin/env bash
# Install MarkItDown Web UI as a macOS background service (auto-start at login).
# Idempotent: safe to re-run. Generates a per-user launchd LaunchAgent that points
# at THIS checkout, then loads it. Works for any user / any clone location.
set -euo pipefail
unset PYTHONPATH 2>/dev/null || true

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL="com.$(id -un).markitdown-webui"
DOMAIN="gui/$(id -u)"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
PORT="${PORT:-5001}"
PY="$DIR/.venv/bin/python"

echo "==> Repo:  $DIR"
echo "==> Label: $LABEL"
echo "==> Port:  $PORT"

# 1. Ensure venv + dependencies -------------------------------------------------
if [ ! -x "$PY" ]; then
    echo "==> Creating .venv ..."
    if command -v uv >/dev/null 2>&1; then
        uv venv --python 3.11 "$DIR/.venv"
    else
        python3 -m venv "$DIR/.venv"
    fi
fi
echo "==> Installing dependencies ..."
if command -v uv >/dev/null 2>&1; then
    # uv-created venvs have no pip; uv pip installs straight into the target venv
    uv pip install --python "$PY" -q -r "$DIR/requirements.txt"
else
    "$PY" -m pip install -q --upgrade pip
    "$PY" -m pip install -q -r "$DIR/requirements.txt"
fi
mkdir -p "$DIR/logs"

# 2. Generate the LaunchAgent plist --------------------------------------------
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${DIR}/.venv/bin/python</string>
        <string>${DIR}/serve.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${DIR}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>${DIR}/.venv/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>PORT</key>
        <string>${PORT}</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>StandardOutPath</key>
    <string>${DIR}/logs/webui.log</string>
    <key>StandardErrorPath</key>
    <string>${DIR}/logs/webui.log</string>
</dict>
</plist>
PLIST_EOF

plutil -lint "$PLIST" >/dev/null

# 3. (Re)load the agent ---------------------------------------------------------
if launchctl print "${DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    launchctl bootout "${DOMAIN}/${LABEL}" 2>/dev/null || true
    # bootout is asynchronous — wait for launchd to fully drop the job,
    # otherwise the following bootstrap hits "Input/output error 5".
    for _ in $(seq 1 20); do
        launchctl print "${DOMAIN}/${LABEL}" >/dev/null 2>&1 || break
        sleep 0.3
    done
fi
launchctl enable "${DOMAIN}/${LABEL}" 2>/dev/null || true
if ! launchctl bootstrap "${DOMAIN}" "${PLIST}" 2>/dev/null; then
    sleep 1
    launchctl bootstrap "${DOMAIN}" "${PLIST}"   # retry once on transient error
fi

# 4. Health check ---------------------------------------------------------------
URL="http://localhost:${PORT}"
for _ in $(seq 1 20); do
    if curl -s -o /dev/null "${URL}/" 2>/dev/null; then
        echo "✅ Installed and running — auto-starts at every login: ${URL}"
        echo "   Control: ./start.sh ./stop.sh ./restart.sh ./status.sh ./uninstall.sh"
        exit 0
    fi
    sleep 0.5
done
echo "⚠️  Installed but not responding yet — check ${DIR}/logs/webui.log"
exit 1
