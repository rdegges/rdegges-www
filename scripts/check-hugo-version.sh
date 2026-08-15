#!/usr/bin/env bash
#
# The Hugo version is declared in three places that must agree:
#
#   hugo.toml           [module.hugoVersion] min  - what the layouts require
#   docker-compose.yml  image tag                 - local dev + CI
#   render.yaml         HUGO_VERSION env var      - production builds
#
# hugo.toml is the source of truth; this script fails if the pins drift.

set -euo pipefail

cd "$(dirname "$0")/.."

expected=$(sed -n '/\[module.hugoVersion\]/,/^\[/p' hugo.toml \
  | sed -n 's/^min = "\(.*\)"$/\1/p')
compose=$(sed -n 's|.*image: hugomods/hugo:base-\(.*\)$|\1|p' docker-compose.yml)
render=$(sed -n '/key: HUGO_VERSION/,/value:/p' render.yaml \
  | sed -n 's/.*value: "\(.*\)"$/\1/p')

for pair in "hugo.toml:$expected" "docker-compose.yml:$compose" "render.yaml:$render"; do
  if [ -z "${pair#*:}" ]; then
    echo "error: could not parse a Hugo version out of ${pair%%:*}" >&2
    exit 1
  fi
done

status=0
for pair in "docker-compose.yml:$compose" "render.yaml:$render"; do
  file=${pair%%:*}
  found=${pair#*:}
  if [ "$found" != "$expected" ]; then
    echo "error: $file pins Hugo $found, but hugo.toml requires $expected" >&2
    status=1
  fi
done

if [ "$status" -eq 0 ]; then
  echo "Hugo $expected is pinned consistently across hugo.toml, docker-compose.yml and render.yaml."
fi

exit "$status"
