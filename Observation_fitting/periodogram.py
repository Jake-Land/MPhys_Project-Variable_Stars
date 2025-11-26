import numpy as np
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
import pandas as pd

fields = ['JD', 'mag_V', 'err_V']
RZ_Cep_epochs = pd.read_csv('data/RZ_Cep_JC_gloess_readable_all_epochs.csv', usecols=fields)
RZ_Cep_epochs.sort_values(by=['JD'], inplace=True)
RZ_Cep_epochs.dropna(inplace=True)
df = RZ_Cep_epochs.copy()

"""
RV_UMa_epochs = pd.read_csv('data/RV_UMa_gloess_readable.csv', usecols=fields)
RV_UMa_epochs.sort_values(by=['JD'], inplace=True)
RV_UMa_epochs.dropna(inplace=True)
#df = RV_UMa_epochs.copy()
"""

# Convert to numpy arrays
time = np.asarray(df['JD'], dtype=float)
mag = np.asarray(df['mag_V'], dtype=float) + 21 # Assuming zero point of 21 for conversion
err = np.asarray(df['err_V'], dtype=float)

min_period = 0.3
max_period = 0.35
minimum_frequency = 1.0 / max_period
maximum_frequency = 1.0 / min_period

# Lomb–Scargle
ls = LombScargle(time, mag, err, nterms=3)
frequency, power = ls.autopower(minimum_frequency=minimum_frequency, maximum_frequency=maximum_frequency, method='chi2', samples_per_peak=1000)
"""
freqs = []
for _ in range(1000):
    idx = np.random.randint(0, len(time), len(time))
    t_b, y_b, dy_b = time[idx], mag[idx], err[idx]
    err_freq, err_power = ls.autopower(method="chi2")
    freqs.append(err_freq[np.argmax(err_power)])

freqs = np.array(freqs)
sigma_P = np.std(1/freqs)
"""
best_frequency = frequency[np.argmax(power)]
best_period = 1.0 / best_frequency
# Convert best period (in days) to hours, minutes, seconds for easier reading
period_days = best_period
period_hours_total = period_days * 24.0
hours = int(period_hours_total)
minutes = int((period_hours_total - hours) * 60)
seconds = ((period_hours_total - hours) * 60 - minutes) * 60
print(f"Best period: {period_days} days (freq {best_frequency:} 1/d)")
print(f"Which is: {hours}h {minutes}m {seconds:.3f}s ({period_hours_total:.6f} hours)")


# Plot power vs frequency
plt.figure(figsize=(10, 6))
plt.plot(frequency, power)
plt.axvline(best_frequency, color='red', ls='--', label=f'best freq = {best_frequency:.6f}')
plt.xlabel("Frequency (1/days)")
plt.ylabel("Power")
plt.legend()
plt.title("Periodogram (frequency)")
plt.show()


# Plot phased light curve
plt.figure(figsize=(10, 6))
phase = (time / best_period) % 1
plt.scatter([phase, phase + 1], [mag, mag], s=20)
plt.xlabel("Phase")
plt.ylabel("Magnitude")
plt.title("Phased Light Curve")
plt.suptitle(f"Period = {period_days:.6f} days = {hours}h {minutes}m {seconds:.3f}s")
plt.gca().invert_yaxis()
plt.show()