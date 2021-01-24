# owserver

The addon provide owserver to read 1-Wire devices over DS2480B-based bus master serial device

## Configuration

**Note**: _Remember to restart the add-on whenever configuration change._

Example add-on configuration:

```yaml
owhttpd: false
device: ''
```

### Option: `owhttpd`

Enable to start the embedded owhttpd server (Default true).
owhttpd server is exposed via **Ingress (Open Web UI)**

### Option: `device`

Specify DS2480B-based bus master. 
To can find your device go to **Supervisor** -> **System** -> **Host System** -> click three dots -> **Hardware**
Keep it empty '' to mock with FAKE device


## Home Assistant integration

1. Configure and start addon. With default configuration addon starts with fake (mocked) devices.
2. Add to Home Assistant through the Integrations. Go to Integrations, Add Integration, Choose 1-Wire, Connection type: OWServer, Host: 9e0ef242_owserver, Port 4304 (default).
3. That's it. On the integrations page wou will find 1-Wire integration with discovered devices.