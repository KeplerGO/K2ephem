# k2ephem

***Checks  whether a Solar System body is (or was) observable by [NASA's K2 mission](http://keplerscience.arc.nasa.gov).***


## Installation

You need to have a working version of Python installed.
If this requirement is met, you can install `k2ephem`
from the git repository as follows:
```
$ git clone https://github.com/KeplerGO/k2ephem.git
$ cd k2ephem
$ python setup.py install
```
The `setup.py` script will automatically take care of installing two required dependencies (`K2fov` and `pandas`).


# Usage

After installation, you can call `k2ephem` from the command line.
For example, to verify whether comet *Chiron* can be observed by K2,
simply type:
```
$ k2ephem Chiron
```
