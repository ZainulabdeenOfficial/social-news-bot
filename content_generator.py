import openai
import logging
from typing import Dict, List, Optional
from config import Config
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_post_content(self, article: Dict, platform: str) -> Dict:
        """Generate engaging social media post content from an article"""
        try:
            logger.info(f"Generating {platform} post for: {article['title']}")
            
            # Create prompt based on platform
            prompt = self._create_prompt(article, platform)
            
            # Generate content using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional tech content creator who writes engaging social media posts. Write in a conversational, informative tone that encourages engagement."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            generated_content = response.choices[0].message.content.strip()
            
            # Parse the response
            post_data = self._parse_generated_content(generated_content, platform)
            
            # Add article metadata
            post_data.update({
                'original_article': article,
                'platform': platform,
                'generated_at': datetime.now().isoformat()
            })
            
            logger.info(f"Successfully generated {platform} post")
            return post_data
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return self._create_fallback_post(article, platform)
    
    def _create_prompt(self, article: Dict, platform: str) -> str:
        """Create platform-specific prompt for content generation"""
        
        platform_guidelines = {
            'linkedin': {
                'tone': 'professional and insightful',
                'length': '2-3 paragraphs',
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
Create an engaging {platform} post about this tech news article:

Title: {article['title']}
Description: {article['description']}
Source: {article['source']}
Link: {article['link']}

Requirements:
- Tone: {guidelines['tone']}
- Length: {guidelines['length']}
- Include {guidelines['hashtags']}
- {guidelines['call_to_action']}
- Make it engaging and shareable
- Include the article link at the end

Format the response as JSON with these fields:
{{
    "post_text": "the main post content",
    "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
    "call_to_action": "brief call to action",
    "image_prompt": "description for generating an image"
}}
"""
        return prompt
    
    def _parse_generated_content(self, content: str, platform: str) -> Dict:
        """Parse the generated content from OpenAI response"""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return parsed
            else:
                # Fallback parsing
                return self._fallback_parsing(content, platform)
                
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback parsing")
            return self._fallback_parsing(content, platform)
    
    def _fallback_parsing(self, content: str, platform: str) -> Dict:
        """Fallback parsing when JSON parsing fails"""
        # Extract hashtags
        hashtags = re.findall(r'#\w+', content)
        
        # Remove hashtags from main content
        post_text = re.sub(r'#\w+', '', content).strip()
        
        # Generate image prompt
        image_prompt = f"Tech news illustration: {post_text[:100]}..."
        
        return {
            'post_text': post_text,
            'hashtags': hashtags,
            'call_to_action': "What do you think about this? Share your thoughts below! 👇",
            'image_prompt': image_prompt
        }
    
    def _create_fallback_post(self, article: Dict, platform: str) -> Dict:
        """Create a simple fallback post when AI generation fails"""
        post_text = f"🚀 {article['title']}\n\n{article['description'][:200]}...\n\nRead more: {article['link']}"
        
        hashtags = ['#TechNews', '#Innovation', '#Technology']
        if platform == 'linkedin':
            hashtags.extend(['#LinkedIn', '#ProfessionalDevelopment'])
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
    
    def generate_image_prompt(self, article: Dict, post_content: str) -> str:
        """Generate a detailed prompt for image generation"""
        try:
            prompt = f"""
Create a detailed image prompt for a tech news article:

Article: {article['title']}
Content: {post_content[:200]}

Generate a professional, modern image that represents this tech news story.
Style: {Config.IMAGE_STYLE}
Size: {Config.IMAGE_SIZE[0]}x{Config.IMAGE_SIZE[1]} pixels

Focus on:
- Modern, clean design
- Tech-related visual elements
- Professional appearance
- Engaging colors
- Suitable for social media
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at creating detailed image generation prompts for tech content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating image prompt: {e}")
            return f"Modern tech illustration: {article['title']}, professional design, clean layout"
    
    def generate_daily_summary(self, articles: List[Dict]) -> Dict:
        """Generate a daily summary of top tech news"""
        try:
            # Select top 5 articles
            top_articles = articles[:5]
            
            summary_prompt = f"""
Create a daily tech news summary based on these top stories:

{chr(10).join([f"{i+1}. {article['title']} ({article['source']})" for i, article in enumerate(top_articles)])}

Create an engaging summary that:
- Highlights the most important tech developments
- Connects the stories to broader tech trends
- Encourages engagement and discussion
- Uses a professional yet conversational tone
- Includes relevant hashtags

Format as JSON:
{{
    "summary_title": "catchy title",
    "summary_text": "main summary content",
    "key_takeaways": ["takeaway1", "takeaway2", "takeaway3"],
    "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
    "call_to_action": "engagement prompt"
}}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a tech news analyst who creates engaging daily summaries."
                    },
                    {
                        "role": "user",
                        "content": summary_prompt
                    }
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_generated_content(content, 'linkedin')
            
        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")
            return self._create_fallback_summary(articles)
    
    def _create_fallback_summary(self, articles: List[Dict]) -> Dict:
        """Create a simple fallback daily summary"""
        summary_text = "📰 Today's Top Tech News:\n\n"
        for i, article in enumerate(articles[:5], 1):
            summary_text += f"{i}. {article['title']}\n"
        
        summary_text += "\nStay updated with the latest in technology! 🚀"
        
        return {
            'summary_title': "Today's Tech Roundup",
            'summary_text': summary_text,
            'key_takeaways': ["Tech innovation continues", "AI developments", "Industry trends"],
            'hashtags': ['#TechNews', '#DailyRoundup', '#Innovation'],
            'call_to_action': "Which story interests you most? Share your thoughts! 💭"
        }

if __name__ == "__main__":
    # Test the content generator
    from datetime import datetime
    
    generator = ContentGenerator()
    
    # Test article
    test_article = {
        'title': 'OpenAI Releases GPT-5 with Revolutionary Capabilities',
        'description': 'OpenAI has announced the release of GPT-5, featuring unprecedented reasoning abilities and multimodal understanding.',
        'source': 'TechCrunch',
        'link': 'https://example.com/article'
    }
    
    # Generate LinkedIn post
    linkedin_post = generator.generate_post_content(test_article, 'linkedin')
    print("LinkedIn Post:")
    print(json.dumps(linkedin_post, indent=2))
    print()
    
    # Generate Twitter post
    twitter_post = generator.generate_post_content(test_article, 'twitter')
    print("Twitter Post:")
    print(json.dumps(twitter_post, indent=2))
