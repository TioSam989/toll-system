import unittest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.scrapers.brisa_scraper import BrisaScraper
from src.scrapers.portugal_tolls_scraper import PortugalTollsScraper


class TestBrisaScraper(unittest.TestCase):
    
    def setUp(self):
        self.scraper = BrisaScraper(headless=True)
    
    def test_initialization(self):
        self.assertEqual(self.scraper.base_url, "https://www.brisaconcessao.pt/en/clients/tolls/toll-rates")
        self.assertTrue(self.scraper.headless)
        self.assertEqual(self.scraper.timeout, 15)
    
    @patch('src.scrapers.brisa_scraper.requests.get')
    def test_download_pdf(self, mock_get):
        mock_response = Mock()
        mock_response.content = 'fake pdf content'
        mock_get.return_value = mock_response
        
        result = self.scraper._download_pdf('http://example.com/test.pdf')
        
        self.assertIsNotNone(result)
        self.assertTrue(result.endswith('.pdf'))


class TestPortugalTollsScraper(unittest.TestCase):
    
    def setUp(self):
        self.scraper = PortugalTollsScraper(headless=True)
    
    def test_initialization(self):
        self.assertEqual(self.scraper.base_url, "https://www.portugaltolls.com/en/web/portal-de-portagens/tarifarios")
    
    def test_clean_price(self):
        test_cases = [
            ("€22.85", "22.85"),
            ("22,85 EUR", "22.85"),
            ("  €15.50  ", "15.50"),
            ("", ""),
            ("invalid", "invalid")
        ]
        
        for input_price, expected in test_cases:
            with self.subTest(input_price=input_price):
                result = self.scraper._clean_price(input_price)
                self.assertEqual(result, expected)
    
    def test_extract_validity(self):
        test_cases = [
            ("Valid until 2025", "Valid until 2025"),
            ("Current rates", "Current rates"),
            ("", "Current"),
            ("No validity info", "No validity info")
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.scraper._extract_validity(input_text)
                self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()