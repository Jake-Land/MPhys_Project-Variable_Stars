import pandas as pd
import numpy as np
from datetime import datetime

fields = ['Annu_sum_flux', 'Anulus_in_radius (arcsec)', 'Anulus_out_radius (arcsec)', 'epoch']

L_df = pd.read_csv('data/RZ_Cep_luminance_filter.csv', usecols=fields)

annulus_area = np.pi * (L_df['Anulus_out_radius (arcsec)']**2 - L_df['Anulus_in_radius (arcsec)']**2)
flux_per_arcsec2 = L_df['Annu_sum_flux'] / annulus_area

mag_per_arcsec2 = -2.5 * np.log10(flux_per_arcsec2) + 21  # Assuming zero point of 21 for conversion
print(mag_per_arcsec2.head())