DOCKER  = docker

PYTHON = python

PWD := $(shell pwd)

docker-build:
	$(DOCKER) build -t mrupgrade/api-mock:latest .

docker-push:
	$(DOCKER) push mrupgrade/api-mock:latest

docker-run:
	$(DOCKER) run -it -p 8080:8080 -v $(PWD)/mock/:/mock/ mrupgrade/api-mock:latest

docker-debug:
	$(DOCKER) run -it -p 8080:8080 -v $(PWD)/mock/:/mock/ mrupgrade/api-mock:latest /bin/bash

app-run:
	$(PYTHON) apimock.py