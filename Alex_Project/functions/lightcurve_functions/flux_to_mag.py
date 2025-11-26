import numpy as np

def flux_to_mag(flux_array, zeropoint):
    zeropoint = float(zeropoint)
    flux_array = np.asarray(flux_array, dtype=float)
    mag_array = -2.5 * np.log10(flux_array) + zeropoint
    return mag_array

def mag_error(flux_array, flux_err_array, zeropoint, zeropoint_err):
    zeropoint = float(zeropoint)
    flux_array = np.asarray(flux_array, dtype=float)
    flux_err_array = np.asarray(flux_err_array, dtype=float)
    zeropoint_err = float(zeropoint_err)
    dM_dF = - 5 / (2 * np.log(10) * flux_array)
    dM_dZ = 1
    mag_err = np.sqrt(np.square(dM_dF * flux_err_array) + np.square(dM_dZ * zeropoint_err))
    return mag_err