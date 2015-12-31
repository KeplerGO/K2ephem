# K2ephem [![Travis status](https://travis-ci.org/KeplerGO/K2ephem.svg)](https://travis-ci.org/KeplerGO/K2ephem)
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
If this requirement is met, you can install the latest stable version
of `K2ephem` using pip:
```
$ pip install K2ephem
``
Or you can install the most recent development version
from the git repository as follows:
```
$ git clone https://github.com/KeplerGO/K2ephem.git
$ cd K2ephem
$ python setup.py install
```
The `setup.py` script will automatically take care of installing two required dependencies (`K2fov` and `pandas`).

## Usage
After installation, you can call `K2ephem` from the command line.
For example, to verify whether comet *Chiron* can be observed by K2,
simply type:
```
K2ephem Chiron
```

## Authors
Created by Geert Barentsen (geert.barentsen at nasa.gov)
on behalf of the Kepler/K2 Guest Observer Office.
