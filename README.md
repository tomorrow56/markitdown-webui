# MarkItDown Web UI

A modern web interface for Microsoft's MarkItDown document conversion tool.

## 🚀 Live Demo

**https://markitdown-webui-fawn.vercel.app/**

## Features

- **Drag & Drop Upload**: Intuitive file upload with drag-and-drop support
- **Document Conversion**: Convert PDF, Word, PowerPoint, Excel files
- **Web Content**: Convert HTML and web pages to Markdown
- **Data Formats**: Support for CSV, JSON, XML conversion
- **Live Preview**: See a preview of your converted Markdown before downloading
- **Modern UI**: Clean, responsive interface built with Tailwind CSS
- **Error Handling**: Comprehensive error reporting and validation
- **File Management**: Automatic cleanup of temporary files

## Supported File Formats

- **Documents**: PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS
- **Web**: HTML, HTM
- **Data**: CSV, JSON, XML
- **Text**: TXT, MD

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tomorrow56/markitdown-webui.git
   cd markitdown-webui
   ```

2. Create a virtual environment and install dependencies **into it**:

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   **Windows (PowerShell):**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. Run the application (inside the activated venv):
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5001`

> ### ⚠️ macOS: `zsh: command not found: pip` (and why `python app.py` fails too)
>
> On a modern Mac the bare `pip` and `python` commands **do not exist** — Apple
> and Homebrew ship them as `pip3` / `python3`. So the classic
> `pip install -r requirements.txt` gives:
> ```
> zsh: command not found: pip
> ```
> And even `pip3 install -r requirements.txt` usually fails with an
> **`error: externally-managed-environment`** ([PEP 668](https://peps.python.org/pep-0668/)),
> because Homebrew / python.org Python refuse to let you install packages into
> the system Python.
>
> **Fix: always install into a virtual environment** (step 2 above). Once the
> venv is activated, `pip` and `python` exist and point at the venv, so every
> command in this README works verbatim — no `pip3`/`python3` juggling, no
> PEP 668 error.
>
> **Faster alternative with [uv](https://github.com/astral-sh/uv):**
> ```bash
> uv venv --python 3.11 .venv
> uv pip install --python .venv/bin/python -r requirements.txt   # uv-made venvs have no pip; use `uv pip`
> .venv/bin/python app.py
> ```
>
> **Or skip all of this on macOS** and let [`./install.sh`](#macos-run-as-a-background-service-auto-start-at-login)
> build the venv, install everything, and run the app as a background service
> for you (see the next section).

## macOS: Run as a Background Service (auto-start at login)

On macOS you can run the Web UI as a managed **launchd** service so it starts
automatically at login and restarts itself if it crashes — no need to launch it
manually or keep a terminal open.

```bash
# From the repo folder — creates the .venv, installs deps, generates a
# per-user LaunchAgent, and starts the service:
./install.sh
```

That's it. The UI is now always available at `http://localhost:5001` and comes
back on every reboot.

### One-click control scripts

| Command | What it does |
|---------|--------------|
| `./install.sh`  | Install/repair the service + auto-start (idempotent). |
| `./start.sh`    | Start now. |
| `./stop.sh`     | Stop now (still auto-starts again at next login). |
| `./restart.sh`  | Restart the running server. |
| `./status.sh`   | Show launchd state, port, and HTTP health. |
| `./uninstall.sh`| Remove auto-start (deletes the LaunchAgent). Repo/venv untouched. |

Details and internals are documented in [`CONTROL.md`](CONTROL.md).

- Runs `serve.py` (production entry point: no Flask debug-reloader, binds
  `127.0.0.1` only) instead of `app.py`.
- Logs to `logs/webui.log`.
- To change the port: `PORT=5055 ./install.sh`.

## Usage

1. **Upload a file**: Drag and drop a file onto the upload area or click "Browse Files"
2. **Wait for conversion**: The file will be automatically converted to Markdown
3. **Preview the result**: See a preview of the converted content
4. **Download**: Click "Download Markdown" to save the converted file

## Configuration

- **Maximum file size**: 50MB (configurable in `app.py`)
- **Supported formats**: Defined in `ALLOWED_EXTENSIONS` in `app.py`
- **Cleanup interval**: Files older than 1 hour are automatically deleted
- **Port**: Application runs on port 5001

## Requirements

- Python 3.10 or higher
- MarkItDown library with all dependencies
- Flask web framework

## API Endpoints

- `GET /`: Main web interface
- `POST /convert`: Convert uploaded file to Markdown
- `GET /download/<filename>`: Download converted file
- `POST /cleanup`: Clean up old temporary files

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- File size limits
- Conversion failures
- Network errors
- File system errors

## Security Features

- File type validation
- Secure filename handling
- Automatic cleanup of temporary files
- File size limits
- Input sanitization

## Troubleshooting

### `command not found: pip` / `externally-managed-environment`
You're not inside a virtual environment. See the **macOS pip note** in the
[Installation](#installation) section — create and activate a `.venv` first,
then `pip` works.

### PDF / Office Conversion Issues
If a conversion fails with a `MissingDependencyException` (e.g. for `.xlsx`,
`.pptx`, `.docx`, or `.pdf`), the format's optional dependency isn't installed
**in the venv the app runs from**. Reinstall the full dependency set into that
venv:
```bash
source .venv/bin/activate          # make sure you're in the app's venv
pip install --force-reinstall -r requirements.txt   # requirements pins markitdown[all]
```
Notes:
- `requirements.txt` already requests `markitdown[all]`, which pulls in
  `openpyxl` (xlsx), `python-pptx` (pptx), `mammoth` (docx), `pdfminer-six` /
  `pdfplumber` (pdf), etc.
- A **separate** `markitdown` CLI you may have installed elsewhere (e.g.
  `uv tool install markitdown`) has its **own** environment — upgrading it does
  **not** affect this web app's venv. Always install extras into `.venv`.
- After installing new dependencies, **restart** the app (or `./restart.sh` if
  running as the launchd service) so the new packages are loaded.

### Port Already in Use
If port 5001 is already in use:
```bash
# Kill existing process
lsof -ti:5001 | xargs kill -9
# Or change port in app.py
```

## License

This project is built using Microsoft's MarkItDown library. Please refer to the original MarkItDown license for usage terms.

## Contributing

Feel free to submit issues and enhancement requests!
