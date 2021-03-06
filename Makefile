# Makefile for structure_and_landscapes

# Uses gcc for compiling
CC=gcc
LD=gcc

# Flags for compiling (mostly needed for Vienna RNA and cython)
CFLAGS=-shared -fopenmp -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/usr/include/python2.7 -I/usr/local/include/ViennaRNA
LFLAGS=-L/usr/local/lib/ViennaRNA -lRNA 

# Not real targets
.PHONY: test coverage run install style profile clean clean_cython analysis cython_compile all

# Default target; runs all 'not slow' tests (excludes integration tests)
test: all
	nosetests -A 'not slow  and not probabilistic' -- 

# Runs all tests (including integration tests)
test-all: all
	nosetests --

# Default target to be (currently 'test' to ease testing)
all: cython_compile

# Tells us unittesting line coverage 
coverage: all
	nosetests --with-coverage --cover-package=structure_and_landscapes --

# Installs the needed dependancies
install: all
	pip install nose coverage pep8 cython RunSnakeRun

# Runs pep8 (python style checker) on all .py file
style:
	find . -name \*.py | xargs pep8

# Removes compilation product (should be just source surviving)
clean: clean_cython
	-find . -name \*.pyc | xargs rm 
	-rm profiledata
	-rm -r .coverage

# Visual profiler
profile: install .profiledata
	mkdir ~/.config
	runsnake $<


# Cleans cython specific files
clean_cython:
	-rm organism/rna/vienna_distance.c
	-rm organism/rna/*.o
	-rm organism/rna/*.so

# Cython complied libraries 
cython_compile: organism/rna/vienna_distance.so

organism/rna/vienna_distance.so: organism/rna/vienna_distance.c organism/rna/vienna_utils.o
	$(CC) $(CFLAGS) -o $@ organism/rna/vienna_distance.c organism/rna/vienna_utils.o $(LFLAGS)
	
organism/rna/vienna_distance.c: organism/rna/vienna_distance.pyx
	cython organism/rna/vienna_distance.pyx -o $@

organism/rna/vienna_utils.o: organism/rna/vienna_utils.c organism/rna/vienna_utils.h
	$(CC) $(CFLAGS) -c organism/rna/vienna_utils.c -o $@ $(LFLAGS)

.profiledata: main.py
	python -m cProfile -o $@ main.py
