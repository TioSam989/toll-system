"""
Data export utilities
"""

import csv
import json
import os
from datetime import datetime
from typing import Dict, List


class DataExporter:
    """Utility class for exporting toll data"""
    
    def __init__(self, output_dir: str = "data/exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def export_to_csv(self, tariffs: List[Dict], filename: str = None) -> str:
        """Export tariffs to CSV file"""
        if not filename:
            filename = f"portuguese_tolls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if tariffs:
                    fieldnames = tariffs[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(tariffs)
                    
            print(f"✓ CSV exported: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return None
            
    def export_to_json(self, tariffs: List[Dict], filename: str = None) -> str:
        """Export tariffs to JSON file"""
        if not filename:
            filename = f"portuguese_tolls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump({
                    'scraped_at': datetime.now().isoformat(),
                    'total_tariffs': len(tariffs),
                    'tariffs': tariffs
                }, jsonfile, indent=2, ensure_ascii=False)
                
            print(f"✓ JSON exported: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return None
            
    def export_location_data(self, location_data: Dict, filename: str = None) -> str:
        """Export location-based toll data"""
        if not filename:
            filename = f"tolls_by_location_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(location_data, f, indent=2, ensure_ascii=False)
                
            print(f"✓ Location data exported: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error exporting location data: {e}")
            return None