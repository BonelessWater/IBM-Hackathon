import os
import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from django.conf import settings
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
PROJECT_ID = os.getenv('PROJECT_ID')

"""
# Initialize Watson ModelInference
credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key=API_KEY,
)
client = APIClient(credentials)

model = ModelInference(
    model_id="ibm/granite-13b-chat-v2",
    api_client=client,
    project_id=PROJECT_ID,
    params={"max_new_tokens": 50},
)
"""

# Decorator to enforce login
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not settings.DEBUG or not request.session.get('user_id'):
            logger.info("Unauthorized access attempt to %s", request.path)
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def home(request):
    logger.info("User %s accessed the home page", request.session.get('user_id'))
    return render(request, 'home.html')

def signup(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = make_password(request.POST['password'])
        email = request.POST['email'].strip()
        address = request.POST['address'].strip()
        phone_number = request.POST['phone_number'].strip()
        emergency_contact_name = request.POST['emergency_contact_name'].strip()
        emergency_contact_phone = request.POST['emergency_contact_phone'].strip()

        if User.objects.filter(username__iexact=username).exists():
            error_message = f"Username '{username}' is already taken."
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
                error_message = "An error occurred during signup."
                logger.error("Signup failed due to IntegrityError: %s", str(e))

    return render(request, 'signup.html', {'error_message': error_message})

def login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            logger.info("User %s logged in", username)
            return redirect('home')
        else:
            error_message = "Invalid username or password."
            logger.warning("Failed login attempt for username %s", username)

    return render(request, 'login.html', {'error_message': error_message})

def logout(request):
    user_id = request.session.get('user_id')
    request.session.flush()
    logger.info("User %s logged out", user_id)
    return redirect('login')

"""
@csrf_exempt
def chatbot_message(request):

    if request.method == 'POST':
        try:
            user_message = json.loads(request.body).get('message', '')

            # Create the prompt for Watson
            prompt = (
    f"You are an expert disaster prevention assistant. Your role is to provide precise, actionable advice "
    f"for individuals facing natural disasters or emergencies. If the user needs emergency help, respond with "
    f"calm and helpful guidance. If the user seeks prevention tips, provide them with practical suggestions. "
    f"Use concise language and avoid unnecessary details. Now, respond to the following message:\n\n{user_message}"
)

            # Get Watson's generated response
            response = model.generate_text(prompt)

            # Ensure response is a string; return it directly
            if isinstance(response, str):
                watson_reply = response
            else:
                watson_reply = response.get('generated_text', "I'm not sure how to respond.")

            return JsonResponse({'response': watson_reply})
        except Exception as e:
            logger.error(f"Error in chatbot_message: {e}")
            return JsonResponse({'error': 'An error occurred while communicating with Watson.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

"""

