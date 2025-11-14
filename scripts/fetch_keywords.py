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
    
    # Expanded keywords by category (50+ per category)
    category_keywords = {
        'games': [
            'puzzle game', 'action game', 'strategy game', 'casual game', 'multiplayer game',
            'rpg game', 'adventure game', 'racing game', 'sports game', 'simulation game',
            'card game', 'board game', 'trivia game', 'word game', 'arcade game',
            'shooter game', 'platformer game', 'fighting game', 'horror game', 'survival game',
            'idle game', 'clicker game', 'match 3 game', 'tower defense', 'battle royale',
            'moba game', 'mmorpg', 'sandbox game', 'roguelike game', 'rhythm game',
            'puzzle solver', 'brain teaser', 'logic game', 'memory game', 'quiz game',
            'kids game', 'family game', 'offline game', 'online game', 'free game',
            'premium game', 'indie game', 'retro game', 'pixel game', '3d game',
            'vr game', 'ar game', 'educational game', 'math game', 'typing game'
        ],
        'business': [
            'project management', 'team collaboration', 'business analytics', 'crm software', 'invoice app',
            'accounting software', 'expense tracking', 'time tracking', 'payroll app', 'hr management',
            'employee scheduling', 'task management', 'workflow automation', 'document management', 'file sharing',
            'video conferencing', 'team chat', 'email client', 'calendar sync', 'meeting scheduler',
            'sales crm', 'lead management', 'customer support', 'help desk', 'ticketing system',
            'inventory management', 'pos system', 'e-commerce platform', 'payment processing', 'billing software',
            'contract management', 'proposal software', 'quote generator', 'business plan', 'financial planning',
            'budget planner', 'cash flow', 'profit tracker', 'roi calculator', 'business dashboard',
            'kpi tracking', 'performance metrics', 'data visualization', 'reporting tool', 'analytics platform',
            'marketing automation', 'email marketing', 'social media management', 'seo tools', 'content management'
        ],
        'productivity': [
            'task manager', 'todo list', 'note taking', 'calendar app', 'time tracker',
            'habit tracker', 'goal setting', 'planner app', 'organizer', 'reminder app',
            'focus timer', 'pomodoro timer', 'time management', 'productivity tracker', 'daily planner',
            'weekly planner', 'monthly planner', 'bullet journal', 'digital notebook', 'note organizer',
            'markdown editor', 'text editor', 'writing app', 'document scanner', 'pdf editor',
            'file manager', 'cloud storage', 'backup app', 'password manager', 'secure notes',
            'clipboard manager', 'launcher app', 'automation app', 'workflow app', 'shortcut app',
            'mind map', 'brainstorming', 'idea organizer', 'project planner', 'kanban board',
            'gtd app', 'eisenhower matrix', 'priority matrix', 'time blocking', 'schedule app',
            'meeting notes', 'voice recorder', 'transcription app', 'ocr app', 'barcode scanner'
        ],
        'education': [
            'learning app', 'study tools', 'language learning', 'math tutor', 'flashcards',
            'vocabulary builder', 'grammar checker', 'spelling app', 'reading app', 'speed reading',
            'comprehension test', 'quiz maker', 'test prep', 'exam practice', 'homework help',
            'tutoring app', 'online courses', 'video lessons', 'interactive learning', 'educational games',
            'kids learning', 'preschool app', 'kindergarten app', 'elementary education', 'high school app',
            'college prep', 'sat prep', 'act prep', 'gre prep', 'gmat prep',
            'language course', 'spanish learning', 'french learning', 'german learning', 'chinese learning',
            'japanese learning', 'korean learning', 'english learning', 'esl app', 'pronunciation guide',
            'science app', 'physics app', 'chemistry app', 'biology app', 'astronomy app',
            'history app', 'geography app', 'world atlas', 'periodic table', 'calculator app'
        ],
        'entertainment': [
            'streaming app', 'video player', 'music app', 'podcast player', 'radio app',
            'movie app', 'tv shows', 'anime app', 'drama app', 'documentary app',
            'music streaming', 'music player', 'audio player', 'equalizer', 'lyrics app',
            'karaoke app', 'music maker', 'beat maker', 'dj app', 'remix app',
            'podcast app', 'audiobook player', 'radio player', 'fm radio', 'internet radio',
            'live streaming', 'video streaming', 'screen recorder', 'video editor', 'photo editor',
            'meme maker', 'gif maker', 'video maker', 'slideshow maker', 'collage maker',
            'drawing app', 'painting app', 'sketch app', 'coloring app', 'art app',
            'comic reader', 'manga reader', 'ebook reader', 'news app', 'magazine app',
            'trivia app', 'joke app', 'prank app', 'magic tricks', 'party games'
        ],
        'finance': [
            'budget tracker', 'expense manager', 'investment app', 'banking app', 'crypto wallet',
            'money manager', 'personal finance', 'financial planner', 'savings tracker', 'debt tracker',
            'bill reminder', 'bill payment', 'split bills', 'expense splitter', 'receipt scanner',
            'tax calculator', 'tax prep', 'tax filing', 'income tracker', 'paycheck calculator',
            'retirement planner', 'investment tracker', 'portfolio manager', 'stock tracker', 'stock market',
            'trading app', 'forex trading', 'crypto trading', 'bitcoin wallet', 'ethereum wallet',
            'nft wallet', 'defi app', 'blockchain app', 'crypto exchange', 'crypto portfolio',
            'loan calculator', 'mortgage calculator', 'interest calculator', 'compound interest', 'roi calculator',
            'net worth tracker', 'asset manager', 'wealth tracker', 'financial goals', 'money goals',
            'credit score', 'credit monitoring', 'identity protection', 'fraud alert', 'secure banking'
        ],
        'health-fitness': [
            'fitness tracker', 'workout app', 'calorie counter', 'meditation app', 'sleep tracker',
            'exercise app', 'gym workout', 'home workout', 'yoga app', 'pilates app',
            'running app', 'walking app', 'cycling app', 'swimming app', 'hiking app',
            'step counter', 'pedometer', 'activity tracker', 'heart rate monitor', 'blood pressure',
            'weight tracker', 'bmi calculator', 'body fat calculator', 'macro calculator', 'meal planner',
            'diet app', 'nutrition tracker', 'food diary', 'water tracker', 'fasting app',
            'intermittent fasting', 'keto diet', 'vegan recipes', 'healthy recipes', 'meal prep',
            'mindfulness app', 'breathing exercises', 'stress relief', 'anxiety relief', 'mental health',
            'therapy app', 'mood tracker', 'journal app', 'gratitude journal', 'self care',
            'period tracker', 'pregnancy tracker', 'baby tracker', 'health records', 'symptom checker'
        ],
        'lifestyle': [
            'recipe app', 'home design', 'fashion app', 'travel planner', 'dating app',
            'cooking app', 'meal ideas', 'grocery list', 'shopping list', 'pantry organizer',
            'interior design', 'room planner', 'furniture app', 'home decor', 'diy projects',
            'style guide', 'outfit planner', 'wardrobe organizer', 'fashion trends', 'shopping app',
            'trip planner', 'travel guide', 'hotel booking', 'flight booking', 'vacation planner',
            'itinerary planner', 'packing list', 'travel tips', 'city guide', 'tourist attractions',
            'dating tips', 'relationship advice', 'matchmaking', 'chat app', 'meet people',
            'wedding planner', 'event planner', 'party planner', 'gift ideas', 'wish list',
            'pet care', 'dog training', 'cat care', 'pet tracker', 'vet finder',
            'gardening app', 'plant identifier', 'plant care', 'lawn care', 'home maintenance'
        ],
        'social-networking': [
            'messaging app', 'social media', 'video chat', 'community app', 'forum app',
            'chat app', 'group chat', 'private messaging', 'secure chat', 'encrypted messaging',
            'voice call', 'video call', 'conference call', 'screen sharing', 'live streaming',
            'social network', 'photo sharing', 'video sharing', 'story app', 'status updates',
            'friend finder', 'people nearby', 'local community', 'neighborhood app', 'nextdoor alternative',
            'professional network', 'business networking', 'linkedin alternative', 'career network', 'job search',
            'dating network', 'singles app', 'meet friends', 'make friends', 'social discovery',
            'interest groups', 'hobby groups', 'club app', 'meetup app', 'event app',
            'anonymous chat', 'random chat', 'stranger chat', 'pen pal', 'language exchange'
        ],
        'utilities': [
            'file manager', 'calculator', 'scanner app', 'weather app', 'vpn app',
            'file explorer', 'file browser', 'zip app', 'unzip app', 'file compressor',
            'scientific calculator', 'graphing calculator', 'unit converter', 'currency converter', 'tip calculator',
            'document scanner', 'pdf scanner', 'qr scanner', 'barcode scanner', 'business card scanner',
            'weather forecast', 'weather radar', 'weather alerts', 'temperature app', 'climate app',
            'vpn service', 'proxy app', 'ad blocker', 'privacy app', 'security app',
            'flashlight app', 'compass app', 'level app', 'ruler app', 'magnifier app',
            'alarm clock', 'timer app', 'stopwatch', 'world clock', 'time zone converter',
            'battery saver', 'battery monitor', 'storage cleaner', 'cache cleaner', 'phone cleaner',
            'wifi analyzer', 'network scanner', 'speed test', 'data monitor', 'call blocker'
        ]
    }
    
    keywords = category_keywords.get(category, ['app', 'mobile app', 'ios app'])
    
    sample_data = []
    for i, keyword in enumerate(keywords):
        # Vary popularity more realistically
        base_popularity = 95
        popularity = max(10, base_popularity - (i * 1.5))
        
        # Vary competition based on popularity
        if popularity > 80:
            bid_strength = 'VERY_HIGH'
        elif popularity > 60:
            bid_strength = 'HIGH'
        elif popularity > 40:
            bid_strength = 'MEDIUM'
        else:
            bid_strength = 'LOW'
        
        sample_data.append({
            'id': str(uuid.uuid4()),
            'keyword': keyword,
            'searchPopularity': popularity,
            'bidStrength': bid_strength,
            'suggestedBidAmount': {
                'min': round(0.3 + (popularity / 100), 2),
                'max': round(1.5 + (popularity / 50), 2),
                'currency': 'USD'
            },
            'category': category.replace('-', ' ').title()
        })
    
    return sample_data

def process_keywords(raw_data):
    """Process raw API data into our format"""
    if not raw_data or 'data' not in raw_data:
        return []
