from api import GlassnodeAPI
from datetime import datetime
import time
import os
import json

# Initialize API client
api = GlassnodeAPI()

# EDIT THESE PARAMETERS AS NEEDED
# endpoint = "addresses/holder_retention"  

# Generate filename with asset symbol and time interval
# filename = f"{endpoint.replace('/', '_')}_{params['a']}_{params['i']}"

# Change this to your desired metric
bulk_endpoints = [
    "addresses/holder_retention",
    "addresses/holder_retention",
]
params = {
    'a': 'BTC',                 # Asset symbol (BTC, ETH, etc.)
    's': '2020-01-01',          # Start date (YYYY-MM-DD)
    'u': '2023-12-31',          # End date (YYYY-MM-DD)
    'i': '24h',                  # Time interval (1h, 24h, 1w, 1month)
    'f': 'csv'                 # Output format: csv, json
}

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

def fetch_all_endpoints_data():
    # Convert date strings to unix timestamps for 's' and 'u' params
    api_params = params.copy()
    if 's' in api_params:
        api_params['s'] = date_to_timestamp(api_params['s'])
    if 'u' in api_params:
        api_params['u'] = date_to_timestamp(api_params['u'])
    
    failed_endpoints = []
    
    for endpoint_path in bulk_endpoints:
        try:
            print(f"Fetching: {endpoint_path}")
            data = api.fetch_data(endpoint_path, **api_params)
            if data:
                endpoint_filename = f"{endpoint_path.replace('/', '_')}_{params['a']}_{params['i']}"
                save_data(data, endpoint_filename, params['f'])
            else:
                failed_endpoints.append(endpoint_path)
        except Exception as e:
            print(f"Failed {endpoint_path}: {e}")
            failed_endpoints.append(endpoint_path)
        
        # Add delay between API calls to avoid rate limiting
        time.sleep(1)
    
    if failed_endpoints:
        print(f"\nFailed endpoints: {failed_endpoints}")

if __name__ == "__main__":
    """Fetch data from all breakdown endpoints"""
    fetch_all_endpoints_data()