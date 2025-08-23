import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Optional
import time
import random
from config import Config

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
        """Fetch news from a single RSS source"""
        try:
            logger.info(f"Fetching news from {source['name']}")
            
            # Parse RSS feed
            feed = feedparser.parse(source['url'])
            
            articles = []
            for entry in feed.entries[:10]:  # Get latest 10 articles
                try:
                    # Extract article data
                    article = {
                        'title': entry.get('title', ''),
                        'description': entry.get('summary', ''),
                        'link': entry.get('link', ''),
                        'published': self._parse_date(entry.get('published', '')),
                        'source': source['name'],
                        'category': source['category']
                    }
                    
                    # Get full content if available
                    if hasattr(entry, 'content'):
                        article['content'] = entry.content[0].value
                    else:
                        article['content'] = article['description']
                    
                    # Get image if available
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
        """Fetch news from all sources"""
        all_articles = []
        
        for source in self.sources:
            articles = self.fetch_news_from_source(source)
            all_articles.extend(articles)
            
            # Add delay to be respectful to servers
            time.sleep(random.uniform(1, 3))
        
        # Sort by publication date (newest first)
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        
        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles
    
    def get_recent_news(self, hours: int = 24) -> List[Dict]:
        """Get news from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        all_articles = self.fetch_all_news()
        
        recent_articles = [
            article for article in all_articles 
            if article['published'] and article['published'] > cutoff_time
        ]
        
        logger.info(f"Found {len(recent_articles)} recent articles (last {hours} hours)")
        return recent_articles
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        if not date_str:
            return None
        
        # Common date formats
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
        """Extract image URL from RSS entry"""
        # Check for media content
        if hasattr(entry, 'media_content') and entry.media_content:
            return entry.media_content[0]['url']
        
        # Check for media thumbnail
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0]['url']
        
        # Check for enclosures
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    return enclosure.get('href')
        
        # Try to extract from content
        if hasattr(entry, 'content'):
            soup = BeautifulSoup(entry.content[0].value, 'html.parser')
            img = soup.find('img')
            if img and img.get('src'):
                return img['src']
        
        return None
    
    def get_trending_topics(self, articles: List[Dict]) -> List[str]:
        """Extract trending topics from articles"""
        # Simple keyword extraction (can be enhanced with NLP)
        keywords = []
        for article in articles:
            title_words = article['title'].lower().split()
            # Filter out common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            keywords.extend([word for word in title_words if word not in stop_words and len(word) > 3])
        
        # Count frequency
        from collections import Counter
        keyword_counts = Counter(keywords)
        
        # Return top 10 trending keywords
        return [keyword for keyword, count in keyword_counts.most_common(10)]

if __name__ == "__main__":
    # Test the news fetcher
    fetcher = NewsFetcher()
    recent_news = fetcher.get_recent_news(hours=24)
    
    print(f"Found {len(recent_news)} recent articles:")
    for article in recent_news[:5]:
        print(f"- {article['title']} ({article['source']})")
        print(f"  Published: {article['published']}")
        print(f"  Link: {article['link']}")
        print()
