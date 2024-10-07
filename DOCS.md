# owserver

The addon provides owserver to read 1-Wire devices over serial/i2c or usb device.

## Configuration

**Note**: _Remember to restart the add-on whenever configuration change._

Example add-on configuration (YAML mode):

```yaml
owhttpd: true
temperature_scale: Celsius
device_type: serial_or_i2c
device: /dev/serial/by-id/usb-MERA-PROJEKT_USB__-__1Wire__MP00202__MPVVSOBE-if00-port0
debug: false
```

### Option: `owhttpd`

Enable to start the embedded owhttpd server _(Default true)_.
owhttpd server is exposed via **Ingress (Open Web UI)**

### Option: `device`

Specify owserver device, if using the "serial_or_i2c" type.

### Option: `device_type`

Specify owserver device_type from the options below:
- serial_or_i2c device
- usb device
- ha7net device
- w1 device (direct access via GPIO on RasPi)
- fake device (random simulated device)

Specify "/dev/null" as device, if using usb/ha7net/w1/fake type.

### Option: `temperature_scale`

Specify temperature scale used by owserver from the options below:
- Celsius _default_
- Fahrenheit 
- Kelvin 
- Rankine 

### Option: `ha7net_server`

Specify ha7net server. Use it with ha7net device only.

### Option: `debug`

Specify debug mode for owserver. _Please note that once DEBUG mode is enabled you will not be able to connect to the owserver. Use debug mode only to troubleshoot issues with 1wire connectivity_


## Home Assistant integration

1. Configure and start addon. With default configuration addon starts with fake (mocked) devices.
1. Add to Home Assistant through the Integrations. Go to Integrations, Add Integration, Choose 1-Wire
    - Host: `provide add-on's hostname (from add-on details page)`
    - Port: `4304` _(default)_
1. That's it. On the integrations page wou will find 1-Wire integration with discovered devices.