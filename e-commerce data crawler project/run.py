"""
Main runner script
"""
from database import create_tables, save_product
from crawler import crawl_all_platforms
import sys

def main():
    """Main execution function"""
    print("=" * 50)
    print("E-commerce Data Crawler System")
    print("=" * 50)
    
    # Create database tables
    print("Creating database tables...")
    create_tables()
    
    # Get search keyword
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = input("Enter search keyword: ").strip()
    
    if not keyword:
        keyword = "laptop"  # Default keyword
    
    # Crawl data
    print(f"\nStarting crawl for keyword: '{keyword}'")
    products = crawl_all_platforms(keyword, pages=5)  # Crawl 5 pages per platform
    
    # Save to database
    print(f"\nSaving {len(products)} products to database...")
    saved_count = 0
    
    for product in products:
        if save_product(product):
            saved_count += 1
    
    print(f"Successfully saved {saved_count} products")
    
    # Analysis
    if products:
        print("\nAnalysis Results:")
        print(f"Total products collected: {len(products)}")
        
        # Calculate average price
        prices = [p['current_price'] for p in products if p.get('current_price')]
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"Average price: ${avg_price:.2f}")
    
    print("\nTo start the web dashboard, run:")
    print("python app.py")
    print("\nThen open: http://localhost:5000")

if __name__ == '__main__':
    main()