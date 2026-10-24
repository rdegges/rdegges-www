#!/usr/bin/env bash
#
# Production build: installs the pinned Hugo, then builds into ./public.
#
# Hosted build images ship whatever Hugo they ship, so rather than depend on
# one, this downloads the exact version we pin and verifies its checksum.
#
# The version comes from the image tag in docker-compose.yml, which is the
# single source of truth for this repo -- local dev, CI and production all build
# with the same Hugo, and there is no second copy to drift out of sync.
#
# Extra arguments are passed through to hugo; CI passes --panicOnWarning.

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
hugo --minify "$@"
