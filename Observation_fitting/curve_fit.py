from lombscargle import lomb_scargle_analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fold_lightcurve import fold_lightcurve

fields = ['JD', 'mag_V', 'err_V', 'epoch']
Cep_epoch_photometry = pd.read_csv(f"data/RZ_Cep_JC_gloess_readable_all_epochs.csv", usecols=fields)
Cep_period = 0.3078801283505586
UMa_period = 0.46808109934410064
#UMa_epoch_photometry = pd.read_csv(f"data/RV_UMa_gloess_readable_all_epochs.csv", usecols=fields)
n_terms = 3
current_photometry = Cep_epoch_photometry
current_period = Cep_period

def curve_fit(df ,period, nterms=n_terms, epoch=None):
    fields = ['JD', 'mag_V', 'err_V']
    df.sort_values(by=['JD'], inplace=True)
    df.dropna(inplace=True)

    # Convert to numpy arrays
    time = np.asarray(df['JD'], dtype=float)
    mag = np.asarray(df['mag_V'], dtype=float)
    err = np.asarray(df['err_V'], dtype=float)
    phase, phase_mag, phase_err = fold_lightcurve(time, mag, err, period)
    

    t_fit, y_fit = lomb_scargle_analysis(phase, phase_mag, phase_err, terms=nterms)

    return t_fit, y_fit, phase, phase_mag, phase_err


t_fit, y_fit, phase, phase_mag, phase_mag_err = curve_fit(current_photometry, period=current_period, nterms=n_terms)


global_t_fit, global_y_fit, _, _, _ = curve_fit(current_photometry, period=current_period, nterms=n_terms)

# Plot phase lightcurve
fig, ax = plt.subplots(figsize=(10, 6))

epoch_min = int(current_photometry['epoch'].min())
epoch_max = int(current_photometry['epoch'].max())
epochs = list(range(epoch_min, epoch_max + 1))
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown']

for i, epoch in enumerate(epochs):
    per_epoch_df = current_photometry[current_photometry['epoch'] == epoch].copy()

    # per-epoch phases
    time = np.asarray(per_epoch_df['JD'], dtype=float)
    mag = np.asarray(per_epoch_df['mag_V'], dtype=float)# Assuming zero point of 21 for conversion
    err = np.asarray(per_epoch_df['err_V'], dtype=float)
    phase, phase_mag, phase_mag_err = fold_lightcurve(time, mag, err, current_period)

    color = colors[i]
    ax.errorbar(phase, phase_mag, yerr=phase_mag_err, fmt='.', color=color, label=f"epoch {epoch}")

# plot the Lomb-Scargle fit derived from all epochs
ax.plot(global_t_fit, global_y_fit, color='k', lw=2, ls='--', label='Lomb-Scargle fit (all epochs)')

def days_to_hms(days):
    total_seconds = float(days) * 24.0 * 3600.0
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60.0
    return hours, minutes, seconds

# Print current period in days and H:M:S for clarity
hrs, mins, secs = days_to_hms(current_period)
print(f"Current period: {current_period:.6f} days")
print(f"Which is: {hrs}h {mins}m {secs:.3f}s")

ax.set_title(f"Lomb–Scargle Fit (nterms={n_terms}) - {current_period} days = {hrs}h {mins}m {secs:.3f}s")
ax.set_xlabel("Phase")
ax.set_ylabel("Magnitude")
ax.invert_yaxis()
ax.legend(ncol=2, fontsize='small')
plt.tight_layout()
plt.show()

#fig.savefig("RZ_Cep_JC_phase_diagram.pdf", bbox_inches='tight')
BPO_2025_epoch = 2460997.421527778
BPO_old_period = 0.3086298997995992
monson_Cep_period = 0.30868
monson_Cep_epoch = 2456755.135
BPO_Cep_epoch_old = 2460328.4969055
BPO_Cep_epoch = 2459921.3392968
monson_zeta = -1.420 * 10**(-3) # days / year

epoch_diff = (BPO_2025_epoch - BPO_Cep_epoch) / 365.25 # in years
period_diff = Cep_period - BPO_old_period
monson_period_diff = monson_zeta * epoch_diff
print("epoch difference (years): ", epoch_diff)
p_hrs, p_mins, p_secs = days_to_hms(np.abs(period_diff))
print(f"period change: {p_hrs}h {p_mins}m {p_secs:.3f}s")
m_hrs, m_mins, m_secs = days_to_hms(np.abs(monson_period_diff))
print(f"monson predicted period change: {m_hrs}h {m_mins}m {m_secs:.3f}s")
print("monson predicted period: ", monson_Cep_period + monson_period_diff)
print("calculated zeta: ", period_diff / (epoch_diff / 365.25))