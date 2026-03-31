# owserver

The app provides owserver enabling access to 1-Wire sensors over serial, i2c, usb, w1, pbm, ha7net fake devices.

## Configuration

**Note**: _Remember to restart the app whenever configuration change._

Example app configurations:

```yaml
devices:
  - device_type: serial
    device: /dev/ttyUSB0
owhttpd: true
temperature_scale: Celsius
debug: false
```

```yaml
devices:
  - device_type: ha7net
    server: 192.168.50.1
  - device_type: ha7net
    server: 192.168.50.2
owhttpd: true
temperature_scale: Celsius
debug: false
```

```yaml
devices:
  - device_type: enet
    server: 192.168.10.83
owhttpd: true
temperature_scale: Celsius
debug: false
```

```yaml
devices:
  - device_type: etherweather
    server: 192.168.10.100
owhttpd: true
temperature_scale: Celsius
debug: false
```

```yaml
devices:
  - device_type: link
    server: 192.168.10.50
owhttpd: true
temperature_scale: Celsius
debug: false
```

```yaml
devices:
  - device_type: link
    device: /dev/ttyUSB0
owhttpd: true
temperature_scale: Celsius
debug: false
```

**Note**, these are just example configurations, don't copy, please create your own.


### Option: `devices`

This option allows you to specify list of 1-Wire devices.

#### Sub-option: `device_type`

Specify the owserver device type from the following options:
- serial
- passive (passive serial device)
- i2c
- usb
- pbm (ElabNET's Professional Bus Master PBM-01)
- ha7net (Ethernet 1-Wire Host Adapter by Embedded Data Systems)
- enet (OW-SERVER-ENET-2 by Embedded Data Systems)
- etherweather (EtherWeather)
- link (LinkHub-E, serial/USB or network)
- w1 (direct access via GPIO on RasPi)
- fake (random simulated device)

#### Sub-option: `device`

Specify the device.
This is mandatory option only for following **device_type**:
- serial
- passive
- i2c
- pbm

#### Sub-option: `server`

Specify the network address of the device (IP address or hostname, optionally with port).
This is mandatory option for following **device_type**:
- ha7net
- enet
- etherweather
- link (when using network connection)

#### Sub-option: `ha7net_server` (deprecated)

> **Deprecated**: `ha7net_server` is deprecated and will be removed in a future release (June 2026).
> Please migrate your configuration to use `server` instead.

Previously used to specify the address of the ha7net device. Use `server` instead.

### Option: `owhttpd`

Enable to start the embedded owhttpd server _(Default true)_.
owhttpd server is exposed via **Ingress (Open Web UI)**

### Option: `temperature_scale`

Specify temperature scale used by owserver from the options below:
- Celsius _default_
- Fahrenheit
- Kelvin
- Rankine

### Option: `debug`

Specify debug mode for owserver. _Please note that once DEBUG mode is enabled you will not be able to connect to the owserver. Use debug mode only to troubleshoot issues with 1-Wire connectivity_.

## Network: Exposing owserver port to LAN

By default, the owserver port (4304) is only accessible within the Home Assistant network. If you need other devices on your LAN to query owserver directly, you can optionally expose the port.

To enable:
1. Go to **Settings → Add-ons → owserver → Configuration → Network**
2. Set the port number (e.g. `4304`) in the **"owserver 1-Wire (set port number to expose to LAN)"** field
3. Click **Save** and restart the addon

To disable, clear the port field, save and restart.

## Home Assistant integration

1. Configure and start app. With default configuration app starts with fake (mocked) devices.
1. Add to Home Assistant through the Integrations. Go to Integrations, Add Integration, Choose 1-Wire
    - Host: `provide app's hostname (from app details page)`
    - Port: `4304` _(default)_
1. ... or use Home Asistant auto discovery (since 2025.2.0). Go to Integrations, find discovered app and Add it.
1. That's it. On the integrations page wou will find 1-Wire integration with 1-Wire devices.
