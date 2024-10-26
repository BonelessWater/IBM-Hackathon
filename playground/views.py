from django.conf import settings  # To access the DEBUG setting
from django.shortcuts import render, redirect
from .models import User

# Control whether login is enforced during debug mode
ENFORCE_LOGIN_DEBUG = False  # Change this to True to enforce login while debugging

def login_required(view_func):
    """Decorator to enforce login based on debug mode and settings."""
    def wrapper(request, *args, **kwargs):
        # Enforce login only if DEBUG is False or ENFORCE_LOGIN_DEBUG is True
        if not settings.DEBUG or ENFORCE_LOGIN_DEBUG:
            if not request.session.get('user_id'):
                return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def home(request):
    """Home view, accessible only when logged in (if conditions apply)."""
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        emergency_contact_name = request.POST['emergency_contact_name']
        emergency_contact_phone = request.POST['emergency_contact_phone']

        User.objects.create(
            username=username,
            password=password,
            email=email,
            address=address,
            phone_number=phone_number,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
        )
        return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_id'] = user.id  # Simple session tracking
            return redirect('home')

    return render(request, 'login.html')

def logout(request):
    request.session.flush()  # Clear the session
    return redirect('login')
