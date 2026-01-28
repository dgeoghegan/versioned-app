# versioned-app

Minimal HTTP service that reports its runtime identity.

The service returns:
- application name
- environment
- resolved version (semver preferred, SHA fallback)

No auth, no database, no frameworks. Python standard library only.

## Version resolution contract

The service computes a display version using the following precedence:

1. `APP_VERSION` if set and not `unversioned` (e.g. `v0.1.4`)
2. `GIT_SHA` if set (displayed as `sha-<12>`)
3. `(unknown)` if neither is available

This mirrors a GitOps deployment model:
- **dev** may deploy arbitrary commit builds (SHA-based)
- **staging / prod** deploy explicit releases (semver)

## Required environment variables

The service expects the following environment variables at runtime:

- `APP_ENV`  
  Logical environment name (e.g. `dev`, `staging`, `prod`)

- `APP_VERSION`  
  Semver release tag (e.g. `v0.1.4`) or `unversioned`

- `GIT_SHA`  
  12-character git commit SHA (empty for semver-only deploys)

## Local run (WSL / Linux / macOS)

Requires Python 3.11+.

### Example: semver-style run

```bash
export APP_ENV=local
export APP_VERSION=v0.1.0
export GIT_SHA=
python3 app.py
```

### Example: SHA-style run

```bash
export APP_ENV=local
export APP_VERSION=unversioned
export GIT_SHA=16391d20efc2
python3 app.py
```

The service will resolve and display the appropriate version automatically.
