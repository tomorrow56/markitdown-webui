#!/usr/bin/env bash
# STATUS of MarkItDown Web UI.
LABEL="com.$(id -un).markitdown-webui"
DOMAIN="gui/$(id -u)"
URL="http://localhost:${PORT:-5001}"

echo "=== launchd (${LABEL}) ==="
if launchctl print "${DOMAIN}/${LABEL}" >/dev/null 2>&1; then
    launchctl print "${DOMAIN}/${LABEL}" \
      | grep -E "state = |pid = |last exit code = " \
      | sed 's/^[[:space:]]*/  /'
else
    echo "  not loaded"
fi

echo "=== port ${PORT:-5001} ==="
pids="$(lsof -ti:"${PORT:-5001}" 2>/dev/null | tr '\n' ' ')"
[ -n "$pids" ] && echo "  listening (pid ${pids})" || echo "  not listening"

echo "=== HTTP ==="
code="$(curl -s -o /dev/null -w "%{http_code}" "${URL}/" --max-time 5 2>/dev/null || echo 000)"
echo "  GET ${URL}/ -> HTTP ${code}"
