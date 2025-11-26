import matplotlib.pyplot as plt
from find_fit_gradient import mag_at_time
from clean_data import clean_data
import numpy as np
import pandas as pd

UMa_epoch_photometry = pd.read_csv(f"data/RV_UMa_epoch_photometry.csv")
period = 0.4680590552559243 # days

def GLOESS_fit(epoch_photometry, period):
    df = pd.read_csv('data/RV_UMa_gloess_fit.csv')
    df.sort_values(by='phase', inplace=True)
    phase_fit = df['phase'].values
    mag_G = df['mag_G'].values

    fig, ax = plt.subplots(figsize=(10, 6))

    phase, phase_mag, phase_mag_err = clean_data(
            epoch_photometry, period, band=0
    )

    ax.errorbar(phase, phase_mag, yerr=phase_mag_err, fmt=".", color='g', label="data")
    ax.plot(
                phase_fit, mag_G, color="k",
                lw=2, label=f"GLOESS Fit"
            )
    
    ax.set_xlabel("Phase")
    ax.set_ylabel("Magnitude")
    ax.invert_yaxis()
    ax.legend()
    plt.tight_layout()
    plt.show()

GLOESS_fit(UMa_epoch_photometry, period)