#!/usr/bin/env python3

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class TollJSONLogger:
    def __init__(self):
        self.output_dir = "data/logs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def log_scraping_result(self, toll_data: List[Dict], api_result: Dict[str, Any]) -> str:
        """Log scraping and API results to JSON file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.output_dir, f"toll_scraping_log_{timestamp}.json")
        
        log_data = {
            'scraping_info': {
                'scraped_at': datetime.now().isoformat(),
                'total_records': len(toll_data),
                'scraping_success': len(toll_data) > 0
            },
            'api_info': {
                'api_success': api_result.get('success', False),
                'status_code': api_result.get('status_code'),
                'records_sent': api_result.get('records_sent', 0),
                'sent_at': api_result.get('sent_at'),
                'error': api_result.get('error'),
                'response': api_result.get('response')
            },
            'toll_data': toll_data
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        return log_file
    
    def log_error(self, error_message: str, error_details: Dict = None) -> str:
        """Log error to JSON file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.output_dir, f"toll_error_log_{timestamp}.json")
        
        error_data = {
            'error_info': {
                'occurred_at': datetime.now().isoformat(),
                'error_message': error_message,
                'error_details': error_details or {}
            },
            'scraping_info': {
                'scraped_at': datetime.now().isoformat(),
                'total_records': 0,
                'scraping_success': False
            },
            'api_info': {
                'api_success': False,
                'records_sent': 0
            }
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, indent=2, ensure_ascii=False)
        
        return log_file