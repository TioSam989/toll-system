# Portuguese Toll Tariffs Scraper

Python application for scraping Portuguese toll tariffs from official transportation websites.

## 🏗️ Project Structure

```
toll-system/
├── src/                    # Source code
│   ├── scrapers/          # Web scrapers
│   │   ├── base_scraper.py
│   │   ├── brisa_scraper.py
│   │   └── portugal_tolls_scraper.py
│   ├── parsers/           # Data parsers
│   │   └── pdf_parser.py
│   └── utils/             # Utilities
│       └── data_exporter.py
├── config/                # Configuration
│   └── settings.py
├── data/                  # Data storage
│   ├── pdfs/             # Downloaded PDFs
│   ├── parsed/           # Parsed data
│   └── exports/          # Final exports
├── logs/                 # Application logs
├── tests/                # Unit tests
├── main.py              # Main entry point
└── requirements.txt     # Dependencies
```

## Features

- Modular architecture with clean separation of concerns
- Multiple data sources: Brisa Concessao, Portugal Tolls, Infraestruturas de Portugal
- PDF processing with automatic download and parsing
- Location-based organization of toll data
- Export formats: CSV, JSON with location grouping
- Error handling with fallback mechanisms
- Structured logging with file output

## 📦 Installation

1. **Clone the repository**
```bash
git clone <https://github.com/TioSam989/toll-system>
cd toll-system
```

2. **Install Browser Driver (Required for Selenium)**

### For Debian/Ubuntu WSL (Tested & Working):
```bash
# Step 1: Update package repositories
sudo apt update

# Step 2: Install Chromium browser
sudo apt install chromium

# Step 3: Clear any broken webdriver cache
rm -rf ~/.wdm

# Step 4: Install system ChromeDriver (recommended)
sudo apt install chromium-driver

# Step 5: Verify installation
which chromium
/usr/bin/chromedriver --version
```

### Alternative Methods (if above fails):
```bash
# Method 1: Install Chromium via snap
sudo apt install snapd
sudo snap install chromium

# Method 2: Manual Chrome installation
cd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Method 3: Install Firefox as fallback
sudo apt install firefox
```

### For Kali Linux:
```bash
# Kali has limited repositories, use Firefox
sudo apt update
sudo apt install firefox
```

### Troubleshooting:
- If you get "Exec format error", clear webdriver cache: `rm -rf ~/.wdm`
- Script automatically detects Chrome, Chromium, or Firefox
- System drivers are preferred over webdriver-manager downloads

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### Programmatic Usage
```python
from src.scrapers.brisa_scraper import BrisaScraper
from src.parsers.pdf_parser import PDFParser
from src.utils.data_exporter import DataExporter

# Initialize components
scraper = BrisaScraper()
parser = PDFParser()
exporter = DataExporter()

# Scrape data
data = scraper.scrape()

# Export results
exporter.export_to_json(data)
```

## 📊 Output Files

The application generates organized output in the `data/` directory:

- **`data/pdfs/`**: Downloaded PDF files
- **`data/parsed/`**: Parsed toll data organized by location
- **`data/exports/`**: Final CSV and JSON exports
- **`logs/`**: Application logs

### Location-Based JSON Structure
```json
{
  "A1 Lisboa-Porto": [
    {
      "route": "A1 Lisboa-Porto",
      "vehicle_class": "Class 1",
      "price": "22.85",
      "currency": "EUR"
    }
  ]
}
```

## 🔧 Configuration

Modify `config/settings.py` to customize:
- Output directories
- Scraper timeouts
- Website URLs
- Logging configuration

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/
```

### TestCafe E2E Tests (TypeScript)
```bash
# Install dependencies
npm install

# Run all TestCafe tests
npm run test:e2e

# Run tests in headless mode
npm run test:e2e:headless

# Run tests in Firefox
npm run test:e2e:firefox

# Run specific test file
testcafe chrome tests/testcafe/initial-test.ts
```

### CLI Toll Calculator
```bash
# Calculate toll between two addresses
npm run toll-calc "Lisboa" "Porto"
npm run toll-calc "1250-161" "4000-322"
npm run toll-calc "Coimbra" "Aveiro"

# Perfect for Raspberry Pi automation
npm run toll-calc "Your Origin" "Your Destination"
```

## 📝 Logging

Logs are written to:
- Console (INFO level)
- `logs/toll_scraper.log` (INFO level)

## 🛠️ Development

### Adding New Scrapers
1. Create new scraper class inheriting from `BaseScraper`
2. Implement the `scrape()` method
3. Add to main execution flow

### Adding New Parsers
1. Create parser class in `src/parsers/`
2. Implement parsing logic
3. Integrate with data exporter

## 📋 Requirements

- Python 3.7+
- Browser: Chromium (recommended), Chrome, or Firefox
- ChromeDriver or GeckoDriver (auto-installed)
- Internet connection

## 🔒 Legal Notice

This scraper is intended for educational and research purposes. Ensure compliance with website terms of service and robots.txt files before use.

## 📄 License

This project is licensed under the MIT License.