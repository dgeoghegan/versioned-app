# versioned-app

Minimal HTTP service that returns: `versioned-app vX.Y.Z`

No auth, no database, no frameworks. Standard library only.

## Local run (WSL Ubuntu)

Requires Python 3.11+.

```bash
export APP_VERSION=0.1.0
python3 app.py
