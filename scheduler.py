import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
from config import Config
from news_fetcher import NewsFetcher
from content_generator import ContentGenerator
from image_generator import ImageGenerator
from social_media_poster import SocialMediaPoster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAgentScheduler:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.content_generator = ContentGenerator()
        self.image_generator = ImageGenerator()
        self.social_poster = SocialMediaPoster()
        self.posting_schedule = Config.POSTING_SCHEDULE
        self.max_posts_per_day = Config.MAX_POSTS_PER_DAY
        self.posted_articles = set()  # Track posted articles to avoid duplicates
        
    def start_scheduler(self):
        """Start the automated scheduling system"""
        logger.info("Starting News Agent Scheduler...")
        
        # Schedule daily news fetching and posting
        self._setup_daily_schedules()
        
        # Schedule platform-specific posting times
        self._setup_platform_schedules()
        
        # Run the scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _setup_daily_schedules(self):
        """Setup daily recurring schedules"""
        # Fetch news every morning at 6 AM
        schedule.every().day.at("06:00").do(self._fetch_and_prepare_daily_news)
        
        # Generate daily summary at 7 AM
        schedule.every().day.at("07:00").do(self._generate_daily_summary)
        
        # Clean up old data weekly
        schedule.every().sunday.at("02:00").do(self._cleanup_old_data)
    
    def _setup_platform_schedules(self):
        """Setup platform-specific posting schedules"""
        for platform, times in self.posting_schedule.items():
            for time_str in times:
                schedule.every().day.at(time_str).do(
                    self._post_scheduled_content, platform
                )
                logger.info(f"Scheduled {platform} posts for {time_str}")
    
    def _fetch_and_prepare_daily_news(self):
        """Fetch news and prepare content for the day"""
        try:
            logger.info("Fetching daily news...")
            
            # Fetch recent news
            recent_news = self.news_fetcher.get_recent_news(hours=24)
            
            if not recent_news:
                logger.warning("No recent news found")
                return
            
            # Store news for later posting
            self.daily_news = recent_news
            
            # Generate content for top articles
            self._generate_content_for_articles(recent_news[:self.max_posts_per_day])
            
            logger.info(f"Prepared {len(recent_news)} articles for daily posting")
            
        except Exception as e:
            logger.error(f"Error fetching daily news: {e}")
    
    def _generate_content_for_articles(self, articles: List[Dict]):
        """Generate content and images for articles"""
        try:
            self.prepared_content = {}
            
            for article in articles:
                article_id = article.get('link', article.get('title', ''))
                
                if article_id in self.posted_articles:
                    continue  # Skip already posted articles
                
                # Generate content for each platform
                for platform in self.posting_schedule.keys():
                    try:
                        # Generate post content
                        post_data = self.content_generator.generate_post_content(article, platform)
                        
                        # Generate image
                        image_prompt = post_data.get('image_prompt', f"Tech news: {article['title']}")
                        image_path = f"images/{platform}_{article_id.replace('/', '_')}.png"
                        
                        generated_image = self.image_generator.generate_image(image_prompt, image_path)
                        
                        if generated_image:
                            # Optimize image for platform
                            optimized_image = self.image_generator.optimize_for_platform(
                                generated_image, platform
                            )
                            post_data['image_path'] = optimized_image
                        
                        # Store prepared content
                        if platform not in self.prepared_content:
                            self.prepared_content[platform] = []
                        
                        self.prepared_content[platform].append({
                            'post_data': post_data,
                            'article': article,
                            'image_path': post_data.get('image_path')
                        })
                        
                        logger.info(f"Generated content for {platform}: {article['title'][:50]}...")
                        
                    except Exception as e:
                        logger.error(f"Error generating content for {platform}: {e}")
                        continue
            
            logger.info(f"Generated content for {len(articles)} articles across {len(self.posting_schedule)} platforms")
            
        except Exception as e:
            logger.error(f"Error generating content for articles: {e}")
    
    def _post_scheduled_content(self, platform: str):
        """Post content at scheduled time for a specific platform"""
        try:
            logger.info(f"Posting scheduled content for {platform}...")
            
            if not hasattr(self, 'prepared_content') or platform not in self.prepared_content:
                logger.warning(f"No prepared content for {platform}")
                return
            
            # Get the next article to post
            platform_content = self.prepared_content[platform]
            
            if not platform_content:
                logger.warning(f"No content available for {platform}")
                return
            
            # Take the first available post
            post_item = platform_content.pop(0)
            post_data = post_item['post_data']
            article = post_item['article']
            image_path = post_item.get('image_path')
            
            # Post to the platform
            success = self.social_poster.post_to_platform(platform, post_data, image_path)
            
            if success:
                # Mark article as posted
                article_id = article.get('link', article.get('title', ''))
                self.posted_articles.add(article_id)
                logger.info(f"Successfully posted to {platform}: {article['title'][:50]}...")
            else:
                logger.error(f"Failed to post to {platform}")
            
        except Exception as e:
            logger.error(f"Error posting scheduled content for {platform}: {e}")
    
    def _generate_daily_summary(self):
        """Generate and post daily summary"""
        try:
            logger.info("Generating daily summary...")
            
            if not hasattr(self, 'daily_news') or not self.daily_news:
                logger.warning("No daily news available for summary")
                return
            
            # Generate summary content
            summary_data = self.content_generator.generate_daily_summary(self.daily_news)
            
            # Generate summary image
            summary_image_prompt = "Daily tech news summary, professional layout, modern design"
            summary_image_path = f"images/daily_summary_{datetime.now().strftime('%Y%m%d')}.png"
            
            generated_image = self.image_generator.generate_image(summary_image_prompt, summary_image_path)
            
            if generated_image:
                # Optimize for LinkedIn (best for summaries)
                optimized_image = self.image_generator.optimize_for_platform(generated_image, 'linkedin')
                summary_data['image_path'] = optimized_image
            
            # Post summary to LinkedIn
            success = self.social_poster.post_to_platform('linkedin', summary_data, summary_data.get('image_path'))
            
            if success:
                logger.info("Successfully posted daily summary to LinkedIn")
            else:
                logger.error("Failed to post daily summary")
            
        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")
    
    def _cleanup_old_data(self):
        """Clean up old data and images"""
        try:
            logger.info("Cleaning up old data...")
            
            # Clear posted articles tracking (keep last 7 days)
            cutoff_date = datetime.now() - timedelta(days=7)
            # This is a simplified cleanup - in a real system you'd store this in a database
            
            # Clean up old images (older than 30 days)
            import os
            import glob
            
            image_files = glob.glob("images/*.png")
            for image_file in image_files:
                file_time = datetime.fromtimestamp(os.path.getctime(image_file))
                if file_time < cutoff_date:
                    try:
                        os.remove(image_file)
                        logger.info(f"Removed old image: {image_file}")
                    except Exception as e:
                        logger.error(f"Error removing {image_file}: {e}")
            
            logger.info("Cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def post_now(self, platform: str = None):
        """Post content immediately (for testing or manual triggers)"""
        try:
            logger.info("Posting content now...")
            
            # Fetch fresh news
            recent_news = self.news_fetcher.get_recent_news(hours=6)  # Last 6 hours
            
            if not recent_news:
                logger.warning("No recent news found")
                return
            
            # Generate content for the first article
            article = recent_news[0]
            
            if platform:
                platforms = [platform]
            else:
                platforms = list(self.posting_schedule.keys())
            
            for platform in platforms:
                try:
                    # Generate content
                    post_data = self.content_generator.generate_post_content(article, platform)
                    
                    # Generate image
                    image_prompt = post_data.get('image_prompt', f"Tech news: {article['title']}")
                    image_path = f"images/immediate_{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    
                    generated_image = self.image_generator.generate_image(image_prompt, image_path)
                    
                    if generated_image:
                        optimized_image = self.image_generator.optimize_for_platform(generated_image, platform)
                        post_data['image_path'] = optimized_image
                    
                    # Post immediately
                    success = self.social_poster.post_to_platform(platform, post_data, post_data.get('image_path'))
                    
                    if success:
                        logger.info(f"Successfully posted to {platform}")
                    else:
                        logger.error(f"Failed to post to {platform}")
                    
                except Exception as e:
                    logger.error(f"Error posting to {platform}: {e}")
            
        except Exception as e:
            logger.error(f"Error in immediate posting: {e}")
    
    def get_schedule_status(self) -> Dict:
        """Get current schedule status"""
        return {
            'next_runs': schedule.get_jobs(),
            'posted_articles_count': len(self.posted_articles),
            'prepared_content_count': len(getattr(self, 'prepared_content', {})),
            'daily_news_count': len(getattr(self, 'daily_news', []))
        }

if __name__ == "__main__":
    # Test the scheduler
    scheduler = NewsAgentScheduler()
    
    # Test immediate posting
    print("Testing immediate posting...")
    scheduler.post_now('linkedin')
    
    # Show schedule status
    print("\nSchedule status:")
    status = scheduler.get_schedule_status()
    print(f"Next runs: {len(status['next_runs'])} scheduled jobs")
    print(f"Posted articles: {status['posted_articles_count']}")
    
    # Start scheduler (uncomment to run continuously)
    # scheduler.start_scheduler()
