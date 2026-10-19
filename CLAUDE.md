# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Home Assistant app (add-on) that runs OWFS `owserver` (1-Wire server, port 4304) and optionally `owhttpd` (web UI, port 8099, shown in HA through ingress). Supported archs: `amd64`, `aarch64`.

Write docs, comments and commit messages in simple, plain English.

## Commands

Lint (needs `yamllint`, `hadolint`, `shellcheck`):

```bash
make lint
```

Tests (need Docker with Compose, `yq`, Python 3.10+, packages from `tests/requirements.txt`):

```bash
make test
```

The default platform is `linux/arm64`, because arm64 is the main development platform for this project. On an x86_64 machine without QEMU, set the arch, or the image build fails:

```bash
BUILD_ARCH=amd64 BUILD_PLATFORM=linux/amd64 pytest tests/ -v --tb=short
```

If `pytest` is not installed, use `uv`:

```bash
BUILD_ARCH=amd64 BUILD_PLATFORM=linux/amd64 \
  uv run --no-project --with pytest --with requests pytest tests/ -v --tb=short
```

Run one test or one file:

```bash
pytest tests/test_template.py::TestDeviceTypes::test_usb_all -v
pytest tests/ -m template -v    # markers: integration, template
```

Important notes about tests:

- `BUILD_FROM` is read from `build.yaml` with `yq` in `tests/conftest.py`. You do not need to set it for pytest. You need it only when you call `docker compose` by hand.
- The image `local/owserver:ci` is built only if it does not exist. After you change `Dockerfile`, `patches/` or `rootfs/`, remove the old image first: `docker image rm local/owserver:ci`.
- A full run takes about 6 minutes. Most of the time is container restarts in `test_validation.py`.

Manual smoke test (starts the stack, checks owdir/owread/owhttpd, then stops it): `dev/test.sh`.

To bump the base image in `build.yaml`, use the `bump-base-image` skill (`.claude/skills/bump-base-image/SKILL.md`).

## Architecture

**Image build (`Dockerfile`)** has two stages. Stage 1 builds OWFS from source on Alpine (version in `OWFS_VERSION`) and applies the patches from `patches/` (owhttpd relative paths for ingress, and HA theme CSS). Stage 2 uses the HA base image from `build.yaml` (`BUILD_FROM`) and copies the OWFS binaries and `rootfs/`.

**Add-on options** are defined in `config.yaml` (`schema`). The user sets a list of `devices` (each has `device_type` and, depending on the type, `device`, `server` or the deprecated `ha7net_server`), plus `owhttpd`, `temperature_scale`, `debug`.

**Startup (s6-overlay, `rootfs/etc/s6-overlay/s6-rc.d/`):**

1. `owserver-init` (oneshot): checks the device options with bashio (missing `device`/`server`, `link` rules, `ha7net_server` deprecation warning). Then it renders `/etc/owfs.conf` from `rootfs/etc/owfs.template.conf` with `tempio` and `/data/options.json`.
2. `owserver`: runs `owserver -c /etc/owfs.conf` (with `--debug` if `debug: true`).
3. `owhttpd`: waits for port 4304, then runs `owhttpd`. If `owhttpd: false`, it only pauses.
4. `discovery`: sends `onewire` discovery (host + port 4304) to the Supervisor.

When you add or change a device type, update all of these together: `config.yaml` schema, validation in `owserver-init/run`, `owfs.template.conf`, `DOCS.md`, and tests in `tests/test_template.py` / `tests/test_validation.py`.

**Local dev stack (`dev/`):** `docker-compose.dev.yml` runs the add-on next to `mock-supervisor.py`, a small fake of the Supervisor API (it serves options and accepts discovery). `OPTIONS_JSON_PATH` selects the options file mounted as `/data/options.json`. Tests use the compose project name `owserver-test`, `dev/test.sh` uses `owserver-dev`.

**Tests (`tests/`):**

- `test_integration.py`: runs `owdir`/`owread` in the container against the `fake` DS18B20 device.
- `test_template.py`: renders the template with a downloaded `tempio` binary on Linux (inside the container on other systems) and checks the output. It does not start owserver with each config.
- `test_validation.py`: restarts the container with bad options and checks the log messages from `owserver-init`.

## Repo rules

- Branch prefixes: `feature/` (new things), `fix/` (bugs and CI fixes), `chore/` (maintenance, e.g. base image bumps). PRs go to `develop` (not `master`).
- A release is a PR from `develop` to `master` with the title `Release vX.Y.Z: merge develop into master`.
- Never merge a PR. The maintainer always does the final merge.
- Release notes come from PR titles and labels (release-drafter). Keep PR titles clear.
- User docs are in `DOCS.md`.

## Changelog and releases

Each PR with a user-facing change adds a line under `## Unreleased` at the top of `CHANGELOG.md` (create the section if it is missing). Do not guess a version number in a PR.

Release-drafter uses `commitish: master`, so its draft shows the right version only after `develop` is merged into `master`. That is too late for the changelog. Before a release, find the next version yourself. The rule comes from `.github/release-drafter.yml`: a PR with `breaking-change` → major, `feature` → minor, anything else → patch.

```bash
since=$(gh release view --json publishedAt --jq .publishedAt)   # latest published release
# PRs merged into develop since then, with labels:
gh pr list --base develop --state merged --search "merged:>$since" \
  --json number,title,labels --jq '.[] | "#\(.number) [\(.labels|map(.name)|join(","))] \(.title)"'
# Bump type:
gh pr list --base develop --state merged --search "merged:>$since" \
  --json labels --jq '[.[].labels[].name] | if index("breaking-change") then "major" elif index("feature") then "minor" else "patch" end'
```

Release steps:

1. On `develop`, rename `## Unreleased` to `## X.Y.Z`. Commit and push to `develop` directly (no extra PR, so it does not show up in the release notes).
2. Open a PR `develop` → `master` with the title `Release vX.Y.Z: merge develop into master`.
3. After the merge, check that the release-drafter draft has the same version.
