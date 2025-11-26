import glob
import numpy as np
import pandas as pd
from astropy.timeseries import LombScargle
from astropy.time import Time
import matplotlib.pyplot as plt

segements = "data/segments/observations_segment_*.csv"
output_csv = "data/segments_periods.csv"

min_period = 0.25
max_period = 0.35

def analyze_segment(path, nfreq=10000):
    df = pd.read_csv(path, usecols=["jd", "mag", "uncertainty"])
    df = df.dropna().sort_values("jd")
    
    time = df["jd"].to_numpy(dtype=float)
    mag = df["mag"].to_numpy(dtype=float)
    err = df["uncertainty"].to_numpy(dtype=float)

    minimum_frequency = 1.0 / max_period
    maximum_frequency = 1.0 / min_period

    frequency = np.linspace(minimum_frequency, maximum_frequency, nfreq)

    ls = LombScargle(time, mag, err, nterms=3)
    power = ls.power(frequency)

    max_power = np.argmax(power)
    best_frequency = frequency[max_power]
    best_period = 1.0 / best_frequency


    return {
        "start_jd": float(time.min()),
        "end_jd": float(time.max()),
        "best_period_days": float(best_period),
        "best_frequency": float(best_frequency),
    }

files = sorted(glob.glob(segements))
results = []
for file in files:
    res = analyze_segment(file, nfreq=10000)
    results.append(res)
    print(f"period={res['best_period_days']} days, jd={res['start_jd']}")

pd.DataFrame(results).to_csv(output_csv, index=False)