from astropy.time import Time
import numpy as np

s_time = (Time("2025-10-27 12:30:00"))
e_time = (Time("2025-10-27 13:30:00"))

def observing_score(start_time, end_time, block, score):
    scores = []
    start_time = Time(start_time).jd
    end_time = Time(end_time).jd
    block = block / 1440 # Convert block from minutes to days
    for time in np.arange(start_time, end_time, block):
        scores.append((score(time)))
    return scores
