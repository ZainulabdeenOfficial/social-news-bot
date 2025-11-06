import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List

from src.config import Config
from src.services.news_fetcher import NewsFetcher
from src.ai.content_generator import ContentGenerator
from src.ai.image_generator import ImageGenerator
from src.services.social_media_poster import SocialMediaPoster


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
        self.posted_articles = set()

    def start_scheduler(self):
        logger.info("Starting News Agent Scheduler...")
        self._setup_daily_schedules()
        self._setup_platform_schedules()
        while True:
            schedule.run_pending()
            time.sleep(60)

    def _setup_daily_schedules(self):
        schedule.every().day.at("06:00").do(self._fetch_and_prepare_daily_news)
        schedule.every().day.at("07:00").do(self._generate_daily_summary)
        schedule.every().sunday.at("02:00").do(self._cleanup_old_data)

    def _setup_platform_schedules(self):
        for platform, times in self.posting_schedule.items():
            for time_str in times:
                schedule.every().day.at(time_str).do(self._post_scheduled_content, platform)
                logger.info(f"Scheduled {platform} posts for {time_str}")

    def _fetch_and_prepare_daily_news(self):
        try:
            logger.info("Fetching daily news...")
            recent_news = self.news_fetcher.get_recent_news(hours=24)
            if not recent_news:
                logger.warning("No recent news found")
                return
            self.daily_news = recent_news
            self._generate_content_for_articles(recent_news[:self.max_posts_per_day])
            logger.info(f"Prepared {len(recent_news)} articles for daily posting")
        except Exception as e:
            logger.error(f"Error fetching daily news: {e}")

    def _generate_content_for_articles(self, articles: List[Dict]):
        try:
            self.prepared_content = {}
            for article in articles:
                article_id = article.get('link', article.get('title', ''))
                if article_id in self.posted_articles:
                    continue
                for platform in self.posting_schedule.keys():
                    try:
                        post_data = self.content_generator.generate_post_content(article, platform)
                        image_prompt = post_data.get('image_prompt', f"Tech news: {article['title']}")
                        image_path = f"images/{platform}_{article_id.replace('/', '_')}.png"
                        generated_image = self.image_generator.generate_image(image_prompt, image_path)
                        if generated_image:
                            optimized_image = self.image_generator.optimize_for_platform(generated_image, platform)
                            post_data['image_path'] = optimized_image
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
        try:
            logger.info(f"Posting scheduled content for {platform}...")
            if not hasattr(self, 'prepared_content') or platform not in self.prepared_content:
                logger.warning(f"No prepared content for {platform}")
                return
            platform_content = self.prepared_content[platform]
            if not platform_content:
                logger.warning(f"No content available for {platform}")
                return
            post_item = platform_content.pop(0)
            post_data = post_item['post_data']
            article = post_item['article']
            image_path = post_item.get('image_path')
            success = self.social_poster.post_to_platform(platform, post_data, image_path)
            if success:
                article_id = article.get('link', article.get('title', ''))
                self.posted_articles.add(article_id)
                logger.info(f"Successfully posted to {platform}: {article['title'][:50]}...")
            else:
                logger.error(f"Failed to post to {platform}")
        except Exception as e:
            logger.error(f"Error posting scheduled content for {platform}: {e}")

    def _generate_daily_summary(self):
        try:
            logger.info("Generating daily summary...")
            if not hasattr(self, 'daily_news') or not self.daily_news:
                logger.warning("No daily news available for summary")
                return
            summary_data = self.content_generator.generate_daily_summary(self.daily_news)
            summary_image_prompt = "Daily tech news summary, professional layout, modern design"
            summary_image_path = f"images/daily_summary_{datetime.now().strftime('%Y%m%d')}.png"
            generated_image = self.image_generator.generate_image(summary_image_prompt, summary_image_path)
            if generated_image:
                optimized_image = self.image_generator.optimize_for_platform(generated_image, 'linkedin')
                summary_data['image_path'] = optimized_image
            self.social_poster.post_to_platform('linkedin', summary_data, summary_data.get('image_path'))
        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")

    def _cleanup_old_data(self):
        try:
            logger.info("Cleaning up old data...")
            cutoff_date = datetime.now() - timedelta(days=7)
            import glob
            import os
            image_files = glob.glob("images/*.png")
            for image_file in image_files:
                file_time = datetime.fromtimestamp(os.path.getctime(image_file))
                if file_time < cutoff_date:
                    try:
                        os.remove(image_file)
                        logger.info(f"Removed old image: {image_file}")
                    except Exception as e:
                        logger.error(f"Error removing {image_file}: {e}")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def post_now(self, platform: str = None):
        try:
            logger.info("Posting content now...")
            recent_news = self.news_fetcher.get_recent_news(hours=6)
            if not recent_news:
                logger.warning("No recent news found")
                return
            article = recent_news[0]
            platforms = [platform] if platform else list(self.posting_schedule.keys())
            for p in platforms:
                try:
                    post_data = self.content_generator.generate_post_content(article, p)
                    image_prompt = post_data.get('image_prompt', f"Tech news: {article['title']}")
                    image_path = f"images/immediate_{p}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    generated_image = self.image_generator.generate_image(image_prompt, image_path)
                    if generated_image:
                        optimized_image = self.image_generator.optimize_for_platform(generated_image, p)
                        post_data['image_path'] = optimized_image
                    self.social_poster.post_to_platform(p, post_data, post_data.get('image_path'))
                except Exception as e:
                    logger.error(f"Error posting to {p}: {e}")
        except Exception as e:
            logger.error(f"Error in immediate posting: {e}")

    def get_schedule_status(self) -> Dict:
        return {
            'next_runs': schedule.get_jobs(),
            'posted_articles_count': len(self.posted_articles),
            'prepared_content_count': len(getattr(self, 'prepared_content', {})),
            'daily_news_count': len(getattr(self, 'daily_news', []))
        }


