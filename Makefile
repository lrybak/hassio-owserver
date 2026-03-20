.PHONY: lint

lint:
	yamllint -c .yamllint.yml .
	hadolint -c .hadolint.yaml Dockerfile
	shellcheck --shell=bash --external-sources \
		rootfs/etc/s6-overlay/s6-rc.d/*/run \
		rootfs/etc/s6-overlay/s6-rc.d/*/check
