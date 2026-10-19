---
name: bump-base-image
description: Bump the Home Assistant add-on base image (hassio-addons/addon-base) in build.yaml to a newer version, on its own chore/ branch in a separate git worktree. Use when the user asks to bump, update or check the base image.
---

# Bump the add-on base image

The base image is set in `build.yaml` (`build_from`, one line per arch). This skill moves both lines to a newer version of `ghcr.io/hassio-addons/base`.

The bump is its own change. Do it on its own branch, in a separate git worktree, so the user's current branch and uncommitted work stay untouched.

## 1. Find the versions

```bash
yq '.build_from' build.yaml
gh release list -R hassio-addons/addon-base --limit 10
```

Release tags look like `v21.0.8`. Image tags have no `v`: `ghcr.io/hassio-addons/base/amd64:21.0.8`.

If no release is newer than `build.yaml`, tell the user and stop.

If the user did not name a version, use the latest release. Show the user the release notes of all versions between the current and the new one (`gh release view -R hassio-addons/addon-base vX.Y.Z`). Point out a major version change, or a new Alpine version.

Check that the image exists for both archs:

```bash
docker manifest inspect ghcr.io/hassio-addons/base/amd64:X.Y.Z > /dev/null
docker manifest inspect ghcr.io/hassio-addons/base/aarch64:X.Y.Z > /dev/null
```

## 2. Check the Alpine version

The `Dockerfile` builds OWFS in an Alpine stage (`FROM alpine:3.xx AS builder`) and copies the binaries into the base image. Both must use the same Alpine minor version, or the binaries may not run.

Find the Alpine version of the new base:

```bash
gh api repos/hassio-addons/addon-base/contents/base/build.yaml?ref=vX.Y.Z --jq .content | base64 -d
```

If the Alpine minor version (e.g. `3.24`) is different from the builder stage, tell the user. Update the builder `FROM` line in the same branch only if the user agrees.

## 3. Create the worktree and branch

Always start from the latest `develop` on the remote:

```bash
git fetch origin develop
git worktree add ../hassio-owserver-bump-X.Y.Z -b chore/bump-base-X.Y.Z origin/develop
```

Do all next steps inside `../hassio-owserver-bump-X.Y.Z`. Do not change the user's main working tree.

## 4. Change the files

- `build.yaml`: change both `aarch64` and `amd64` lines to `X.Y.Z`.
- `Dockerfile`: only if step 2 needs it and the user agreed.
- `CHANGELOG.md`: add `- Bump addon base image to X.Y.Z` under `## Unreleased` at the top. If there is no `## Unreleased` section, create it right below `# Changelog`. If `## Unreleased` already has an older base image bump line, replace that line. Do not write a version number heading; the version is set at release time (see `CLAUDE.md`).

## 5. Lint and test

The test image `local/owserver:ci` is reused if it exists. Remove it first, or the tests run against the old base:

```bash
docker image rm local/owserver:ci
make lint
BUILD_ARCH=amd64 BUILD_PLATFORM=linux/amd64 pytest tests/ -v --tb=short
```

Use `BUILD_ARCH`/`BUILD_PLATFORM` only on an x86_64 machine. If `pytest` is missing, use `uv run --no-project --with pytest --with requests pytest ...`. The full test run takes about 6 minutes, so run it in the background.

If a tool for `make lint` is missing, say which one. Do not skip a failed check.

## 6. Report and wait

Show the user:

- old version → new version
- short summary of the release notes
- the diff
- lint and test results

Then stop. **Do not commit until the user says "GO".** Do not push or open a PR unless the user asks.

When the user says GO, commit with the message `Bump addon base image to X.Y.Z`.

If the user asks for a PR:

- base: `develop`
- title: `Bump addon base image to X.Y.Z`
- body: fill in `.github/pull_request_template.md`. Check only the items that were really done.
- The branch name `chore/` gives the PR the `docker` label (release-drafter).
- Do not merge the PR. The user always does the final merge.

## 7. Clean up

After the PR is merged, or if the user drops the bump:

```bash
git worktree remove ../hassio-owserver-bump-X.Y.Z
```
