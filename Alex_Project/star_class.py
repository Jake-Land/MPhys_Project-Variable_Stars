from functions.data_functions.get_star_data import get_star_data
from functions.data_functions.get_id_from_name import get_gaia_dr3_id
from find_phase_offset import find_phase_offset
from functions.observing_functions.find_airmass import find_airmass
from functions.lightcurve_functions.get_times_and_mags import get_times_and_fluxes
from calculate_score import calculate_total_score
from find_fit_gradient import mag_at_time
from observing_score import observing_score
from plot_fit import plot_fit
import pandas as pd
import numpy as np
from astropy.time import Time

class Star:
    def __init__(self, name):
        self.name = name
        self.id = int(get_gaia_dr3_id(name))
        self.data = get_star_data(self.id)
        self.epoch_photometry = pd.read_csv(f"data/{name.replace(' ', '_')}_JC_gloess_readable_all_epochs.csv")
        self.period = self.data['period'].iloc[0]
        self.classification = self.data['best_classification'].iloc[0]
        self.ra = self.data['ra'].iloc[0]
        self.dec = self.data['dec'].iloc[0]
        self.epoch_jd = np.min(get_times_and_fluxes('JD', 'mag_V', 'err_V', self.epoch_photometry)[0])


    def phase_offset(self, time):
        offset = find_phase_offset(self.epoch_photometry, self.period, time) # Replace epoch_photometry with actual observation data
        return offset

    def airmass(self, time):
        airmass = find_airmass(self.ra, self.dec, time)
        return airmass

    def score(self, time):
        total_score = calculate_total_score(self.phase_offset(time), self.gradient(time), self.airmass(time), self.ra, self.dec, time)
        return total_score
    
    def lightcurve(self, band, time_jd, nterms=7):
        fit = plot_fit(self.epoch_photometry, self.epoch_jd, self.period, band, time_jd, nterms=nterms)
        return fit
    
    def current_phase_and_mag(self, band, time):
        phase, mag, _ = mag_at_time(self.epoch_photometry, self.period, self.epoch_jd, time, band)
        return phase, mag
    
    def gradient(self, time, band=0):
        _, _, gradient = mag_at_time(self.epoch_photometry, self.period, self.epoch_jd, time, band)
        return gradient
    
    def observing_scores(self, start_time, end_time, block=30):
        scores = observing_score(start_time, end_time, block, self.score)
        return scores
 
current_time = Time.now().jd

#RV_UMa = Star("RV UMa")
RZ_Cep = Star("RZ Cep")
#RR_Lyr = Star("RR Lyr")
#RU_Psc = Star("RU Psc")

RZ_Cep.lightcurve('all', current_time, nterms=5)

"""
RV_UMa_scores = RV_UMa.observing_scores("2025-11-05 17:30:00", "2025-11-05 23:50:00", block=30)
RZ_Cep_scores = RZ_Cep.observing_scores("2025-11-05 17:30:00", "2025-11-05 23:50:00", block=30)
RR_Lyr_scores = RR_Lyr.observing_scores("2025-11-05 17:30:00", "2025-11-05 23:50:00", block=30)


scores = {"RV UMa": RV_UMa_scores, "RZ Cep": RZ_Cep_scores, "RR Lyr": RR_Lyr_scores}

observation_plan = [
    max(scores, key=lambda name: scores[name][i])
    for i in range(len(next(iter(scores.values()))))
]

print(observation_plan)
"""