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
#
# Extra arguments are passed through to hugo; CI passes --panicOnWarning.

set -euo pipefail

cd "$(dirname "$0")/.."

version="$(sed -n 's|^[[:space:]]*image:[[:space:]]*ghcr\.io/gohugoio/hugo:v\([0-9.]*\)[[:space:]]*$|\1|p' docker-compose.yml)"
if [ -z "$version" ]; then
  echo "error: could not read the Hugo version from docker-compose.yml" >&2
  exit 1
fi

# The plain archive, not hugo_extended_*: Hugo v0.170.0 removed the extended
# edition and keeps the old name only as a compatibility alias. Every version
# this site has pinned builds it identically with the plain binary (there is no
# Sass here), so one archive name covers 0.169.x and later.
archive="hugo_${version}_linux-amd64.tar.gz"
base="https://github.com/gohugoio/hugo/releases/download/v${version}"
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

echo "==> Downloading Hugo ${version}"
curl -sSfL "${base}/${archive}" -o "${workdir}/${archive}"
curl -sSfL "${base}/hugo_${version}_checksums.txt" -o "${workdir}/checksums.txt"

echo "==> Verifying checksum"
# Match the archive name literally: the dots are escaped so they cannot match
# other characters, and the name must end the line so hugo_..._linux-amd64.tar.gz
# cannot match a longer name such as one ending in .sig.
archive_re="${archive//./\\.}"
if [ "$(grep -c -E " ${archive_re}\$" "${workdir}/checksums.txt")" != 1 ]; then
  echo "error: expected exactly one checksum for ${archive} in Hugo's checksums file" >&2
  exit 1
fi
(cd "$workdir" && grep -E " ${archive_re}\$" checksums.txt | sha256sum -c -)

tar -xzf "${workdir}/${archive}" -C "$workdir" hugo
export PATH="${workdir}:${PATH}"

echo "==> Building with $(hugo version)"
hugo --minify "$@"
