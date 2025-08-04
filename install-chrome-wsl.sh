#!/bin/bash
# Install Chrome in WSL Kali for Selenium WebDriver

echo "Installing Google Chrome in WSL Kali..."

# Update package list
sudo apt update

# Install wget and dependencies
sudo apt install -y wget gnupg

# Add Google's signing key
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Add Google Chrome repository
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list

# Update package list again
sudo apt update

# Install Google Chrome
sudo apt install -y google-chrome-stable

# Verify installation
google-chrome --version

echo "Chrome installation completed!"
echo "You can now run your Python toll scraper."