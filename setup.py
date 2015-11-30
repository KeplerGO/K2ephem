#!/usr/bin/env python
from setuptools import setup

# Command-line tools
entry_points = {'console_scripts': [
    'K2ephem = K2ephem.K2ephem:K2ephem_main'
]}

setup(name='K2ephem',
      version='1.0.0',
      description="Check if a Solar System object is "
                  "(or was) observable by NASA's K2 mission. "
                  "This command will query JPL/Horizons "
                  "to find out.",
      author='Geert Barentsen',
      author_email='geert.barentsen@nasa.gov',
      packages=['K2ephem'],
      data_files=[('K2ephem', ['K2ephem/k2-campaigns.csv'])],
      install_requires=["pandas", "K2fov"],
      entry_points=entry_points,
      )
