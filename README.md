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


## Testing

```bash
make test
```

The tests in `tests/` check the *built* site in `./public` rather than the
templates: every internal link and image resolves, every page has a title,
description and language, every sitemap URL exists, and the feed is valid
Atom. They use only Python's standard library, so there's nothing to install.

CI runs the same build with `--panicOnWarning`, so a Hugo deprecation fails
the build the day it appears, then runs these tests and
[zizmor](https://docs.zizmor.sh) over the workflows.


## Deployment

[Cloudflare Workers](https://developers.cloudflare.com/workers/static-assets/)
serves production. After the tests pass, every push to `main` deploys to the
Worker `rdegges-www`, which serves https://rdegges.com. The configuration is in
`cloudflare.config.ts` and `wrangler.config.ts`. The workers.dev URL is off
(`workersDev: false`), so the site has one public address.

The custom domain `rdegges.com` was attached to the Worker by hand.
`cloudflare.config.ts` does not list it, so a deploy leaves it in place. A
Cloudflare redirect rule sends `www.rdegges.com` to `rdegges.com`.

[Render](https://render.com) also deploys every push to `main`, from
`render.yaml`. It is kept only as the rollback host until it is removed.

On every run, CI packages the tested `public/` with `npx cf build`, then runs
`npx cf deploy --prebuilt --dry-run`. On `main`, the `deploy` job then uploads
that same package with `npx cf deploy --prebuilt`. It does not rebuild. You can
also start a deploy of `main` from the Actions tab (Build, then Run workflow).

**Cloudflare deploy token:** The `deploy` job gets `CLOUDFLARE_API_TOKEN` from
the `cloudflare` GitHub environment. Only `main` can use that environment. The
account ID is the environment variable `CLOUDFLARE_ACCOUNT_ID`, not a secret.

The token has one permission: Individual Workers Editor, on the `rdegges-www`
Worker only. It can deploy new versions of that Worker. It cannot change other
Workers. It also cannot create Workers or change routes or custom domains.
The `rdegges-www` Worker existed before this repo used it, and the deploy
reuses it.

The token has no expiry date. The owner chose this. To rotate the token:

1. In the Cloudflare dashboard, create a new account API token. Give it
   Individual Workers Editor on Specified Workers, then `rdegges-www`.
2. Copy the new token, then run:
   `pbpaste | gh secret set CLOUDFLARE_API_TOKEN --env cloudflare --repo rdegges/rdegges-www`
3. Run the Build workflow on `main` and make sure that the `deploy` job passes.
4. Delete the old token in the dashboard.

Response headers live in two files: `render.yaml` for Render and
`static/_headers` for Cloudflare. `tests/test_headers.py` fails when the two
files differ. The exceptions are Content-Type and Link, which only Cloudflare
sets. Link names the HTML post as the canonical URL of its Markdown copy.

`package.json` exists only for this Cloudflare tooling. It pins `cf` and
`wrangler` to exact versions. `cf` hands static-asset packaging to the
`wrangler` package, and only `wrangler.config.ts` can set the assets
directory. Nobody runs the `wrangler` CLI directly.

**Hugo version:** It lives in exactly one place — the image tag in
`docker-compose.yml`:

```yaml
image: ghcr.io/gohugoio/hugo:v0.168.0
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
