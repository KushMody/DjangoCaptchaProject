# captcha/models.py

from PIL import Image, ImageDraw, ImageFont
import random, string
import io

class Captcha:
    @staticmethod
    def generate_captcha():
        # Generate random CAPTCHA text
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Create an image with the CAPTCHA text
        image = Image.new('RGB', (200, 50), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()  # Load a default font

        draw.text((10, 10), captcha_text, font=font, fill=(0, 0, 0))

        # Use BytesIO to create an in-memory image
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)  # Move to the beginning of the BytesIO stream

        # Return the in-memory image and the CAPTCHA text
        return image_bytes, captcha_text  # Return the BytesIO object and the text
    @staticmethod
    def validate_captcha(input_captcha, session_captcha):
        """Check if the provided CAPTCHA input matches the stored CAPTCHA text."""
        return input_captcha == session_captcha