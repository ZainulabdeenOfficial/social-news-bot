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
from src.database.database import SessionLocal, init_db
from src.database.models import Article, GeneratedContent, PostedContent


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
        init_db()

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
        db = SessionLocal()
        try:
            logger.info("Fetching daily news...")
            recent_news = self.news_fetcher.get_recent_news(hours=24)
            if not recent_news:
                logger.warning("No recent news found")
                return

            for article_data in recent_news:
                existing_article = db.query(Article).filter_by(link=article_data['link']).first()
                if not existing_article:
                    new_article = Article(**article_data)
                    db.add(new_article)
            db.commit()

            articles_to_process = db.query(Article).order_by(Article.pub_date.desc()).limit(self.max_posts_per_day).all()
            self._generate_content_for_articles(articles_to_process)
            logger.info(f"Prepared {len(articles_to_process)} articles for daily posting")
        except Exception as e:
            logger.error(f"Error fetching daily news: {e}")
        finally:
            db.close()

    def _generate_content_for_articles(self, articles: List[Article]):
        db = SessionLocal()
        try:
            for article in articles:
                # Check if content has already been generated
                existing_content = db.query(GeneratedContent).filter_by(article_id=article.id).first()
                if existing_content:
                    continue

                for platform in self.posting_schedule.keys():
                    try:
                        post_data = self.content_generator.generate_post_content(article.__dict__, platform)
                        image_prompt = post_data.get('image_prompt', f"Tech news: {article.title}")
                        image_path = f"images/{platform}_{article.link.replace('/', '_')}.png"
                        generated_image = self.image_generator.generate_image(image_prompt, image_path)
                        if generated_image:
                            optimized_image = self.image_generator.optimize_for_platform(generated_image, platform)
                            post_data['image_path'] = optimized_image

                        new_content = GeneratedContent(
                            article_id=article.id,
                            platform=platform,
                            post_text=post_data['post_text'],
                            hashtags=",".join(post_data['hashtags']),
                            image_prompt=image_prompt,
                            image_path=post_data.get('image_path')
                        )
                        db.add(new_content)
                        logger.info(f"Generated content for {platform}: {article.title[:50]}...")
                    except Exception as e:
                        logger.error(f"Error generating content for {platform}: {e}")
                        continue
            db.commit()
            logger.info(f"Generated content for {len(articles)} articles across {len(self.posting_schedule)} platforms")
        except Exception as e:
            logger.error(f"Error generating content for articles: {e}")
        finally:
            db.close()

    def _post_scheduled_content(self, platform: str):
        db = SessionLocal()
        try:
            logger.info(f"Posting scheduled content for {platform}...")
            content_to_post = db.query(GeneratedContent).filter(
                GeneratedContent.platform == platform,
                ~GeneratedContent.posted_content.any()
            ).first()

            if not content_to_post:
                logger.warning(f"No content available for {platform}")
                return

            post_data = {
                'post_text': content_to_post.post_text,
                'hashtags': content_to_post.hashtags.split(','),
            }
            image_path = content_to_post.image_path

            success, post_url = self.social_poster.post_to_platform(platform, post_data, image_path)

            if success:
                new_post = PostedContent(
                    generated_content_id=content_to_post.id,
                    platform=platform,
                    post_url=post_url,
                    status='success'
                )
                db.add(new_post)
                db.commit()
                logger.info(f"Successfully posted to {platform}: {content_to_post.article.title[:50]}...")
            else:
                new_post = PostedContent(
                    generated_content_id=content_to_post.id,
                    platform=platform,
                    status='failed',
                    error_message="Failed to post"
                )
                db.add(new_post)
                db.commit()
                logger.error(f"Failed to post to {platform}")
        except Exception as e:
            logger.error(f"Error posting scheduled content for {platform}: {e}")
        finally:
            db.close()

    def _generate_daily_summary(self):
        db = SessionLocal()
        try:
            logger.info("Generating daily summary...")
            daily_articles = db.query(Article).filter(Article.pub_date >= datetime.utcnow() - timedelta(days=1)).all()
            if not daily_articles:
                logger.warning("No daily news available for summary")
                return

            summary_data = self.content_generator.generate_daily_summary([article.__dict__ for article in daily_articles])
            summary_image_prompt = "Daily tech news summary, professional layout, modern design"
            summary_image_path = f"images/daily_summary_{datetime.now().strftime('%Y%m%d')}.png"
            generated_image = self.image_generator.generate_image(summary_image_prompt, summary_image_path)
            if generated_image:
                optimized_image = self.image_generator.optimize_for_platform(generated_image, 'linkedin')
                summary_data['image_path'] = optimized_image
            self.social_poster.post_to_platform('linkedin', summary_data, summary_data.get('image_path'))
        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")
        finally:
            db.close()

    def _cleanup_old_data(self):
        db = SessionLocal()
        try:
            logger.info("Cleaning up old data...")
            cutoff_date = datetime.utcnow() - timedelta(days=7)

            # Clean up old articles, generated content, and posts
            db.query(PostedContent).filter(PostedContent.posted_at < cutoff_date).delete()
            db.query(GeneratedContent).filter(GeneratedContent.created_at < cutoff_date).delete()
            db.query(Article).filter(Article.created_at < cutoff_date).delete()
            db.commit()

            import glob
            import os
            image_files = glob.glob("images/*.png")
            for image_file in image_files:
                file_time = datetime.fromtimestamp(os.path.getctime(image_file))
                if file_time < datetime.now() - timedelta(days=7):
                    try:
                        os.remove(image_file)
                        logger.info(f"Removed old image: {image_file}")
                    except Exception as e:
                        logger.error(f"Error removing {image_file}: {e}")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
        finally:
            db.close()

    def post_now(self, platform: str = None, article_link: str = None):
        db = SessionLocal()
        try:
            logger.info("Posting content now...")
            if article_link:
                article = db.query(Article).filter_by(link=article_link).first()
            else:
                article = db.query(Article).order_by(Article.pub_date.desc()).first()

            if not article:
                logger.warning("No recent news found")
                return

            platforms = [platform] if platform else list(self.posting_schedule.keys())
            for p in platforms:
                try:
                    post_data = self.content_generator.generate_post_content(article.__dict__, p)
                    image_prompt = post_data.get('image_prompt', f"Tech news: {article.title}")
                    image_path = f"images/immediate_{p}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    generated_image = self.image_generator.generate_image(image_prompt, image_path)
                    if generated_image:
                        optimized_image = self.image_generator.optimize_for_platform(generated_image, p)
                        post_data['image_path'] = optimized_image

                    success, post_url = self.social_poster.post_to_platform(p, post_data, post_data.get('image_path'))

                    # Find or create GeneratedContent
                    generated_content = db.query(GeneratedContent).filter_by(article_id=article.id, platform=p).first()
                    if not generated_content:
                        generated_content = GeneratedContent(
                            article_id=article.id,
                            platform=p,
                            post_text=post_data['post_text'],
                            hashtags=",".join(post_data.get('hashtags', [])),
                            image_prompt=image_prompt,
                            image_path=post_data.get('image_path')
                        )
                        db.add(generated_content)
                        db.commit()

                    if success:
                        new_post = PostedContent(
                            generated_content_id=generated_content.id,
                            platform=p,
                            post_url=post_url,
                            status='success'
                        )
                        db.add(new_post)
                        db.commit()
                        logger.info(f"Successfully posted to {p}: {article.title[:50]}...")
                    else:
                        new_post = PostedContent(
                            generated_content_id=generated_content.id,
                            platform=p,
                            status='failed',
                            error_message="Failed to post"
                        )
                        db.add(new_post)
                        db.commit()
                        logger.error(f"Failed to post to {p}")

                except Exception as e:
                    logger.error(f"Error posting to {p}: {e}")
        except Exception as e:
            logger.error(f"Error in immediate posting: {e}")
        finally:
            db.close()

    def get_schedule_status(self) -> Dict:
        db = SessionLocal()
        try:
            return {
                'next_runs': schedule.get_jobs(),
                'posted_articles_count': db.query(PostedContent).count(),
                'prepared_content_count': db.query(GeneratedContent).count(),
                'daily_news_count': db.query(Article).filter(Article.pub_date >= datetime.utcnow() - timedelta(days=1)).count()
            }
        finally:
            db.close()


