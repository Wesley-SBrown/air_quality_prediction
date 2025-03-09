
import requests
import pandas as pd
import time

api_key = "e11821ce-172c-41ce-a27a-6367972df663"
base_url = "https://et.water.ca.gov/api/data?"


stations = ["6","43","80","87","88","125","211","224","233", "262"]
date_ranges = [
    ("2013-01-01", "2016-12-31"),
    ("2017-01-01", "2020-12-31"),
    ("2021-01-01", "2024-12-31")
]

main_df = []

for station in stations: 
    for start_date, end_date in date_ranges:
        api_url = f"https://et.water.ca.gov/api/data?appKey={api_key}&targets={station}&startDate={start_date}&endDate={end_date}"

        response = requests.get(api_url)
        
        data = response.json()

        records = data["Data"]["Providers"][0]["Records"]
        df = pd.json_normalize(records)
        main_df.append(df)
        
        time.sleep(1)

final_df = pd.concat(main_df, ignore_index=False)

final_df.to_csv("data/Raw_MET_CA(2013_2024).csv", index = False)
print(len(df))