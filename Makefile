# Makefile
#
# This file contains some helper scripts for building / deploying this site.

build:
	rm -rf public
	hugo

develop:
	rm -rf public
	hugo server --watch

deploy:
	aws s3 sync public/ s3://www.rdegges.com --acl public-read --delete
