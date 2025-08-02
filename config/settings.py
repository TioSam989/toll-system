"""
Configuration settings for the toll scraper
"""

import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Data subdirectories
PDF_DIR = os.path.join(DATA_DIR, 'pdfs')
PARSED_DIR = os.path.join(DATA_DIR, 'parsed')
EXPORTS_DIR = os.path.join(DATA_DIR, 'exports')

# Scraper settings
SCRAPER_SETTINGS = {
    'headless': True,
    'timeout': 15,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Website URLs
URLS = {
    'brisa': 'https://www.brisaconcessao.pt/en/clients/tolls/toll-rates',
    'portugal_tolls': 'https://www.portugaltolls.com/en/web/portal-de-portagens/tarifarios',
    'infraestruturas': 'https://www.infraestruturasdeportugal.pt/pt-pt/rede/rodoviaria/portagens'
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'toll_scraper.log'),
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}