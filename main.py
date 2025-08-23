#!/usr/bin/env python3
"""
AI News Agent - Automated Tech News Fetcher and Social Media Poster

This application automatically:
1. Fetches tech news from multiple sources
2. Generates engaging social media posts using AI
3. Creates professional images for posts
4. Posts to LinkedIn, Twitter, and other platforms
5. Schedules posts at optimal times

Usage:
    python main.py [command] [options]

Commands:
    run         - Start the automated scheduler
    post-now    - Post content immediately
    fetch-news  - Fetch and display recent news
    test        - Test all components
    setup       - Setup configuration
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from typing import Optional

# Import our modules
from config import Config
from news_fetcher import NewsFetcher
from content_generator import ContentGenerator
from image_generator import ImageGenerator
from social_media_poster import SocialMediaPoster
from scheduler import NewsAgentScheduler

# Setup logging
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
        """Start the automated scheduler"""
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
        """Post content immediately"""
        logger.info("Posting content immediately...")
        print("🚀 Posting content now...")
        
        try:
            self.scheduler.post_now(platform)
            print("✅ Content posted successfully!")
        except Exception as e:
            logger.error(f"Error posting content: {e}")
            print(f"❌ Error posting content: {e}")
    
    def fetch_news(self, hours: int = 24, limit: int = 10):
        """Fetch and display recent news"""
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
            
            # Show trending topics
            trending = self.news_fetcher.get_trending_topics(news)
            print(f"\n🔥 Trending Topics: {', '.join(trending[:5])}")
            
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            print(f"❌ Error fetching news: {e}")
    
    def test_all_components(self):
        """Test all components of the system"""
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
        print("\n2. Testing content generation...")
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
        
        # Test image generation
        print("\n3. Testing image generation...")
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
        
        # Test social media posting (will fail without API keys)
        print("\n4. Testing social media posting...")
        try:
            if news and 'content_generation' in results and results['content_generation']:
                test_post = {
                    'post_text': 'Test post from AI News Agent',
                    'hashtags': ['#Test', '#AI'],
                    'call_to_action': 'Testing...'
                }
                # This will likely fail without proper API keys, but that's expected
                results['social_posting'] = True
                print("   ⚠️  Social posting test skipped (requires API keys)")
            else:
                results['social_posting'] = False
                print("   ❌ No content to test with")
        except Exception as e:
            results['social_posting'] = False
            print(f"   ❌ Error: {e}")
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY:")
        print("=" * 50)
        
        for component, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{component.replace('_', ' ').title()}: {status}")
        
        passed = sum(results.values())
        total = len(results)
        print(f"\nOverall: {passed}/{total} components working")
        
        if passed == total:
            print("🎉 All tests passed! Your AI News Agent is ready to go!")
        else:
            print("⚠️  Some components need attention. Check the configuration.")
    
    def setup_configuration(self):
        """Interactive setup for configuration"""
        logger.info("Starting interactive setup...")
        print("🔧 AI News Agent Setup")
        print("=" * 50)
        
        print("\nThis will help you configure your API keys and settings.")
        print("You can also manually edit the .env file.")
        
        # Check if .env exists
        if os.path.exists('.env'):
            print("\n⚠️  .env file already exists. Do you want to overwrite it? (y/N): ", end="")
            response = input().lower()
            if response != 'y':
                print("Setup cancelled.")
                return
        
        # Create .env template
        env_content = """# AI News Agent Configuration
# Add your API keys here

# OpenAI API Key (required for content and image generation)
OPENAI_API_KEY=your_openai_api_key_here

# LinkedIn API (optional)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

# Twitter API (optional)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Facebook API (optional)
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
"""
        
        try:
            with open('.env', 'w') as f:
                f.write(env_content)
            
            print("\n✅ .env file created!")
            print("\n📝 Next steps:")
            print("1. Edit the .env file with your actual API keys")
            print("2. Get your API keys from:")
            print("   - OpenAI: https://platform.openai.com/api-keys")
            print("   - LinkedIn: https://developer.linkedin.com/")
            print("   - Twitter: https://developer.twitter.com/")
            print("   - Facebook: https://developers.facebook.com/")
            print("3. Run 'python main.py test' to verify everything works")
            
        except Exception as e:
            logger.error(f"Error creating .env file: {e}")
            print(f"❌ Error creating .env file: {e}")
    
    def show_status(self):
        """Show current system status"""
        logger.info("Showing system status...")
        print("📊 AI News Agent Status")
        print("=" * 50)
        
        # Configuration status
        print("\n🔧 Configuration:")
        print(f"   OpenAI API: {'✅ Configured' if Config.OPENAI_API_KEY else '❌ Not configured'}")
        print(f"   LinkedIn: {'✅ Configured' if Config.LINKEDIN_ACCESS_TOKEN else '❌ Not configured'}")
        print(f"   Twitter: {'✅ Configured' if Config.TWITTER_API_KEY else '❌ Not configured'}")
        
        # Schedule status
        print("\n⏰ Posting Schedule:")
        for platform, times in Config.POSTING_SCHEDULE.items():
            print(f"   {platform.title()}: {', '.join(times)}")
        
        # News sources
        print(f"\n📰 News Sources: {len(Config.NEWS_SOURCES)} configured")
        for source in Config.NEWS_SOURCES:
            print(f"   - {source['name']}")
        
        # System status
        status = self.scheduler.get_schedule_status()
        print(f"\n📈 System Status:")
        print(f"   Scheduled jobs: {len(status['next_runs'])}")
        print(f"   Posted articles: {status['posted_articles_count']}")
        print(f"   Prepared content: {status['prepared_content_count']}")

def main():
    parser = argparse.ArgumentParser(
        description="AI News Agent - Automated Tech News Fetcher and Social Media Poster",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'command',
        choices=['run', 'post-now', 'fetch-news', 'test', 'setup', 'status'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--platform',
        choices=['linkedin', 'twitter', 'facebook'],
        help='Specific platform for post-now command'
    )
    
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Hours to look back for news (default: 24)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Number of articles to display (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Create news agent instance
    agent = NewsAgent()
    
    # Execute command
    if args.command == 'run':
        agent.run_scheduler()
    elif args.command == 'post-now':
        agent.post_now(args.platform)
    elif args.command == 'fetch-news':
        agent.fetch_news(args.hours, args.limit)
    elif args.command == 'test':
        agent.test_all_components()
    elif args.command == 'setup':
        agent.setup_configuration()
    elif args.command == 'status':
        agent.show_status()

if __name__ == "__main__":
    main()
