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

.PHONY: lint
lint:  ## Lint and black reformat files
	# NOTE(willkg): Make sure this matches what's in tox.ini.
	black --target-version=py37 --line-length=88 setup.py fx_crash_sig tests
	tox -e py37-lint

.PHONY: clean
clean:  ## Clean build artifacts
	rm -rf build dist ${PROJECT}.egg-info .tox .pytest_cache .cache
	find . -name __pycache__ | xargs rm -rf
	find . -name '*.pyc' | xargs rm -rf

.PHONY: release
release:  ## Release a tag
	./bin/release.sh
