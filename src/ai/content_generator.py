import logging
import json
import re
from datetime import datetime
from typing import Dict, List

import google.generativeai as genai

from src.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentGenerator:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set. Content generation will use fallback.")
        else:
            genai.configure(api_key=Config.GEMINI_API_KEY)
        # Use a generally available text model
        self.model_name = getattr(Config, 'GEMINI_TEXT_MODEL', 'gemini-1.5-flash')

    def generate_post_content(self, article: Dict, platform: str) -> Dict:
        try:
            logger.info(f"Generating {platform} post (Gemini) for: {article['title']}")

            prompt = self._create_prompt(article, platform)

            if not Config.GEMINI_API_KEY:
                raise RuntimeError("Missing GEMINI_API_KEY")

            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)

            generated_content = (response.text or "").strip()
            post_data = self._parse_generated_content(generated_content, platform)

            post_data.update({
                'original_article': article,
                'platform': platform,
                'generated_at': datetime.now().isoformat()
            })

            logger.info(f"Successfully generated {platform} post (Gemini)")
            return post_data

        except Exception as e:
            logger.error(f"Error generating content via Gemini: {e}")
            return self._create_fallback_post(article, platform)

    def _create_prompt(self, article: Dict, platform: str) -> str:
        platform_guidelines = {
            'linkedin': {
                'tone': 'professional and insightful',
                'length': '2-3 short paragraphs',
                'hashtags': '3-5 relevant hashtags',
                'call_to_action': 'encourage comments and shares'
            },
            'twitter': {
                'tone': 'concise and engaging',
                'length': 'within 280 characters',
                'hashtags': '2-3 relevant hashtags',
                'call_to_action': 'encourage retweets and replies'
            },
            'facebook': {
                'tone': 'friendly and informative',
                'length': '1-2 paragraphs',
                'hashtags': '2-4 relevant hashtags',
                'call_to_action': 'encourage likes and comments'
            }
        }

        guidelines = platform_guidelines.get(platform, platform_guidelines['linkedin'])

        prompt = f"""
You are a tech social media copywriter. Write an engaging {platform} post about this tech news article.

Article:
- Title: {article['title']}
- Description: {article['description']}
- Source: {article['source']}
- Link: {article['link']}

Requirements:
- Tone: {guidelines['tone']}
- Length: {guidelines['length']}
- Include {guidelines['hashtags']}
- {guidelines['call_to_action']}
- Keep it clear, scannable, and informative
- Add the article link at the end

Respond ONLY with JSON in the following schema:
{{
  "post_text": "the main post content",
  "hashtags": ["#tag1", "#tag2", "#tag3"],
  "call_to_action": "brief call to action",
  "image_prompt": "description for generating a matching image"
}}
"""
        return prompt

    def _parse_generated_content(self, content: str, platform: str) -> Dict:
        try:
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                return json.loads(json_match.group())
            return self._fallback_parsing(content, platform)
        except Exception:
            return self._fallback_parsing(content, platform)

    def _fallback_parsing(self, content: str, platform: str) -> Dict:
        hashtags = re.findall(r'#\w+', content)
        post_text = re.sub(r'#\w+', '', content).strip()
        image_prompt = f"Tech news illustration: {post_text[:100]}..." if post_text else "Modern tech illustration"
        return {
            'post_text': post_text or 'Tech update inside. Read more at the link below.',
            'hashtags': hashtags or ['#TechNews', '#Innovation'],
            'call_to_action': 'What do you think? Share your thoughts below! 👇',
            'image_prompt': image_prompt
        }

    def _create_fallback_post(self, article: Dict, platform: str) -> Dict:
        post_text = f"🚀 {article['title']}\n\n{article['description'][:200]}...\n\nRead more: {article['link']}"
        hashtags = ['#TechNews', '#Innovation', '#Technology']
        if platform == 'linkedin':
            hashtags.extend(['#LinkedIn'])
        elif platform == 'twitter':
            hashtags.extend(['#Tech', '#News'])
        return {
            'post_text': post_text,
            'hashtags': hashtags,
            'call_to_action': "What's your take on this? Comment below! 💬",
            'image_prompt': f"Modern tech illustration for: {article['title']}",
            'original_article': article,
            'platform': platform,
            'generated_at': datetime.now().isoformat()
        }

    def generate_daily_summary(self, articles: List[Dict]) -> Dict:
        try:
            if not Config.GEMINI_API_KEY:
                raise RuntimeError("Missing GEMINI_API_KEY")
            top_articles = articles[:5]
            summary_lines = "\n".join([f"- {a['title']} ({a['source']})" for a in top_articles])
            prompt = f"""
Create a daily tech news summary based on these stories:

{summary_lines}

Respond ONLY with JSON:
{{
  "summary_title": "catchy title",
  "summary_text": "main summary content",
  "key_takeaways": ["takeaway1", "takeaway2", "takeaway3"],
  "hashtags": ["#tag1", "#tag2"],
  "call_to_action": "engagement prompt"
}}
"""
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            content = (response.text or "").strip()
            parsed = self._parse_generated_content(content, 'linkedin')
            return parsed
        except Exception as e:
            logger.error(f"Error generating daily summary via Gemini: {e}")
            return {
                'summary_title': "Today's Tech Roundup",
                'summary_text': "\n".join([f"• {a['title']}" for a in articles[:5]]),
                'key_takeaways': ["Tech innovation continues", "AI developments", "Industry trends"],
                'hashtags': ['#TechNews', '#DailyRoundup', '#Innovation'],
                'call_to_action': 'Which story interests you most? 💭'
            }


