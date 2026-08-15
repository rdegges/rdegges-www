# Makefile
#
# Helper commands for building and developing the site.

.PHONY: dev build check clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev    - Start development server with live reload (http://localhost:1313)"
	@echo "  make build  - Build the site for production (output in ./public)"
	@echo "  make check  - Verify the pinned Hugo version matches across config files"
	@echo "  make clean  - Remove build artifacts"

# Start the development server with live reload
dev:
	docker compose up

# Build the site for production
build: check
	docker compose run --rm hugo hugo --minify

# Verify hugo.toml, docker-compose.yml and render.yaml agree on the Hugo version
check:
	./scripts/check-hugo-version.sh

# Remove build artifacts
clean:
	rm -rf public resources
