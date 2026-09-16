#!/usr/bin/env python3
"""Production launcher for MarkItDown Web UI (used by launchd + one-click scripts).

Differences from `app.py`'s built-in runner:
  - debug=False, use_reloader=False  -> single stable process (launchd-friendly)
  - binds 127.0.0.1 only             -> not exposed to the LAN
  - honors PORT env var (default 5001)

Defensive: strip any leaked Hermes-venv entries so imports resolve from THIS venv.
"""
import os
import sys

# Belt-and-suspenders: ignore a leaked PYTHONPATH and any Hermes venv on sys.path.
os.environ.pop("PYTHONPATH", None)
sys.path[:] = [p for p in sys.path if ".hermes/hermes-agent/venv" not in p]

from app import app  # noqa: E402  (import after sanitizing sys.path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
