.PHONY: lint test clean

lint:
	yamllint -c .yamllint.yml .
	hadolint -c .hadolint.yaml Dockerfile
	shellcheck --shell=bash --external-sources \
		rootfs/etc/s6-overlay/s6-rc.d/*/run \
		rootfs/etc/s6-overlay/s6-rc.d/*/check

test:
	pytest tests/ -v --tb=short

clean:
	find tests -type d -name __pycache__ -exec rm -rf {} +
	find tests -type d -name .pytest_cache -exec rm -rf {} +
