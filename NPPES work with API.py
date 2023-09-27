import json
import csv
import time
import requests
import pandas as pd
import os

def fetchNPIData(url, skip, limit, postal_code, version):
    data = requests.get(f"{url}?postal_code={postal_code}&skip={skip}&limit={limit}&pretty&version={version}")
    return data.json()

def createExcelFile(data):
    # Return the data fetched from the API
    return data

skip = 0
limit = 200

while True:
    api_data = fetchNPIData("https://npiregistry.cms.hhs.gov/api/", skip, limit, 10001, 2.1)
    
    # Check if the fetched data is empty (no more data)
    if not api_data:
        break

    # Filter records with enumeration_date in 2023
    filtered_data = [record for record in api_data['results'] if 'enumeration_date' in record['basic'] and record['basic']['enumeration_date'].startswith('2023')]
    
    if filtered_data:
        df = pd.DataFrame(filtered_data)
        # Give the CSV file Path
        csv_file_path = 'D:\Office\personal code\NPPES work with API/example.csv'
        
        # Check if the CSV file already exists
        if os.path.exists(csv_file_path):
            df.to_csv(csv_file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_file_path, mode='a', header=True, index=False)
    
    skip = limit
    limit = limit + 200