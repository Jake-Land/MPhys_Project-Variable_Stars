import numpy as np
from astropy.timeseries import LombScargle
import matplotlib.pyplot as plt
import pandas as pd

def lomb_scargle_analysis(t, y, errors, terms=3):
  ls = LombScargle(t, y, dy=errors, fit_mean=True, nterms=terms)
  frequency, power = ls.autopower(minimum_frequency=0.1)
  best_frequency = frequency[np.argmax(power)]
  theta = ls.model_parameters(best_frequency)

  t_fit = np.linspace(min(t), max(t), 1000)
  y_fit = ls.model(t_fit, best_frequency)
 
  return t_fit, y_fit