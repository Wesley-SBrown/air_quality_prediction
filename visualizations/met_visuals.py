import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

met = pd.DataFrame(pd.read_csv('cleaned_met.csv'))

# Convert 'date' column to datetime if not already
met['Date'] = pd.to_datetime(met['Date'])

# Extract Year-Month
met['Year-Month'] = met['Date'].dt.to_period('M')

# Group by Year-Month and compute mean for temperature, humidity, wind speed
met_monthly = met.groupby('Year-Month')[['DayAirTmpAvg (F)', 'DayRelHumAvg (%)', 'DayWindSpdAvg (MPH)']].mean().reset_index()

# Convert Year-Month back to datetime for plotting
met_monthly['Year-Month'] = met_monthly['Year-Month'].astype(str)

# Plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=met_monthly, x='Year-Month', y='DayAirTmpAvg (F)', label='Temperature (°F)', color='r')
sns.lineplot(data=met_monthly, x='Year-Month', y='DayRelHumAvg (%)', label='Humidity (%)', color='b')
sns.lineplot(data=met_monthly, x='Year-Month', y='DayWindSpdAvg (MPH)', label='Wind Speed (m/s)', color='g')

# Adjust x-axis ticks to show every 6 months
plt.xticks(range(0, len(met_monthly), 6), met_monthly['Year-Month'][::6], rotation=45)

plt.xlabel('Year-Month')
plt.ylabel('Average Value')
plt.title('Monthly Trends: Temperature, Humidity, and Wind Speed (2013-2023)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()


# Group by Year-Month and Region, then compute the mean temperature
met_region_monthly = met.groupby(['Year-Month', 'Region'])['DayAirTmpAvg (F)'].mean().reset_index()

# Convert Year-Month back to string for plotting
met_region_monthly['Year-Month'] = met_region_monthly['Year-Month'].astype(str)

# Plot temperature trends per region
plt.figure(figsize=(12, 6))
sns.lineplot(data=met_region_monthly, x='Year-Month', y='DayAirTmpAvg (F)', hue='Region', palette='tab10')

# Adjust x-axis ticks to show every 6 months
plt.xticks(range(0, len(met_region_monthly['Year-Month'].unique()), 6), 
           met_region_monthly['Year-Month'].unique()[::6], rotation=45)

plt.xlabel('Year-Month')
plt.ylabel('Average Temperature (°F)')
plt.title('Temperature Trends by Region (2013-2023)')
plt.legend(title='Region')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()
