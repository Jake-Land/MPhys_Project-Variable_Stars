import matplotlib.pyplot as plt
from find_fit_gradient import mag_at_time
import numpy as np
from curve_fit import curve_fit

def plot_fit(epoch_photometry, epoch_jd, period, band='all', time_jd=None, nterms=5):

    band_map = {'V': 2, 'B': 0, 'R': 1}
    colors = {'V': 'g', 'B': 'b', 'R': 'r'}
    labels = {'V': 'G', 'B': 'BP', 'R': 'RP'}

    current_phase, _, _ = mag_at_time(epoch_photometry, period, epoch_jd, time_jd, band=0)

    fig, ax = plt.subplots(figsize=(10, 6))

    if band == 'all':
        for band_name, band_num in band_map.items():
            t_fit, y_fit, phase, phase_mag, phase_mag_err = curve_fit(
                epoch_photometry, period, band_num, nterms=nterms
            )

            ax.errorbar(
                phase, phase_mag, yerr=phase_mag_err,
                fmt=".", color=colors[band_name],
                label=f"{labels[band_name]} data"
            )
            ax.plot(
                t_fit, y_fit, color="k",
                lw=2, label=f"{labels[band_name]} {nterms}-term fit"
            )

        ax.set_title(f"Lomb–Scargle Fit (nterms={nterms}) - All Bands")

    else:
        if band not in band_map:
            raise ValueError("Band must be 'V', 'B', 'R', or 'all'.")

        band_num = band_map[band]
        t_fit, y_fit, phase, phase_mag, phase_mag_err = curve_fit(
            epoch_photometry, period, band_num, nterms=nterms
        )
        
        ax.errorbar(phase, phase_mag, yerr=phase_mag_err, fmt=".", color=colors[band], label="data")
        ax.plot(t_fit, y_fit, color="black", lw=2, label=f"{nterms}-term fit")
        ax.set_title(f"Lomb–Scargle Fit (nterms={nterms}) - {labels[band]} Band")
    
    ax.vlines([current_phase, current_phase + 1], ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], color='black', linestyle='--', alpha=0.8)
    ax.set_xlabel("Phase")
    ax.set_ylabel("Magnitude")
    ax.invert_yaxis()
    ax.legend()
    plt.tight_layout()
    plt.show()
