"""
Flask web application
"""
from flask import Flask, render_template, request, jsonify
import json
from database import get_products
from analysis import analyze_products

app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    """Search products"""
    keyword = request.args.get('keyword', '')
    platform = request.args.get('platform', '')
    
    # Get products from database
    products = get_products(keyword if keyword else None, limit=50)
    
    if platform and platform != 'all':
        products = [p for p in products if p.get('platform') == platform]
    
    # Analyze data
    analysis = analyze_products(products) if products else {}
    
    return render_template('results.html', 
                         products=products[:20],  # Show first 20
                         keyword=keyword,
                         analysis=analysis,
                         total_results=len(products))

@app.route('/api/products', methods=['GET'])
def api_products():
    """API endpoint for products"""
    keyword = request.args.get('keyword', '')
    limit = int(request.args.get('limit', 50))
    
    products = get_products(keyword if keyword else None, limit=limit)
    
    return jsonify({
        "success": True,
        "count": len(products),
        "products": products
    })

@app.route('/api/analyze', methods=['GET'])
def api_analyze():
    """API endpoint for analysis"""
    keyword = request.args.get('keyword', '')
    products = get_products(keyword if keyword else None, limit=100)
    
    analysis = analyze_products(products) if products else {}
    
    return jsonify({
        "success": True,
        "analysis": analysis
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)