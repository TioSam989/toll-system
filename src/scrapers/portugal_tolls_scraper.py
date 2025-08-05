import time
from datetime import datetime
from typing import Dict, List

from selenium.webdriver.common.by import By

from .base_scraper import BaseScraper


class PortugalTollsScraper(BaseScraper):
    
    def __init__(self, headless: bool = True, timeout: int = 15):
        super().__init__(headless, timeout)
        self.base_url = "https://www.portugaltolls.com/en/web/portal-de-portagens/tarifarios"
        
    def scrape(self) -> List[Dict]:
        tariffs = []
        
        try:
            if not self.initialize_driver():
                return []
                
            if not self.navigate_to_page(self.base_url):
                return []
                
            time.sleep(3)
            
            tables = self.driver.find_elements(By.CSS_SELECTOR, "table, .tariff-table, .price-table")
            
            for table in tables:
                try:
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    
                    for row in rows[1:]:
                        cells = row.find_elements(By.TAG_NAME, "td")
                        
                        if len(cells) >= 3:
                            tariff = {
                                'route_segment': cells[0].text.strip(),
                                'vehicle_type': cells[1].text.strip() if len(cells) > 1 else 'Standard',
                                'price': self._clean_price(cells[-2].text.strip()),
                                'validity_period': self._extract_validity(cells[-1].text.strip()),
                                'source': 'Portugal Tolls',
                                'scraped_at': datetime.now().isoformat()
                            }
                            
                            if tariff['route_segment'] and tariff['price']:
                                tariffs.append(tariff)
                                
                except Exception as e:
                    self.logger.warning(f"Error processing table row: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error scraping Portugal Tolls: {e}")
        finally:
            self.cleanup()
            
        return tariffs
        
    def _clean_price(self, price_text: str) -> str:
        if not price_text:
            return ""
            
        price = price_text.strip().replace('€', '').replace('EUR', '').strip()
        
        import re
        match = re.search(r'(\d+[.,]\d+|\d+)', price)
        if match:
            return match.group(1).replace(',', '.')
        
        return price
        
    def _extract_validity(self, validity_text: str) -> str:
        if not validity_text:
            return "Current"
            
        validity_keywords = ['valid', 'until', 'expires', 'current', 'effective']
        
        for keyword in validity_keywords:
            if keyword.lower() in validity_text.lower():
                return validity_text.strip()
                
        return "Current"