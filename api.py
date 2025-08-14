import os
import requests
from dotenv import load_dotenv

load_dotenv()

class GlassnodeAPI:
    def __init__(self):
        self.api_key = os.getenv('GLASSNODE_API_KEY')
        self.base_url = "https://api.glassnode.com/v1/metrics/"
        
        if not self.api_key:
            raise ValueError("GLASSNODE_API_KEY not found in environment variables")
    
    def fetch_data(self, endpoint, **params):
        """
        Fetch data from Glassnode API
        
        Args:
            endpoint (str): The metric endpoint (e.g., 'addresses/active_count')
            **params: Query parameters like a(asset), s(since), u(until), i(interval), f(output format), etc.
        
        Returns:
            dict: JSON response from API
        """
        url = f"{self.base_url}{endpoint}"
        
        # Add API key to parameters
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Handle both CSV and JSON responses
            if params.get('f') == 'csv':
                return response.text
            else:
                return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
