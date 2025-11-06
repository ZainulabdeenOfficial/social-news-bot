import logging
import requests
from typing import Dict, Optional
from datetime import datetime

import tweepy

from src.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInPoster:
    def __init__(self):
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN
        self.api_url = "https://api.linkedin.com/v2"

    def post_content(self, post_data: Dict, image_path: Optional[str] = None) -> bool:
        try:
            logger.info("Posting to LinkedIn...")
            post_text = self._format_post_text(post_data)
            post_payload = {
                "author": "urn:li:person:YOUR_LINKEDIN_ID",  # TODO: user must replace
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_text},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            response = requests.post(f"{self.api_url}/ugcPosts", headers=headers, json=post_payload)
            if response.status_code == 201:
                logger.info("Successfully posted to LinkedIn")
                return True
            logger.error(f"LinkedIn API error: {response.status_code} - {response.text}")
            return False
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return False

    def _format_post_text(self, post_data: Dict) -> str:
        text = post_data.get('post_text', '')
        hashtags = ' '.join(post_data.get('hashtags', []))
        call_to_action = post_data.get('call_to_action', '')
        full_text = f"{text}\n\n{hashtags}\n\n{call_to_action}"
        if len(full_text) > 3000:
            full_text = full_text[:2997] + "..."
        return full_text


class TwitterPoster:
    def __init__(self):
        self.api_key = Config.TWITTER_API_KEY
        self.api_secret = Config.TWITTER_API_SECRET
        self.access_token = Config.TWITTER_ACCESS_TOKEN
        self.access_token_secret = Config.TWITTER_ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def post_content(self, post_data: Dict, image_path: Optional[str] = None) -> bool:
        try:
            logger.info("Posting to Twitter...")
            post_text = self._format_post_text(post_data)
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
        text = post_data.get('post_text', '')
        hashtags = ' '.join(post_data.get('hashtags', []))
        full_text = f"{text}\n\n{hashtags}"
        if len(full_text) > 280:
            available = 280 - len(hashtags) - 3
            full_text = f"{text[:max(0, available)]}...\n\n{hashtags}"
        return full_text


class FacebookPoster:
    def __init__(self):
        self.access_token = Config.FACEBOOK_ACCESS_TOKEN
        self.page_id = Config.FACEBOOK_PAGE_ID
        self.api_url = "https://graph.facebook.com/v18.0"

    def post_content(self, post_data: Dict, image_path: Optional[str] = None) -> bool:
        try:
            logger.info("Posting to Facebook...")
            post_text = self._format_post_text(post_data)
            post_payload = {"message": post_text, "access_token": self.access_token}
            if image_path:
                with open(image_path, 'rb') as image_file:
                    files = {'source': image_file}
                    response = requests.post(f"{self.api_url}/{self.page_id}/photos", data=post_payload, files=files)
            else:
                response = requests.post(f"{self.api_url}/{self.page_id}/feed", data=post_payload)
            if response.status_code == 200:
                logger.info("Successfully posted to Facebook")
                return True
            logger.error(f"Facebook API error: {response.status_code} - {response.text}")
            return False
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return False

    def _format_post_text(self, post_data: Dict) -> str:
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
        results = {}
        if Config.LINKEDIN_ACCESS_TOKEN:
            results['linkedin'] = self.linkedin_poster.post_content(post_data, image_path)
        else:
            logger.warning("LinkedIn access token not configured")
            results['linkedin'] = False

        if Config.TWITTER_API_KEY and Config.TWITTER_ACCESS_TOKEN:
            results['twitter'] = self.twitter_poster.post_content(post_data, image_path)
        else:
            logger.warning("Twitter API keys not configured")
            results['twitter'] = False

        if Config.FACEBOOK_ACCESS_TOKEN:
            results['facebook'] = self.facebook_poster.post_content(post_data, image_path)
        else:
            logger.warning("Facebook access token not configured")
            results['facebook'] = False

        return results

    def post_to_platform(self, platform: str, post_data: Dict, image_path: Optional[str] = None) -> bool:
        if platform == 'linkedin':
            return self.linkedin_poster.post_content(post_data, image_path)
        if platform == 'twitter':
            return self.twitter_poster.post_content(post_data, image_path)
        if platform == 'facebook':
            return self.facebook_poster.post_content(post_data, image_path)
        logger.error(f"Unknown platform: {platform}")
        return False


