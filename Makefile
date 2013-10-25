
all:
	# nothing to do

test:
	nosetests ./tests

clean:
	$(RM) $(shell find . -name "*~") $(shell find . -name "*.pyc")
