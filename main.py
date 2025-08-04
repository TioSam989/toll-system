#!/usr/bin/env python3

import logging.config
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import LOGGING_CONFIG, DATA_DIR, LOGS_DIR
from src.scrapers.brisa_scraper import BrisaScraper
from src.scrapers.portugal_tolls_scraper import PortugalTollsScraper
from src.parsers.pdf_parser import PDFParser
from src.utils.data_exporter import DataExporter


def setup_directories():
    directories = [DATA_DIR, LOGS_DIR, 'data/pdfs', 'data/parsed', 'data/exports']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def main():
    setup_directories()
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Portuguese Toll Scraper")
    
    exporter = DataExporter()
    pdf_parser = PDFParser()
    all_tariffs = []
    
    try:
        logger.info("Attempting Brisa scraper...")
        brisa_scraper = BrisaScraper()
        brisa_data = brisa_scraper.scrape()
        
        if brisa_data and any('pdf_path' in item for item in brisa_data):
            pdf_path = next(item['pdf_path'] for item in brisa_data if 'pdf_path' in item)
            logger.info(f"Parsing PDF: {pdf_path}")
            
            location_data = pdf_parser.parse_brisa_pdf(pdf_path)
            if location_data:
                pdf_parser.save_parsed_data(location_data)
                exporter.export_location_data(location_data)
                
                for location, routes in location_data.items():
                    for route_data in routes:
                        all_tariffs.append({
                            'route_segment': f"{location}",
                            'vehicle_type': route_data.get('vehicle_class', 'Class 1'),
                            'price': route_data.get('price', '0.00'),
                            'validity_period': '2025',
                            'source': 'Brisa PDF',
                            'scraped_at': route_data.get('scraped_at', '')
                        })
        
        all_tariffs.extend(brisa_data)
        logger.info(f"Brisa scraper completed: {len(brisa_data)} records")
        
    except Exception as e:
        logger.error(f"Brisa scraper failed: {e}")
    
    if not all_tariffs:
        try:
            logger.info("Using fallback: Portugal Tolls scraper...")
            portugal_scraper = PortugalTollsScraper()
            portugal_data = portugal_scraper.scrape()
            all_tariffs.extend(portugal_data)
            logger.info(f"Portugal Tolls scraper completed: {len(portugal_data)} records")
            
        except Exception as e:
            logger.error(f"Portugal Tolls scraper failed: {e}")
    
    if all_tariffs:
        exporter.export_to_csv(all_tariffs)
        exporter.export_to_json(all_tariffs)
        logger.info(f"Successfully processed {len(all_tariffs)} toll records")
        print(f"✓ Scraping completed! {len(all_tariffs)} records processed")
    else:
        logger.warning("No toll data was scraped")
        print("✗ No toll data was scraped")


if __name__ == "__main__":
    main()