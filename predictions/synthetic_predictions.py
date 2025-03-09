import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

def generate_synthetic_future_data(data_path, prediction_window, region_filter=None):
    """Generates synthetic future data for a given prediction window and optional region filter."""

    df = pd.read_csv(data_path)
    df['date_local'] = pd.to_datetime(df['date_local'])

    if region_filter:
        df = df[df['Region'] == region_filter]

    last_date = df['date_local'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, prediction_window + 1)]
    future_df = pd.DataFrame({'date_local': future_dates})

    # Generate synthetic values for each feature
    for col in df.columns:
        if col == 'date_local' or col == 'PM2.5 - Local Conditions' or col == 'AQI_Category' or col == 'WindCategory':
            continue  # Skip date, target, and category columns

        if pd.api.types.is_numeric_dtype(df[col]):
            # Example: Use the last known value + some random noise
            last_value = df[col].iloc[-1]
            future_df[col] = last_value + np.random.normal(0, 0.1 * abs(last_value), prediction_window) #add some noise.
        else:
            # Example: Use the most common category
            if col == 'Region':
                if region_filter:
                    future_df[col] = region_filter
                else:
                    future_df[col] = df[col].mode()[0]
            else:
                future_df[col] = df[col].iloc[-1]

    return future_df

def make_predictions_synthetic(model_path, data_path, target_column, features_to_exclude, prediction_window, output_file='predictions.csv', region_filter=None):
    """Makes predictions using synthetic future data and saves them to a file, with optional region filter."""

    # Generate synthetic future data
    future_df = generate_synthetic_future_data(data_path, prediction_window, region_filter)
    future_df.to_csv('predictions/synthetic_predictions.py', index=False) #save the data.

    # Load the trained model
    best_rf = joblib.load(model_path)

    # Load the training data
    df = pd.read_csv(data_path)
    df['date_local'] = pd.to_datetime(df['date_local'])

    if region_filter:
        df = df[df['Region'] == region_filter]

    # Add lagged features
    df['PM2.5_lag1'] = df[target_column].shift(1)

    # Select numeric columns and fill NaNs
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Prepare features and target
    features = [col for col in df.columns if col not in features_to_exclude]
    X = df[features]
    y = df[target_column]

    # Retrain the model on the full dataset
    best_rf.fit(X, y)

    # Prepare future data
    future_df['PM2.5_lag1'] = df[target_column].iloc[-1] #set the first lag value.
    numeric_cols = future_df.select_dtypes(include=['number']).columns
    future_df[numeric_cols] = future_df[numeric_cols].fillna(future_df[numeric_cols].mean())
    future_X = future_df[features]

    # Make predictions
    predictions = best_rf.predict(future_X)

    # Create a DataFrame for predictions
    predictions_df = pd.DataFrame({'date_local': future_df['date_local'], 'predicted_PM2.5': predictions})
    predictions_df.to_csv(output_file, index=False)

    # Visualize predictions
    plt.figure(figsize=(12, 6))
    plt.plot(df['date_local'], df[target_column], label='Actual PM2.5')
    plt.plot(future_df['date_local'], predictions, label='Predicted PM2.5', color='red')
    plt.title(f'PM2.5 Predictions (Synthetic Future Data) - Region: {region_filter if region_filter else "All Regions"}')
    plt.xlabel('Date')
    plt.ylabel('PM2.5')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print a confirmation message
    print(f"Predictions saved to {output_file}")

# Example usage:
model_path = 'model_development/best_random_forest.joblib'
data_path = 'feature_engineering/processed_engineered_data.csv'
target_column = 'PM2.5 - Local Conditions'
features_to_exclude = ['date_local', target_column, 'AQI_Category', 'WindCategory']
prediction_window = 365
output_file = 'predictions/pm25_predictions(2025).csv'
region_to_predict = 1 #select region 1. Set to None for all regions.

make_predictions_synthetic(model_path, data_path, target_column, features_to_exclude, prediction_window, output_file, region_to_predict)