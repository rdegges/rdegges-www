#!/usr/bin/env bash
#
# Checks that the site serves the security.txt a deploy just uploaded.
#
# The deploy job runs this after every deploy to main, including the monthly
# scheduled one that exists to renew Expires. Comparing the live Expires line
# with the packaged one proves this deploy is what visitors get; a threshold
# such as "more than 170 days out" would also pass on an older deploy.
#
# Usage: check-live-security-txt.sh PACKAGED_SECURITY_TXT URL

set -uo pipefail

if [ $# -ne 2 ]; then
  echo "usage: $0 PACKAGED_SECURITY_TXT URL" >&2
  exit 2
fi
packaged=$1
url=$2

# The Expires value of the security.txt on stdin. Fails when there is not
# exactly one Expires line: two would leave readers to pick one.
expires() {
  local values
  values=$(sed -n 's/^Expires: //p')
  [ "$(printf '%s' "$values" | grep -c '')" -eq 1 ] || return 1
  printf '%s\n' "$values"
}

if ! want=$(expires < "$packaged"); then
  echo "::error::$packaged must have exactly one Expires line"
  exit 1
fi

# Guards the template: Hugo sets Expires to 180 days from the build.
if ! expires_at=$(date -u -d "$want" +%s); then
  echo "::error::cannot read the packaged Expires value '$want'"
  exit 1
fi
days=$(( (expires_at - $(date -u +%s)) / 86400 ))
if [ "$days" -lt 179 ]; then
  echo "::error::the packaged security.txt expires in $days days; the template should give 180"
  exit 1
fi

# The new version can take a few seconds to reach every Cloudflare location.
for attempt in 1 2 3 4 5 6; do
  if body=$(curl --fail -sS --proto '=https' --max-time 10 "$url"); then
    got=$(expires <<< "$body") || got="(not exactly one Expires line)"
    if [ "$got" = "$want" ]; then
      echo "ok: $url serves Expires $got, $days days out"
      exit 0
    fi
    echo "attempt $attempt: $url serves Expires $got, want $want"
  else
    echo "attempt $attempt: could not fetch $url"
  fi
  if [ "$attempt" -lt 6 ]; then
    sleep 15
  fi
done

echo "::error::$url does not serve the security.txt this deploy uploaded"
exit 1
