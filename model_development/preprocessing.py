import pandas as pd
import numpy as np

# Load datasets (assuming they are already loaded as fire, aqi, and met)
fire = pd.DataFrame(pd.read_csv('data/trimmed_perimeters.csv'))
aqi = pd.DataFrame(pd.read_csv('data/trimmed_aqi.csv'))
met = pd.DataFrame(pd.read_csv('data/clean_MET.csv'))

### 1. Handling Missing Values ###
aqi["pollutant_standard"].fillna("Unknown", inplace=True)
fire.drop(columns=["complex_name"], inplace=True)

### 2. Handling Outliers ###
# Remove negative AQI values
aqi["arithmetic_mean"] = aqi["arithmetic_mean"].clip(lower=0)

# Cap extreme values in meteorological dataset
met["DayDewPnt (F)"] = met["DayDewPnt (F)"].clip(lower=-20)
met["DayWindRun (MPH)"] = met["DayWindRun (MPH)"].clip(upper=200)

### 3. Feature Engineering ###
# Convert date columns to datetime
aqi["date_local"] = pd.to_datetime(aqi["date_local"])
fire["alarm_date"] = pd.to_datetime(fire["alarm_date"])

# Extract Month & Year
aqi["Month"] = aqi["date_local"].dt.month
aqi["Year"] = aqi["date_local"].dt.year

# Categorize AQI levels
def categorize_aqi(value):
    if value <= 50:
        return "Good"
    elif value <= 100:
        return "Moderate"
    else:
        return "Unhealthy"
aqi["AQI_Category"] = aqi["arithmetic_mean"].apply(categorize_aqi)

# Compute temperature range
met["Temp_Range"] = met["DayAirTmpMax (F)"] - met["DayAirTmpMin (F)"]

# Define wind categories
bins = [0, 5, 15, 50]
labels = ["Low", "Medium", "High"]
met["WindCategory"] = pd.cut(met["DayWindSpdAvg (MPH)"], bins=bins, labels=labels, include_lowest=True)

# Define fire season based on month
fire["fire_season"] = fire["alarm_date"].dt.month.apply(lambda x: "Fire Season" if 5 <= x <= 10 else "Off Season")

# Normalize fire intensity
fire["normalized_intensity"] = (fire["intensity"] - fire["intensity"].min()) / (fire["intensity"].max() - fire["intensity"].min())

# Save cleaned datasets
aqi.to_csv("data/cleaned_aqi.csv", index=False)
met.to_csv("data/cleaned_met.csv", index=False)
fire.to_csv("data/cleaned_fire.csv", index=False)

print("Preprocessing complete.")
