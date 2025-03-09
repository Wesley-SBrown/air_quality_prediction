import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import joblib  # For saving and loading the model

def validate_random_forest_model(model_path, data_path, target_column, features_to_exclude):
    """
    Validates a trained Random Forest model using time series cross-validation and a hold-out test set.

    Args:
        model_path (str): Path to the saved Random Forest model.
        data_path (str): Path to the CSV data file.
        target_column (str): Name of the target column.
        features_to_exclude (list): List of feature columns to exclude.
    """

    # Load the trained model
    best_rf = joblib.load(model_path)

    # Load the data
    df = pd.read_csv(data_path)

    # Add lagged features
    df['PM2.5_lag1'] = df[target_column].shift(1)

    # Select numeric columns and fill NaNs
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Prepare features and target
    features = [col for col in df.columns if col not in features_to_exclude]
    X = df[features]
    y = df[target_column]

    # Time Series Split for Validation
    tscv = TimeSeriesSplit(n_splits=5)

    # Validation Loop
    mse_scores = []
    r2_scores = []
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        y_pred = best_rf.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        mse_scores.append(mse)
        r2_scores.append(r2)

    # Overall Validation Metrics
    print("Time Series Cross-Validation Results:")
    print(f"Mean MSE: {pd.Series(mse_scores).mean()}")
    print(f"Mean R-squared: {pd.Series(r2_scores).mean()}")

    # Hold-out Test Set Evaluation (Using the last split as the test set)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    y_pred_test = best_rf.predict(X_test)
    mse_test = mean_squared_error(y_test, y_pred_test)
    r2_test = r2_score(y_test, y_pred_test)

    print("\nHold-out Test Set Results:")
    print(f"Test MSE: {mse_test}")
    print(f"Test R-squared: {r2_test}")

# Example usage:
model_path = 'best_random_forest.joblib'  # Replace with your model's path
data_path = 'feature_engineering/processed_engineered_data.csv'  # Replace with your data's path
target_column = 'PM2.5 - Local Conditions'
features_to_exclude = ['date_local', target_column, 'AQI_Category', 'WindCategory']

validate_random_forest_model(model_path, data_path, target_column, features_to_exclude)