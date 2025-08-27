#!/usr/bin/env python3
"""
Simple test script to verify the web scraper functionality
"""

import sys
import os

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper_core import WebScraper
import json

def test_basic_scraping():
    """Test basic scraping functionality"""
    print("Testing basic scraping functionality...")
    
    scraper = WebScraper()
    
    try:
        # Test with a simple, public website
        test_url = "https://httpbin.org/html"
        test_selectors = ["h1", "p"]
        
        print(f"Scraping {test_url} with selectors: {test_selectors}")
        
        data = scraper.scrape_page(test_url, test_selectors)
        
        print("Scraped data:")
        print(json.dumps(data, indent=2))
        
        # Test saving to file
        test_output_file = "test_output.json"
        with open(test_output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data saved to {test_output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False
    finally:
        scraper.close()

def test_specific_elements():
    """Test specific element scraping"""
    print("\nTesting specific element scraping...")
    
    scraper = WebScraper()
    
    try:
        test_url = "https://httpbin.org/html"
        element_config = {
            'title': {'selector': 'h1', 'extract': 'text'},
            'content': {'selector': 'p', 'extract': 'text'}
        }
        
        print(f"Scraping {test_url} with element config")
        
        data = scraper.scrape_specific_elements(test_url, element_config)
        
        print("Scraped data:")
        print(json.dumps(data, indent=2))
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False
    finally:
        scraper.close()

def main():
    """Run all tests"""
    print("Web Scraper Test Suite")
    print("=" * 50)
    
    # Test basic scraping
    basic_success = test_basic_scraping()
    
    # Test specific elements
    specific_success = test_specific_elements()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Basic scraping: {'PASS' if basic_success else 'FAIL'}")
    print(f"Specific elements: {'PASS' if specific_success else 'FAIL'}")
    
    if basic_success and specific_success:
        print("\nAll tests passed! The scraper is working correctly.")
        return 0
    else:
        print("\nSome tests failed. Please check the error messages above.")
        return 1

if __name__ == "__main__":
    exit(main())

