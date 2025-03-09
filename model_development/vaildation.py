import pandas as pd
import numpy as np

def process_engineered_data(input_file, output_file):
    """
    Processes the engineered data, handling missing values, data types, and dropping AQI_Category.
    """

    df = pd.read_csv(input_file)

    # Convert date_local to datetime
    df['date_local'] = pd.to_datetime(df['date_local'])

    # Convert numerical columns to float
    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].astype(float)

    # Impute missing AQI values (example: mean imputation)
    aqi_cols = ['Carbon monoxide', 'Nitrogen dioxide (NO2)', 'Ozone', 'PM2.5 - Local Conditions']
    for col in aqi_cols:
        df[col] = df[col].fillna(df[col].mean())

    # Impute missing fire values with 0.
    fire_cols = ['gis_acres', 'shape__area', 'shape__length', 'duration_days', 'normalized_intensity']
    for col in fire_cols:
        df[col] = df[col].fillna(0)

    # Impute missing meteorological values with the mean.
    met_cols = [col for col in df.columns if col not in ['date_local', 'Region', 'Month', 'Year', 'Carbon monoxide', 
                                                         'Nitrogen dioxide (NO2)', 'Ozone', 'PM2.5 - Local Conditions', 
                                                         'gis_acres', 'shape__area', 'shape__length', 'duration_days', 
                                                         'WindCategory','normalized_intensity']]
    for col in met_cols:
        if df[col].isnull().any(): # only impute if there are null values.
            df[col] = df[col].fillna(df[col].mean())

    # Drop the AQI_Category column
    df = df.drop(columns=['AQI_Category'])

    # Save to new CSV file
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# Example usage
input_file = 'feature_engineering/engineered_data.csv'  # Replace with your input file name
output_file = 'feature_engineering/processed_engineered_data.csv' # Replace with your desired output file name

process_engineered_data(input_file, output_file)