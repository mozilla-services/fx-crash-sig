DEFAULT_GOAL := help
PROJECT=fx_crash_sig

.PHONY: help
help:
	@echo "Available rules:"
	@echo ""
	@fgrep -h "##" Makefile | fgrep -v fgrep | sed 's/\(.*\):.*##/\1:  /'

.PHONY: test
test:  ## Run tests, linting, and static typechecking
	tox

.PHONY: format
format:  ## Format files
	tox exec -e py38-lint -- ruff format

.PHONY: lint
lint:  ## Lint files
	tox -e py38-lint

.PHONY: clean
clean:  ## Clean build artifacts
	rm -rf build dist ${PROJECT}.egg-info .tox .pytest_cache .cache
	find . -name __pycache__ | xargs rm -rf
	find . -name '*.pyc' | xargs rm -rf
