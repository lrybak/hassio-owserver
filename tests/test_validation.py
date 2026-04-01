"""Validation tests — bad configs should produce expected error messages."""

import pytest
import subprocess
import requests

def make_options(devices, owhttpd=True):
    return {
        "devices": devices if isinstance(devices, list) else [devices],
        "owhttpd": owhttpd,
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

class TestOwhttpd:
    @staticmethod
    def is_owhttpd_running(host, port):
        try:
            requests.get(f"http://{host}:{port}/", timeout=2)
            return True
        except requests.ConnectionError:
            return False

    def test_owhttpd_is_up(self, start_with_config):
        logs = start_with_config(
            make_options({"device_type": "fake"}, owhttpd=True),
        )
        
        assert "starting owhttpd" in logs.lower()
        assert self.is_owhttpd_running("localhost", 8099)

    def test_owhttpd_is_down(self, start_with_config):
        logs = start_with_config(
            make_options({"device_type": "fake"}, owhttpd=False),
        )

        assert "owhttpd is disabled" in logs
        assert not self.is_owhttpd_running("127.0.0.1", 8099)
