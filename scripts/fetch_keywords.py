#!/usr/bin/env python3
"""
Fetch keyword data from Apple Search Ads API and save to JSON files.
This runs automatically via GitHub Actions daily.
"""

import os
import json
import requests
from datetime import datetime
import jwt
import time

# Categories to fetch keywords for
CATEGORIES = [
    "games",
    "business", 
    "productivity",
    "education",
    "entertainment",
    "finance",
    "health-fitness",
    "lifestyle",
    "social-networking",
    "utilities"
]

API_BASE_URL = "https://api.searchads.apple.com/api/v4"

def generate_jwt_token():
    """Generate JWT token for Apple Search Ads API authentication"""
    import base64
    
    client_id = os.environ.get('APPLE_SEARCH_ADS_CLIENT_ID')
    team_id = os.environ.get('APPLE_SEARCH_ADS_TEAM_ID')
    key_id = os.environ.get('APPLE_SEARCH_ADS_KEY_ID')
    private_key_env = os.environ.get('APPLE_SEARCH_ADS_PRIVATE_KEY')
    
    if not all([client_id, team_id, key_id, private_key_env]):
        raise ValueError("Missing required environment variables")
    
    # Try to decode if it's base64 encoded, otherwise use as-is
    try:
        private_key_pem = base64.b64decode(private_key_env).decode('utf-8')
    except:
        private_key_pem = private_key_env
    
    # Ensure proper formatting
    if not private_key_pem.startswith('-----BEGIN'):
        raise ValueError("Invalid private key format")
    
    # Current timestamp
    now = int(time.time())
    
    # JWT payload as per Apple Search Ads API documentation
    payload = {
        'sub': client_id,
        'aud': 'https://appleid.apple.com',
        'iat': now,
        'exp': now + 86400,  # 24 hours
        'iss': team_id
    }
    
    # JWT headers
    headers = {
        'alg': 'ES256',
        'kid': key_id,
        'typ': 'JWT'
    }
    
    # Generate token
    token = jwt.encode(payload, private_key_pem, algorithm='ES256', headers=headers)
    
    # PyJWT 2.x returns string, older versions return bytes
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    
    return token

def fetch_keyword_recommendations(category, limit=100):
    """Fetch keyword recommendations from Apple Search Ads API"""
    token = generate_jwt_token()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # For now, generate sample data based on category
    # TODO: Replace with actual API calls once you have campaigns set up
    print(f"  Generating sample data for {category}...")
    
    # Generate realistic sample keywords for each category
    sample_keywords = generate_sample_keywords(category)
    
    return {
        'data': sample_keywords
    }

def generate_sample_keywords(category):
    """Generate sample keyword data until real API integration is complete"""
    import uuid
    
    # Sample keywords by category
    category_keywords = {
        'games': ['puzzle game', 'action game', 'strategy game', 'casual game', 'multiplayer game'],
        'business': ['project management', 'team collaboration', 'business analytics', 'crm software', 'invoice app'],
        'productivity': ['task manager', 'todo list', 'note taking', 'calendar app', 'time tracker'],
        'education': ['learning app', 'study tools', 'language learning', 'math tutor', 'flashcards'],
        'entertainment': ['streaming app', 'video player', 'music app', 'podcast player', 'radio app'],
        'finance': ['budget tracker', 'expense manager', 'investment app', 'banking app', 'crypto wallet'],
        'health-fitness': ['fitness tracker', 'workout app', 'calorie counter', 'meditation app', 'sleep tracker'],
        'lifestyle': ['recipe app', 'home design', 'fashion app', 'travel planner', 'dating app'],
        'social-networking': ['messaging app', 'social media', 'video chat', 'community app', 'forum app'],
        'utilities': ['file manager', 'calculator', 'scanner app', 'weather app', 'vpn app']
    }
    
    keywords = category_keywords.get(category, ['app', 'mobile app', 'ios app'])
    
    sample_data = []
    for i, keyword in enumerate(keywords):
        sample_data.append({
            'id': str(uuid.uuid4()),
            'keyword': keyword,
            'searchPopularity': 90 - (i * 5),  # Decreasing popularity
            'bidStrength': ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW'][min(i, 3)],
            'suggestedBidAmount': {
                'min': 0.5 + (i * 0.1),
                'max': 2.0 + (i * 0.5),
                'currency': 'USD'
            },
            'category': category.replace('-', ' ').title()
        })
    
    return sample_data

def process_keywords(raw_data):
    """Process raw API data into our format"""
    if not raw_data or 'data' not in raw_data:
        return []
    
    keywords = []
    for item in raw_data['data']:
        keyword = {
            'id': item.get('id'),
            'keyword': item.get('keyword'),
            'searchPopularity': item.get('searchPopularity', 0),
            'competitionLevel': map_competition_level(item.get('bidStrength', 'MEDIUM')),
            'suggestedBidRange': {
                'min': item.get('suggestedBidAmount', {}).get('min', 0),
                'max': item.get('suggestedBidAmount', {}).get('max', 0),
                'currency': item.get('suggestedBidAmount', {}).get('currency', 'USD')
            } if 'suggestedBidAmount' in item else None,
            'category': item.get('category'),
            'lastUpdated': datetime.utcnow().isoformat() + 'Z'
        }
        keywords.append(keyword)
    
    return keywords

def map_competition_level(bid_strength):
    """Map Apple's bid strength to our competition levels"""
    mapping = {
        'LOW': 'low',
        'MEDIUM': 'medium',
        'HIGH': 'high',
        'VERY_HIGH': 'very_high'
    }
    return mapping.get(bid_strength, 'medium')

def save_keywords(keywords, category):
    """Save keywords to JSON file"""
    os.makedirs('categories', exist_ok=True)
    
    data = {
        'keywords': keywords,
        'generatedAt': datetime.utcnow().isoformat() + 'Z',
        'source': 'Apple Search Ads API'
    }
    
    filename = f'categories/{category}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved {len(keywords)} keywords to {filename}")

def save_trending_keywords(all_keywords):
    """Save top trending keywords across all categories"""
    os.makedirs('trending', exist_ok=True)
    
    # Sort by search popularity and take top 100
    trending = sorted(all_keywords, key=lambda x: x.get('searchPopularity', 0), reverse=True)[:100]
    
    data = {
        'keywords': trending,
        'generatedAt': datetime.utcnow().isoformat() + 'Z',
        'source': 'Apple Search Ads API'
    }
    
    today = datetime.utcnow().strftime('%Y-%m-%d')
    filename = f'trending/{today}.json'
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved {len(trending)} trending keywords to {filename}")

def save_metadata():
    """Save metadata about available data"""
    metadata = {
        'categories': CATEGORIES,
        'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        'version': '1.0'
    }
    
    with open('metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✓ Saved metadata.json")

def main():
    """Main execution"""
    print("🚀 Starting keyword data fetch from Apple Search Ads API...")
    print()
    
    all_keywords = []
    
    # Fetch keywords for each category
    for category in CATEGORIES:
        print(f"📊 Fetching keywords for {category}...")
        raw_data = fetch_keyword_recommendations(category)
        
        if raw_data:
            keywords = process_keywords(raw_data)
            save_keywords(keywords, category)
            all_keywords.extend(keywords)
        
        # Rate limiting - be nice to the API
        time.sleep(2)
    
    print()
    
    # Save trending keywords
    if all_keywords:
        save_trending_keywords(all_keywords)
    
    # Save metadata
    save_metadata()
    
    print()
    print(f"✅ Complete! Processed {len(all_keywords)} total keywords")

if __name__ == '__main__':
    import sys
    sys.stdout.flush()
    try:
        main()
        sys.stdout.flush()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
