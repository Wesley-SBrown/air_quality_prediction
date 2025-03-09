import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

aqi_df = pd.DataFrame(pd.read_csv('data/cleaned_aqi.csv'))

# Ensure 'Year' column is in integer format
aqi_df['Year'] = aqi_df['Year'].astype(int)

# Filter data for 2013-2023
aqi_filtered = aqi_df[(aqi_df['Year'] >= 2013) & (aqi_df['Year'] <= 2023)]

# Group by Year and Region, taking the mean AQI
aqi_trends = aqi_filtered.groupby(['Year', 'Region'])['arithmetic_mean'].mean().reset_index()

# Set style
sns.set_style("whitegrid")

# Create the plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=aqi_trends, x='Year', y='arithmetic_mean', hue='Region', marker='o', palette='tab10')

# Customize plot
plt.title('Average AQI Trends (2013-2023) by Region', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average AQI', fontsize=12)
plt.legend(title='Region')
plt.xticks(range(2013, 2024))
plt.show()



# Create the boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(data=aqi_filtered, x='Year', y='arithmetic_mean', palette='coolwarm')

# Customize plot
plt.title('AQI Distribution by Year (2013-2023)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('AQI', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()
