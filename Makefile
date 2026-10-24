# Makefile
#
# Helper commands for building and developing the site.

.PHONY: dev build test clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev    - Start development server with live reload (http://localhost:1313)"
	@echo "  make build  - Build the site for production (output in ./public)"
	@echo "  make test   - Build, then run the site tests against ./public"
	@echo "  make clean  - Remove build artifacts"

# Start the development server with live reload
dev:
	docker compose up

# Build the site for production
build:
	docker compose run --rm hugo build --minify

# Check the built site: links, metadata, sitemap, feed
test: build
	python3 -m unittest discover --start-directory tests

# Remove build artifacts
clean:
	rm -rf public resources
