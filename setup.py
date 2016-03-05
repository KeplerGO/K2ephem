#!/usr/bin/env python
import os
import sys
from setuptools import setup

if "publish" in sys.argv[-1]:
    os.system("python setup.py sdist upload -r pypi")
    sys.exit()
elif "testpublish" in sys.argv[-1]:
    os.system("python setup.py sdist upload -r pypitest")
    sys.exit()

# Load the __version__ variable without importing the package
exec(open('K2ephem/version.py').read())

# Command-line tools; we're not using "entry_points" for now due to
# a bug in pip which turns all the tools into lowercase
scripts = ['scripts/K2ephem']

setup(name='K2ephem',
      version=__version__,
      description="Check if a Solar System object is "
                  "(or was) observable by NASA's K2 mission. "
                  "This command will query JPL/Horizons "
                  "to find out.",
      author='Geert Barentsen',
      author_email='hello@geert.io',
      url='https://github.com/KeplerGO/K2ephem',
      packages=['K2ephem'],
      install_requires=["pandas>=0.16", "K2fov>=3.0"],
      scripts=scripts,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Astronomy",
          ],
      )
