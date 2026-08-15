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

# Verify the pinned Hugo version matches across config files
make check

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

**Why there's a build script:** Render's static-site build image ships its own
pinned Hugo (0.124.x) and ignores `HUGO_VERSION` — setting it has no effect on
which binary `hugo` resolves to. Since these layouts need the template system
introduced in Hugo 0.146, `scripts/render-build.sh` downloads the pinned Hugo
(verifying its checksum) and builds with that instead.

**Hugo version:** The Hugo version is declared in three places that must stay in
sync:
- `hugo.toml` (`[module.hugoVersion] min`) — the source of truth; Hugo warns
  up front when built with anything older
- `docker-compose.yml` (image tag) — used for local development and CI
- `render.yaml` (`HUGO_VERSION` env var) — read by `scripts/render-build.sh`
  for production builds on Render

When upgrading Hugo, update all three and run `make check`. CI runs the same
check (`scripts/check-hugo-version.sh`) and fails the build if they drift.

Dependabot opens weekly PRs for the Docker image and GitHub Actions, so an image
bump will show up as a PR that fails `make check` until the other two files are
updated to match.


## Theme

I've built my own custom theme here for my personal usage — feel free to take
from it what you want. I release it into the public domain.
