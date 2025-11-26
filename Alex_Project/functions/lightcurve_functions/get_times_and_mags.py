# Gets observation times and magnitudes for each band for each star

import numpy as np

def get_times_and_fluxes(time, flux, flux_err, votable_data):
    band_time  = np.array(votable_data[time])
    band_flux = np.array(votable_data[flux])
    band_flux_err = np.array(votable_data[flux_err])
    return (band_time, band_flux, band_flux_err)