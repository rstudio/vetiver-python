# Minimal makefile for quartodoc documentation

.PHONY: help Makefile stable latest

# Catch-all target:
%: Makefile


latest:
	python version_config.py
	python -m quartodoc build
	python -m quartodoc interlinks
	quarto render --profile latest

stable:
	python version_config.py
	python -m quartodoc build
	python -m quartodoc interlinks
	quarto render
