import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data\\air_quality_prediction\\clean_MET.csv")
stations = ["6", "43", "88", "211", "233"]

#Station as Categorical
df["Station"] = df["Station"].astype(str)

#CSV file with Summary Table Grouped by Station
with open("summary.csv", "w") as f: 
    for num in stations:
        station = df[df["Station"] == num]
        table = station.describe().drop(index=["25%", "50%", "75%"]).round(0)
        
        f.write(f"\nSummary Statistics for Station {num}\n")
        
        table.to_csv(f)

#Boxplots (Before Removing Outliers)
fig, axes = plt.subplots(2,4, figsize=(12, 5))

sns.boxenplot(df, x = "DayAirTmpAvg (F)", ax = axes[0,0])
sns.boxenplot(df, x = "DayDewPnt (F)", ax = axes[1,0])
sns.boxenplot(df, x = "DayPrecip (in)", ax = axes[0,1])
sns.boxenplot(df, x = "DayRelHumAvg (%)", ax = axes[1,1])
sns.boxenplot(df, x = "DaySolRadAvg (Ly/day)", ax = axes[0,2])
sns.boxenplot(df, x = "DayVapPresAvg (mBars)", ax = axes[1,2])
sns.boxenplot(df, x = "DayWindRun (MPH)", ax = axes[0,3])
sns.boxenplot(df, x = "DayWindSpdAvg (MPH)", ax = axes[1,3])

plt.suptitle("Boxplots for Variables (With Outliers)", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

#Removing Outliers using IQR Method

outlier_df = df.drop(columns=["DayPrecip (in)"]) #Not removing outliers for this column

for column in outlier_df.columns[3:]:
    Q1 = np.percentile(df[column].dropna(), 25)
    Q3 = np.percentile(df[column].dropna(), 75)

    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    #15202 rows -> 13412 rows

#Boxplots (After Removing Outliers)
fig, axes = plt.subplots(2,4, figsize=(12, 5))

sns.boxenplot(df, x = "DayAirTmpAvg (F)", ax = axes[0,0])
sns.boxenplot(df, x = "DayDewPnt (F)", ax = axes[1,0])
sns.boxenplot(df, x = "DayPrecip (in)", ax = axes[0,1])
sns.boxenplot(df, x = "DayRelHumAvg (%)", ax = axes[1,1])
sns.boxenplot(df, x = "DaySolRadAvg (Ly/day)", ax = axes[0,2])
sns.boxenplot(df, x = "DayVapPresAvg (mBars)", ax = axes[1,2])
sns.boxenplot(df, x = "DayWindRun (MPH)", ax = axes[0,3])
sns.boxenplot(df, x = "DayWindSpdAvg (MPH)", ax = axes[1,3])

plt.suptitle("Boxplots for Variables (Without Outliers)", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

