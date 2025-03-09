from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import requests
import requests_cache
import json
import time
from datetime import datetime
import calendar
import os
import csv

# Initialize a cache for requests
session = requests_cache.CachedSession('EPA_air_quality')

# AES key generation - for example, you can save this securely somewhere
key = get_random_bytes(16)  # AES-128 (16 bytes key length)
api_key = "key"  # Replace with your real API key

# Function to check if the year is a leap year
def is_leap_year(year):
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

# Function to get the correct number of days in a month
def get_days_in_month(year, month):
    if month == 2:  # February
        return 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:  # April, June, September, November
        return 30
    else:  # January, March, May, July, August, October, December
        return 31
    
def encrypt_data(data, key):
    """Encrypt the data using AES"""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

def decrypt_data(enc_data, key):
    """Decrypt the data using AES"""
    iv = enc_data[:16]
    ct = enc_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ct), AES.block_size)
    return decrypted_data.decode()

# Encrypt and save the API key (do this once, and store the encrypted data somewhere)
def encrypt_and_save_api_key(api_key, filename='encrypted_api_key.bin'):
    encrypted_key = encrypt_data(api_key, key)
    with open(filename, 'wb') as f:
        f.write(encrypted_key)
    print("API Key encrypted and saved to file.")

# Decrypt and use the API key from file when needed
def decrypt_api_key(filename='encrypted_api_key.bin'):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Encrypted API key file '{filename}' not found. Please encrypt the API key first.")
    
    with open(filename, 'rb') as f:
        encrypted_key = f.read()
    return decrypt_data(encrypted_key, key)

# Example: If you don't have the encrypted file yet, use the following function to encrypt it first:
# Uncomment the line below and run it once to encrypt and save the API key
encrypt_and_save_api_key(f"{api_key}")  # Replace with your real API key

# After encryption, you can now decrypt and use the API key as needed
try:
    EPA_API_KEY = decrypt_api_key()  # Use the decrypted API key
    print("API Key successfully decrypted!")
except FileNotFoundError as e:
    print(str(e))
    # Encrypt and save the API key for the first time
    encrypt_and_save_api_key(f"{api_key}")  # Replace with your real API key
    exit(1)  # Exit the script if the API key is not available

# Retrieve states (using decrypted API key)
email = "email@example.com"
state_endpoint = "https://aqs.epa.gov/data/api/list/states"
param = {"email": f"{email}", "key": EPA_API_KEY}  # Replace with your real email

# Sending request for state data
response = session.get(state_endpoint, params=param)
response.raise_for_status()
states_data = response.json()['Data']
# Transform data into DataFrame for easy manipulation
import pandas as pd
state_df = pd.DataFrame(states_data)
print(state_df.head())

# Function to fetch daily data for a given state and date range
def get_daily_data_by_state(state_code, bdate, edate):
    endpoint = "https://aqs.epa.gov/data/api/dailyData/byState"
    param = {
        "email": f"{email}",  # Replace with your email
        "key": EPA_API_KEY,
        "state": state_code,
        "param": "88101,42101,42602,42102,44201",  # Example parameters
        "bdate": bdate,
        "edate": edate,
    }

    # Make the API request
    response = session.get(endpoint, params=param)
    if response.status_code == 400:  # Bad Request (likely due to an invalid date)
        print(f"Error fetching data for {bdate}: {response.status_code} - Invalid date.")
        return None
    elif response.status_code == 429:  # Rate limit error (too many requests)
        print("Rate limit reached. Sleeping for 60 seconds...")
        time.sleep(60)  # Sleep for 60 seconds and retry
        return get_daily_data_by_state(state_code, bdate, edate)  # Retry
    response.raise_for_status()  # Raise other HTTP errors
    return response.json()


# Function to extract specific fields from the API response
def extract_fields(data):
    """
    Extract specific fields from the API response using 'date_local' directly.
    """
    extracted_data = []
    for record in data['Data']:
        extracted_record = {
            'latitude': record.get('latitude'),
            'longitude': record.get('longitude'),
            'parameter': record.get('parameter'),
            'sample_duration': record.get('sample_duration'),
            'pollutant_standard': record.get('pollutant_standard'),
            'date_local': record.get('date_local'),
            'units_of_measure': record.get('units_of_measure'),
            'arithmetic_mean': record.get('arithmetic_mean'),
            'first_max_value': record.get('first_max_value'),
            'state': record.get('state'),
            'city': record.get('city')
        }
        extracted_data.append(extracted_record)
    return extracted_data

# Function to process and collect daily data from a specific state
def process_state_data(state_code, start_year, end_year):
    repository = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):  # Iterate through all months
            days_in_month = get_days_in_month(year, month)  # Get correct days for the month
            for day in range(1, days_in_month + 1):  # Iterate through all days in the month
                try:
                    bdate = f"{year}{month:02d}{day:02d}"
                    edate = bdate  # We're fetching data for a single day
                    data = get_daily_data_by_state(state_code, bdate, edate)
                    if data:  # Only append if valid data is returned
                        extracted_data = extract_fields(data)
                        repository.extend(extracted_data)
                except Exception as e:
                    print(f"Error fetching data for {year}-{month:02d}-{day:02d}: {str(e)}")
                time.sleep(1)  # Avoid hitting API rate limits
    return repository

# Function to save the data to a CSV file
def save_data_to_csv(data, filename='data/Raw_EPA_CA_AQI_Daily(2013_2024).csv'):
    # Open the CSV file for writing
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude', 'parameter', 'sample_duration', 'pollutant_standard', 'date_local',
                      'units_of_measure', 'arithmetic_mean', 'first_max_value',
                      'state', 'city']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header
        for record in data:
            writer.writerow(record)  # Write each record

# Example to process data for California (state_code "06") from 2013 to 2024
california_data = process_state_data("06", 2013, 2024)

# Save the processed data to CSV
save_data_to_csv(california_data)

# Output some of the processed data
print("Processed data saved to CSV successfully!")
