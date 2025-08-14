from api import GlassnodeAPI
from datetime import datetime
import time
import os
import json

# Initialize API client
api = GlassnodeAPI()

# EDIT THESE PARAMETERS AS NEEDED
endpoint = "addresses/holder_retention"  # Change this to your desired metric
params = {
    'a': 'BTC',                 # Asset symbol (BTC, ETH, etc.)
    's': '2020-01-01',          # Start date (YYYY-MM-DD)
    'u': '2023-12-31',          # End date (YYYY-MM-DD)
    'i': '24h',                  # Time interval (1h, 24h, 1w, 1month)
    'f': 'csv'                 # Output format: csv, json
}

# Generate filename with asset symbol and time interval
filename = f"{endpoint.replace('/', '_')}_{params['a']}_{params['i']}"

def date_to_timestamp(date_str):
    """Convert YYYY-MM-DD date string to unix timestamp"""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return int(time.mktime(dt.timetuple()))

def save_data(data, filename, output_format='json'):
    """
    Save data as received from API to downloads directory
    
    Args:
        data: Data to save (already in the format returned by API)
        filename (str): Output filename
        output_format (str): 'json' or 'csv'
    """
    if not data:
        print("Failed to download data")
        return
    
    # Count records properly based on format
    if output_format.lower() == 'csv' and isinstance(data, str):
        # For CSV, count lines minus header
        record_count = len(data.strip().split('\n')) - 1
    else:
        # For JSON, count list items
        record_count = len(data) if isinstance(data, list) else 1
    
    # Create downloads directory if it doesn't exist
    downloads_dir = "downloads"
    os.makedirs(downloads_dir, exist_ok=True)
    
    # Add appropriate file extension
    if output_format.lower() == 'csv':
        full_filename = f"{downloads_dir}/{filename}.csv"
    else:
        full_filename = f"{downloads_dir}/{filename}.json"
    
    try:
        if isinstance(data, str):
            # Data is CSV string from API
            with open(full_filename, 'w') as f:
                f.write(data)
        else:
            # Data is JSON from API
            with open(full_filename, 'w') as f:
                json.dump(data, f, indent=2)
        
        print(f"Data saved to {full_filename}")
        print(f"Successfully downloaded {record_count} records")
        
    except Exception as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    print(f"Fetching data from: {endpoint}")
    
    # Convert date strings to unix timestamps for 's' and 'u' params
    api_params = params.copy()
    if 's' in api_params:
        api_params['s'] = date_to_timestamp(api_params['s'])
    if 'u' in api_params:
        api_params['u'] = date_to_timestamp(api_params['u'])
    
    print(f"API Parameters with timestamps: {api_params}")
    
    # Fetch data
    data = api.fetch_data(endpoint, **api_params)
    
    # Save data
    save_data(data, filename, params['f'])