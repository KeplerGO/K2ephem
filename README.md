# K2ephem [![PyPI](http://img.shields.io/pypi/v/K2ephem.svg)](https://pypi.python.org/pypi/K2ephem/) [![PyPI](http://img.shields.io/pypi/dm/K2ephem.svg)](https://pypi.python.org/pypi/K2ephem/) [![Travis status](https://travis-ci.org/KeplerGO/K2ephem.svg)](https://travis-ci.org/KeplerGO/K2ephem) [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.44363.svg)](http://dx.doi.org/10.5281/zenodo.44363)
***Checks  whether a Solar System body is (or was) observable by [NASA's K2 mission](http://keplerscience.arc.nasa.gov).***

[NASA's K2 mission](http://keplerscience.arc.nasa.gov) is using 
the unique assets of the repurposed Kepler space telescope 
to perform long-baseline, high-cadence, high-precision photometry 
of targets selected by the community. 
Unlike the original Kepler mission, the loss of two reaction wheels 
requires K2 to point near the ecliptic plane. 
As a result, K2 can provide high-precision lightcurves 
for large numbers of asteroids, comets, and (dwarf) planets.  

This repository provides a command-line tool that uses the JPL/Horizons
service to check whether a Solar System body is (or was) in the footprint
of one of the past or future [K2 Campaign fields](http://keplerscience.arc.nasa.gov/k2-fields.html).

## Installation
You need to have a working version of Python installed.
If this requirement is met, you can install the latest stable version
of `K2ephem` using pip:
```
$ pip install K2ephem
```
If you have a previous version installed, you can upgrade it using:
```
pip install K2ephem --upgrade
```
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

Or you can type `K2ephem --help` to see the detailed usage instructions:
```
$ K2ephem --help
usage: K2ephem [-h] [--first campaign] [--last campaign] [-p] target

Check if a Solar System object is (or was) observable by NASA's K2 mission.
This command will query JPL/Horizons to find out.

positional arguments:
  target            Name of the target. Must be known to JPL/Horizons.

optional arguments:
  -h, --help        show this help message and exit
  --first campaign  First campaign to check (default: 0)
  --last campaign   Final campaign to check (default: 18)
  -p, --plot        Produce plot showing the object position with respect to
                    each campaign.
```

## Background
The [JPL/Horizons](http://ssd.jpl.nasa.gov/horizons.cgi)
ephemeris service allows users to predict the position
of Solar System bodies in the sky as seen from the Kepler/K2 spacecraft.
This can be achieved by entering `@-227` as the "Observer Location".
Setting the location to be the Kepler spacecraft is *crucial*,
because Kepler is more than 0.5 AU away from the Earth!

## Attribution
Created by Geert Barentsen for the NASA Kepler/K2 Guest Observer Office.

If this tool aided your research, please cite it using the [DOI identifier](http://dx.doi.org/10.5281/zenodo.44363)
or the following BibTeX entry:
```
@misc{geert_barentsen_2016_44363,
  author       = {Geert Barentsen},
  title        = {K2ephem: v1.1.1},
  month        = jan,
  year         = 2016,
  doi          = {10.5281/zenodo.44363},
  url          = {http://dx.doi.org/10.5281/zenodo.44363}
}
```
