import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('data/segments_periods.csv')
df.sort_values(by=['start_jd'], inplace=True)
ref_period = df['best_period_days'].mean()

# O-C in days (difference between segment period and ref period)
df['O-C'] = df['best_period_days'] - ref_period


# plot
plt.figure(figsize=(10, 6))
plt.scatter(df['start_jd'], df['O-C'])

plt.xlabel('Julian Date')
plt.ylabel('O-C (days)')
plt.title(f'O-C diagram (ref period = {ref_period} days)')
plt.grid()
plt.tight_layout()
plt.show()
