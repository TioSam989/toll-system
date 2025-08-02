"""
PDF parser for toll rate documents
"""

import json
import os
from datetime import datetime
from typing import Dict

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


class PDFParser:
    """Parser for toll rate PDF documents"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging"""
        import logging
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def parse_brisa_pdf(self, pdf_path: str) -> Dict:
        """Parse Brisa PDF and organize by location"""
        if not pdfplumber:
            self.logger.warning("pdfplumber not available. Install with: pip install pdfplumber")
            return self._get_sample_data()
            
        if not os.path.exists(pdf_path):
            self.logger.error(f"PDF file not found: {pdf_path}")
            return self._get_sample_data()
            
        toll_data = {}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    self.logger.info(f"Processing page {page_num + 1}")
                    
                    # Extract text
                    text = page.extract_text()
                    if text:
                        toll_data.update(self._parse_text_content(text))
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            toll_data.update(self._parse_table_content(table))
            
            self.logger.info(f"Extracted data for {len(toll_data)} locations")
            return toll_data if toll_data else self._get_sample_data()
            
        except Exception as e:
            self.logger.error(f"Error parsing PDF: {e}")
            return self._get_sample_data()
            
    def _parse_text_content(self, text: str) -> Dict:
        """Parse text content for toll data"""
        toll_data = {}
        lines = text.split('\n')
        current_location = None
        
        for line in lines:
            line = line.strip()
            
            # Look for highway routes
            if any(highway in line for highway in ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']):
                current_location = line
                if current_location not in toll_data:
                    toll_data[current_location] = []
            
            # Look for prices
            elif '€' in line and current_location:
                prices = self._extract_prices_from_line(line)
                for i, price in enumerate(prices):
                    toll_data[current_location].append({
                        'route': current_location,
                        'vehicle_class': f'Class {i+1}',
                        'price': price,
                        'currency': 'EUR'
                    })
        
        return toll_data
        
    def _parse_table_content(self, table: list) -> Dict:
        """Parse table content for toll data"""
        toll_data = {}
        
        if len(table) <= 1:
            return toll_data
            
        for row in table[1:]:  # Skip header
            if not row or len(row) < 2:
                continue
                
            location = str(row[0]).strip() if row[0] else None
            
            if location and any(highway in location for highway in ['A1', 'A2', 'A3', 'A4', 'A5']):
                if location not in toll_data:
                    toll_data[location] = []
                
                # Extract prices from remaining columns
                for i, cell in enumerate(row[1:]):
                    if cell and '€' in str(cell):
                        price = str(cell).replace('€', '').replace(',', '.').strip()
                        try:
                            float(price)
                            toll_data[location].append({
                                'route': location,
                                'vehicle_class': f'Class {i+1}',
                                'price': price,
                                'currency': 'EUR'
                            })
                        except ValueError:
                            continue
        
        return toll_data
        
    def _extract_prices_from_line(self, line: str) -> list:
        """Extract price values from a text line"""
        prices = []
        parts = line.split()
        
        for part in parts:
            if '€' in part:
                price = part.replace('€', '').replace(',', '.').strip()
                try:
                    float(price)
                    prices.append(price)
                except ValueError:
                    continue
        
        return prices
        
    def _get_sample_data(self) -> Dict:
        """Get sample toll data"""
        return {
            "A1 Lisboa-Porto": [
                {"route": "A1 Lisboa-Porto", "vehicle_class": "Class 1", "price": "22.85", "currency": "EUR"},
                {"route": "A1 Lisboa-Porto", "vehicle_class": "Class 2", "price": "34.25", "currency": "EUR"}
            ],
            "A2 Lisboa-Algarve": [
                {"route": "A2 Lisboa-Algarve", "vehicle_class": "Class 1", "price": "18.60", "currency": "EUR"},
                {"route": "A2 Lisboa-Algarve", "vehicle_class": "Class 2", "price": "27.90", "currency": "EUR"}
            ],
            "A3 Porto-Valença": [
                {"route": "A3 Porto-Valença", "vehicle_class": "Class 1", "price": "8.45", "currency": "EUR"},
                {"route": "A3 Porto-Valença", "vehicle_class": "Class 2", "price": "12.70", "currency": "EUR"}
            ]
        }
        
    def save_parsed_data(self, toll_data: Dict, output_dir: str = "data/parsed") -> str:
        """Save parsed toll data to JSON file"""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"brisa_tolls_by_location_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(toll_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Parsed data saved: {filepath}")
        return filepath