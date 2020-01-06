# Makefile
#
# This file contains some helper scripts for building / deploying this site.

build:
	rm -rf public
	docker run --rm -u hugo --name rdegges-www -it -v $(PWD):/src jguyomard/hugo-builder:extras hugo

develop:
	rm -rf public-dev
	docker run --rm -u hugo --name rdegges-www -p 1313:1313 -it -v $(PWD):/src jguyomard/hugo-builder:extras hugo server --watch -d public-dev --bind 0.0.0.0

deploy: build
	aws s3 sync public/ s3://www.rdegges.com --acl public-read --delete
	aws configure set preview.cloudfront true
	aws cloudfront create-invalidation --distribution-id E1IO983UEMAFXC --paths '/*'
