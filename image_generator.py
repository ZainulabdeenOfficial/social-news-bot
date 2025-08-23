import openai
import requests
import logging
from PIL import Image, ImageDraw, ImageFont
import io
import os
from typing import Optional, Tuple
from config import Config
import base64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.image_size = Config.IMAGE_SIZE
        self.style = Config.IMAGE_STYLE
    
    def generate_image(self, prompt: str, save_path: Optional[str] = None) -> Optional[str]:
        """Generate an image using DALL-E 3"""
        try:
            logger.info(f"Generating image with prompt: {prompt[:100]}...")
            
            # Enhance the prompt with style guidelines
            enhanced_prompt = self._enhance_prompt(prompt)
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size=f"{self.image_size[0]}x{self.image_size[1]}",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download and save the image
            if save_path:
                image_path = self._download_and_save_image(image_url, save_path)
                logger.info(f"Image saved to: {image_path}")
                return image_path
            else:
                return image_url
                
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return self._create_fallback_image(prompt, save_path)
    
    def _enhance_prompt(self, prompt: str) -> str:
        """Enhance the prompt with style guidelines"""
        enhanced = f"""
{prompt}

Style requirements:
- {self.style}
- High quality, professional appearance
- Clean, modern design
- Suitable for social media platforms
- Engaging and visually appealing
- No text overlays (we'll add them separately)
- Optimized for {self.image_size[0]}x{self.image_size[1]} pixels
"""
        return enhanced.strip()
    
    def _download_and_save_image(self, image_url: str, save_path: str) -> str:
        """Download and save image from URL"""
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Save the image
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return save_path
            
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
            raise
    
    def create_image_with_text(self, base_image_path: str, text: str, output_path: str) -> str:
        """Add text overlay to an image"""
        try:
            # Open the base image
            with Image.open(base_image_path) as img:
                # Create a copy to work with
                img_copy = img.copy()
                
                # Create a drawing object
                draw = ImageDraw.Draw(img_copy)
                
                # Calculate font size based on image dimensions
                font_size = min(img_copy.size) // 20
                
                # Try to use a professional font, fallback to default
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # Calculate text position (center)
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (img_copy.width - text_width) // 2
                y = img_copy.height - text_height - 50  # 50px from bottom
                
                # Add text shadow for better readability
                shadow_offset = 2
                draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill='black')
                draw.text((x, y), text, font=font, fill='white')
                
                # Save the result
                img_copy.save(output_path)
                
                logger.info(f"Image with text saved to: {output_path}")
                return output_path
                
        except Exception as e:
            logger.error(f"Error adding text to image: {e}")
            return base_image_path
    
    def _create_fallback_image(self, prompt: str, save_path: Optional[str] = None) -> Optional[str]:
        """Create a simple fallback image when DALL-E fails"""
        try:
            # Create a simple gradient image
            img = Image.new('RGB', self.image_size, color='#1a1a1a')
            draw = ImageDraw.Draw(img)
            
            # Add a gradient effect
            for y in range(self.image_size[1]):
                # Create a subtle gradient
                r = int(26 + (y / self.image_size[1]) * 50)
                g = int(26 + (y / self.image_size[1]) * 50)
                b = int(26 + (y / self.image_size[1]) * 50)
                draw.line([(0, y), (self.image_size[0], y)], fill=(r, g, b))
            
            # Add some tech-themed elements
            # Draw a simple circuit pattern
            for i in range(0, self.image_size[0], 50):
                for j in range(0, self.image_size[1], 50):
                    draw.rectangle([i, j, i+2, j+2], fill='#00ff00')
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 30)
            except:
                font = ImageFont.load_default()
            
            text = "Tech News"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (self.image_size[0] - text_width) // 2
            y = self.image_size[1] // 2
            
            draw.text((x, y), text, font=font, fill='white')
            
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                img.save(save_path)
                return save_path
            else:
                # Save to temporary file and return path
                temp_path = "temp_fallback_image.png"
                img.save(temp_path)
                return temp_path
                
        except Exception as e:
            logger.error(f"Error creating fallback image: {e}")
            return None
    
    def create_carousel_image(self, articles: list, output_path: str) -> str:
        """Create a carousel image with multiple articles"""
        try:
            # Create a wide image for carousel
            carousel_size = (1080, 1080)  # Instagram carousel size
            img = Image.new('RGB', carousel_size, color='#ffffff')
            draw = ImageDraw.Draw(img)
            
            # Calculate layout
            num_articles = min(len(articles), 3)  # Max 3 articles per carousel
            section_height = carousel_size[1] // num_articles
            
            try:
                title_font = ImageFont.truetype("arial.ttf", 24)
                source_font = ImageFont.truetype("arial.ttf", 16)
            except:
                title_font = ImageFont.load_default()
                source_font = ImageFont.load_default()
            
            for i, article in enumerate(articles[:num_articles]):
                y_start = i * section_height
                y_end = (i + 1) * section_height
                
                # Add background color for each section
                colors = ['#f0f8ff', '#f5f5f5', '#fff8f0']
                draw.rectangle([0, y_start, carousel_size[0], y_end], fill=colors[i % len(colors)])
                
                # Add title
                title = article['title'][:60] + "..." if len(article['title']) > 60 else article['title']
                draw.text((20, y_start + 20), title, font=title_font, fill='#333333')
                
                # Add source
                draw.text((20, y_start + 60), f"Source: {article['source']}", font=source_font, fill='#666666')
                
                # Add separator line
                if i < num_articles - 1:
                    draw.line([(0, y_end), (carousel_size[0], y_end)], fill='#cccccc', width=2)
            
            # Save the carousel image
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path)
            
            logger.info(f"Carousel image saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating carousel image: {e}")
            return self._create_fallback_image("Tech news carousel", output_path)
    
    def optimize_for_platform(self, image_path: str, platform: str) -> str:
        """Optimize image for specific social media platform"""
        try:
            with Image.open(image_path) as img:
                # Platform-specific optimizations
                if platform == 'linkedin':
                    # LinkedIn: 1200x630
                    target_size = (1200, 630)
                elif platform == 'twitter':
                    # Twitter: 1200x675
                    target_size = (1200, 675)
                elif platform == 'facebook':
                    # Facebook: 1200x630
                    target_size = (1200, 630)
                elif platform == 'instagram':
                    # Instagram: 1080x1080
                    target_size = (1080, 1080)
                else:
                    target_size = self.image_size
                
                # Resize image maintaining aspect ratio
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                
                # Create new image with target size and paste resized image
                new_img = Image.new('RGB', target_size, color='#ffffff')
                paste_x = (target_size[0] - img.width) // 2
                paste_y = (target_size[1] - img.height) // 2
                new_img.paste(img, (paste_x, paste_y))
                
                # Save optimized image
                optimized_path = image_path.replace('.png', f'_{platform}.png')
                new_img.save(optimized_path, quality=95, optimize=True)
                
                logger.info(f"Image optimized for {platform}: {optimized_path}")
                return optimized_path
                
        except Exception as e:
            logger.error(f"Error optimizing image for {platform}: {e}")
            return image_path

if __name__ == "__main__":
    # Test the image generator
    generator = ImageGenerator()
    
    # Test image generation
    test_prompt = "Modern tech illustration: AI and machine learning, professional design, clean layout"
    image_path = generator.generate_image(test_prompt, "test_image.png")
    
    if image_path:
        print(f"Image generated successfully: {image_path}")
        
        # Test adding text
        text_image_path = generator.create_image_with_text(
            image_path, 
            "AI News", 
            "test_image_with_text.png"
        )
        print(f"Image with text: {text_image_path}")
    else:
        print("Failed to generate image")
