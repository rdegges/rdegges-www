# rdegges-www

My personal website: https://www.rdegges.com


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


## Theme

I've built my own custom theme here for my personal usage — feel free to take
from it what you want. I release it into the public domain.
