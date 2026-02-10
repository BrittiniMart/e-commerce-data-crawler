"""
Database management for e-commerce data
"""
import sqlite3
from config import DB_PATH

def get_connection():
    """Establish database connection"""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Create necessary database tables"""
    conn = get_connection()
    cur = conn.cursor()

    # Products table
    cur.execute('''CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        platform TEXT,
        category TEXT,
        store TEXT,
        image_url TEXT,
        attributes TEXT,
        crawl_time TEXT
    )''')

    # Prices table
    cur.execute('''CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT,
        current_price REAL,
        original_price REAL,
        crawled_at TEXT,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )''')

    # Reviews table
    cur.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id TEXT,
        rating REAL,
        review_count INTEGER,
        sentiment_score REAL,
        crawled_at TEXT,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )''')

    conn.commit()
    conn.close()

def save_product(product_data):
    """Save product data to database"""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Insert or update product
        cur.execute('''INSERT OR REPLACE INTO products 
                      (product_id, name, platform, category, store, image_url, attributes, crawl_time)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (product_data.get('product_id'),
                    product_data.get('name'),
                    product_data.get('platform', 'amazon'),
                    product_data.get('category'),
                    product_data.get('store'),
                    product_data.get('image_url'),
                    str(product_data.get('attributes', {})),
                    product_data.get('crawl_time')))
        
        # Save price history
        if product_data.get('current_price'):
            cur.execute('''INSERT INTO prices (product_id, current_price, original_price, crawled_at)
                          VALUES (?, ?, ?, ?)''',
                       (product_data.get('product_id'),
                        product_data.get('current_price'),
                        product_data.get('original_price'),
                        product_data.get('crawl_time')))
        
        # Save review data
        if product_data.get('rating'):
            cur.execute('''INSERT INTO reviews (product_id, rating, review_count, sentiment_score, crawled_at)
                          VALUES (?, ?, ?, ?, ?)''',
                       (product_data.get('product_id'),
                        product_data.get('rating'),
                        product_data.get('review_count', 0),
                        product_data.get('sentiment_score', 0),
                        product_data.get('crawl_time')))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving product: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_products(keyword=None, limit=100):
    """Retrieve products from database"""
    conn = get_connection()
    cur = conn.cursor()
    
    if keyword:
        cur.execute('''SELECT p.*, pr.current_price, pr.crawled_at as price_time, 
                      r.rating, r.review_count
                      FROM products p
                      LEFT JOIN prices pr ON p.product_id = pr.product_id
                      LEFT JOIN reviews r ON p.product_id = r.product_id
                      WHERE p.name LIKE ? 
                      ORDER BY pr.crawled_at DESC
                      LIMIT ?''', (f'%{keyword}%', limit))
    else:
        cur.execute('''SELECT p.*, pr.current_price, pr.crawled_at as price_time, 
                      r.rating, r.review_count
                      FROM products p
                      LEFT JOIN prices pr ON p.product_id = pr.product_id
                      LEFT JOIN reviews r ON p.product_id = r.product_id
                      ORDER BY pr.crawled_at DESC
                      LIMIT ?''', (limit,))
    
    columns = [description[0] for description in cur.description]
    products = [dict(zip(columns, row)) for row in cur.fetchall()]
    
    conn.close()
    return products