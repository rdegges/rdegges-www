# Makefile
#
# This file contains some helper scripts for building / deploying this site.

deploy:
	aws s3 sync public/ s3://www.rdegges.com --exclude '.git/*' --exclude '*.yml' --exclude 'Makefile' --exclude 'README.md' --acl public-read --delete
