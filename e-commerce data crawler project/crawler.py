"""
Web crawler for e-commerce platforms
"""
import requests
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime
from config import HEADERS_LIST, PROXIES, REQUEST_DELAY, MAX_PAGES, SITES

def get_headers():
    """Get random headers for request"""
    return {"User-Agent": random.choice(HEADERS_LIST)}

def simulate_crawl(base_url, keyword, pages=MAX_PAGES, platform="amazon"):
    """
    Simulate crawling for demonstration purposes
    In production, replace with actual website parsing
    """
    products = []
    
    for page in range(1, pages + 1):
        print(f"Crawling {platform} - Page {page} for keyword: {keyword}")
        
        # Simulate request delay
        time.sleep(REQUEST_DELAY)
        
        # Generate mock product data (replace with actual parsing)
        for i in range(1, 21):  # 20 products per page
            product_id = f"{platform}_{keyword}_{page}_{i}"
            
            # Generate realistic mock data
            base_price = random.uniform(50, 2000)
            discount = random.choice([0, 0.1, 0.2, 0.3])
            current_price = round(base_price * (1 - discount), 2)
            original_price = round(base_price, 2) if discount > 0 else None
            
            product = {
                "product_id": product_id,
                "name": f"{keyword.capitalize()} Product {i} - Premium Quality",
                "current_price": current_price,
                "original_price": original_price,
                "rating": round(random.uniform(3.5, 5.0), 1),
                "review_count": random.randint(10, 5000),
                "store": f"{platform.capitalize()} Official Store",
                "platform": platform,
                "category": keyword,
                "image_url": f"https://example.com/images/{product_id}.jpg",
                "attributes": f"{{'brand': 'Demo Brand', 'color': 'Black', 'weight': '1.5kg'}}",
                "crawl_time": datetime.now().isoformat()
            }
            products.append(product)
    
    return products

def crawl_amazon(keyword, pages=MAX_PAGES):
    """Amazon-specific crawler (simulated)"""
    return simulate_crawl(SITES["amazon"]["base_url"], keyword, pages, "amazon")

def crawl_jd(keyword, pages=MAX_PAGES):
    """JD.com-specific crawler (simulated)"""
    return simulate_crawl(SITES["jd"]["base_url"], keyword, pages, "jd")

def crawl_all_platforms(keyword, pages=MAX_PAGES):
    """Crawl all supported platforms"""
    products = []
    
    # Crawl Amazon
    amazon_products = crawl_amazon(keyword, pages)
    products.extend(amazon_products)
    
    # Crawl JD.com
    jd_products = crawl_jd(keyword, pages)
    products.extend(jd_products)
    
    print(f"Total products collected: {len(products)}")
    return products