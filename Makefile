.PHONY: clean-pyc clean-build clean docs
UNAME := $(shell uname)

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
	uv run pip freeze | grep -v '^vetiver' | grep -v '^-e ' > requirements.txt
	echo 'vetiver' >> requirements.txt
	uvx --from git+https://github.com/posit-dev/with-connect@0783dabdd24e360e985a4588ce1239c3dc31c542 \
		with-connect -- uv run --with pytest pytest vetiver/tests/test_rsconnect.py -m 'rsc_test'

coverage:
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs doc documentation:
	$(MAKE) -C docs docs

release: dist
	twine upload dist/*

typecheck:
	pyright

