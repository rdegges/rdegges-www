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

The site deploys automatically to [Render](https://render.com) on every push
to `main`. Configuration is in `render.yaml`.

**Hugo version:** It lives in exactly one place — the image tag in
`docker-compose.yml`:

```yaml
image: hugomods/hugo:base-0.165.0
```

Local dev and CI use that image directly. Production reads the same tag:
`scripts/render-build.sh` parses the version out of `docker-compose.yml`,
downloads that Hugo (verifying its checksum) and builds with it. So upgrading
Hugo means editing one line, and Dependabot's weekly Docker PR does it for you —
merge it and local dev, CI and production all move together.

The build script exists because Render's static-site image ships its own pinned
Hugo (0.124.x) and ignores `HUGO_VERSION`; setting that variable has no effect
on which binary `hugo` resolves to.

`hugo.toml` also sets `[module.hugoVersion] min`, but that's the *oldest* Hugo
the layouts support rather than the version we pin — it stays put when you
upgrade, and only moves if the templates start relying on a newer feature.


## Theme

I've built my own custom theme here for my personal usage — feel free to take
from it what you want. I release it into the public domain.
