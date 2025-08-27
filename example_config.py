# Example configuration and custom scraping logic
# This file demonstrates how to extend the scraper with custom functionality

from scraper_core import WebScraper
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Example 1: Basic scraping configuration
BASIC_CONFIG = {
    'url': 'https://example.com',
    'selectors': [
        'h1',
        '.title',
        '#content',
        'a[href*="article"]'
    ],
    'interval': 300,  # 5 minutes
    'output_file': 'example_data.json'
}

# Example 2: Advanced scraping with custom element configuration
ADVANCED_CONFIG = {
    'url': 'https://news-website.com',
    'element_config': {
        'headlines': {
            'selector': 'h2.article-title',
            'extract': 'text'
        },
        'article_links': {
            'selector': 'a.article-link',
            'extract': 'href'
        },
        'publish_dates': {
            'selector': 'span.publish-date',
            'extract': 'text'
        },
        'images': {
            'selector': 'img.article-image',
            'extract': 'src'
        }
    },
    'interval': 600,  # 10 minutes
    'output_file': 'news_data.json'
}

# Example 3: Custom scraping class for specific website
class NewsScraper(WebScraper):
    def __init__(self):
        super().__init__(use_selenium=False, timeout=30)
    
    def scrape_news_articles(self, url):
        """
        Custom method to scrape news articles with specific structure
        """
        try:
            html_content = self._get_page_content(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            articles = []
            
            # Find all article containers
            article_containers = soup.select('article, .article, .post')
            
            for container in article_containers:
                article_data = {}
                
                # Extract title
                title_elem = container.select_one('h1, h2, h3, .title')
                if title_elem:
                    article_data['title'] = title_elem.get_text(strip=True)
                
                # Extract content
                content_elem = container.select_one('.content, .body, p')
                if content_elem:
                    article_data['content'] = content_elem.get_text(strip=True)
                
                # Extract link
                link_elem = container.select_one('a')
                if link_elem and link_elem.get('href'):
                    article_data['link'] = link_elem.get('href')
                
                # Extract image
                img_elem = container.select_one('img')
                if img_elem and img_elem.get('src'):
                    article_data['image'] = img_elem.get('src')
                
                # Extract date
                date_elem = container.select_one('.date, .published, time')
                if date_elem:
                    article_data['date'] = date_elem.get_text(strip=True)
                
                if article_data:
                    articles.append(article_data)
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping news articles: {e}")
            return []

# Example 4: E-commerce product scraper
class ProductScraper(WebScraper):
    def __init__(self):
        super().__init__(use_selenium=True, timeout=30)  # Use Selenium for dynamic content
    
    def scrape_products(self, url):
        """
        Custom method to scrape product information
        """
        try:
            html_content = self._get_page_content(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            products = []
            
            # Find product containers
            product_containers = soup.select('.product, .item, [data-product]')
            
            for container in product_containers:
                product_data = {}
                
                # Extract product name
                name_elem = container.select_one('.product-name, .title, h3')
                if name_elem:
                    product_data['name'] = name_elem.get_text(strip=True)
                
                # Extract price
                price_elem = container.select_one('.price, .cost, [data-price]')
                if price_elem:
                    product_data['price'] = price_elem.get_text(strip=True)
                
                # Extract image
                img_elem = container.select_one('img')
                if img_elem and img_elem.get('src'):
                    product_data['image'] = img_elem.get('src')
                
                # Extract rating
                rating_elem = container.select_one('.rating, .stars')
                if rating_elem:
                    product_data['rating'] = rating_elem.get_text(strip=True)
                
                # Extract availability
                availability_elem = container.select_one('.stock, .availability')
                if availability_elem:
                    product_data['availability'] = availability_elem.get_text(strip=True)
                
                if product_data:
                    products.append(product_data)
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error scraping products: {e}")
            return []

# Example 5: Social media scraper
class SocialMediaScraper(WebScraper):
    def __init__(self):
        super().__init__(use_selenium=True, timeout=30)
    
    def scrape_posts(self, url):
        """
        Custom method to scrape social media posts
        """
        try:
            html_content = self._get_page_content(url)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            posts = []
            
            # Find post containers
            post_containers = soup.select('.post, .tweet, .status')
            
            for container in post_containers:
                post_data = {}
                
                # Extract post text
                text_elem = container.select_one('.text, .content, p')
                if text_elem:
                    post_data['text'] = text_elem.get_text(strip=True)
                
                # Extract author
                author_elem = container.select_one('.author, .username')
                if author_elem:
                    post_data['author'] = author_elem.get_text(strip=True)
                
                # Extract timestamp
                time_elem = container.select_one('.timestamp, time')
                if time_elem:
                    post_data['timestamp'] = time_elem.get_text(strip=True)
                
                # Extract engagement metrics
                likes_elem = container.select_one('.likes, .favorites')
                if likes_elem:
                    post_data['likes'] = likes_elem.get_text(strip=True)
                
                shares_elem = container.select_one('.shares, .retweets')
                if shares_elem:
                    post_data['shares'] = shares_elem.get_text(strip=True)
                
                if post_data:
                    posts.append(post_data)
            
            return posts
            
        except Exception as e:
            self.logger.error(f"Error scraping social media posts: {e}")
            return []

# Example usage functions
def run_basic_scraping():
    """Example of basic scraping usage"""
    scraper = WebScraper()
    
    try:
        data = scraper.scrape_page(
            BASIC_CONFIG['url'],
            BASIC_CONFIG['selectors']
        )
        
        # Save data
        with open(BASIC_CONFIG['output_file'], 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"Data saved to {BASIC_CONFIG['output_file']}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()

def run_news_scraping():
    """Example of news scraping usage"""
    news_scraper = NewsScraper()
    
    try:
        articles = news_scraper.scrape_news_articles('https://example-news-site.com')
        
        # Save articles
        with open('news_articles.json', 'w') as f:
            json.dump(articles, f, indent=2)
            
        print(f"Scraped {len(articles)} articles")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        news_scraper.close()

def run_product_scraping():
    """Example of product scraping usage"""
    product_scraper = ProductScraper()
    
    try:
        products = product_scraper.scrape_products('https://example-store.com')
        
        # Save products
        with open('products.json', 'w') as f:
            json.dump(products, f, indent=2)
            
        print(f"Scraped {len(products)} products")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        product_scraper.close()

if __name__ == "__main__":
    # Uncomment the function you want to test
    # run_basic_scraping()
    # run_news_scraping()
    # run_product_scraping()
    pass
