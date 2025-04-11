import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

class Captcha:
    @staticmethod
    def generate_captcha():
        # Generate a random string for the CAPTCHA
        captcha_text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))

        # Create an image with a white background
        image = Image.new('RGB', (250, 100), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Load a TrueType font with variable size
        font_path = "arial.ttf"  # Path to the font file
        font_size = random.randint(27, 35)  # Variable font size for complexity
        font = ImageFont.truetype(font_path, font_size)

        # Draw each character with random rotation and position
        for i, char in enumerate(captcha_text):
            char_x = 20 + i * 40  # Adjust the spacing between characters
            char_y = random.randint(10, 30)  # Random vertical position
            angle = random.randint(-30, 30)  # Random angle for rotation

            # Create a temporary image to rotate the text
            temp_image = Image.new('RGBA', (60, 60), (255, 255, 255, 0))  # Transparent background
            temp_draw = ImageDraw.Draw(temp_image)
            temp_draw.text((10, 10), char, font=font, fill=(0, 0, 0))
            rotated_image = temp_image.rotate(angle, resample=Image.BICUBIC, expand=1)

            # Paste rotated character onto main image
            image.paste(rotated_image, (char_x, char_y), rotated_image)

        # Add random noise (dots)
        for _ in range(100):  # Number of dots
            x = random.randint(0, image.width)
            y = random.randint(0, image.height)
            draw.point((x, y), fill=(0, 0, 0))

        # Add random lines
        for _ in range(5):  # Number of lines
            x1, y1 = random.randint(0, image.width), random.randint(0, image.height)
            x2, y2 = random.randint(0, image.width), random.randint(0, image.height)
            draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)

        # Apply slight blur to the entire image
        image = image.filter(ImageFilter.GaussianBlur(1))

        # Save the image to a bytes buffer
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)

        return buf, captcha_text
