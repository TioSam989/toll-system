#!/usr/bin/env python3

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import logging

class TollAPIClient:
    def __init__(self):
        self.api_url = os.getenv('LARAVEL_API_URL')
        self.api_token = os.getenv('LARAVEL_API_TOKEN')
        self.logger = logging.getLogger(__name__)
        
        if not self.api_url or not self.api_token:
            raise ValueError("LARAVEL_API_URL and LARAVEL_API_TOKEN must be set in environment")
    
    def send_toll_data(self, toll_data: List[Dict]) -> Dict[str, Any]:
        """Send toll data to Laravel API via PUT request"""
        
        # Prepare data for API
        api_data = {
            'tolls': toll_data,
            'scraped_at': datetime.now().isoformat(),
            'total_records': len(toll_data)
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            self.logger.info(f"Sending {len(toll_data)} toll records to {self.api_url}")
            
            response = requests.put(
                f"{self.api_url}/api/tolls/update",
                json=api_data,
                headers=headers,
                timeout=60
            )
            
            response.raise_for_status()
            
            result = {
                'success': True,
                'status_code': response.status_code,
                'response': response.json(),
                'records_sent': len(toll_data),
                'sent_at': datetime.now().isoformat()
            }
            
            self.logger.info(f"Successfully sent toll data. Response: {response.status_code}")
            return result
            
        except requests.exceptions.RequestException as e:
            error_result = {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                'response': getattr(e.response, 'text', None) if hasattr(e, 'response') else None,
                'records_sent': 0,
                'sent_at': datetime.now().isoformat()
            }
            
            self.logger.error(f"Failed to send toll data: {e}")
            return error_result
    
    def format_toll_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Format toll data for API"""
        formatted_data = []
        
        for toll in raw_data:
            formatted_toll = {
                'route_segment': toll.get('route_segment', ''),
                'vehicle_type': toll.get('vehicle_type', 'Class 1'),
                'price': self._parse_price(toll.get('price', '0')),
                'currency': toll.get('currency', 'EUR'),
                'validity_period': toll.get('validity_period', '2025'),
                'source': toll.get('source', 'Brisa PDF'),
                'scraped_at': toll.get('scraped_at', datetime.now().isoformat())
            }
            formatted_data.append(formatted_toll)
        
        return formatted_data
    
    def _parse_price(self, price_str: str) -> float:
        """Parse price string to float"""
        if isinstance(price_str, (int, float)):
            return float(price_str)
        
        price_clean = str(price_str).replace('€', '').replace('EUR', '').replace(',', '.').strip()
        try:
            return float(price_clean)
        except ValueError:
            return 0.0