import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import time
import random

from src.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsFetcher:
    def __init__(self):
        self.sources = Config.NEWS_SOURCES
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_news_from_source(self, source: Dict) -> List[Dict]:
        try:
            logger.info(f"Fetching news from {source['name']}")
            feed = feedparser.parse(source['url'])
            articles = []
            for entry in feed.entries[:10]:
                try:
                    article = {
                        'title': entry.get('title', ''),
                        'description': entry.get('summary', ''),
                        'link': entry.get('link', ''),
                        'published': self._parse_date(entry.get('published', '')),
                        'source': source['name'],
                        'category': source['category']
                    }
                    if hasattr(entry, 'content'):
                        article['content'] = entry.content[0].value
                    else:
                        article['content'] = article['description']
                    article['image_url'] = self._extract_image(entry)
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Error processing article from {source['name']}: {e}")
                    continue
            logger.info(f"Successfully fetched {len(articles)} articles from {source['name']}")
            return articles
        except Exception as e:
            logger.error(f"Error fetching from {source['name']}: {e}")
            return []

    def fetch_all_news(self) -> List[Dict]:
        all_articles = []
        for source in self.sources:
            articles = self.fetch_news_from_source(source)
            all_articles.extend(articles)
            time.sleep(random.uniform(1, 3))
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles

    def get_recent_news(self, hours: int = 24) -> List[Dict]:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_articles = self.fetch_all_news()
        return [a for a in all_articles if a['published'] and a['published'] > cutoff_time]

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        if not date_str:
            return None
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S %Z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S'
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        logger.warning(f"Could not parse date: {date_str}")
        return None

    def _extract_image(self, entry) -> Optional[str]:
        if hasattr(entry, 'media_content') and entry.media_content:
            return entry.media_content[0]['url']
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0]['url']
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    return enclosure.get('href')
        if hasattr(entry, 'content'):
            soup = BeautifulSoup(entry.content[0].value, 'html.parser')
            img = soup.find('img')
            if img and img.get('src'):
                return img['src']
        return None


