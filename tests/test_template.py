"""Template rendering tests — fast, no container restart needed."""

import pytest

pytestmark = pytest.mark.template


def make_options(devices, temperature_scale="Celsius", owhttpd=True, debug=True):
    return {
        "devices": devices if isinstance(devices, list) else [devices],
        "owhttpd": owhttpd,
        "temperature_scale": temperature_scale,
        "debug": debug,
    }


class TestDeviceTypes:
    def test_fake(self, render_template):
        conf = render_template(make_options({"device_type": "fake"}))
        assert "server: FAKE = DS18B20" in conf

    def test_serial(self, render_template):
        conf = render_template(make_options({"device_type": "serial", "device": "/dev/ttyUSB0"}))
        assert "server: device = /dev/ttyUSB0" in conf

    def test_usb_all(self, render_template):
        conf = render_template(make_options({"device_type": "usb"}))
        assert "server: usb = all" in conf

    def test_usb_specific(self, render_template):
        conf = render_template(make_options({"device_type": "usb", "device": "/dev/bus/usb/001/002"}))
        assert "server: usb = /dev/bus/usb/001/002" in conf

    def test_ha7net_with_server(self, render_template):
        conf = render_template(make_options({"device_type": "ha7net", "server": "192.168.1.10"}))
        assert "server: ha7net = 192.168.1.10" in conf

    def test_ha7net_with_ha7net_server(self, render_template):
        conf = render_template(make_options({"device_type": "ha7net", "ha7net_server": "192.168.1.10"}))
        assert "server: ha7net = 192.168.1.10" in conf

    def test_ha7net_server_takes_precedence(self, render_template):
        conf = render_template(make_options({
            "device_type": "ha7net",
            "server": "primary.local",
            "ha7net_server": "deprecated.local",
        }))
        assert "server: ha7net = primary.local" in conf
        assert "deprecated.local" not in conf

    def test_enet(self, render_template):
        conf = render_template(make_options({"device_type": "enet", "server": "192.168.10.83"}))
        assert "server: enet = 192.168.10.83" in conf

    def test_etherweather(self, render_template):
        conf = render_template(make_options({"device_type": "etherweather", "server": "10.0.0.5"}))
        assert "server: etherweather = 10.0.0.5" in conf

    def test_w1(self, render_template):
        conf = render_template(make_options({"device_type": "w1"}))
        assert "server: w1" in conf

    def test_passive(self, render_template):
        conf = render_template(make_options({"device_type": "passive", "device": "/dev/ttyS0"}))
        assert "server: passive = /dev/ttyS0" in conf

    def test_i2c(self, render_template):
        conf = render_template(make_options({"device_type": "i2c", "device": "/dev/i2c-1"}))
        assert "server: i2c = /dev/i2c-1:ALL" in conf

    def test_link_device(self, render_template):
        conf = render_template(make_options({"device_type": "link", "device": "/dev/ttyUSB0"}))
        assert "server: link = /dev/ttyUSB0" in conf

    def test_link_server(self, render_template):
        conf = render_template(make_options({"device_type": "link", "server": "192.168.1.50:10001"}))
        assert "server: link = 192.168.1.50:10001" in conf

    def test_pbm(self, render_template):
        conf = render_template(make_options({"device_type": "pbm", "device": "/dev/ttyACM0"}))
        assert "server: usb = all" in conf
        assert "server: usb = scan" in conf
        assert "pbm = /dev/ttyACM0" in conf


class TestTemperatureScales:
    @pytest.mark.parametrize("scale", ["Celsius", "Fahrenheit", "Kelvin", "Rankine"])
    def test_temperature_scale(self, render_template, scale):
        conf = render_template(make_options({"device_type": "fake"}, temperature_scale=scale))
        assert scale in conf


class TestMultiDevice:
    def test_two_devices(self, render_template):
        devices = [
            {"device_type": "fake"},
            {"device_type": "enet", "server": "192.168.1.100"},
        ]
        conf = render_template(make_options(devices))
        assert "server: FAKE = DS18B20" in conf
        assert "server: enet = 192.168.1.100" in conf

    def test_common_config_present(self, render_template):
        conf = render_template(make_options({"device_type": "fake"}))
        assert "server: port = 4304" in conf
        assert "http: port = 8099" in conf
