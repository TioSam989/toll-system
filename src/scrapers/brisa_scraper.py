import os
import time
from datetime import datetime
from typing import Dict, List

import requests
from selenium.webdriver.common.by import By

from .base_scraper import BaseScraper


class BrisaScraper(BaseScraper):
    
    def __init__(self, headless: bool = True, timeout: int = 15):
        super().__init__(headless, timeout)
        self.base_url = "https://www.brisaconcessao.pt/en/clients/tolls/toll-rates"
        
    def scrape(self) -> List[Dict]:
        try:
            if not self.initialize_driver():
                return []
                
            self.logger.info(f"Navigating to {self.base_url}")
            if not self.navigate_to_page(self.base_url):
                return []
                
            time.sleep(3)
            
            download_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "Click here to download the rates for 2025")
            
            if not download_links:
                download_links = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "download")
                download_links.extend(self.driver.find_elements(By.PARTIAL_LINK_TEXT, "2025"))
                
            if download_links:
                pdf_url = download_links[0].get_attribute('href')
                self.logger.info(f"Found PDF URL: {pdf_url}")
                
                pdf_path = self._download_pdf(pdf_url)
                if pdf_path:
                    return [{
                        'route_segment': 'PDF Downloaded',
                        'vehicle_type': 'All Classes',
                        'price': 'See PDF',
                        'validity_period': '2025',
                        'source': f'Brisa PDF: {os.path.basename(pdf_path)}',
                        'scraped_at': datetime.now().isoformat(),
                        'pdf_path': pdf_path
                    }]
                    
            return []
            
        except Exception as e:
            self.logger.error(f"Error scraping Brisa: {e}")
            return []
        finally:
            self.cleanup()
            
    def _download_pdf(self, pdf_url: str) -> str:
        try:
            response = requests.get(pdf_url)
            
            pdf_dir = 'data/pdfs'
            os.makedirs(pdf_dir, exist_ok=True)
            
            pdf_filename = f"brisa_toll_rates_2025_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
                
            self.logger.info(f"PDF downloaded: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            self.logger.error(f"Error downloading PDF: {e}")
            return None