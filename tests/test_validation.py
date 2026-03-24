"""Validation tests — bad configs should produce expected error messages."""

import pytest


def make_options(devices):
    return {
        "devices": devices if isinstance(devices, list) else [devices],
        "owhttpd": True,
        "temperature_scale": "Celsius",
        "debug": True,
    }


class TestDevicePathRequired:
    @pytest.mark.parametrize("device_type", ["serial", "passive", "i2c", "pbm"])
    def test_missing_device_path(self, start_with_config, device_type):
        logs = start_with_config(make_options({"device_type": device_type}))
        assert "Please set the device path" in logs


class TestServerAddressRequired:
    @pytest.mark.parametrize("device_type", ["ha7net", "enet", "etherweather"])
    def test_missing_server_address(self, start_with_config, device_type):
        logs = start_with_config(make_options({"device_type": device_type}))
        assert "Please set the server address" in logs


class TestLinkValidation:
    def test_link_both_device_and_server(self, start_with_config):
        logs = start_with_config(make_options({
            "device_type": "link",
            "device": "/dev/ttyUSB0",
            "server": "192.168.1.50",
        }))
        assert "Cannot set both" in logs

    def test_link_neither_device_nor_server(self, start_with_config):
        logs = start_with_config(make_options({"device_type": "link"}))
        assert "Please set 'device'" in logs


class TestHa7netDeprecation:
    def test_ha7net_server_deprecation_warning(self, start_with_config):
        logs = start_with_config(
            make_options({"device_type": "ha7net", "ha7net_server": "192.168.1.10"}),
        )
        assert "deprecated" in logs.lower()
