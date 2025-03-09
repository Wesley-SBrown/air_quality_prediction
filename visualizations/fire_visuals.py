import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load fire data
fire = pd.read_csv('data/cleaned_fire.csv')

# Ensure 'year' is an integer
fire['year'] = fire['year'].astype(int)

# Filter years within the range 2013-2023
fire = fire[(fire['year'] >= 2013) & (fire['year'] <= 2023)]

# Count fire occurrences per year
fire_counts = fire['year'].value_counts().sort_index().reset_index()
fire_counts.columns = ['year', 'Fire Count']

# Plot Fire Occurrences Per Year
plt.figure(figsize=(10, 5))
sns.lineplot(data=fire_counts, x='year', y='Fire Count', marker='o', color='firebrick')

plt.xlabel('Year')
plt.ylabel('Number of Fires')
plt.title('Fire Occurrences Per Year (2013-2023)')
plt.xticks(range(2013, 2024))
plt.grid(linestyle='--', alpha=0.7)

plt.show()

# Histogram of Fire Sizes
plt.figure(figsize=(10, 5))
sns.histplot(fire['gis_acres'], bins=30, kde=True, color='orange')

plt.xlabel('Fire Size (Acres)')
plt.ylabel('Frequency')
plt.title('Distribution of Fire Sizes')

plt.grid(linestyle='--', alpha=0.7)
plt.show()

# Histogram of Fire Intensity
plt.figure(figsize=(10, 5))
sns.histplot(fire['rescaled_intensity'], bins=30, kde=True, color='red')

plt.xlabel('Fire Intensity')
plt.ylabel('Frequency')
plt.title('Distribution of Fire Intensity')

plt.grid(linestyle='--', alpha=0.7)
plt.show()
