#!/usr/bin/env python3
import argparse
import logging
import sys
import os
from typing import Optional

from src.config import Config
from src.services.news_fetcher import NewsFetcher
from src.ai.content_generator import ContentGenerator
from src.ai.image_generator import ImageGenerator
from src.services.social_media_poster import SocialMediaPoster
from src.scheduler import NewsAgentScheduler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NewsAgent:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.content_generator = ContentGenerator()
        self.image_generator = ImageGenerator()
        self.social_poster = SocialMediaPoster()
        self.scheduler = NewsAgentScheduler()

    def run_scheduler(self):
        logger.info("Starting AI News Agent Scheduler...")
        print("🤖 AI News Agent is running!")
        print("📰 Fetching tech news and posting to social media automatically...")
        print("⏰ Scheduled posts will be published at optimal times")
        print("🛑 Press Ctrl+C to stop")
        try:
            self.scheduler.start_scheduler()
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            print("\n👋 AI News Agent stopped. Goodbye!")

    def post_now(self, platform: Optional[str] = None):
        logger.info("Posting content immediately...")
        print("🚀 Posting content now...")
        try:
            self.scheduler.post_now(platform)
            print("✅ Content posted successfully!")
        except Exception as e:
            logger.error(f"Error posting content: {e}")
            print(f"❌ Error posting content: {e}")

    def fetch_news(self, hours: int = 24, limit: int = 10):
        logger.info(f"Fetching news from last {hours} hours...")
        print(f"📰 Fetching tech news from last {hours} hours...")
        try:
            news = self.news_fetcher.get_recent_news(hours=hours)
            if not news:
                print("❌ No recent news found")
                return
            print(f"\n📊 Found {len(news)} articles:")
            print("=" * 80)
            for i, article in enumerate(news[:limit], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   Source: {article['source']}")
                print(f"   Published: {article['published']}")
                print(f"   Link: {article['link']}")
                print(f"   Description: {article['description'][:150]}...")
                print("-" * 80)
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            print(f"❌ Error fetching news: {e}")

    def test_all_components(self):
        logger.info("Testing all components...")
        print("🧪 Testing all components...")
        results = {}
        # Test news fetching
        print("\n1. Testing news fetching...")
        try:
            news = self.news_fetcher.get_recent_news(hours=6)
            results['news_fetching'] = len(news) > 0
            print(f"   ✅ Found {len(news)} articles")
        except Exception as e:
            results['news_fetching'] = False
            print(f"   ❌ Error: {e}")
        # Test content generation
        print("\n2. Testing content generation (Gemini)...")
        try:
            if news:
                article = news[0]
                post_data = self.content_generator.generate_post_content(article, 'linkedin')
                results['content_generation'] = bool(post_data)
                print(f"   ✅ Generated content: {post_data.get('post_text', '')[:50]}...")
            else:
                results['content_generation'] = False
                print("   ❌ No articles to test with")
        except Exception as e:
            results['content_generation'] = False
            print(f"   ❌ Error: {e}")
        # Test image generation (fallback)
        print("\n3. Testing image generation (fallback)...")
        try:
            if news:
                image_prompt = f"Tech news: {article['title']}"
                image_path = self.image_generator.generate_image(image_prompt, "test_image.png")
                results['image_generation'] = bool(image_path)
                print(f"   ✅ Generated image: {image_path}")
            else:
                results['image_generation'] = False
                print("   ❌ No articles to test with")
        except Exception as e:
            results['image_generation'] = False
            print(f"   ❌ Error: {e}")
        # Social posting (skipped)
        print("\n4. Testing social media posting...")
        results['social_posting'] = False
        print("   ⚠️  Social posting test skipped (requires API keys)")
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY:")
        print("=" * 50)
        for component, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{component.replace('_', ' ').title()}: {status}")

    def show_status(self):
        logger.info("Showing system status...")
        print("📊 AI News Agent Status")
        print("=" * 50)
        print("\n🔧 Configuration:")
        print(f"   Gemini API: {'✅ Configured' if Config.GEMINI_API_KEY else '❌ Not configured'}")
        print(f"   LinkedIn: {'✅ Configured' if Config.LINKEDIN_ACCESS_TOKEN else '❌ Not configured'}")
        print(f"   Twitter: {'✅ Configured' if Config.TWITTER_API_KEY else '❌ Not configured'}")
        print("\n⏰ Posting Schedule:")
        for platform, times in Config.POSTING_SCHEDULE.items():
            print(f"   {platform.title()}: {', '.join(times)}")


def main():
    parser = argparse.ArgumentParser(
        description="AI News Agent - Gemini-powered",
    )
    parser.add_argument('command', choices=['run', 'post-now', 'fetch-news', 'test', 'status'])
    parser.add_argument('--platform', choices=['linkedin', 'twitter', 'facebook'])
    parser.add_argument('--hours', type=int, default=24)
    parser.add_argument('--limit', type=int, default=10)
    args = parser.parse_args()

    agent = NewsAgent()
    if args.command == 'run':
        agent.run_scheduler()
    elif args.command == 'post-now':
        agent.post_now(args.platform)
    elif args.command == 'fetch-news':
        agent.fetch_news(args.hours, args.limit)
    elif args.command == 'test':
        agent.test_all_components()
    elif args.command == 'status':
        agent.show_status()


if __name__ == "__main__":
    main()


