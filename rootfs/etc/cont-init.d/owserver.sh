#!/usr/bin/with-contenv bashio


declare device
device=$(bashio::config 'device')

if bashio::config.has_value 'device' ;then
    bashio::log.info "Configuring ${device} device"
    device=$(bashio::string.replace ${device} '/' '\/')
    if [ '${device}' == 'usb' ]; then
        sed -i "s/%%device%%/usb/g" /etc/owfs.conf
    else
        sed -i "s/%%device%%/device = ${device}/g" /etc/owfs.conf
    fi
else
    bashio::log.info "Configuring fake device"
    sed -i "s/%%device%%/FAKE = DS18B20,DS2405/g" /etc/owfs.conf
fi
