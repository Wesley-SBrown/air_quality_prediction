import pandas as pd

def engineer_features(aqi_file, fire_file, met_file, output_file):
    """
    Performs feature engineering on AQI, fire, and meteorological data.
    """

    aqi_df = pd.read_csv(aqi_file)
    fire_df = pd.read_csv(fire_file)
    met_df = pd.read_csv(met_file)

    # AQI Parameter Combination
    aqi_df['date_local'] = pd.to_datetime(aqi_df['date_local'])
    aqi_grouped = aqi_df.pivot_table(index=['date_local', 'Region', 'Month', 'Year', 'AQI_Category'],
                                      columns='parameter',
                                      values='arithmetic_mean').reset_index()
    aqi_grouped = aqi_grouped.rename_axis(None, axis=1)  # Remove column name from 'parameter'

    # Fire Feature Engineering
    fire_df['alarm_date'] = pd.to_datetime(fire_df['alarm_date'])
    fire_df['cont_date'] = pd.to_datetime(fire_df['cont_date'])
    fire_df['duration_days'] = fire_df['duration_days'].astype(float)
    fire_df['month'] = fire_df['alarm_date'].dt.month

    fire_agg = fire_df.groupby(['month', 'Region'])[['gis_acres', 'shape__area', 'shape__length', 'duration_days', 'normalized_intensity']].mean().reset_index()

    # Meteorological Feature Engineering
    met_df['Date'] = pd.to_datetime(met_df['Date'])
    met_df['month'] = met_df['Date'].dt.month
    met_df = met_df.drop('Station', axis=1) #Drop the station column.
    met_df = met_df.drop('ZipCodes', axis=1) #Drop the ZipCodes column.

    # Merge AQI and Meteorological Data
    aqi_met = pd.merge(aqi_grouped, met_df, left_on=['date_local', 'Region'], right_on=['Date', 'Region'], how='left')

    # Merge Fire Data
    aqi_met_fire = pd.merge(aqi_met, fire_agg, on=['month', 'Region'], how='left')

    # Data Cleaning and Finalization
    aqi_met_fire = aqi_met_fire.drop(columns=['Date', 'month'])

    # Save to CSV
    aqi_met_fire.to_csv(output_file, index=False)
    print(f"{output_file} saved successfully!")

# Example usage
aqi_file = 'data/cleaned_aqi.csv'
fire_file = 'data/cleaned_fire.csv'
met_file = 'data/cleaned_met.csv'
output_file = 'engineered_data.csv'

engineer_features(aqi_file, fire_file, met_file, output_file)