#!/usr/bin/env python3

import logging.config
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.settings import LOGGING_CONFIG, DATA_DIR, LOGS_DIR
from src.scrapers.brisa_scraper import BrisaScraper
from src.scrapers.portugal_tolls_scraper import PortugalTollsScraper
from src.parsers.pdf_parser import PDFParser
from src.utils.data_exporter import DataExporter
from src.utils.api_client import TollAPIClient
from src.utils.json_logger import TollJSONLogger


def setup_directories():
    directories = [DATA_DIR, LOGS_DIR, 'data/pdfs', 'data/parsed', 'data/exports']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def main():
    setup_directories()
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Portuguese Toll Scraper with API integration")
    
    # Initialize components
    exporter = DataExporter()
    pdf_parser = PDFParser()
    json_logger = TollJSONLogger()
    all_tariffs = []
    api_result = {'success': False}
    
    try:
        # Initialize API client
        api_client = TollAPIClient()
        logger.info(f"API client initialized for: {api_client.api_url}")
        
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
                    if 'Página' not in location and 'Dominio' not in location:
                        all_tariffs.append({
                            'route_segment': location,
                            'vehicle_type': 'Class 1',
                            'price': 0.0,
                            'currency': 'EUR',
                            'validity_period': '2025',
                            'source': 'Brisa PDF',
                            'scraped_at': datetime.now().isoformat()
                        })
        
        logger.info(f"Brisa scraper completed: {len(all_tariffs)} records")
        
        # Fallback to Portugal Tolls scraper if no data
        if not all_tariffs:
            try:
                logger.info("Using fallback: Portugal Tolls scraper...")
                portugal_scraper = PortugalTollsScraper()
                portugal_data = portugal_scraper.scrape()
                all_tariffs.extend(portugal_data)
                logger.info(f"Portugal Tolls scraper completed: {len(portugal_data)} records")
                
            except Exception as e:
                logger.error(f"Portugal Tolls scraper failed: {e}")
        
        # Process results
        if all_tariffs:
            # Export to local files (for logging)
            exporter.export_to_csv(all_tariffs)
            exporter.export_to_json(all_tariffs)
            
            # Format and send to API
            formatted_data = api_client.format_toll_data(all_tariffs)
            api_result = api_client.send_toll_data(formatted_data)
            
            # Log everything to JSON
            log_file = json_logger.log_scraping_result(all_tariffs, api_result)
            
            if api_result['success']:
                logger.info(f"✓ Successfully sent {len(all_tariffs)} records to API")
                print(f"✓ Scraping completed! {len(all_tariffs)} records sent to API")
                print(f"✓ Log saved: {log_file}")
            else:
                logger.error(f"✗ API request failed: {api_result.get('error')}")
                print(f"✗ Scraping completed but API failed. Check log: {log_file}")
        else:
            error_msg = "No toll data was scraped"
            logger.warning(error_msg)
            log_file = json_logger.log_error(error_msg)
            print(f"✗ {error_msg}. Log: {log_file}")
            
    except ValueError as e:
        error_msg = f"Configuration error: {e}"
        logger.error(error_msg)
        log_file = json_logger.log_error(error_msg, {'error_type': 'configuration'})
        print(f"✗ {error_msg}. Log: {log_file}")
        
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logger.error(error_msg)
        log_file = json_logger.log_error(error_msg, {'error_type': 'unexpected'})
        print(f"✗ {error_msg}. Log: {log_file}")


if __name__ == "__main__":
    main()