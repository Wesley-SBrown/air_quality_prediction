import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

met = pd.DataFrame(pd.read_csv('data/cleaned_met.csv'))
aqi = pd.DataFrame(pd.read_csv('data/cleaned_aqi.csv'))


# Define wind categories
bins = [0, 2, 6, np.inf]  # Thresholds for calm, moderate, strong
labels = ['Calm', 'Moderate', 'Strong']

# Create wind category column
met['Wind Category'] = pd.cut(met['DayWindSpdAvg (MPH)'], bins=bins, labels=labels, right=False)

# Group by wind category and compute mean AQI
wind_aqi = aqi.merge(met, left_on=['date_local', 'Region'], right_on=['Date', 'Region'])
wind_aqi_grouped = wind_aqi.groupby('Wind Category')['arithmetic_mean'].mean().reset_index()

# Plot
plt.figure(figsize=(8, 5))
sns.barplot(data=wind_aqi_grouped, x='Wind Category', y='arithmetic_mean', palette='coolwarm')

plt.xlabel('Wind Category')
plt.ylabel('Average AQI')
plt.title('Impact of Wind Speed on AQI (2013-2023)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()


plt.figure(figsize=(8, 5))
sns.scatterplot(data=wind_aqi, x='DayWindSpdAvg (MPH)', y='arithmetic_mean', alpha=0.5, color='blue')

plt.xlabel('Wind Speed (m/s)')
plt.ylabel('AQI')
plt.title('Wind Speed vs. AQI')

plt.grid(linestyle='--', alpha=0.7)
plt.show()


plt.figure(figsize=(8, 5))
sns.scatterplot(data=wind_aqi, x='DayAirTmpAvg (F)', y='arithmetic_mean', alpha=0.5, color='red')

plt.xlabel('Temperature (°F)')
plt.ylabel('AQI')
plt.title('Temperature vs. AQI')

plt.grid(linestyle='--', alpha=0.7)
plt.show()
