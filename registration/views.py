# registration/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Import the User model
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .captcha import Captcha  # Import the custom Captcha class from captcha.py
import base64

def register(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['session_captcha'] = request.session.get('captcha_text', '')  # Add session CAPTCHA text

        form = RegistrationForm(post_data)
        if form.is_valid():
            # Extract cleaned data from the form
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists. Please choose another one.')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists. Please choose another one.')
            else:
                # Create a new user and save to SQLite database
                User.objects.create_user(username=username, email=email, password=password)
                return redirect('success')  # Redirect to the success page if registration is successful
    else:
        form = RegistrationForm()

    # Generate new CAPTCHA for the form
    captcha_image, captcha_text = Captcha.generate_captcha()
    request.session['captcha_text'] = captcha_text  # Store CAPTCHA text in session

    # Encode the image to base64
    captcha_image_base64 = base64.b64encode(captcha_image.getvalue()).decode('utf-8')

    return render(request, 'registration/register.html', {'form': form, 'captcha_image': captcha_image_base64})

# Define the success view
def success(request):
    return render(request, 'registration/success.html')  # Render a success template

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('congrats')  # Redirect to the congratulations page
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials.'})
    return render(request, 'registration/login.html')

def congrats(request):
    return render(request, 'registration/congrats.html')