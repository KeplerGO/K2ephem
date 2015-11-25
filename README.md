# k2ephem

***Checks  whether a Solar System body is (or was) observable by [NASA's K2 mission](http://keplerscience.arc.nasa.gov).***

The [JPL/Horizons](http://ssd.jpl.nasa.gov/horizons.cgi)
ephemeris service allows users to predict the position
of Solar System bodies in the sky as seen from the Kepler/K2 spacecraft.
This can be achieved by entering `@-227` as the "Observer Location".
(Setting the location to be the Kepler spacecraft is *crucial*,
because Kepler is more than 0.5 AU away from the Earth!)

This repository provides a command-line tool that uses the JPL/Horizons
service to check whether a Solar System body is (or was) in the footprint
of one of the past or future K2 Campaign fields.

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


## Usage

After installation, you can call `k2ephem` from the command line.
For example, to verify whether comet *Chiron* can be observed by K2,
simply type:
```
$ k2ephem Chiron
```
