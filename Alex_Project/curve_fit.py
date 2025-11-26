from functions.lightcurve_functions.remove_outliers import remove_outliers
from functions.lightcurve_functions.get_times_and_mags import get_times_and_fluxes
from functions.lightcurve_functions.fold_lightcurve import fold_lightcurve
from functions.lightcurve_functions.flux_to_mag import flux_to_mag, mag_error
from functions.lightcurve_functions.lombscargle import lomb_scargle_analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


UMa_epoch_photometry = pd.read_csv(f"data/RV_UMa_epoch_photometry.csv")


def curve_fit(epoch_photometry, period, band, nterms=3, use_jd=False):
    try:
        star_data = remove_outliers(epoch_photometry)
    except Exception:
        star_data = epoch_photometry.copy()

    if use_jd:
        band_map = {0: ('mag_B', 'err_B'), 1: ('mag_R', 'err_R'), 2: ('mag_V', 'err_V')}
        if band not in band_map:
            raise ValueError("band must be 0 (B), 1 (R) or 2 (V) when use_jd=True")

        mag_col, err_col = band_map[band]

        if 'JD' not in star_data.columns or mag_col not in star_data.columns or err_col not in star_data.columns:
            raise KeyError(f"Required columns 'JD', '{mag_col}' or '{err_col}' not found")

        jd = np.array(star_data['JD'], dtype=float)
        mag = np.array(star_data[mag_col], dtype=float)
        mag_err = np.array(star_data[err_col], dtype=float)

        # Remove rows with NaNs
        valid = ~np.isnan(jd) & ~np.isnan(mag) & ~np.isnan(mag_err)
        jd = jd[valid]
        mag = mag[valid]
        mag_err = mag_err[valid]

        t_fit, y_fit = lomb_scargle_analysis(jd, mag, mag_err, terms=nterms)

        return t_fit, y_fit, jd, mag, mag_err

    columns = list(star_data.columns)
    zeropoint_arr = np.loadtxt('data/GaiaEDR3_passbands_zeropoints_version2/zeropt.dat', dtype='str')


    if 'JD' in columns and any(c.startswith('mag_') for c in columns):
        band_map = {0: ('mag_B', 'err_B'), 1: ('mag_R', 'err_R'), 2: ('mag_V', 'err_V')}
        if band not in band_map:
            raise ValueError("band must be 0 (B), 1 (R) or 2 (V)")
        time_col = 'JD'
        mag_col, err_col = band_map[band]
        if mag_col not in columns or err_col not in columns:
            raise KeyError(f"Expected columns '{mag_col}' and '{err_col}' not found in DataFrame")
        time, flux, error = get_times_and_fluxes(time_col, mag_col, err_col, star_data)
    else:
        j = (band * 5) + 1
        time, flux, error = get_times_and_fluxes(columns[0], columns[j+1], columns[j+2], star_data)
    phase, phase_flux, phase_err = fold_lightcurve(time, flux, error, period)
    zeropoint_GAIA = zeropoint_arr[0][band * 2]
    zeropoint_err_GAIA = zeropoint_arr[0][(band * 2) + 1]
    phase_mag = flux_to_mag(phase_flux, zeropoint_GAIA)
    phase_mag_err = mag_error(phase_flux, phase_err, zeropoint_GAIA, zeropoint_err_GAIA)

    t_fit, y_fit = lomb_scargle_analysis(phase, phase_mag, phase_mag_err, terms=nterms)

    return t_fit, y_fit, phase, phase_mag, phase_mag_err
