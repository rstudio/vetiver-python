.PHONY: clean-pyc clean-build clean docs
UNAME := $(shell uname)

RSC_API_KEYS=vetiver/tests/rsconnect_api_keys.json

ifeq ($(UNAME), Darwin)
    BROWSER := open
else
    BROWSER := python -mwebbrowser
endif

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-rsc - run tests for rsconnect"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dev - generate Connect API keys"
	@echo "dev-start - start up development Connect in Docker"
	@echo "dev-stop - stop Connect dev container"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-test:
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/

lint:
	flake8 vetiver

test: clean-test
	pytest -m 'not rsc_test and not docker'

test-pdb: clean-test
	pytest -m 'not rsc_test and not docker' --pdb

test-rsc: clean-test
	pytest

coverage:
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs doc documentation:
	$(MAKE) -C docs docs

release: dist
	twine upload dist/*

dev: vetiver/tests/rsconnect_api_keys.json

dev-start:
	docker compose up -d
	docker compose exec -T rsconnect bash < script/setup-rsconnect/add-users.sh
	# curl fails with error 52 without a short sleep....
	sleep 5
	curl -s --retry 10 --retry-connrefused http://localhost:3939

dev-stop:
	docker compose down
	rm -f $(RSC_API_KEYS)

typecheck:
	pyright

$(RSC_API_KEYS): dev-start
	python script/setup-rsconnect/dump_api_keys.py $@
