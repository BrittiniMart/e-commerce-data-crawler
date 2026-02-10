"""
Configuration settings for the e-commerce crawler
"""

HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36"
]

PROXIES = [
    None,  # Simulated proxy rotation - add actual proxies here
]

REQUEST_DELAY = 2  # Seconds between requests
MAX_PAGES = 10     # Maximum pages to crawl per search
DB_PATH = "data/ecommerce.db"  # Database file path

# Target websites (simulated)
SITES = {
    "amazon": {
        "base_url": "https://www.amazon.com",
        "search_pattern": "/s?k={keyword}&page={page}"
    },
    "jd": {
        "base_url": "https://www.jd.com",
        "search_pattern": "/search?keyword={keyword}&page={page}"
    }
}