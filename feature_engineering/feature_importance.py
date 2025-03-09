import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_feature_importance(model_path, data_path, target_column, features_to_exclude):
    """
    Analyzes and visualizes feature importance from a trained Random Forest model.

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

    # Get feature importances
    importances = best_rf.feature_importances_
    feature_names = X.columns

    # Create a DataFrame for visualization
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    # Visualize feature importances
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
    plt.title('Random Forest Feature Importance')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.show()

    # Print feature importances
    print("Feature Importances:")
    print(feature_importance_df)

# Example usage:
model_path = 'best_random_forest.joblib'  # Replace with your model's path
data_path = 'processed_engineered_data.csv'  # Replace with your data's path
target_column = 'PM2.5 - Local Conditions'
features_to_exclude = ['date_local', target_column, 'AQI_Category', 'WindCategory']

analyze_feature_importance(model_path, data_path, target_column, features_to_exclude)