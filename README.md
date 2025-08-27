# Web Scraper Application

A Python-based web scraping application with a graphical user interface that allows you to scrape websites at regular intervals and save the data to JSON files.

## Features

- **Graphical User Interface**: Easy-to-use tkinter-based GUI
- **Dark/Light Mode**: Switch between dark and light themes for comfortable viewing
- **Configurable Scraping**: Set custom CSS selectors for data extraction
- **Keep-Alive Polling**: Opens page once and keeps it open, capturing dynamic content updates at each interval
- **JSON Output**: Save scraped data in structured JSON format with timestamps
- **Settings Persistence**: Remember your configuration between app launches
- **Dual Scraping Methods**: Support for both requests (fast) and Selenium (JavaScript-heavy pages)
- **Real-time Logging**: Monitor scraping progress in real-time
- **Error Handling**: Robust error handling and recovery

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome WebDriver** (only if you plan to use Selenium):
   - Download ChromeDriver from: https://chromedriver.chromium.org/
   - Add it to your system PATH or place it in the project directory

## Usage

### Running the Application

```bash
python scraper_app.py
```

### Basic Usage

1. **Choose Theme**: Select "light" or "dark" mode from the theme dropdown in the top-right corner
2. **Enter Website URL**: Enter the URL of the website you want to scrape
3. **Set Polling Interval**: Choose how often to check for content changes (in seconds)
4. **Choose Output File**: Select where to save the JSON data
5. **Configure Selectors**: Enter CSS selectors for the elements you want to extract
6. **Start Scraping**: Click "Start Scraping" to open the page and begin monitoring
7. **Save Settings**: Click "Save Settings" to manually save your configuration (optional - settings are automatically saved when closing)

**Note**: Your settings (URL, interval, output file, selectors, and theme preference) are automatically remembered when you restart the application.

**How it works**: The scraper opens the page once when you start, then gets fresh page content from the browser at each interval to capture dynamic updates (WebSockets, AJAX, etc.). This ensures you get the latest data without needing to refresh the entire page.

### CSS Selectors Examples

The application uses CSS selectors to identify elements on the webpage:

- `#header` - Selects element with ID "header"
- `.title` - Selects elements with class "title"
- `h1` - Selects all h1 elements
- `div.content p` - Selects paragraph elements inside div with class "content"
- `a[href*="example"]` - Selects links containing "example" in href

### Output Format

The scraped data is saved in JSON format with timestamps. **Note**: The file is overwritten at each polling interval, so it will always contain only the most recent scraped data:

```json
{
  "timestamp": "2024-01-15T10:30:00.123456",
  "data": {
    "#header": [
      {
        "text": "Website Title",
        "attributes": {"id": "header", "class": "main-header"},
        "tag": "div"
      }
    ],
    ".content": [
      {
        "text": "Article content here",
        "attributes": {"class": "content"},
        "tag": "div"
      }
    ]
  }
}
```

## Advanced Usage

### Settings Persistence

The application automatically saves your configuration to `scraper_settings.json` when you close the app. This file contains:

```json
{
  "url": "https://example.com",
  "interval": 60,
  "output_file": "scraped_data.json",
  "selectors": [
    "#header",
    ".content",
    "h1"
  ],
  "theme": "light",
  "dynamic_wait": "2",
  "refresh_content": false
}
```

You can also manually save settings at any time using the "Save Settings" button.

### Using Selenium for JavaScript-heavy Pages

If you need to scrape websites that heavily rely on JavaScript, you can modify the scraper to use Selenium:

```python
# In scraper_app.py, modify the WebScraper initialization:
self.scraper = WebScraper(use_selenium=True)
```

### Custom Scraping Logic

You can extend the `scraper_core.py` file to add custom scraping logic:

```python
# Example: Custom scraping method
def scrape_custom_data(self, url):
    # Your custom scraping logic here
    pass
```

## File Structure

```
tippmixpro-scraper/
├── scraper_app.py          # Main GUI application
├── scraper_core.py         # Core scraping functionality
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── scraper_settings.json  # Settings file (created automatically)
└── scraped_data.json      # Output file (created when scraping)
```

## Dependencies

- **tkinter**: GUI framework (included with Python)
- **requests**: HTTP library for web requests
- **beautifulsoup4**: HTML parsing library
- **selenium**: Web automation (optional, for JavaScript-heavy pages)
- **lxml**: XML/HTML parser

## Troubleshooting

### Common Issues

1. **"No module named 'requests'"**: Install dependencies with `pip install -r requirements.txt`

2. **ChromeDriver not found**: Download ChromeDriver and add to PATH, or place in project directory

3. **Permission errors**: Run the application with appropriate permissions

4. **Website blocking requests**: Some websites may block automated requests. Try:
   - Using Selenium instead of requests
   - Adding delays between requests
   - Using different User-Agent headers

### Error Messages

- **"Error fetching URL"**: Check if the URL is accessible and correct
- **"No elements found for selector"**: Verify your CSS selectors are correct
- **"Timeout error"**: Increase timeout value or check internet connection

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## License

This project is open source and available under the MIT License.

## Disclaimer

Please ensure you comply with the website's terms of service and robots.txt file when scraping. This tool is for educational and legitimate data collection purposes only.
