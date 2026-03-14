#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_ARCH="${BUILD_ARCH:-aarch64}"
BUILD_PLATFORM="${BUILD_PLATFORM:-linux/arm64}"
BUILD_FROM="$(yq eval ".build_from.${BUILD_ARCH}" "${SCRIPT_DIR}/../build.yaml")"
export BUILD_ARCH BUILD_PLATFORM BUILD_FROM
COMPOSE="docker compose -p owserver-dev -f ${SCRIPT_DIR}/docker-compose.dev.yml"
OWSERVER="localhost:4304"
PASS=0
FAIL=0

pass() { echo "  [PASS] $*"; PASS=$((PASS + 1)); }
fail() { echo "  [FAIL] $*"; FAIL=$((FAIL + 1)); }

cleanup() { $COMPOSE down  || true; }
trap cleanup EXIT

echo "==> Starting containers..."
BUILD_FLAG="--build"
[ "${CI:-}" = "true" ] && BUILD_FLAG="--no-build"
$COMPOSE up -d $BUILD_FLAG

echo "==> Waiting for owhttpd on port 8099..."
for i in $(seq 1 60); do
  if curl -sf http://localhost:8099/ >/dev/null 2>&1; then
    break
  fi
  [ "$i" -eq 60 ] && { echo "  [FAIL] owhttpd did not start in time"; exit 1; }
  sleep 2
done

echo ""
echo "==> Test: owserver responds to owdir"
DEVICES=$(docker exec owserver-dev-owserver-1 owdir -s "$OWSERVER" / 2>/dev/null || true)
if [ -n "$DEVICES" ]; then
  pass "owdir returned device list"
  echo "     Devices: $(echo "$DEVICES" | tr '\n' ' ')"
else
  fail "owdir returned no devices"
fi

echo ""
echo "==> Test: fake DS18B20 sensor present"
SENSOR=$(echo "$DEVICES" | grep -E '^/28\.' | head -1 || true)
if [ -n "$SENSOR" ]; then
  pass "DS18B20 sensor found: $SENSOR"
else
  fail "no DS18B20 sensor (expected fake /28.xxxx)"
fi

echo ""
echo "==> Test: temperature readable"
if [ -n "$SENSOR" ]; then
  TEMP=$(docker exec owserver-dev-owserver-1 owread -s "$OWSERVER" "${SENSOR}/temperature" 2>/dev/null | tr -d ' ' || true)
  if [[ "$TEMP" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
    pass "temperature = ${TEMP}°C"
  else
    fail "temperature invalid or empty: '$TEMP'"
  fi
fi

echo ""
echo "==> Test: owhttpd responds on port 8099"
HTTP=$(curl -sf http://localhost:8099/ 2>/dev/null || true)
if echo "$HTTP" | grep -q "1-Wire"; then
  pass "owhttpd returned HTML"
else
  fail "owhttpd not responding"
fi

echo ""
echo "================================"
echo "  Results: ${PASS} passed, ${FAIL} failed"
echo "================================"
[ "$FAIL" -eq 0 ]
