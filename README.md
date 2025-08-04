# Portuguese Toll Tariffs Scraper

A professional Python application for scraping Portuguese toll tariffs from official transportation websites.

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

## 🚀 Features

- **Modular Architecture**: Clean separation of concerns
- **Multiple Data Sources**: Brisa Concessao, Portugal Tolls, Infraestruturas de Portugal
- **PDF Processing**: Automatic PDF download and parsing
- **Location-Based Organization**: Toll data organized by highway/location
- **Multiple Export Formats**: CSV, JSON with location grouping
- **Robust Error Handling**: Fallback mechanisms and comprehensive logging
- **Professional Logging**: Structured logging with file output

## 📦 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd toll-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
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
- Chrome browser (for Selenium)
- Internet connection

## 🔒 Legal Notice

This scraper is intended for educational and research purposes. Ensure compliance with website terms of service and robots.txt files before use.

## 📄 License

This project is licensed under the MIT License.