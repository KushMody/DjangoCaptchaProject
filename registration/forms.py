# registration/forms.py

from django import forms
from captcha.models import Captcha

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = forms.CharField(max_length=6)

    def clean_captcha(self):
        input_captcha = self.cleaned_data['captcha']
        session_captcha = self.data.get('session_captcha')  # Get the session CAPTCHA text

        # Validate the CAPTCHA input
        if not Captcha.validate_captcha(input_captcha, session_captcha):
            raise forms.ValidationError('Invalid CAPTCHA. Please try again.')

        return input_captcha
