import logging
import requests
import json
from typing import Dict, Optional, List
from datetime import datetime
import time
from config import Config
import tweepy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LinkedInPoster:
    def __init__(self):
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN
        self.api_url = "https://api.linkedin.com/v2"
    
    def post_content(self, post_data: Dict, image_path: Optional[str] = None) -> bool:
        """Post content to LinkedIn"""
        try:
            logger.info("Posting to LinkedIn...")
            
            # Prepare the post text
            post_text = self._format_post_text(post_data)
            
            # Create the post
            post_payload = {
                "author": "urn:li:person:YOUR_LINKEDIN_ID",  # Replace with your LinkedIn ID
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": post_text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            # Add image if provided
            if image_path:
                # Upload image first
                image_urn = self._upload_image(image_path)
                if image_urn:
                    post_payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                    post_payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [{
                        "status": "READY",
                        "description": {
                            "text": "Tech news image"
                        },
                        "media": image_urn,
                        "title": {
                            "text": "Tech News"
                        }
                    }]
            
            # Make the API call
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            response = requests.post(
                f"{self.api_url}/ugcPosts",
                headers=headers,
                json=post_payload
            )
            
            if response.status_code == 201:
                logger.info("Successfully posted to LinkedIn")
                return True
            else:
                logger.error(f"LinkedIn API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False
    
    def _format_post_text(self, post_data: Dict) -> str:
        """Format post text for LinkedIn"""
        text = post_data.get('post_text', '')
        hashtags = ' '.join(post_data.get('hashtags', []))
        call_to_action = post_data.get('call_to_action', '')
        
        # Combine all elements
        full_text = f"{text}\n\n{hashtags}\n\n{call_to_action}"
        
        # LinkedIn has a 3000 character limit
        if len(full_text) > 3000:
            full_text = full_text[:2997] + "..."
        
        return full_text
    
    def _upload_image(self, image_path: str) -> Optional[str]:
        """Upload image to LinkedIn and return URN"""
        try:
            # This is a simplified version - you'll need to implement the full LinkedIn image upload flow
            # LinkedIn requires a multi-step process for image uploads
            logger.warning("LinkedIn image upload not fully implemented - using text-only post")
            return None
        except Exception as e:
            logger.error(f"Error uploading image to LinkedIn: {e}")
            return None

class TwitterPoster:
    def __init__(self):
        self.api_key = Config.TWITTER_API_KEY
        self.api_secret = Config.TWITTER_API_SECRET
        self.access_token = Config.TWITTER_ACCESS_TOKEN
        self.access_token_secret = Config.TWITTER_ACCESS_TOKEN_SECRET
        
        # Initialize Twitter API
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)
    
    def post_content(self, post_data: Dict, image_path: Optional[str] = None) -> bool:
        """Post content to Twitter"""
        try:
            logger.info("Posting to Twitter...")
            
            # Format post text
            post_text = self._format_post_text(post_data)
            
            # Post with image if provided
            if image_path:
                media = self.api.media_upload(image_path)
                self.api.update_status(post_text, media_ids=[media.media_id])
            else:
                self.api.update_status(post_text)
            
            logger.info("Successfully posted to Twitter")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return False
    
    def _format_post_text(self, post_data: Dict) -> str:
        """Format post text for Twitter"""
        text = post_data.get('post_text', '')
        hashtags = ' '.join(post_data.get('hashtags', []))
        
        # Combine text and hashtags
        full_text = f"{text}\n\n{hashtags}"
        
        # Twitter has a 280 character limit
        if len(full_text) > 280:
            # Truncate text to fit hashtags
            available_chars = 280 - len(hashtags) - 3  # 3 for newlines
            full_text = f"{text[:available_chars]}...\n\n{hashtags}"
        
        return full_text

class FacebookPoster:
    def __init__(self):
        self.access_token = Config.FACEBOOK_ACCESS_TOKEN
        self.page_id = Config.FACEBOOK_PAGE_ID
        self.api_url = "https://graph.facebook.com/v18.0"
    
    def post_content(self, post_data: Dict, image_path: Optional[str] = None) -> bool:
        """Post content to Facebook"""
        try:
            logger.info("Posting to Facebook...")
            
            # Format post text
            post_text = self._format_post_text(post_data)
            
            # Prepare post data
            post_data = {
                "message": post_text,
                "access_token": self.access_token
            }
            
            # Add image if provided
            if image_path:
                with open(image_path, 'rb') as image_file:
                    files = {'source': image_file}
                    response = requests.post(
                        f"{self.api_url}/{self.page_id}/photos",
                        data=post_data,
                        files=files
                    )
            else:
                response = requests.post(
                    f"{self.api_url}/{self.page_id}/feed",
                    data=post_data
                )
            
            if response.status_code == 200:
                logger.info("Successfully posted to Facebook")
                return True
            else:
                logger.error(f"Facebook API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return False
    
    def _format_post_text(self, post_data: Dict) -> str:
        """Format post text for Facebook"""
        text = post_data.get('post_text', '')
        hashtags = ' '.join(post_data.get('hashtags', []))
        call_to_action = post_data.get('call_to_action', '')
        
        return f"{text}\n\n{hashtags}\n\n{call_to_action}"

class SocialMediaPoster:
    def __init__(self):
        self.linkedin_poster = LinkedInPoster()
        self.twitter_poster = TwitterPoster()
        self.facebook_poster = FacebookPoster()
    
    def post_to_all_platforms(self, post_data: Dict, image_path: Optional[str] = None) -> Dict[str, bool]:
        """Post content to all configured social media platforms"""
        results = {}
        
        # Post to LinkedIn
        if Config.LINKEDIN_ACCESS_TOKEN:
            results['linkedin'] = self.linkedin_poster.post_content(post_data, image_path)
        else:
            logger.warning("LinkedIn access token not configured")
            results['linkedin'] = False
        
        # Post to Twitter
        if Config.TWITTER_API_KEY and Config.TWITTER_ACCESS_TOKEN:
            results['twitter'] = self.twitter_poster.post_content(post_data, image_path)
        else:
            logger.warning("Twitter API keys not configured")
            results['twitter'] = False
        
        # Post to Facebook
        if hasattr(Config, 'FACEBOOK_ACCESS_TOKEN') and Config.FACEBOOK_ACCESS_TOKEN:
            results['facebook'] = self.facebook_poster.post_content(post_data, image_path)
        else:
            logger.warning("Facebook access token not configured")
            results['facebook'] = False
        
        # Log results
        successful_posts = sum(results.values())
        total_platforms = len(results)
        logger.info(f"Posted to {successful_posts}/{total_platforms} platforms successfully")
        
        return results
    
    def post_to_platform(self, platform: str, post_data: Dict, image_path: Optional[str] = None) -> bool:
        """Post content to a specific platform"""
        if platform == 'linkedin':
            return self.linkedin_poster.post_content(post_data, image_path)
        elif platform == 'twitter':
            return self.twitter_poster.post_content(post_data, image_path)
        elif platform == 'facebook':
            return self.facebook_poster.post_content(post_data, image_path)
        else:
            logger.error(f"Unknown platform: {platform}")
            return False
    
    def schedule_post(self, platform: str, post_data: Dict, image_path: Optional[str] = None, 
                     scheduled_time: datetime = None) -> bool:
        """Schedule a post for later (placeholder for future implementation)"""
        try:
            logger.info(f"Scheduling post for {platform} at {scheduled_time}")
            
            # This is a placeholder - you would typically use a task queue like Celery
            # or a cloud service like AWS Lambda with CloudWatch Events
            
            # For now, we'll just post immediately
            return self.post_to_platform(platform, post_data, image_path)
            
        except Exception as e:
            logger.error(f"Error scheduling post: {e}")
            return False

if __name__ == "__main__":
    # Test the social media poster
    poster = SocialMediaPoster()
    
    # Test post data
    test_post = {
        'post_text': '🚀 Exciting news in the tech world! AI continues to revolutionize industries.',
        'hashtags': ['#TechNews', '#AI', '#Innovation'],
        'call_to_action': 'What do you think about this development? Share your thoughts below! 👇'
    }
    
    # Test posting (will fail without proper API keys)
    results = poster.post_to_all_platforms(test_post)
    print("Posting results:", results)
