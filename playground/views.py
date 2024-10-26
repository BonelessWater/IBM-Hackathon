from django.conf import settings  # To access the DEBUG setting
from django.shortcuts import render, redirect
from .models import User
import os
from django.conf import settings
from django.http import JsonResponse
from django.http import JsonResponse
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

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


def process_audio(request):
    """Process the uploaded audio file and delete it after processing."""
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']

        # Save the uploaded audio file temporarily
        temp_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        with open(temp_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Process the file (for now, just print success and return True)
        print("Audio file processed successfully!")

        # Delete the file after processing
        os.remove(temp_path)
        print("Temporary audio file deleted.")

        return JsonResponse({'success': True, 'message': 'Audio processed successfully'})

    return JsonResponse({'success': False, 'message': 'No audio file uploaded'}, status=400)
