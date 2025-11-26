import numpy as np
import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
import pandas as pd

fields = ['jd', 'mag', 'uncertainty']
RZ_Cep_epochs = pd.read_csv('data/segments/observations_segment_01.csv', usecols=fields)
RZ_Cep_epochs.sort_values(by=['jd'], inplace=True)
RZ_Cep_epochs.dropna(inplace=True)
df = RZ_Cep_epochs.copy()


# Convert to numpy arrays
time = np.asarray(df['jd'], dtype=float)
mag = np.asarray(df['mag'], dtype=float)
err = np.asarray(df['uncertainty'], dtype=float)
min_period = 0.25
max_period = 0.35
minimum_frequency = 1.0 / max_period
maximum_frequency = 1.0 / min_period

# LombScargle
ls = LombScargle(time, mag, err, nterms=3)
frequency, power = ls.autopower(minimum_frequency=minimum_frequency, maximum_frequency=maximum_frequency, samples_per_peak=1000)
best_frequency = frequency[np.argmax(power)]
best_period = 1.0 / best_frequency
# Convert period to hours, minutes, seconds
period_days = best_period
period_hours_total = period_days * 24.0
hours = int(period_hours_total)
minutes = int((period_hours_total - hours) * 60)
seconds = ((period_hours_total - hours) * 60 - minutes) * 60
print(f"Best period: {period_days:.6f} days (freq {best_frequency:} 1/d)")
print(f"Which is: {hours}h {minutes}m {seconds:.3f}s ({period_hours_total:.6f} hours)")


# power vs frequency
plt.figure(figsize=(10, 6))
plt.plot(frequency, power)
plt.axvline(best_frequency, color='red', ls='--', label=f'best freq = {best_frequency:.6f}')
plt.xlabel("Frequency (1/days)")
plt.ylabel("Power")
plt.legend()
plt.title("Periodogram (frequency)")
plt.show()

# light curve
plt.figure(figsize=(10, 6))
phase = (time / best_period) % 1
plt.scatter([phase, phase + 1], [mag, mag], s=20)
plt.xlabel("Phase")
plt.ylabel("Magnitude")
plt.title("Phased Light Curve")
plt.suptitle(f"Period = {period_days:.6f} days = {hours}h {minutes}m {seconds:.3f}s")
plt.gca().invert_yaxis()
plt.show()