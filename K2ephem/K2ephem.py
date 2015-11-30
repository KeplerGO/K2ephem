"""Checks whether a Solar System Body is in a future K2 field of view.

Requires Python 3!
"""
from __future__ import print_function

import os
import sys
import argparse
import logging
from io import StringIO

try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Legacy Python
    from urllib2 import urlopen

import pandas as pd

from K2fov.K2onSilicon import getFieldInfo, getKeplerFov, onSiliconCheck


logging.basicConfig(level="INFO")

# Which campaigns should we test visibility for?
FIRST_CAMPAIGN = 0
LAST_CAMPAIGN = 13  # Note that K2 may continue beyond this!

# Endpoint to obtain ephemerides from JPL/Horizons
HORIZONS_URL = ("http://ssd.jpl.nasa.gov/horizons_batch.cgi?"
                "batch=1&COMMAND=%27{target}%27&MAKE_EPHEM=%27YES%27%20&"
                "CENTER=%27500@-227%27&TABLE_TYPE=%27OBSERVER%27&"
                "START_TIME=%27{start}%27&STOP_TIME=%27{stop}%27&"
                "STEP_SIZE=%27{step_size}%20d%27%20&ANG_FORMAT=%27DEG%27&"
                "QUANTITIES=%272,3,9%27&CSV_FORMAT=%27YES%27""")


class EphemFailure(Exception):
    # JPL/Horizons ephemerides could not be retrieved
    pass


def jpl2pandas(fileobj):
    """Converts a csv ephemeris file from JPL/Horizons into a DataFrame.

    Parameters
    ----------
    fileobj : file-like object that supports the `readlines()` function.
        Must be in JPL/Horizons' CSV-like format.

    Returns
    -------
    ephemeris : `pandas.DataFrame` object
    """
    jpl = fileobj.readlines()
    logging.debug("JPL Horizons ephemeris contains {} lines.".format(len(jpl)))
    csv_started = False
    csv = StringIO()
    for idx, line in enumerate(jpl):
        line = line.decode('utf-8')
        if line.startswith("$$EOE"):  # "End of ephemerides"
            break
        if csv_started:
            csv.write(line)
        if line.startswith("$$SOE"):  # "Start of ephemerides"
            csv.write(jpl[idx - 2].decode('utf-8'))  # Header line
            csv_started = True
    if len(csv.getvalue()) < 1:
        jpl_output = "\n".join([line.decode("utf-8")
                                for line in jpl])
        logging.error(jpl_output)
        logging.error("Uhoh, something went wrong! "
                      "Most likely, JPL/Horizons did not recognize the target."
                      " Check their response above to understand why.")
        raise EphemFailure()
    csv.seek(0)
    df = pd.DataFrame.from_csv(csv)
    # Rename the columns to make them easier to use
    df = df.rename(columns={'R.A._(a-app)': "ra",
                            ' DEC_(a-app)': "dec",
                            ' dRA*cosD': "dra",
                            'd(DEC)/dt': "ddec",
                            '  APmag': "mag"})
    return df


def get_ephemeris(target, start, stop, step_size=5):
    """Returns a file-like object containing the JPL/Horizons response.

    Parameters
    ----------
    target : str

    start : int
        Ephemeris will begin at the beginning of Campaign number `start`.

    stop : int
        Ephemeris will end at the end of Campaign number `stop`.

    step_size : int
        Resolution of the ephemeris in number of days.

    Returns
    -------
    ephemeris : file-like object.
        Containing the response from JPL/Horizons.
    """
    arg = {
            "target": target,
            "start": getFieldInfo(start)["start"],
            "stop": getFieldInfo(stop)["stop"],
            "step_size": step_size
           }
    print("Obtaining ephemeris for {target} "
          "from JPL/Horizons...".format(**arg))
    url = HORIZONS_URL.format(**arg)
    return urlopen(url)


def check_target(target, start=FIRST_CAMPAIGN, stop=LAST_CAMPAIGN):
    fileobj = get_ephemeris(target, start, stop)
    df = jpl2pandas(fileobj)
    visible_campaigns = []
    for c in range(start, stop + 1):
        visible = False
        fovobj = getKeplerFov(c)
        campaign_ephem = df.loc[getFieldInfo(c)["start"]:getFieldInfo(c)["stop"]]
        for idx, row in campaign_ephem.iterrows():
            if onSiliconCheck(row["ra"], row["dec"], fovobj):
                logging.debug("{} is visible in C{}.".format(target, c))
                logging.debug(campaign_ephem[["dra", "ddec"]])
                visible = True
                break
        if visible:
            visible_campaigns.append(c)
            continue
    return visible_campaigns


def K2ephem_main(args=None):
    """Exposes k2ephem to the command line."""
    parser = argparse.ArgumentParser(
                    description="Check if a Solar System object is "
                                "(or was) observable by NASA's K2 mission. "
                                "This command will query JPL/Horizons "
                                "to find out.")
    parser.add_argument('target',
                        help="Name of the target. "
                             "Must be known to JPL/Horizons.")
    args = parser.parse_args(args)

    try:
        campaigns = check_target(args.target)
        if len(campaigns) == 0:
            print("'{}' does not appear to be visible "
                  "in K2 campaigns {}-{}.".format(args.target,
                                                  FIRST_CAMPAIGN,
                                                  LAST_CAMPAIGN))
        else:
            print("Object '{}' is visible in Campaigns {}.".format(args.target,
                                                                   str(campaigns)))
    except EphemFailure:
        # Something went wrong while querying JPL/Horizons;
        # an error message would have been logging at point of failure
        pass


if __name__ == "__main__":
    K2ephem_main()
