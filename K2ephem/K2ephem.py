"""Checks whether a Solar System Body is in a past or future K2 field of view.
"""
from __future__ import print_function

import argparse
import logging
from io import StringIO

try:
    # Python 3
    from urllib.request import urlopen
except ImportError:
    # Legacy Python
    from urllib2 import urlopen

import numpy as np
import pandas as pd

import K2fov
from K2fov.K2onSilicon import onSiliconCheck


logging.basicConfig(level="INFO")

LAST_CAMPAIGN = 18  # Note that K2 may continue beyond this!

# Endpoint to obtain ephemerides from JPL/Horizons
HORIZONS_URL = ("http://ssd.jpl.nasa.gov/horizons_batch.cgi?"
                "batch=1&COMMAND=%27{target}%27&MAKE_EPHEM=%27YES%27%20&"
                "CENTER=%27500@-227%27&TABLE_TYPE=%27OBSERVER%27&"
                "START_TIME=%27{start}%27&STOP_TIME=%27{stop}%27&"
                "STEP_SIZE=%27{step_size}%27%20&ANG_FORMAT=%27DEG%27&"
                "QUANTITIES=%271,3,9%27&CSV_FORMAT=%27YES%27""")


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
    # Simplify column names for user-friendlyness;
    # 'APmag' is the apparent magnitude which is returned for asteroids;
    # 'Tmag' is the total magnitude returned for comets:
    df.index.name = 'date'
    df = df.rename(columns={'R.A._(ICRF/J2000.0)': "ra",
                            ' DEC_(ICRF/J2000.0)': "dec",
                            ' dRA*cosD': "dra",
                            'd(DEC)/dt': "ddec",
                            '  APmag': 'mag',
                            '  T-mag': 'mag'})
    # Add the angular motion column in units arcsec/h
    cosdec = np.cos(np.radians(df['dec']))
    df.loc[:, 'motion'] = ((df['dra'] * cosdec)**2 + df['ddec']**2)**0.5
    return df


def get_ephemeris_file(target, first, last, step_size=4):
    """Returns a file-like object containing the JPL/Horizons response.

    Parameters
    ----------
    target : str

    first : int
        Ephemeris will begin at the beginning of Campaign number `first`.

    last : int
        Ephemeris will end at the end of Campaign number `last`.

    step_size : int
        Resolution of the ephemeris in number of days.

    Returns
    -------
    ephemeris : file-like object.
        Containing the response from JPL/Horizons.
    """
    arg = {
            "target": target.replace(" ", "%20"),
            "start": K2fov.getFieldInfo(first)["start"],
            "stop": K2fov.getFieldInfo(last)["stop"],
            "step_size": "{}%20d".format(step_size)
           }
    if step_size < 1:  # Hack: support step-size in hours
        arg['step_size'] = "{:.0f}%20h".format(step_size * 24)
    print("Obtaining ephemeris for {target} "
          "from JPL/Horizons...".format(**arg))
    url = HORIZONS_URL.format(**arg)
    return urlopen(url)


def get_ephemeris_dataframe(target, first, last, step_size=4):
    """Returns the ephemeris dataframe for a single campaign."""
    fileobj = get_ephemeris_file(target, first, last, step_size)
    return jpl2pandas(fileobj)


def check_target(target, first=0, last=LAST_CAMPAIGN, verbose=True,
                 create_plot=False, print_speed=True):
    """
    Returns
    -------
    visible_campaigns : list of int
        List of campaign numbers in which the object is visible.
    """
    K2fov.logger.disabled = True  # Disable warnings about prelim fields
    ephem = get_ephemeris_dataframe(target, first, last)
    visible_campaigns = []
    for c in range(first, last + 1):
        visible = False
        fovobj = K2fov.getKeplerFov(c)
        campaign_ephem = ephem.loc[K2fov.getFieldInfo(c)["start"]:K2fov.getFieldInfo(c)["stop"]]
        if create_plot:
            import matplotlib.pyplot as pl
            from K2fov import projection
            ph = projection.PlateCaree()
            pl.figure()
            fovobj.plotPointing(ph, showOuts=False)
            pl.plot(campaign_ephem["ra"], campaign_ephem["dec"],
                    color="black", lw=3)
            #plot_padding = 5
            #pl.xlim([campaign_ephem["ra"].max() + plot_padding,
            #         campaign_ephem["ra"].min() - plot_padding])
            #pl.ylim([campaign_ephem["dec"].min() - plot_padding,
            #         campaign_ephem["dec"].max() + plot_padding])
            pl.xlabel('R.A. [degrees]')
            pl.ylabel('Declination [degrees]')
            pl.gca().invert_xaxis()
            pl.minorticks_on()
            pl.title("Visibility of {0} in K2 C{1}".format(target, c))
            plot_fn = "{}-c{}.png".format(target.replace("/", "_"), c)
            print("Writing {}".format(plot_fn))
            pl.savefig(plot_fn)
            pl.close()
        for idx, row in campaign_ephem.iterrows():
            if onSiliconCheck(row["ra"], row["dec"], fovobj):
                logging.debug("{} is visible in C{}.".format(target, c))
                logging.debug(campaign_ephem[["dra", "ddec"]])
                visible = True
                break
        if visible:
            visible_campaigns.append(c)
            if verbose:
                mag = campaign_ephem['mag']
                if mag.dtype == float:  # can also be the string "n/a"
                    min_mag, max_mag = mag.min(), mag.max()
                else:
                    min_mag, max_mag = -99.9, -99.9
                print("Object '{}' is visible in C{} ("
                      "mag {:.1f}..{:.1f}; "
                      "{:.1f}..{:.1f}\"/h; "
                      "ra {:.3f}..{:.3f}; "
                      "dec {:.3f}..{:.3f}).".format(
                          target,
                          c,
                          min_mag,
                          max_mag,
                          campaign_ephem['motion'].min(),
                          campaign_ephem['motion'].max(),
                          campaign_ephem['ra'].min(),
                          campaign_ephem['ra'].max(),
                          campaign_ephem['dec'].min(),
                          campaign_ephem['dec'].max())
                      )
            continue
    K2fov.logger.disabled = False
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
    parser.add_argument('--first', metavar='campaign', type=int, default=0,
                        help='First campaign to check (default: 0)')
    parser.add_argument('--last', metavar='campaign', type=int, default=LAST_CAMPAIGN,
                        help='Final campaign to check (default: {})'.format(LAST_CAMPAIGN))
    parser.add_argument('-p', '--plot', action='store_true',
                        help="Produce plot showing the object position "
                             "with respect to each campaign.")
    args = parser.parse_args(args)

    try:
        campaigns = check_target(args.target, first=args.first, last=args.last,
                                 create_plot=args.plot, verbose=True)
        if len(campaigns) == 0:
            print("'{}' does not appear to be visible "
                  "in K2 campaigns {}-{}.".format(args.target,
                                                  args.first,
                                                  args.last))
    except EphemFailure:
        # Something went wrong while querying JPL/Horizons;
        # an error message would have been printed at the point of failure
        pass


if __name__ == "__main__":
    K2ephem_main()
