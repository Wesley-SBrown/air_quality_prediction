import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Load the processed data
df = pd.read_csv('feature_engineering/processed_engineered_data.csv')

# Convert date_local to datetime
df['date_local'] = pd.to_datetime(df['date_local'])

# Select features (X) and target variable (y)
features = ['Region', 'Month', 'Year', 'Carbon monoxide', 'Nitrogen dioxide (NO2)', 'Ozone',
            'DayAirTmpAvg (F)', 'DayPrecip (in)',
            'DayRelHumAvg (%)', 'DaySolRadAvg (Ly/day)', 'DayVapPresAvg (mBars)',
            'DayWindRun (MPH)', 'DayWindSpdAvg (MPH)', 'Temp_Range', 'WindCategory',
            'gis_acres', 'shape__area', 'shape__length', 'duration_days', 'normalized_intensity']

target = 'PM2.5 - Local Conditions'  # Example target variable, change as needed.
X = df[features]
y = df[target]

# Handle categorical features (WindCategory) and impute missing values
categorical_features = ['WindCategory']
numerical_features = [col for col in X.columns if col not in categorical_features]

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')) #impute missing values with the mean.
])

transformer = ColumnTransformer(transformers=[
    ('onehot', OneHotEncoder(drop='first'), categorical_features),
    ('numerical', numerical_transformer, numerical_features)
])

X = transformer.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")