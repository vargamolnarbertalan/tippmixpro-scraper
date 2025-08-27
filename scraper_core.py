import requests
from bs4 import BeautifulSoup
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException

class WebScraper:
    def __init__(self, use_selenium=False, timeout=30, dynamic_wait_timeout=5):
        """
        Initialize the web scraper
        
        Args:
            use_selenium (bool): Whether to use Selenium for JavaScript-heavy pages
            timeout (int): Timeout for requests in seconds
            dynamic_wait_timeout (int): Timeout for waiting for dynamic elements
        """
        self.use_selenium = use_selenium
        self.timeout = timeout
        self.dynamic_wait_timeout = dynamic_wait_timeout
        self.session = requests.Session()
        self.driver = None
        
        # Keep-alive scraping variables
        self.current_url = None
        self.is_page_open = False
        
        # Setup session headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _setup_selenium_driver(self):
        """Setup Selenium WebDriver with Chrome options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            chrome_options.add_argument("--disable-speech-api")
            chrome_options.add_argument("--disable-speech-synthesis-api")
            chrome_options.add_argument("--disable-voice-transcription")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            
            # Try to create driver without specifying service first
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except WebDriverException:
                # If that fails, try with service
                service = Service(log_output=os.devnull)  # Redirect logs to null
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.driver.set_page_load_timeout(self.timeout)
            return True
            
        except Exception as e:
            print(f"Error setting up Selenium driver: {e}")
            return False
    
    def open_page(self, url):
        """
        Open a page and keep it open for keep-alive scraping
        
        Args:
            url (str): The URL to open
        """
        self.current_url = url
        
        if self.use_selenium:
            self._open_page_with_selenium(url)
        else:
            self._open_page_with_requests(url)
        
        self.is_page_open = True
    
    def _open_page_with_requests(self, url):
        """Open page using requests (for static content)"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            self.current_content = response.text
        except Exception as e:
            raise Exception(f"Error opening page with requests: {e}")
    
    def _open_page_with_selenium(self, url):
        """Open page using Selenium (for dynamic content)"""
        try:
            if not self.driver:
                if not self._setup_selenium_driver():
                    raise Exception("Failed to setup Selenium driver")
            
            self.driver.get(url)
            time.sleep(2)  # Wait for page to load
            self.current_content = self.driver.page_source
            
        except Exception as e:
            raise Exception(f"Error opening page with Selenium: {e}")
    
    def refresh_page_content(self):
        """Refresh the page content from the browser (for dynamic updates)"""
        if not self.is_page_open:
            raise Exception("No page is currently open")
        
        if self.use_selenium and self.driver:
            # Get fresh page source from the browser
            self.current_content = self.driver.page_source
        else:
            # For requests-based scraping, make a new request
            try:
                response = self.session.get(self.current_url, timeout=self.timeout)
                response.raise_for_status()
                self.current_content = response.text
            except Exception as e:
                raise Exception(f"Error refreshing page content: {e}")
    

    
    def _wait_for_dynamic_elements(self, selectors, timeout=None):
        """
        Wait for dynamic elements to appear on the page
        
        Args:
            selectors (list): List of CSS selectors to wait for
            timeout (int): Maximum time to wait in seconds (uses self.dynamic_wait_timeout if None)
        """
        if timeout is None:
            timeout = self.dynamic_wait_timeout
        if not self.driver:
            return
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            for selector in selectors:
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                except TimeoutException:
                    print(f"Warning: Selector '{selector}' not found within {timeout} seconds")
        except Exception as e:
            print(f"Error waiting for dynamic elements: {e}")
    
    def scrape_current_page(self, selectors):
        """
        Scrape the currently open page with the given selectors
        
        Args:
            selectors (list): List of CSS selectors to extract
            
        Returns:
            dict: Dictionary with selector as key and extracted data as value
        """
        if not self.is_page_open:
            raise Exception("No page is currently open")
        
        # Get fresh page content from the browser to capture dynamic updates
        if self.use_selenium and self.driver:
            # Get current page source (includes JavaScript updates)
            current_content = self.driver.page_source
        else:
            # For requests-based scraping, use the stored content
            current_content = self.current_content
        
        # Parse the HTML content
        soup = BeautifulSoup(current_content, 'html.parser')
        
        # Extract data for each selector
        data = {}
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    # Extract text from all matching elements
                    extracted_data = []
                    for element in elements:
                        # Get text content, stripping whitespace
                        text = element.get_text(strip=True)
                        if text:
                            extracted_data.append(text)
                    
                    # If we found data, add it to results
                    if extracted_data:
                        if len(extracted_data) == 1:
                            data[selector] = extracted_data[0]
                        else:
                            data[selector] = extracted_data
                    else:
                        data[selector] = None
                else:
                    data[selector] = None
                    
            except Exception as e:
                print(f"Error extracting data for selector '{selector}': {e}")
                data[selector] = None
        
        return data
    
    def close_page(self):
        """Close the currently open page and clean up resources"""
        self.is_page_open = False
        self.current_url = None
        self.current_content = None
        
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    # Legacy methods for backward compatibility
    def scrape_page(self, url, selectors):
        """
        Legacy method: Scrape a page once (opens and closes the page)
        
        Args:
            url (str): The URL to scrape
            selectors (list): List of CSS selectors to extract
            
        Returns:
            dict: Dictionary with selector as key and extracted data as value
        """
        try:
            self.open_page(url)
            data = self.scrape_current_page(selectors)
            return data
        finally:
            self.close_page()
    
    def scrape_specific_elements(self, url, selectors):
        """
        Legacy method: Alias for scrape_page
        
        Args:
            url (str): The URL to scrape
            selectors (list): List of CSS selectors to extract
            
        Returns:
            dict: Dictionary with selector as key and extracted data as value
        """
        return self.scrape_page(url, selectors)
    
    def close(self):
        """Close the scraper and clean up resources"""
        self.close_page()
        if self.session:
            self.session.close()
