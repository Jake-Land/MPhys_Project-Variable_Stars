import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

fields = ['jd', 'mag', 'uncertainty']

df = pd.read_csv('data/observations_20251121_124930/observations_20251121_124930.csv', usecols=fields)

df = df.sort_values('jd').reset_index(drop=True)

segments = []
start_index = 0
for i in range(1, len(df)):
    if df.loc[i, 'jd'] - df.loc[i-1, 'jd'] > 1:
        segments.append(df.iloc[start_index:i].copy())
        start_index = i
if start_index < len(df):
    segments.append(df.iloc[start_index:].copy())

for i, seg in enumerate(segments, start=1):
    seg.to_csv(f'data/segments/observations_segment_{i}.csv', index=False)

plt.figure(figsize=(10, 6))
colors = plt.cm.get_cmap('tab10')
for k, seg in enumerate(segments):
    plt.errorbar(seg['jd'], seg['mag'], yerr=seg['uncertainty'], fmt='.', color=colors(k % 10), label=f'segment {k+1}')
plt.xlabel("Julian Date")
plt.ylabel("Magnitude")
plt.title("RZ Cep")
plt.gca().invert_yaxis()
plt.legend()
plt.show()
plt.show()