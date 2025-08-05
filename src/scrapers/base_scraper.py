import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions


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
            
            chrome_paths = [
                '/usr/bin/google-chrome',
                '/usr/bin/google-chrome-stable', 
                '/usr/bin/chromium',
                '/usr/bin/chromium-browser',
                '/snap/bin/chromium',
                '/opt/google/chrome/chrome'
            ]
            
            chrome_binary = None
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    chrome_binary = chrome_path
                    chrome_options.binary_location = chrome_path
                    self.logger.info(f"Found Chrome at: {chrome_path}")
                    break
            
            if chrome_binary:
                system_drivers = ['/usr/bin/chromedriver', '/usr/local/bin/chromedriver']
                driver_path = None
                
                for sys_driver in system_drivers:
                    if os.path.exists(sys_driver):
                        driver_path = sys_driver
                        self.logger.info(f"Using system ChromeDriver: {sys_driver}")
                        break
                
                if driver_path:
                    service = Service(driver_path)
                else:
                    if 'chromium' in chrome_binary:
                        service = Service(ChromeDriverManager(chrome_type="chromium").install())
                    else:
                        service = Service(ChromeDriverManager().install())
                
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                firefox_paths = ['/usr/bin/firefox', '/usr/bin/firefox-esr']
                firefox_binary = None
                
                for firefox_path in firefox_paths:
                    if os.path.exists(firefox_path):
                        firefox_binary = firefox_path
                        self.logger.info(f"Found Firefox at: {firefox_path}")
                        break
                
                if firefox_binary:
                    firefox_options = FirefoxOptions()
                    if self.headless:
                        firefox_options.add_argument('--headless')
                    firefox_options.binary_location = firefox_binary
                    
                    service = Service(GeckoDriverManager().install())
                    self.driver = webdriver.Firefox(service=service, options=firefox_options)
                else:
                    raise Exception("Neither Chrome/Chromium nor Firefox found. Please install a browser.")
            
            self.wait = WebDriverWait(self.driver, self.timeout)
            self.logger.info("WebDriver initialized successfully")
            return True
            
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