# -*- coding:utf-8; mode: make -*-

all:
	# nothing to do for all

test:
	nosetests ./tests

clean:
	$(RM) $(shell find . -name "*~") $(shell find . -name "*.pyc")
	$(RM) -r $(shell find . -name "__pycache__") build

dist-clean: clean
	$(RM) -r accli.egg-info dist
