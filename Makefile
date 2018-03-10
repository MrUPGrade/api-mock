DOCKER  = docker

PYTHON = python

PWD := $(shell pwd)

DOCKER_IMAGE_ARGS = -it -p 8080:8080 -v $(PWD)/mock/:/mock/ mrupgrade/api-mock:latest

docker-build:
	$(DOCKER) build -t mrupgrade/api-mock:latest .

docker-push:
	$(DOCKER) push mrupgrade/api-mock:latest

docker-run:
	$(DOCKER) run -e APIMOCK_DEBUG=True $(DOCKER_IMAGE_ARGS)

docker-debug:
	$(DOCKER) run $(DOCKER_IMAGE_ARGS) /bin/bash

app-run:
	$(PYTHON) apimock.py