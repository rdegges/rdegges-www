#!/usr/bin/env bash
#
# Production build for Render.
#
# Render's static-site build image ships its own pinned Hugo (0.124.x as of
# writing) and does NOT honour the HUGO_VERSION environment variable -- setting
# it has no effect on which binary `hugo` resolves to. Since this site's layouts
# require the template system introduced in Hugo 0.146, we download the pinned
# version ourselves rather than using whatever the image provides.
#
# HUGO_VERSION comes from render.yaml and is kept in sync with hugo.toml and
# docker-compose.yml by scripts/check-hugo-version.sh.

set -euo pipefail

: "${HUGO_VERSION:?HUGO_VERSION is not set (it should come from render.yaml)}"

archive="hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
base="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}"
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

echo "==> Downloading Hugo ${HUGO_VERSION} (extended)"
curl -sSfL "${base}/${archive}" -o "${workdir}/${archive}"
curl -sSfL "${base}/hugo_${HUGO_VERSION}_checksums.txt" -o "${workdir}/checksums.txt"

echo "==> Verifying checksum"
(cd "$workdir" && grep " ${archive}\$" checksums.txt | sha256sum -c -)

tar -xzf "${workdir}/${archive}" -C "$workdir" hugo
export PATH="${workdir}:${PATH}"

echo "==> Building with $(hugo version)"
hugo --minify
