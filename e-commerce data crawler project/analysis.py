"""
Data analysis functions
"""
import pandas as pd
import numpy as np
from datetime import datetime

def price_distribution(products):
    """Analyze price distribution"""
    df = pd.DataFrame(products)
    
    if df.empty:
        return {"error": "No data available"}
    
    price_stats = {
        "count": int(len(df)),
        "mean": float(df['current_price'].mean()),
        "median": float(df['current_price'].median()),
        "std": float(df['current_price'].std()),
        "min": float(df['current_price'].min()),
        "max": float(df['current_price'].max()),
        "q25": float(df['current_price'].quantile(0.25)),
        "q75": float(df['current_price'].quantile(0.75))
    }
    
    return price_stats

def sentiment_score(text):
    """Calculate basic sentiment score"""
    positive_words = ["good", "great", "excellent", "love", "best", "perfect", "amazing", "wonderful"]
    negative_words = ["bad", "poor", "terrible", "hate", "worst", "awful", "disappointing"]
    
    if not isinstance(text, str):
        return 0
    
    text_lower = text.lower()
    score = 0
    
    for word in positive_words:
        if word in text_lower:
            score += 1
    
    for word in negative_words:
        if word in text_lower:
            score -= 1
    
    # Normalize score
    return max(-1, min(1, score / 10))

def analyze_products(products):
    """Comprehensive product analysis"""
    df = pd.DataFrame(products)
    
    if df.empty:
        return {"error": "No data available"}
    
    analysis = {
        "price_analysis": price_distribution(products),
        "platform_stats": df['platform'].value_counts().to_dict(),
        "rating_stats": {
            "average": float(df['rating'].mean()),
            "median": float(df['rating'].median()),
            "count": int(df['rating'].count())
        },
        "total_products": len(df)
    }
    
    return analysis