#!/command/with-contenv bashio

# validating user's options
for device in $(bashio::config "devices|keys"); do
    if bashio::config.equals "devices[${device}].device_type" "serial" || \
        bashio::config.equals "devices[${device}].device_type" "passive" || \
        bashio::config.equals "devices[${device}].device_type" "i2c" || \
        bashio::config.equals "devices[${device}].device_type" "pbm"; then
        if ! bashio::config.has_value "devices[${device}].device"; then
            bashio::config.require "device" "Please set the device"
        fi
    fi
    if bashio::config.equals "devices[${device}].device_type" "ha7net"; then
        if ! bashio::config.has_value "devices[${device}].ha7net_server"; then
            bashio::config.require "device" "Please set the ha7net server address"
        fi
    fi
done

# generating owfs config file
tempio \
    -conf /data/options.json \
    -template /etc/owfs.template.conf \
    -out /etc/owfs.conf

owfs_generated_config=$(cat /etc/owfs.conf)
bashio::log.info "Generated owfs.config file:"
bashio::log.info "${owfs_generated_config}"