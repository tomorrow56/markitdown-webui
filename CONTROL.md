# MarkItDown Web UI — Control & Auto-start (macOS)

Runs the app as a managed **launchd** LaunchAgent so it starts at login and
auto-restarts on crash. Everything is driven by scripts in this folder.

## Install / enable auto-start
```bash
./install.sh          # creates .venv, installs deps, generates the LaunchAgent, starts it
PORT=5055 ./install.sh   # use a custom port
```
`install.sh` is idempotent — re-run it any time to repair or update the service.

It generates a per-user agent:
- **Label:** `com.<your-username>.markitdown-webui`
- **Plist:** `~/Library/LaunchAgents/com.<your-username>.markitdown-webui.plist`
- `RunAtLoad` (start at login) + `KeepAlive` (restart on crash)
- Runs `serve.py` via the repo's `.venv` — single process, no Flask debug-reloader, binds `127.0.0.1` only
- Logs: `logs/webui.log`

## One-click control
| Command | What it does |
|---------|--------------|
| `./install.sh`   | Install/repair service + auto-start (idempotent). |
| `./start.sh`     | Start now (loads the agent if needed). |
| `./stop.sh`      | Stop now. **Still auto-starts again at next login.** |
| `./restart.sh`   | Restart the running server. |
| `./status.sh`    | Show launchd state, port, and HTTP health. |
| `./uninstall.sh` | Permanently remove auto-start (deletes the plist). Repo/venv untouched. |

## Notes
- Default URL: http://localhost:5001
- Change the port: `PORT=<n> ./install.sh` (regenerates the plist), then it persists.
- `stop.sh` won't disable login auto-start — use `uninstall.sh` for that.
- The scripts derive their paths from this checkout, so the repo works from any
  location and for any user.
- `app.py`'s built-in `python app.py` runner (debug mode, port 5001) still works
  for quick local dev; the service uses `serve.py` instead.
