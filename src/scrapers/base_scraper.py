import logging
import os
import tempfile
import time
import zipfile
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException


class BaseScraper(ABC):
    
    def __init__(self, headless: bool = True, timeout: int = 10):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def initialize_driver(self) -> bool:
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            temp_dir = tempfile.mkdtemp()
            chrome_options.add_argument(f'--user-data-dir={temp_dir}')
            
            driver_dir = tempfile.mkdtemp()
            url = 'https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.183/linux64/chromedriver-linux64.zip'
            
            response = requests.get(url)
            zip_path = os.path.join(driver_dir, 'chromedriver.zip')
            
            with open(zip_path, 'wb') as f:
                f.write(response.content)
                
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(driver_dir)
                
            for root, dirs, files in os.walk(driver_dir):
                for file in files:
                    if file == 'chromedriver':
                        actual_driver = os.path.join(root, file)
                        os.chmod(actual_driver, 0o755)
                        service = Service(actual_driver)
                        self.driver = webdriver.Chrome(service=service, options=chrome_options)
                        self.wait = WebDriverWait(self.driver, self.timeout)
                        self.logger.info("WebDriver initialized successfully")
                        return True
                        
            raise Exception("ChromeDriver executable not found")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            return False
            
    def navigate_to_page(self, url: str) -> bool:
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self.logger.info(f"Successfully navigated to {url}")
            return True
        except Exception as e:
            self.logger.error(f"Error navigating to {url}: {e}")
            return False
            
    def cleanup(self):
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {e}")
                
    @abstractmethod
    def scrape(self) -> List[Dict]:
        pass