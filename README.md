# TippmixPro Scraper API by B3RC1

A specialized Python web scraping application designed specifically for extracting betting market data from TippmixPro.hu. Features a modern GUI with dark/light theme support and real-time data monitoring.

## 🎯 **Purpose**

This application is designed to scrape live betting markets from TippmixPro.hu, extracting market titles, odds, and outcomes for specific events. It's optimized for the TippmixPro website structure and handles dynamic content updates automatically.

## ✨ **Features**

- **🎨 Modern GUI**: Clean tkinter interface with dark/light theme switching
- **🔄 Keep-Alive Scraping**: Opens page once and monitors for real-time updates
- **📊 Specialized Data Extraction**: Automatically extracts market titles, odds, and outcomes
- **💾 Settings Persistence**: Remembers your configuration between sessions
- **🔒 URL Validation**: Ensures URLs end with `/all` or `/all/` for proper functionality
- **⚠️ Safety Features**: Confirmation dialog when closing during active scraping
- **📝 Real-time Logging**: Monitor scraping progress with timestamped logs
- **🎯 TippmixPro Optimized**: Custom URL conversion and element targeting

## 🚀 **Installation**

### Download and run the lates `.exe` from releases.

**OR**

### Prerequisites
- Python 3.7+
- Google Chrome browser

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/vargamolnarbertalan/tippmixpro-scraper.git
   cd tippmixpro-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python scraper_app.py
   ```

## 📖 **Usage**

### Getting Started

1. **Launch the Application**: Run `python scraper_app.py`
2. **Enter TippmixPro URL**: Must end with `/all` or `/all/`
   - Example: `https://www.tippmixpro.hu/hu/elo/i/elo-esemenyek/186/coun/vilag/blast-open-fall-closed-qualifier/flyquest-spirit/279204529400057856/all`
3. **Set Polling Interval**: How often to check for updates (in seconds)
4. **Choose Output File**: Where to save the JSON data
5. **Select Theme**: Choose between light and dark mode
6. **Start Scraping**: Click "Start Scraping" to begin monitoring
7. **Save settings**: Click "Save Settings" to manually save settings. The app auto-saves settings, if closed gracefully.

### URL Format Requirements

The application automatically converts TippmixPro URLs:
- **Input**: `https://www.tippmixpro.hu/hu/elo/i/elo-esemenyek/.../all`
- **Converted**: `https://sports2.tippmixpro.hu/hu/elo-esemenyek/.../all`

**Important**: URLs must end with `/all` or `/all/` to be accepted.

### Output Data Structure

The application extracts betting market data in this format:

```json
{
  "timestamp": "2025-09-27 14:30:25",
  "data": [
    {
      "market_id": "12345",
      "market_part": "1",
      "legend": "Match Winner",
      "outcomes": [
        {
          "text": "Team A",
          "odds": "1.85"
        },
        {
          "text": "Team B", 
          "odds": "2.10"
        }
      ]
    }
  ]
}
```

### Data Fields Explained

- **`market_id`**: Unique identifier for the betting market
- **`market_part`**: Part number of the market (such as map 2 round 2)
- **`legend`**: The betting market title/description
- **`outcomes`**: Array of possible outcomes with their odds

## ⚙️ **Configuration**

### Settings File

Settings are automatically saved to `scraper_settings.json`:

```json
{
  "url": "https://www.tippmixpro.hu/hu/elo/i/elo-esemenyek/.../all",
  "interval": 1,
  "output_file": "scraped_data.json",
  "theme": "dark"
}
```

### Theme Options

- **Light Theme**: Clean, bright interface
- **Dark Theme**: Easy on the eyes for extended use


## 🛠️ **Troubleshooting**


1. **"URL must end with '/all' or '/all/'"**
   - Ensure your TippmixPro URL ends correctly
   - Example: `https://www.tippmixpro.hu/.../all`

2. **"No betting options found yet..."**
   - The page may still be loading
   - Check if the URL is correct and accessible
   - Wait for the page to fully load

### Browser Requirements

- **Chrome**: Latest version recommended

## 🔒 **Safety Features**

- **URL Validation**: Prevents invalid URLs from being processed
- **Close Confirmation**: Warns when closing during active scraping
- **Error Recovery**: Graceful handling of network and parsing errors
- **Resource Cleanup**: Proper browser cleanup on exit

## 📝 **Logging**

The application provides real-time logging:
- **Timestamped entries**: All actions are logged with timestamps
- **Error reporting**: Detailed error messages for troubleshooting
- **Progress tracking**: Shows scraping status


## 📄 **License**

This software is not open source. You are not permitted to use, distribute, or modify this software without prior written permission and payment to the creator.
To use this software, you must purchase a license.
For licensing inquiries, please contact: [vargamolnarb@gmail.com].
Unauthorized use is strictly prohibited and may result in legal action.