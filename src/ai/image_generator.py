import logging
import os
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from src.config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self):
        self.image_size = Config.IMAGE_SIZE
        self.style = Config.IMAGE_STYLE

    def generate_image(self, prompt: str, save_path: Optional[str] = None) -> Optional[str]:
        """Fallback local image generation (free)."""
        try:
            return self._create_fallback_image(prompt, save_path)
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None

    def _create_fallback_image(self, prompt: str, save_path: Optional[str]) -> Optional[str]:
        img = Image.new('RGB', self.image_size, color='#1a1a1a')
        draw = ImageDraw.Draw(img)

        # Subtle gradient
        for y in range(self.image_size[1]):
            val = int(26 + (y / max(1, self.image_size[1])) * 50)
            draw.line([(0, y), (self.image_size[0], y)], fill=(val, val, val))

        # Tech dots
        step = max(40, min(self.image_size) // 20)
        for i in range(0, self.image_size[0], step):
            for j in range(0, self.image_size[1], step):
                draw.rectangle([i, j, i+2, j+2], fill='#00ff88')

        # Title text
        text = "Tech News"
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        x = (self.image_size[0] - (bbox[2] - bbox[0])) // 2
        y = self.image_size[1] // 2
        draw.text((x, y), text, font=font, fill='white')

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            img.save(save_path)
            return save_path
        temp_path = "temp_fallback_image.png"
        img.save(temp_path)
        return temp_path

    def optimize_for_platform(self, image_path: str, platform: str) -> str:
        try:
            with Image.open(image_path) as img:
                if platform == 'linkedin':
                    target_size = (1200, 630)
                elif platform == 'twitter':
                    target_size = (1200, 675)
                elif platform == 'facebook':
                    target_size = (1200, 630)
                else:
                    target_size = self.image_size

                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                new_img = Image.new('RGB', target_size, color='#ffffff')
                paste_x = (target_size[0] - img.width) // 2
                paste_y = (target_size[1] - img.height) // 2
                new_img.paste(img, (paste_x, paste_y))
                optimized_path = image_path.replace('.png', f'_{platform}.png')
                new_img.save(optimized_path, quality=95, optimize=True)
                return optimized_path
        except Exception:
            return image_path


