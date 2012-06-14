test:
	nosetests --

coverage: 
	nosetests --with-coverage --

run:
	python2.7 main.py

install:
	pip install nose coverage pep8

style:
	pep8 *.py