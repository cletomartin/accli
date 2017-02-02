# -*- coding:utf-8; mode: make -*-

.PHONY: all test lint clean dist-clean

all:
	@echo "Nothing to do for 'all'"

test:
	nosetests ./tests

lint:
	flake8

clean:
	$(RM) $(shell find . -name "*~") $(shell find . -name "*.pyc")
	$(RM) -r $(shell find . -name "__pycache__") build

dist-clean: clean
	$(RM) -r accli.egg-info dist
