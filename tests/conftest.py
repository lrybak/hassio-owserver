"""Shared fixtures for owserver tests."""

import json
import os
import platform
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEV_DIR = PROJECT_DIR / "dev"
TEMPLATE_PATH = PROJECT_DIR / "rootfs" / "etc" / "owfs.template.conf"
TEMPIO_VERSION = "2026.07.0"  # same version as in the base image from build.yaml
COMPOSE_CMD = ["docker", "compose", "-p", "owserver-test", "-f", str(DEV_DIR / "docker-compose.dev.yml")]
CONTAINER = "owserver-test-owserver-1"
OWSERVER = "localhost:4304"

DEFAULT_OPTIONS = {
    "devices": [{"device_type": "fake"}],
    "owhttpd": True,
    "temperature_scale": "Celsius",
    "debug": True,
}


def _wait_for_owhttpd(timeout: int = 120) -> None:
    """Wait until owhttpd responds on port 8099."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            result = subprocess.run(
                ["curl", "-sf", "http://localhost:8099/"],
                capture_output=True, timeout=5,
            )
            if result.returncode == 0:
                return
        except subprocess.TimeoutExpired:
            pass
        time.sleep(2)
    pytest.fail("owhttpd did not start within timeout")


def _write_options(tmp_path: Path, options: dict) -> Path:
    """Write options dict to a JSON file and return the path."""
    options_file = tmp_path / "options.json"
    options_file.write_text(json.dumps(options))
    return options_file


@pytest.fixture(scope="session")
def compose_project(tmp_path_factory):
    """Start the docker compose stack with default fake config for the session."""
    tmp_path = tmp_path_factory.mktemp("owserver")
    options_file = _write_options(tmp_path, DEFAULT_OPTIONS)

    env = {
        "OPTIONS_JSON_PATH": str(options_file),
        "BUILD_PLATFORM": os.environ.get("BUILD_PLATFORM", "linux/arm64"),
        "BUILD_ARCH": os.environ.get("BUILD_ARCH", "aarch64"),
        "PATH": subprocess.check_output(
            ["bash", "-lc", "echo $PATH"], text=True
        ).strip(),
    }

    # Resolve BUILD_FROM
    build_yaml = DEV_DIR.parent / "build.yaml"
    build_from = subprocess.run(
        ["yq", "eval", f'.build_from.{env["BUILD_ARCH"]}', str(build_yaml)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    env["BUILD_FROM"] = build_from

    # Build and start
    build_flag = "--no-build" if subprocess.run(
        ["docker", "image", "inspect", "local/owserver:ci"],
        capture_output=True,
    ).returncode == 0 else "--build"

    subprocess.run(
        [*COMPOSE_CMD, "up", "-d", build_flag],
        env=env, check=True,
    )

    _wait_for_owhttpd()

    yield {"env": env, "tmp_path": tmp_path}

    subprocess.run([*COMPOSE_CMD, "down"], env=env, check=False)


@pytest.fixture
def run_in_container(compose_project):
    """Run a command inside the owserver container."""
    def _run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["docker", "exec", CONTAINER, *cmd],
            capture_output=True, text=True, **kwargs,
        )
    return _run


# (sys.platform, platform.machine()) -> name suffix of the tempio release binary
TEMPIO_BINARY_MAP = {
    ("linux", "x86_64"): "amd64",
    ("linux", "aarch64"): "aarch64",
    ("darwin", "x86_64"): "darwin_amd64",
    ("darwin", "arm64"): "darwin_arm64",
}


def _download_tempio(tmp_path_factory) -> Path | None:
    """Download tempio binary for the current OS and arch (Linux or macOS)."""
    suffix = TEMPIO_BINARY_MAP.get((sys.platform, platform.machine()))
    if suffix is None:
        return None
    url = f"https://github.com/home-assistant/tempio/releases/download/{TEMPIO_VERSION}/tempio_{suffix}"
    binary = tmp_path_factory.mktemp("bin") / "tempio"
    urllib.request.urlretrieve(url, binary)
    binary.chmod(0o755)
    return binary


def _render_with_binary(tempio_bin: Path, options: dict) -> str:
    """Render template using local tempio binary."""
    result = subprocess.run(
        [str(tempio_bin),
         "-conf", "/dev/stdin",
         "-template", str(TEMPLATE_PATH),
         "-out", "/dev/stdout"],
        input=json.dumps(options), capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"tempio failed: {result.stderr}")
    return result.stdout


def _render_with_container(options: dict) -> str:
    """Render template using tempio inside the owserver container (fallback for other systems)."""
    result = subprocess.run(
        ["docker", "exec", "-i", CONTAINER,
         "tempio", "-conf", "/dev/stdin",
         "-template", "/etc/owfs.template.conf",
         "-out", "/dev/stdout"],
        input=json.dumps(options), capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"tempio failed: {result.stderr}")
    return result.stdout


@pytest.fixture(scope="session")
def tempio_bin(tmp_path_factory):
    """Download tempio binary on Linux and macOS, None on other platforms."""
    return _download_tempio(tmp_path_factory)


@pytest.fixture
def render_template(request, tempio_bin):
    """Render owfs.template.conf — local binary on Linux and macOS, container as fallback.

    The container is started only for the fallback, so template tests with a local binary do not need Docker.
    """
    if tempio_bin is not None:
        def _render(options: dict) -> str:
            return _render_with_binary(tempio_bin, options)
    else:
        request.getfixturevalue("compose_project")

        def _render(options: dict) -> str:
            return _render_with_container(options)
    return _render


@pytest.fixture(scope="module")
def start_with_config(compose_project):
    """Restart the owserver container with a new options.json config.

    Returns container logs after restart. Used for validation failure tests.
    Scoped to module — restores default config only once at the end.
    """
    env = compose_project["env"]
    tmp_path = compose_project["tmp_path"]

    def _start(options: dict, wait: bool = False) -> str:
        options_file = _write_options(tmp_path, options)
        env_with_options = {**env, "OPTIONS_JSON_PATH": str(options_file)}

        subprocess.run(
            [*COMPOSE_CMD, "up", "-d", "--force-recreate", "owserver"],
            env=env_with_options, check=True,
        )

        if wait:
            _wait_for_owhttpd(timeout=30)

        # Give container time to start/fail
        time.sleep(5)

        result = subprocess.run(
            [*COMPOSE_CMD, "logs", "owserver"],
            env=env_with_options, capture_output=True, text=True,
        )
        return result.stdout + result.stderr

    yield _start

    # Restore default config once at end of module
    options_file = _write_options(tmp_path, DEFAULT_OPTIONS)
    env["OPTIONS_JSON_PATH"] = str(options_file)
    subprocess.run(
        [*COMPOSE_CMD, "up", "-d", "--force-recreate", "owserver"],
        env=env, check=True,
    )
    _wait_for_owhttpd()
