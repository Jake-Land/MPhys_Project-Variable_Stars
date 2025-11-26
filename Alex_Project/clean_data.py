from functions.lightcurve_functions.remove_outliers import remove_outliers
from functions.lightcurve_functions.get_times_and_mags import get_times_and_fluxes
from functions.lightcurve_functions.fold_lightcurve import fold_lightcurve
from functions.lightcurve_functions.flux_to_mag import flux_to_mag, mag_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


UMa_epoch_photometry = pd.read_csv(f"data/RV_UMa_epoch_photometry.csv")


def clean_data(epoch_photometry, period, band):
    star_data = remove_outliers(epoch_photometry)
    columns = star_data.columns
    zeropoint_arr = np.loadtxt('data/GaiaEDR3_passbands_zeropoints_version2/zeropt.dat', dtype='str')
    j = (band * 5) + 1
    time, flux, error = get_times_and_fluxes(columns[j], columns[j+1], columns[j+2], star_data)
    phase, phase_flux, phase_err = fold_lightcurve(time, flux, error, period)
    zeropoint_GAIA = zeropoint_arr[0][band * 2]
    zeropoint_err_GAIA = zeropoint_arr[0][(band * 2) + 1]
    phase_mag = flux_to_mag(phase_flux, zeropoint_GAIA)
    phase_mag_err = mag_error(phase_flux, phase_err, zeropoint_GAIA, zeropoint_err_GAIA)
    
    return phase, phase_mag, phase_mag_err
