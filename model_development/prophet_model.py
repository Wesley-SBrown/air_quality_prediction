import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

# Load the processed data
df = pd.read_csv('feature_engineering/processed_engineered_data.csv')

# Convert date_local to datetime
df['date_local'] = pd.to_datetime(df['date_local'])

# Outlier Handling (IQR method)
target = 'PM2.5 - Local Conditions'
Q1 = df[target].quantile(0.25)
Q3 = df[target].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df[target] >= lower_bound) & (df[target] <= upper_bound)]

# Reset index
df = df.reset_index(drop=True)

# Select features
features = ['Region', 'Month', 'Year', 'Carbon monoxide', 'Nitrogen dioxide (NO2)',
            'DayAirTmpAvg (F)', 'DayPrecip (in)',
            'DayRelHumAvg (%)', 'DaySolRadAvg (Ly/day)', 'DayVapPresAvg (mBars)',
            'DayWindRun (MPH)', 'DayWindSpdAvg (MPH)', 'Temp_Range',
            'gis_acres', 'shape__area', 'shape__length', 'duration_days', 'normalized_intensity']

# One-hot encode WindCategory
wind_dummies = pd.get_dummies(df['WindCategory'], prefix='WindCategory')
df = pd.concat([df, wind_dummies], axis=1)

# Add wind category columns to features.
features = features + list(wind_dummies.columns)

# Select target and features
X = df[['date_local', target] + features].copy()

# Rename columns for Prophet
X = X.rename(columns={'date_local': 'ds', target: 'y'})

# Train/Test Split
train_size = int(len(X) * 0.8)
train, test = X[0:train_size], X[train_size:len(X)]

# Prophet Model
model = Prophet()

# Add regressors
for col in features:
    model.add_regressor(col)

model.fit(train)

# Make predictions
future = model.make_future_dataframe(periods=len(test))

for col in features:
    future[col] = df[col]

print(future['Region'].isnull().sum()) #Add this line.
print(future['Region'].head()) #Add this line.

forecast = model.predict(future)

# Evaluate the model
y_true = test['y'].values
y_pred = forecast['yhat'][-len(test):].values

mse = mean_squared_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")