# Changelog

## 0.6.0
- Send discovery information to Home Assistant.
- Add a new device type "passive" for special serial devices.
- Add possibility to optionally specify device name of usb device.
- Update hassio-addons/addon-base to v16.3.6

## 0.5.0
- Ability to add multiple 1-Wire devices - **breaking change**, requires addon re-configuration
- Update hassio-addons/addon-base to v16.3.4

### Breaking change: read before you upgrade!

This update introduces the ability to add multiple 1-Wire devices which required changes to to add-on configuration.
Devices now need to be specified as a YAML list. Please refer to the documentation page for more details before you upgrade.

## 0.4.0
- Added option to support PBM (ElabNET's Professioinal Bumster PBM-01) by @SamGamdschie in https://github.com/lrybak/hassio-owserver/pull/27

## 0.3.9

- Update hassio-addons/addon-base to v16.3.2
- Bump Github Actions version

## 0.3.8

- Added support for special "w1" device

## 0.3.7

- Update hassio-addons/addon-base to v15.0.9

## 0.3.6

- Update hassio-addons/addon-base to v15.0.6

## 0.3.5

- Update hassio-addons/addon-base to v15.0.2

## 0.3.4

- Update hassio-addons/addon-base to v14.3.3

## 0.3.3

- Feature request: Make it working with HA7NET devices #13

## 0.3.2

- Update hassio-addons/addon-base to v14.3.2
- Fixes #5

## 0.3.1

- Add device type selector (usb)
- Add debug mode for owserver
- Add temperature scale selector
- Change auto_uart to uart to get rid of home assistant warning
- Updated documentation

## 0.3.0

This version aims to update the add-on installation process. Currently, users have to manually add the repository https://github.com/lrybak/hassio-owserver/ to install the add-on.
With this pull request, three new repositories are introduced:

https://github.com/lrybak/addon-repository - containing stable releases of the addon, which is recommended for most users.
https://github.com/lrybak/addon-repository-beta - containing release candidate versions of the add-on, which is recommended only for those who want to test new features.
https://github.com/lrybak/addon-repository-edge - containing bleeding edge builds of the add-on, suitable only for development purposes and may be unstable or not work at all.

This change makes it easier to release new updates for the add-on and provides a more streamlined installation process for users.

Please note that the current repository (https://github.com/lrybak/hassio-owserver/) will be supported until the end of July 2023. 
Repository still will be used to host addon code, 
After that time, all users will need to switch to the new repositories mentioned above to get updates.

### Breaking change:

After changing add-on repository in Home Assistant, the hostname of add-on will also change. You need to add the 1-wire integration again with the new hostname (simple method) or modify the one already installed integration (advanced method). Please note that the Home Assistant UI does not allow you to change the hostname. To modify an existing integration, edit the .storage/core.config_entries file. It's recommended to have copy of the file copy before making any changes. After making the change, remember to restart Home Assistant.

### Apart of the above this change brings below changes as well:

- Update hassio-addons/addon-base to v13.2.2
- Update docs
- Code refactor

Thank you for your understanding and support.

## 0.2.1

- Upgrades addon-base to 10.0.2
- Changes auto_uart to uart for Home Assistant compatibility 

## 0.2.0

- Upgrades addon-base to 9.1.0
- Migrates repository (from **https://github.com/lrybak/hassio-addons/owserver** to: **https://github.com/lrybak/hassio-owserver**)
- Adds Github Actions workflow to build and publish multi-arch images into Docker Hub

## 0.1.4

- Fix links in Ingress
- Add panel icon
- run owhttpd in read only mode

## 0.1.3

- Adds Ingress support

## 0.1.2

- Upgrades owserver to v3.2p4
- Upgrades addon-base to 8.0.6
- Minor fixes
