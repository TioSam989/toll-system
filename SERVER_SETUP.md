# Portuguese Toll Scraper - Server Setup Guide

## 1. Install WebDriver & Dependencies

### Ubuntu/Debian Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Chrome (recommended)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv xvfb -y
```

### Alternative: Install Chromium
```bash
sudo apt install chromium-browser -y
```

## 2. Check WebDriver Installation

### Verify Chrome Installation
```bash
# Check Chrome version
google-chrome --version

# Check Chrome location
which google-chrome

# Test headless mode
google-chrome --headless --no-sandbox --disable-gpu --dump-dom https://google.com
```

### Verify Chromium Installation
```bash
# Check Chromium version
chromium-browser --version

# Check Chromium location
which chromium-browser
```

## 3. Set Up Python Environment

```bash
# Navigate to project
cd /path/to/toll-system

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit .env file
nano .env
```

**Production .env settings:**
```bash
LARAVEL_API_URL=https://processing.vaisdepop.pt
LARAVEL_API_TOKEN=657f8b8da628ef83cf69101b6817150a
LOG_LEVEL=INFO
```

## 5. Test Installation

### Test API Connection (No Browser Required)
```bash
python test_api.py
```

### Test Full Scraper (Requires Browser)
```bash
python main.py
```

## 6. Check Results

### View Generated Files
```bash
# Check data directories
ls -la data/
ls -la data/exports/
ls -la data/logs/

# View latest scraping log
cat data/logs/toll_scraping_log_*.json | jq '.'

# Check for errors
grep -i "error" data/logs/toll_*.json
```

### Verify API Success
```bash
# Check if API calls succeeded
grep -i "api_success.*true" data/logs/toll_*.json
```

## 7. Troubleshooting

### Browser Issues
```bash
# Clear webdriver cache
rm -rf ~/.wdm

# Test Chrome manually
google-chrome --headless --no-sandbox --disable-gpu --version

# Check for missing dependencies
ldd $(which google-chrome) | grep "not found"
```

### Python Issues
```bash
# Check Python version
python3 --version

# Check installed packages
pip list | grep -E "(selenium|requests|pdfplumber)"

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Permission Issues
```bash
# Make sure directories are writable
chmod 755 data/
chmod 755 data/logs/
chmod 755 data/exports/
```

## 8. Production Deployment

### Set Up Cron Job (Annual Updates)
```bash
# Edit crontab
crontab -e

# Add this line (runs January 1st at midnight)
0 0 1 1 * cd /path/to/toll-system && /path/to/toll-system/venv/bin/activate && python main.py
```

### Monitor Logs
```bash
# View real-time logs
tail -f data/logs/toll_*.json

# Check system logs
journalctl -u cron -f
```

## 9. Expected Output

### Successful Run
```
✓ Scraping completed! X records sent to API
✓ Log saved: data/logs/toll_scraping_log_YYYYMMDD_HHMMSS.json
```

### Failed Run
```
✗ No toll data was scraped. Log: data/logs/toll_error_log_YYYYMMDD_HHMMSS.json
```

## 10. File Structure

```
toll-system/
├── data/
│   ├── exports/           # CSV/JSON exports
│   ├── logs/             # Scraping logs
│   ├── parsed/           # Parsed PDF data
│   └── pdfs/             # Downloaded PDFs
├── src/
│   ├── scrapers/         # Web scrapers
│   ├── parsers/          # PDF parsers
│   └── utils/            # API client & logger
├── main.py              # Main scraper
├── test_api.py          # API test script
├── .env                 # Environment variables
└── requirements.txt     # Python dependencies
```

## 11. Laravel API Endpoint

The scraper sends data to: `PUT /api/tolls/update`

**Required headers:**
- `Authorization: Bearer {token}`
- `Content-Type: application/json`

**Expected response:**
```json
{
  "success": true,
  "message": "Toll data updated successfully",
  "records_updated": 103,
  "updated_at": "2025-09-03T15:07:26.893928Z"
}
```