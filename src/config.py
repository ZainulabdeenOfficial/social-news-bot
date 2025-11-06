import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_TEXT_MODEL = os.getenv('GEMINI_TEXT_MODEL', 'gemini-1.5-flash')

    # LinkedIn Configuration
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

    # Twitter Configuration
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    # Optional Facebook
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

    # News Sources
    NEWS_SOURCES = [
        {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/', 'category': 'tech'},
        {'name': 'The Verge', 'url': 'https://www.theverge.com/rss/index.xml', 'category': 'tech'},
        {'name': 'Wired', 'url': 'https://www.wired.com/feed/rss', 'category': 'tech'},
        {'name': 'Ars Technica', 'url': 'https://feeds.arstechnica.com/arstechnica/index', 'category': 'tech'},
        {'name': 'Engadget', 'url': 'https://www.engadget.com/rss.xml', 'category': 'tech'},
    ]

    # Posting Schedule
    POSTING_SCHEDULE = {
        'linkedin': ['09:00', '12:00', '15:00', '18:00'],
        'twitter': ['08:00', '11:00', '14:00', '17:00', '20:00'],
        'facebook': ['10:00', '13:00', '16:00', '19:00'],
    }

    # Content/Image Settings
    MAX_POSTS_PER_DAY = int(os.getenv('MAX_POSTS_PER_DAY', '5'))
    IMAGE_SIZE = (1200, 630)
    IMAGE_STYLE = "modern, professional, tech-focused"

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///news_agent.db')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'news_agent.log')


