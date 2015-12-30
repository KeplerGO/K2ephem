#!/usr/bin/env python
from setuptools import setup

# Command-line tools
entry_points = {'console_scripts': [
    'K2ephem = K2ephem:K2ephem_main'
]}

setup(name='K2ephem',
      version='1.1.0',
      description="Check if a Solar System object is "
                  "(or was) observable by NASA's K2 mission. "
                  "This command will query JPL/Horizons "
                  "to find out.",
      author='Geert Barentsen',
      author_email='geert.barentsen@nasa.gov',
      packages=['K2ephem'],
      install_requires=["pandas>=0.16", "K2fov>=3.0"],
      entry_points=entry_points,
      )
