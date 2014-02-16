
all:
	# nothing to do for all

test:
	nosetests ./tests

clean:
	$(RM) $(shell find . -name "*~") $(shell find . -name "*.pyc")
