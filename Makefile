# Makefile
#
# This file contains some helper scripts for building / deploying this site.

build:
	rm -rf public
	hugo

develop:
	rm -rf public
	hugo server --watch -d public-dev

deploy: build
	aws s3 sync public/ s3://www.rdegges.com --acl public-read --delete
	aws configure set preview.cloudfront true
	aws cloudfront create-invalidation --distribution-id E1IO983UEMAFXC --paths '/*'
