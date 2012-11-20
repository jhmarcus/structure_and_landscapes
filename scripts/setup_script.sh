#!/usr/bin/env bash
apt-get -y update
#May be unneeded
#apt-get -y upgrade
#apt-get -y dist-upgrade
apt-get -y install make python-numpy python-scipy python-matplotlib build-essential python2.7-dev python-pip vim screen python-profiler python-wxgtk2.8 python-setuptools git-core cython python-nose
cd ..
wget http://www.tbi.univie.ac.at/~ronny/RNA/ViennaRNA-2.0.7.tar.gz
tar -xf ViennaRNA-2.0.7.tar.gz
cd ViennaRNA-2.0.7
./configure
make
make install
cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)
cd structure_and_landscapes
make install