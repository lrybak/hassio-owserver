"""Integration tests — port of dev/test.sh."""

import re
import subprocess

import pytest

pytestmark = pytest.mark.integration

OWSERVER = "localhost:4304"


@pytest.fixture(scope="module")
def devices(compose_project):
    """Get the device list from owdir (shared across tests in this module)."""
    from conftest import CONTAINER
    result = subprocess.run(
        ["docker", "exec", CONTAINER, "owdir", "-s", OWSERVER, "/"],
        capture_output=True, text=True,
    )
    return result.stdout.strip().splitlines()


@pytest.fixture(scope="module")
def ds18b20_sensor(devices):
    """Find the first DS18B20 sensor from the device list."""
    for device in devices:
        if re.match(r"^/28\.", device):
            return device
    return None


class TestOwserver:
    def test_owdir_returns_devices(self, devices):
        assert len(devices) > 0, "owdir returned no devices"

    def test_ds18b20_sensor_present(self, ds18b20_sensor):
        assert ds18b20_sensor is not None, "no DS18B20 sensor (expected fake /28.xxxx)"

    def test_temperature_readable(self, compose_project, ds18b20_sensor):
        if ds18b20_sensor is None:
            pytest.skip("no DS18B20 sensor found")

        from conftest import CONTAINER
        result = subprocess.run(
            ["docker", "exec", CONTAINER, "owread", "-s", OWSERVER,
             f"{ds18b20_sensor}/temperature"],
            capture_output=True, text=True,
        )
        temp = result.stdout.strip()
        assert re.match(r"^-?\d+(\.\d+)?$", temp), f"temperature invalid: '{temp}'"

    def test_owhttpd_responds(self, compose_project):
        result = subprocess.run(
            ["curl", "-sf", "http://localhost:8099/"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "1-Wire" in result.stdout
