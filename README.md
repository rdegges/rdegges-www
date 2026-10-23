# rdegges-www

My personal website: https://rdegges.com


## Development

This site is built using [Hugo](https://gohugo.io/), a fast static site generator.
The development environment is fully containerized — just have Docker installed.

```bash
# Start development server with live reload (http://localhost:1313)
make dev

# Build the site for production
make build

# Clean build artifacts
make clean
```

### Without Docker

If you prefer running Hugo directly:

```bash
brew install hugo
hugo server
```

Hugo Extended is required.


## Deployment

The site is a static build served by [Cloudflare](https://developers.cloudflare.com/workers/static-assets/).
Production builds with:

```bash
./scripts/build.sh   # output in ./public
```

Response headers (security headers, caching) live in `static/_headers`, which
Hugo copies into the build output, where Cloudflare reads it.

**Hugo version:** It lives in exactly one place, the image tag in
`docker-compose.yml`. Local dev uses that image directly, and
`scripts/build.sh` parses the version out of the same file, then downloads
that Hugo (verifying its checksum) and builds with it, which is what CI and
production run. Hosted build images ship whatever Hugo they ship, so we never
rely on one. Upgrading Hugo means editing one line, and Dependabot's weekly
Docker PR does it for you.

`hugo.toml` also sets `[module.hugoVersion] min`, but that's the *oldest* Hugo
the layouts support rather than the version we pin: it stays put when you
upgrade, and only moves if the templates start relying on a newer feature.


## Theme

I've built my own custom theme here for my personal usage — feel free to take
from it what you want. I release it into the public domain.
