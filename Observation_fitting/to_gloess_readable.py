import pandas as pd
import numpy as np
from datetime import datetime

fields = ['time', 'Source_Mag_norm', 'Source_Mag_Error_norm', 'epoch']

B_df = pd.read_csv('data/RZ_Cep_JC_B.csv', usecols=fields)
R_df = pd.read_csv('data/RZ_Cep_JC_R.csv', usecols=fields)
V_df = pd.read_csv('data/RZ_Cep_JC_V.csv', usecols=fields)

def to_gloess_readable(df, filter_name):
    df.Source_Mag_norm
    df.Source_Mag_Error_norm *= -1
    #df = df[df['epoch'] >= 3]

    df['time'] = pd.to_datetime(df['time'])

    df['JD'] = df['time'].apply(lambda ts: ts.to_julian_date())
    df = df.drop('time', axis=1)

    mag_col = 'mag_' + filter_name
    err_col = 'err_' + filter_name
    df.rename(columns={'Source_Mag_norm': mag_col, 'Source_Mag_Error_norm': err_col}, inplace=True)
    df.dropna(subset='JD', inplace=True)

    return df[['JD', mag_col, err_col, 'epoch']]

B_df = to_gloess_readable(B_df, 'B')
R_df = to_gloess_readable(R_df, 'R')
V_df = to_gloess_readable(V_df, 'V')


combined_df = pd.concat([B_df, R_df, V_df])
combined_df.to_csv('data/RZ_Cep_JC_gloess_readable_all_epochs.csv', index=False)