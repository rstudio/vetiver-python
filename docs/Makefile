# Minimal makefile for quartodoc documentation

.PHONY: help Makefile

# Catch-all target:
%: Makefile
	python version_config.py
	python -m quartodoc build --verbose
	python -m quartodoc interlinks
	quarto render
