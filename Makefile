# Makefile
#
# Helper commands for building and developing the site.

.PHONY: dev build deploy clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  make dev    - Start development server with live reload (http://localhost:1313)"
	@echo "  make build  - Build the site for production (output in ./public)"
	@echo "  make deploy - Build and deploy to AWS S3/CloudFront"
	@echo "  make clean  - Remove build artifacts"

# Start the development server with live reload
dev:
	docker compose up

# Build the site for production
build:
	docker compose run --rm hugo hugo --minify

# Build and deploy to AWS
deploy: build
	aws s3 sync public/ s3://www.rdegges.com --acl public-read --delete
	aws configure set preview.cloudfront true
	aws cloudfront create-invalidation --distribution-id E1IO983UEMAFXC --paths '/*'

# Remove build artifacts
clean:
	rm -rf public resources
