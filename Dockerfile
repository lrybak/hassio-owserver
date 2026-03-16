ARG BUILD_FROM

# Stage 1: Build OWFS from source
FROM alpine:3.21 AS builder

ARG OWFS_VERSION=v3.2p4

RUN apk add --no-cache \
  alpine-keys bash automake make git rsync tar gcc g++ \
  binutils libstdc++ libgfortran readline readline-dev python3-dev dev86 m4 libtool autoconf swig \
  linux-headers build-base util-linux \
  libftdi1-dev libusb-dev

RUN git clone --single-branch --branch ${OWFS_VERSION} --depth 1 https://github.com/owfs/owfs /owfs-code

COPY patches/ /owfs-code/patches/
RUN cd /owfs-code \
  && git apply patches/0001-owhttpd-ingress-relative-paths.patch \
  && git apply patches/0002-owhttpd-css-homeassistant-theme.patch

RUN cd /owfs-code \
  && ./bootstrap \
  && ./configure \
    --disable-owftpd \
    --disable-owexternal \
    --disable-ownet \
    --disable-owcapi \
    --disable-owperl \
    --disable-owphp \
    --disable-owpython \
    --disable-owtcl \
    --disable-owtap \
    --disable-owmon \
    --disable-owfs \
    --disable-zero \
    --disable-avahi \
    --enable-debug \
    --enable-owserver \
    --enable-owhttpd \
    --enable-ftdi \
    --enable-usb \
    --enable-owshell \
    --enable-w1 \
  && make -j $(nproc 2>/dev/null || echo 2) && make install

# Stage 2: Runtime image
FROM ${BUILD_FROM}

ENV LANG=C.UTF-8

RUN apk add --no-cache libftdi1 libusb libgcc

COPY --from=builder /opt/owfs/ /opt/owfs/
COPY --from=builder /usr/local/lib/libow*.so* /usr/local/lib/
COPY --from=builder /usr/local/bin/ow* /usr/local/bin/

# Copy data for add-on
COPY rootfs /

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION
ARG BUILD_REPOSITORY
ARG BUILD_NAME
ARG BUILD_DESCRIPTION

ENV PATH="/opt/owfs/bin:/usr/local/bin:${PATH}"

# Labels
LABEL \
  io.hass.name="${BUILD_NAME}" \
  io.hass.description="${BUILD_DESCRIPTION}" \
  io.hass.arch="${BUILD_ARCH}" \
  io.hass.type="addon" \
  io.hass.version=${BUILD_VERSION} \
  maintainer="Łukasz Rybak <lukasz.rybak@gmail.com>" \
  org.opencontainers.image.authors="Łukasz Rybak <lukasz.rybak@gmail.com>" \
  org.opencontainers.image.created="${BUILD_DATE}" \
  org.opencontainers.image.revision="${BUILD_REF}" \
  org.opencontainers.image.version="${BUILD_VERSION}" \
  org.opencontainers.image.title="${BUILD_NAME}" \
  org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
  org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/master/README.md" \
  org.opencontainers.image.licenses="MIT"
