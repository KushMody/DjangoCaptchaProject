# captcha/views.py

from django.shortcuts import render
from .models import Captcha

def get_captcha_image(request):
    image_path, captcha_text = Captcha.generate_captcha()

    # Store CAPTCHA text in session for later validation
    request.session['captcha_text'] = captcha_text

    return render(request, 'captcha/captcha_image.html', {'image_path': image_path})