#!/usr/bin/env python3

import json
import os
from datetime import datetime

def export_clean_tolls():
    """Export clean toll data for external import"""
    
    # Read latest MySQL export data
    exports_dir = "data/mysql_exports"
    files = [f for f in os.listdir(exports_dir) if f.startswith('tolls_mysql_') and f.endswith('.json')]
    
    if not files:
        print("No toll data found")
        return
    
    latest_file = max(files)
    file_path = os.path.join(exports_dir, latest_file)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Clean and format data
    clean_tolls = []
    
    for toll in data:
        # Skip page headers and empty data
        if 'Página' in toll['route_segment'] or 'Dominio' in toll['route_segment']:
            continue
            
        # Extract highway from route
        route_parts = toll['route_segment'].split(' ')
        highway = route_parts[0] if route_parts else 'Unknown'
        
        clean_tolls.append({
            "highway": highway,
            "route_segment": toll['route_segment'],
            "vehicle_type": toll['vehicle_type'],
            "price": toll['price'],
            "currency": toll['currency'],
            "validity_period": toll['validity_period'],
            "source": toll['source'],
            "scraped_at": toll['scraped_at'],
            "status": "active"
        })
    
    # Export to simple JSON
    output_file = f"data/toll_import_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(clean_tolls, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(clean_tolls)} toll records to: {output_file}")
    return output_file

if __name__ == "__main__":
    export_clean_tolls()