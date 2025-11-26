import pandas as pd
from functions.lightcurve_functions.remove_outliers import remove_outliers
from functions.lightcurve_functions.fold_lightcurve import fold_lightcurve
from functions.lightcurve_functions.get_times_and_mags import get_times_and_fluxes
from functions.lightcurve_functions.flux_to_mag import flux_to_mag, mag_error
from datetime import datetime

def find_phase_offset(star_data, period, time):

    star_data = remove_outliers(star_data)
    obs_times, _, _ = get_times_and_fluxes('g_transit_time', 'g_transit_flux', 'g_transit_flux_error', star_data)
    phase = ((time - obs_times) / period) % 1
    offset = [1 - x if x >= 0.5 else x for x in phase]
    star_offset = min(offset) 
    return star_offset



