import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import joblib  # Import joblib


# Load data and prepare features (X) and target (y)
df = pd.read_csv('feature_engineering/processed_engineered_data.csv')

# add lagged features.
df['PM2.5_lag1'] = df['PM2.5 - Local Conditions'].shift(1)

#Select the numeric columns.
numeric_cols = df.select_dtypes(include=['number']).columns

# Fill missing values only in numeric columns.
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

target = 'PM2.5 - Local Conditions'
features = [col for col in df.columns if col not in ['date_local', target,'AQI_Category','WindCategory']]

X = df[features]
y = df[target]

# Define the parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)

# Initialize the Random Forest model
rf = RandomForestRegressor(random_state=42)

# Grid search with time series cross-validation
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=tscv, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)
grid_search.fit(X, y)

# Best model
best_rf = grid_search.best_estimator_

# Make predictions on the test set (or entire dataset for evaluation)
y_pred = best_rf.predict(X)

# Evaluate the model
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print(f"Best Parameters: {grid_search.best_params_}")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Save the model
joblib.dump(best_rf, 'best_random_forest.joblib')
print("Random Forest model saved to best_random_forest.joblib")