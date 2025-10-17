#!/bin/bash

# Portuguese Toll Scraper - Production Runner
# This script activates venv and runs the scraper

# Set script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Log file for cron output
LOG_FILE="$SCRIPT_DIR/data/logs/cron_$(date +%Y%m%d_%H%M%S).log"

# Ensure log directory exists
mkdir -p "$SCRIPT_DIR/data/logs"

echo "$(date): Starting Portuguese Toll Scraper" >> "$LOG_FILE"

# Activate virtual environment
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    echo "$(date): Virtual environment activated" >> "$LOG_FILE"
else
    echo "$(date): ERROR - Virtual environment not found at $SCRIPT_DIR/venv/bin/activate" >> "$LOG_FILE"
    exit 1
fi

# Check if .env exists
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "$(date): ERROR - .env file not found" >> "$LOG_FILE"
    exit 1
fi

# Run the scraper
echo "$(date): Running toll scraper..." >> "$LOG_FILE"
python "$SCRIPT_DIR/main.py" >> "$LOG_FILE" 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    echo "$(date): Toll scraper completed successfully" >> "$LOG_FILE"
else
    echo "$(date): Toll scraper failed with exit code $?" >> "$LOG_FILE"
fi

# Deactivate virtual environment
deactivate

echo "$(date): Script finished" >> "$LOG_FILE"