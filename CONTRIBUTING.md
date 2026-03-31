# Contributing

Thanks for your interest in contributing to the `owserver` app!

## Reporting issues

Please use one of the issue templates:

- **Bug report** — for general app issues
- **Connectivity issue** — for problems connecting Home Assistant to owserver

## Getting started

1. Fork the repository
2. Clone your fork
3. Create a branch with a `feature/`, `fix/`, or `hotfix/` prefix
4. Make your changes
5. Open a PR from your fork to the `develop` branch

CI runs automatically on pull requests.

## Development setup

Prerequisites:

- Docker with Compose plugin
- Python 3.10+
- `yq` (YAML processor)

Build the image locally:

See [dev/test.sh](dev/test.sh)

## Linting

Prerequisites:

- yamllint
- hadolint
- shellcheck

```bash
make lint
```

This runs yamllint, hadolint (Dockerfile) and shellcheck (shell scripts). CI enforces the same checks.

## Testing

```bash
make test
```

Tests build and start the addon container automatically. CI enforces the same checks. See [tests/README.md](tests/README.md) for details on environment variables and test structure.

## Pull requests

- Target the `develop` branch
- Fill in the PR template checklist (lint, tests, documentation)
- Labels are auto-assigned based on branch name and changed files

## Releases

Releases are managed by maintainers. Release notes are generated automatically from PR titles and labels via release-drafter.
