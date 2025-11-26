import pandas as pd
import numpy as np


def fold_lightcurve(time, mag, error, period):
    """
    Folds the lightcurve given a period.
    time: input time (same unit as period)
    mag: input magnitude
    error: input error
    period: period to be folded to, needs to same unit as time (i.e. days)
    returns: phase, folded magnitude, folded error
    """
    # Create a pandats dataframe from
    data = pd.DataFrame({"time": time, "flux": mag, "error": error})

    # create the phase
    data["phase"] = data.apply(lambda x: ((x.time / period) - np.floor(x.time / period)), axis=1)

    # Creates the out phase, flux and error
    phase_long = np.concatenate((data["phase"], data["phase"] + 1.0))
    mag_long = np.concatenate((mag, mag))
    err_long = np.concatenate((error, error))

    phase_sort = np.argsort(phase_long)
    phase_long_sorted = phase_long[phase_sort]
    mag_long_sorted = mag_long[phase_sort]
    err_long_sorted = err_long[phase_sort]

    nanmask = ~np.isnan(phase_long_sorted) & ~np.isnan(mag_long_sorted) & ~np.isnan(err_long_sorted)
    
    return (phase_long_sorted[nanmask], mag_long_sorted[nanmask], err_long_sorted[nanmask])