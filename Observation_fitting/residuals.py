from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from lombscargle import lomb_scargle_analysis
from fold_lightcurve import fold_lightcurve
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle


n_terms = 5
fields = ['JD', 'mag_L', 'err_L']
Cep_epoch_photometry = pd.read_csv(f"data/RZ_Cep_gloess_readable_all_epochs.csv", usecols=fields)
#UMa_epoch_photometry = pd.read_csv(f"data/RV_UMa_gloess_readable_all_epochs.csv", usecols=fields)

Cep_period_Monson = 0.30868
Cep_period_GAIA = 0.3087043245277305
Cep_predicted_period_Monson = 0.2963705952047736
UMa_period = 0.4680590552559243
df = Cep_epoch_photometry.copy()
#print(df)
df.sort_values(by=['JD'], inplace=True)
df.dropna(inplace=True)

time = np.asarray(df['JD'], dtype=float)
mag = np.asarray(df['mag_L'], dtype=float) # Assuming zero point of 21 for conversion
err = np.asarray(df['err_L'], dtype=float)

period_guess = Cep_period_Monson

periods = np.linspace(0.301, 0.31, 100)
max_freq = 1/min(periods)
min_freq = 1/max(periods)
print(min_freq, max_freq)

def find_chi_squared(period_guess):
    phase, phase_mag, phase_err = fold_lightcurve(time, mag, err, period_guess)
    ls = LombScargle(phase, phase_mag, dy=phase_err, nterms=n_terms)
    frequency, power = ls.autopower(minimum_frequency=min_freq, maximum_frequency=max_freq, samples_per_peak=100)
    best_frequency = frequency[np.argmax(power)]
    t_fit = np.linspace(min(phase), max(phase), 1000)
    y_fit = ls.model(t_fit, best_frequency)

    interp_model = interp1d(t_fit, y_fit, kind='linear', fill_value='extrapolate')
    model_at_data = interp_model(phase)
    
    # calculate residuals
    residuals = phase_mag - model_at_data
    
    # calculate chi-squared
    chi_squared = np.sum((residuals / phase_err)**2)


    return chi_squared

#print(periods)
chi_squared_list = []

for period in periods:
    chi_squared = find_chi_squared(period_guess=period)
    chi_squared_list.append(chi_squared)


best_period = periods[np.argmin(chi_squared_list)]
print("Best period =", best_period)


# plot residuals against period
plt.plot(periods, chi_squared_list, '-')
plt.xlabel('Trial period')
plt.ylabel('Residual sum of squares')
plt.title(f'Finding best-fit period - {best_period} days')
plt.show()



print("original period chi^2: ", find_chi_squared(Cep_period_Monson))
print("GAIA period chi^2: ", find_chi_squared(Cep_period_GAIA))
print("monson predicted period chi^2: ", find_chi_squared(Cep_predicted_period_Monson))
