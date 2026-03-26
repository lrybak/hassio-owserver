# Home Assistant App: owserver

[![Releases][releases-shield]][releases]

![amd64][amd64-shield]
![aarch64][aarch64-shield]

## About

A robust owserver instance designed to bridge your 1-Wire network with Home Assistant. It acts as a gateway, allowing the native 1-Wire integration to communicate with various bus masters over Serial, USB, or Ethernet.

### Supported devices
App has been tested with
- [MERA-PROJEKT MP00206-P](http://www.meraprojekt.com.pl/mp00206-p.html)
- [ElabNET's Professional Busmaster PBM-01](https://shop.elabnet.de/en/1-wire/series/h/1-wire-professional-bus-master-pbm01-usb_812_2073)
- [HA7Net - Ethernet 1-Wire Host Adapter](https://www.embeddeddatasystems.com/HA7Net--Ethernet-1-Wire-Host-Adapter_p_22.html) 
- [OW-SERVER-ENET-2 - 1-Wire to Ethernet Server](https://www.embeddeddatasystems.com/OW-SERVER-1-Wire-to-Ethernet-Server-Revision-2_p_152.html) (thanks to [Embedded Data Systems](https://www.embeddeddatasystems.com/) for providing the device for testing)
- DS9490R USB 1-Wire (blue USB to RJ11 dongle)
- [USB to One Wire converter - Virtual Com Port FT232RL based](https://denkovi.com/usb-to-one-wire-interface-adaptor-converter-thermometer)

The following devices are supported but have not been tested yet:
- [EtherWeather](https://owfs.org/index_php_page_etherweather.html)
- [LinkHub-E](https://owfs.org/index_php_page_linkhub-e.html)

If you have successfully set up any of these devices, please open a PR to update the documentation or reach out so we can confirm compatibility.

The app should also work well with other serial/i2c/usb/ha7net/enet devices. Please let me know what device you're using so I will update the device list for further reference.

## Installation and configuration

### Installation

1. Access your Home Assistant, go to **Apps** -> **Install app** and add this URL as an additional repository: 
`https://github.com/lrybak/addon-repository`
1. Find the "owserver (1-Wire)" app and click the "INSTALL" button.
1. Configure the app and click on "START". With default configuration app starts with fake (mocked) devices.
1. Add to Home Assistant through the Integrations. Go to Integrations, Add Integration, Choose 1-Wire
    - Host: `provide app's hostname (from app details page)`
    - Port: `4304` _(default)_
1. ... or use Home Asistant auto discovery (since 2025.2.0). Go to Integrations, find discovered app and Add it.
1. That's it. On the integrations page wou will find 1-Wire integration with discovered devices.

### Configuration
Please check the **[full documentation page](https://github.com/lrybak/hassio-owserver/blob/master/DOCS.md)**.

## Screenshots

![Integration setup 1](https://github.com/lrybak/hassio-owserver/raw/master/images/screenshot_setup1.png)
![Integration setup 2](https://github.com/lrybak/hassio-owserver/raw/master/images/screenshot_setup2.png)
![Integrations page](https://github.com/lrybak/hassio-owserver/raw/master/images/screenshot_integrations.jpg)
![owhttpd](https://github.com/lrybak/hassio-owserver/raw/master/images/screenshot_owhttpd.png)

[releases-shield]: https://img.shields.io/github/release/lrybak/hassio-owserver.svg
[releases]: https://github.com/lrybak/hassio-owserver/releases

[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
