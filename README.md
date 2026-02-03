# versioned-app

Minimal HTTP service that reports its runtime identity.

The service returns:
- application name
- environment
- resolved version (semver preferred, SHA fallback)

No auth, no database, no frameworks. Python standard library only.

## Where this fits

This repository contains the demo app code and the GitHub Actions workflow that builds a container image and pushes it to ECR.

It does **not** provision AWS infrastructure and it does **not** deploy to Kubernetes directly. Deployments happen when `gitops-release-controller` updates environment values (via PR), and Argo CD reconciles.

**End-to-end demo start:**
To run the full demo (EKS cluster, Argo CD, ALB ingress), start with
[`gitops-infra`](https://github.com/dgeoghegan/gitops-infra).

**CI-only review:**
You can review the image build/push workflow entirely within this repository, but running it requires the AWS artifacts from `gitops-infra` (ECR repo + GitHub OIDC + IAM role).

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
