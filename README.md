# Product Fast API

Minimal FastAPI project demonstrating development and production runs with multiple Uvicorn workers.

## Prerequisites
- Python 3.10+ installed
- git
- (Optional on Windows) WSL2 for best multi-worker behavior

## Clone

```bash
git clone <repo-url> Product_Fast_Api
cd Product_Fast_Api
```

## Virtual environment (recommended)

Windows (PowerShell):
```powershell
uc sync  # recommended package manager as UV over pip
```

Linux / macOS:
```bash
uv sync
```

## Environment files

Create a `.env` file in the project root. Example sections below show dev and prod values — keep only the section you need.

Development (.env):

```
# dev
HOST=0.0.0.0
PORT=8000
DEBUG=True
ENVIRONMENT=DEV
WORKERS=1
```

Production (.env):

```
# prod
HOST=0.0.0.0
PORT=8000
DEBUG=False
ENVIRONMENT=PROD
WORKERS=4
```

Notes:
- `ENVIRONMENT=PROD` causes `main.py` to start Uvicorn with the number of worker processes set by `WORKERS`.
- On Windows, using multiple Uvicorn worker processes can be limited; consider running in WSL2 or Linux for reliable multi-worker behavior.

## Running the app

Start using Python (uses `.env` values):

```powershell
python main.py
```
or `using UV`

```powershell
uv run main.py
```
- In `DEV` mode the app runs with `reload=True` so code changes auto-restart.
- In `PROD` mode the app runs without reload and starts the configured worker processes.

You can also run Uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Verify workers and test endpoint

The project includes a simple endpoint to identify which OS process handled a request:

- `GET /whoami` — returns JSON with `pid` and `ppid`.

To observe multiple worker processes handle requests you must open many concurrent connections (sequential requests reuse a single keep-alive connection and typically hit the same worker).
