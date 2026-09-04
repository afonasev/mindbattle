DEPLOY_HOST ?= gfe
APP_DIR ?= /opt/mindbattle

.PHONY: build check deploy

build:
	npm run build

check:
	npm run check

deploy:
	DEPLOY_HOST=$(DEPLOY_HOST) APP_DIR=$(APP_DIR) bash scripts/deploy.sh
