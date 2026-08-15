#!/usr/bin/env bash
#
# Production build for Render.
#
# Render's static-site build image ships its own Hugo (0.124.x) and ignores the
# HUGO_VERSION environment variable, so we install the version we actually want.
#
# The version comes from the image tag in docker-compose.yml, which is the
# single source of truth for this repo -- local dev, CI and production all build
# with the same Hugo, and there is no second copy to drift out of sync.

set -euo pipefail

cd "$(dirname "$0")/.."

version="$(sed -n 's|^[[:space:]]*image:[[:space:]]*hugomods/hugo:base-\(.*\)[[:space:]]*$|\1|p' docker-compose.yml)"
if [ -z "$version" ]; then
  echo "error: could not read the Hugo version from docker-compose.yml" >&2
  exit 1
fi

archive="hugo_extended_${version}_linux-amd64.tar.gz"
base="https://github.com/gohugoio/hugo/releases/download/v${version}"
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

echo "==> Downloading Hugo ${version} (extended)"
curl -sSfL "${base}/${archive}" -o "${workdir}/${archive}"
curl -sSfL "${base}/hugo_${version}_checksums.txt" -o "${workdir}/checksums.txt"

echo "==> Verifying checksum"
(cd "$workdir" && grep " ${archive}\$" checksums.txt | sha256sum -c -)

tar -xzf "${workdir}/${archive}" -C "$workdir" hugo
export PATH="${workdir}:${PATH}"

echo "==> Building with $(hugo version)"
hugo --minify
