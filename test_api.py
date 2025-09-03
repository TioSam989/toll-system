#!/usr/bin/env python3

import os
from datetime import datetime
from dotenv import load_dotenv
from src.utils.api_client import TollAPIClient
from src.utils.json_logger import TollJSONLogger

# Load environment variables
load_dotenv()

def test_api_integration():
    """Test API integration with mock toll data"""
    
    # Mock toll data (similar to what scraper would produce)
    mock_toll_data = [
        {
            'route_segment': 'A1 0112: Sta. M. Feira',
            'vehicle_type': 'Class 1',
            'price': 22.85,
            'currency': 'EUR',
            'validity_period': '2025',
            'source': 'Test Data',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'route_segment': 'A2 0211: Coina PV',
            'vehicle_type': 'Class 1', 
            'price': 15.50,
            'currency': 'EUR',
            'validity_period': '2025',
            'source': 'Test Data',
            'scraped_at': datetime.now().isoformat()
        },
        {
            'route_segment': 'A3 0311: Maia pv',
            'vehicle_type': 'Class 1',
            'price': 18.75,
            'currency': 'EUR',
            'validity_period': '2025',
            'source': 'Test Data',
            'scraped_at': datetime.now().isoformat()
        }
    ]
    
    try:
        # Initialize API client
        api_client = TollAPIClient()
        json_logger = TollJSONLogger()
        
        print(f"Testing API integration with: {api_client.api_url}")
        print(f"Using token: {api_client.api_token[:10]}...")
        
        # Format and send data
        formatted_data = api_client.format_toll_data(mock_toll_data)
        api_result = api_client.send_toll_data(formatted_data)
        
        # Log results
        log_file = json_logger.log_scraping_result(mock_toll_data, api_result)
        
        if api_result['success']:
            print(f"✓ Successfully sent {len(mock_toll_data)} test records to API")
            print(f"✓ Response: {api_result['response']}")
            print(f"✓ Log saved: {log_file}")
        else:
            print(f"✗ API request failed: {api_result.get('error')}")
            print(f"✗ Status: {api_result.get('status_code')}")
            print(f"✗ Response: {api_result.get('response')}")
            print(f"✗ Log saved: {log_file}")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")

if __name__ == "__main__":
    test_api_integration()