from curve_fit import curve_fit
from astropy.time import Time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def mag_at_time(epoch_photometry, period, epoch_jd, time_jd=None, band=0):

    t_fit, y_fit, _, _, _ = curve_fit(epoch_photometry, period, band)

    sort_idx = np.argsort(t_fit)
    t_fit = t_fit[sort_idx]
    y_fit = y_fit[sort_idx]

    if time_jd is None:
        time_jd = Time.now().jd

    phase = ((time_jd - epoch_jd) / period) % 1.0

    t_ext = np.concatenate([t_fit, t_fit + 1.0])
    y_ext = np.concatenate([y_fit, y_fit])

    dy_dphase = np.gradient(y_ext, t_ext)

    deriv = -1 * np.interp(phase, t_ext, dy_dphase)

    mag = np.interp(phase, t_ext, y_ext)
    return phase, mag, deriv

def find_gradient():
    pass