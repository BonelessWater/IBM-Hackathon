import logging
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User

logger = logging.getLogger(__name__)

# Control whether login is enforced during debug mode
ENFORCE_LOGIN_DEBUG = True

def login_required(view_func):
    """Decorator to enforce login based on debug mode and settings."""
    def wrapper(request, *args, **kwargs):
        if not settings.DEBUG or ENFORCE_LOGIN_DEBUG:
            if not request.session.get('user_id'):
                logger.info("Unauthorized access attempt to %s", request.path)
                return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def home(request):
    """Home view, accessible only when logged in."""
    logger.info("User %s accessed the home page", request.session.get('user_id'))
    return render(request, 'home.html')

def signup(request):
    """Handles user signup."""
    error_message = None  # Initialize error message

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = make_password(request.POST['password'])
        email = request.POST['email'].strip()
        address = request.POST['address'].strip()
        phone_number = request.POST['phone_number'].strip()
        emergency_contact_name = request.POST['emergency_contact_name'].strip()
        emergency_contact_phone = request.POST['emergency_contact_phone'].strip()

        # Check if the username exists (case-insensitive)
        if User.objects.filter(username__iexact=username).exists():
            error_message = f"Username '{username}' is already taken. Please choose a different one."
            logger.warning("Signup failed: username %s already exists", username)
        else:
            try:
                User.objects.create(
                    username=username,
                    password=password,
                    email=email,
                    address=address,
                    phone_number=phone_number,
                    emergency_contact_name=emergency_contact_name,
                    emergency_contact_phone=emergency_contact_phone,
                )
                logger.info("New user %s signed up", username)
                return redirect('login')

            except IntegrityError as e:
                error_message = "An error occurred during signup. Please try again."
                logger.error("Signup failed due to IntegrityError: %s", str(e))

    return render(request, 'signup.html', {'error_message': error_message})

def login(request):
    """Handles user login."""
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id  # Track user session
            logger.info("User %s logged in", username)
            return redirect('/')  # Redirect to the base URL
        else:
            error_message = "Invalid username or password. Please try again."
            logger.warning("Failed login attempt for username %s", username)

    return render(request, 'login.html', {'error_message': error_message})

def logout(request):
    """Handles user logout."""
    user_id = request.session.get('user_id')
    request.session.flush()  # Clear the session
    logger.info("User %s logged out", user_id)
    return redirect('login')
