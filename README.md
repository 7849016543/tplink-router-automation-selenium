# tplink-router-automation-selenium
Automated TP-Link Router Configuration using Selenium (PPPoE, WiFi setup, fail-safe retries)


git clone https://github.com/7849016543/tplink-router-automation-selenium.git
cd tplink-router-automation-selenium

pip install -r requirements.txt

🛠️ How This Automation Was Built

This project was built using Python + Selenium WebDriver to automate the complete initial configuration of a TP-Link router.

## Key Steps:
User Input Handling
Script prompts for a WD number
Generates PPPoE credentials dynamically:
Username → WDxxxx
Password → WDxxxx

## Browser Automation Setup
Uses Selenium with Chrome WebDriver
Launches browser and opens router UI (192.168.0.1)

## Initial Router Setup
Detects first-time setup page
Sets admin password automatically
Clicks "Let's Get Started"
## Internet Configuration
Selects PPPoE connection type
Inputs generated credentials

## Wireless Configuration
Sets:
2.4GHz SSID
5GHz SSID
WiFi password

## Handling Unstable UI
Uses:
Explicit waits (WebDriverWait)
Multiple selectors (fallback strategy)
JavaScript click when normal click fails

## Retry Mechanism
Automatically retries on failure
Captures screenshots for debugging

## Final Setup Completion
Skips auto-update step
Completes router setup

**🌐 Chrome & ChromeDriver Compatibility**

This script uses Google Chrome + ChromeDriver.
Check your Chrome version:
Check your Chrome driver verion:

**🚀 Features**
Fully automated TP-Link router setup
Dynamic PPPoE credential generation
Handles UI delays and failures
Retry mechanism with screenshots
Multi-selector fallback strategy
JavaScript fallback clicks
Works with unstable router UI

**🧪 Troubleshooting**
❌ ChromeDriver mismatch
Ensure ChromeDriver version matches Chrome

**❌ Elements not found**
Router UI may differ by firmware version
Update XPath selectors accordingly

**❌ Script timeout**
Increase wait time in:
