import requests
import time
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
            chrome_options.add_argument("--headless")  # Run in background - DISABLED FOR DEBUGGING
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            chrome_options.add_argument("--disable-speech-api")
            chrome_options.add_argument("--disable-speech-synthesis-api")
            chrome_options.add_argument("--disable-voice-transcription")
            # Add these Chrome options
            chrome_options.add_argument("--silent")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # And use Service with null output
            service = Service(log_output=os.devnull)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
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
        # Convert URL for TippmixPro if needed
        if isinstance(self, TippmixProScraper):
            converted_url = self.convert_tippmixpro_url(url)
            if converted_url != url:
                print(f"URL converted: {url} -> {converted_url}")
            self.current_url = converted_url
        else:
            self.current_url = url
        
        if self.use_selenium:
            self._open_page_with_selenium(self.current_url)
        
        self.is_page_open = True
    
    def _open_page_with_selenium(self, url):
        """Open page using Selenium (for dynamic content)"""
        try:
            if not self.driver:
                if not self._setup_selenium_driver():
                    raise Exception("Failed to setup Selenium driver")
            
            self.driver.get(url)
            #time.sleep(2)  # Wait for page to load

            self.current_content = self.driver.page_source
            
        except Exception as e:
            raise Exception(f"Error opening page with Selenium: {e}")
    
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

class TippmixProScraper(WebScraper):
    """
    Custom scraper specifically for TippmixPro website
    Extracts market titles from .MarketGroupsItem children
    """
    
    def convert_tippmixpro_url(self, original_url):
        """
        Convert TippmixPro URLs from www.tippmixpro.hu to sports2.tippmixpro.hu
        and remove /i/ from the path to bypass CORS limitations
        
        Args:
            original_url (str): Original TippmixPro URL
            
        Returns:
            str: Converted URL for scraping
        """
        try:
            # Parse the URL
            if 'www.tippmixpro.hu' in original_url:
                # Replace www.tippmixpro.hu with sports2.tippmixpro.hu
                converted_url = original_url.replace('www.tippmixpro.hu', 'sports2.tippmixpro.hu')
                
                # Remove /i/ from the path if present
                if '/i/' in converted_url:
                    converted_url = converted_url.replace('/i/', '/')
                if '/elo/' in converted_url:
                    converted_url = converted_url.replace('/elo/', '/')
                
                return converted_url
            else:
                # If it's already a sports2 URL or different format, return as is
                return original_url
                
        except Exception as e:
            print(f"Error converting URL: {e}")
            return original_url

    def get_market_id(self,article_element):
        """
        Extracts the market ID from an <article> element's class attribute without regex.

        :param article_element: Selenium WebElement representing the <article>
        :return: Market ID as string if found, else None
        """
        class_attr = article_element.get_attribute("class")
        if not class_attr:
            return None
        
        for cls in class_attr.split():
            if cls.startswith("Market--Id-"):
                return cls.replace("Market--Id-", "")
        
        return None

    def get_market_part(self,article_element):
        """
        Extracts the market part from an <article> element's class attribute without regex.

        :param article_element: Selenium WebElement representing the <article>
        :return: Market part as string if found, else None
        """
        class_attr = article_element.get_attribute("class")
        if not class_attr:
            return None
        
        for cls in class_attr.split():
            if cls.startswith("Market--Part-"):
                return cls.replace("Market--Part-", "")
        
        return None

    def scrape_market_titles(self):
        try:
            element = WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".MarketGroupsItem"))
            )

            bet_list = []
            articles = element.find_elements(By.CSS_SELECTOR, "article")

            for article in articles:
                # get legend text safely
                legend_text = ""
                try:
                    legend = article.find_element(By.CSS_SELECTOR, ".Market__Legend")
                    legend_text = legend.text.strip()
                except Exception as e:
                    pass  # skip if no legend

                outcomes = article.find_elements(By.CSS_SELECTOR, ".Market__OddsGroupItem")
                outcomes_list = []

                for outcome in outcomes:
                    try:
                        text = outcome.find_element(By.CSS_SELECTOR, ".OddsButton__Text").text.strip()
                        odds = outcome.find_element(By.CSS_SELECTOR, ".OddsButton__Odds").text.strip()  
                        outcomes_list.append({"text": text, "odds": odds})
                    except Exception as e:
                        continue  # skip this outcome if one of the children is missing
                        

                if len(outcomes_list) > 0:
                    bet_list.append({"market_id": self.get_market_id(article), "market_part": self.get_market_part(article), "legend": legend_text, "outcomes": outcomes_list})

            #print(f"bet_list: {bet_list}")
            return bet_list

        except TimeoutException as e:
            print(f"Error in scrape_market_titles: {e}")
            return None

    
    def close(self):
        """Close the scraper and clean up resources"""
        self.close_page()
        if self.session:
            self.session.close()