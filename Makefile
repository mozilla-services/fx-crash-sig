DEFAULT_GOAL := help

# Include .env and export it so variables set in there are available in the
# Makefile.
include .env
export

# Set these in the environment to override them. This is helpful for
# development if you have file ownership problems because the user in the
# container doesn't match the user on your host.
USER_ID ?= 10001
GROUP_ID ?= 10001

.PHONY: help
help:
	$(info Available rules:)
	$(info )
	@fgrep -h "##" Makefile | fgrep -v fgrep | sed 's/\(.*\):.*##/\1:/' | column -t -s '|'

.docker-build:
	make build

.env:
	@if [ ! -f .env ]; \
	then \
	echo "Creating .env file..."; \
	echo "# USER_ID=\n# GROUP_ID=\n" > .env; \
	fi

.PHONY: build
build: .env  ## | Build docker image
	docker-compose build --build-arg USER_ID=${USER_ID} --build-arg GROUP_ID=${GROUP_ID} app
	touch .docker-build

.PHONY: clean
clean:  ## | Remove build and runtime artifacts
	rm .docker-build
	rm -rf fx_crash_sig.egg-info
	rm -rf build dist
	find . -name "__pycache__" -type d | xargs rm -rf 

.PHONY: lint
lint: .docker-build  ## | Run linters
	docker-compose run --rm app flake8
	docker-compose run --rm app black --line-length=88 --target-version=py36 --check fx_crash_sig tests

.PHONY: reformat 
reformat:  ## | Reformat code
	docker-compose run --rm app black --line-length=88 --target-version=py36 fx_crash_sig tests

.PHONY: test
test:  ## | Run tests
	docker-compose run --rm app pytest tests/
