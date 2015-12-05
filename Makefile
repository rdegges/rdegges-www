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
	aws s3 sync public/ s3://www.rdegges.com --exclude '.git/*' --exclude '*.yml' --exclude 'Makefile' --exclude 'README.md' --acl public-read --delete
