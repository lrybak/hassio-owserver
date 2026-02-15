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
    ha7net_server: 192.168.50.1
  - device_type: ha7net
    ha7net_server: 192.168.50.2
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
- pbm (ElabNET's Professioinal Bumster PBM-01)
- ha7net
- w1 (direct access via GPIO on RasPi)
- fake (random simulated device)

#### Sub-option: `device`

Specify the device.
This is mandatory option only for following **device_type**:
- serial
- passive
- i2c
- pbm

#### Sub-option: `ha7net_server`

Specify the address of the ha7net device.
This is mandatory option only for following **device_type**:
- ha7net

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

Specify debug mode for owserver. _Please note that once DEBUG mode is enabled you will not be able to connect to the owserver. Use debug mode only to troubleshoot issues with 1-Wire connectivity_


## Home Assistant integration

1. Configure and start app. With default configuration app starts with fake (mocked) devices.
1. Add to Home Assistant through the Integrations. Go to Integrations, Add Integration, Choose 1-Wire
    - Host: `provide app's hostname (from app details page)`
    - Port: `4304` _(default)_
1. ... or use Home Asistant auto discovery (since 2025.2.0). Go to Integrations, find discovered app and Add it.
1. That's it. On the integrations page wou will find 1-Wire integration with 1-Wire devices.
