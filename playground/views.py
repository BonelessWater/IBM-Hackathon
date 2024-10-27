import os
import json
import logging
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.client import ibm_watsonx_ai
from ibm_watsonx_ai.foundation_models import ModelInference
from django.conf import settings
from .models import User, InventoryItem
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from locate_nearby_resources import available_gas_stations, shelter_finnder, hospital_finder, location_to_latlong

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Decorator to enforce login
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        # If in DEBUG mode, skip login check
        if settings.DEBUG:
            logger.info("DEBUG mode enabled, bypassing login for %s", request.path)
            return view_func(request, *args, **kwargs)

        # If not in DEBUG, enforce login
        if not request.session.get('user_id'):
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
        password = request.POST['password']
        hashed_password = make_password(password)  # Ensure password is hashed
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
                    password=hashed_password,  # Store the hashed password
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

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use Django's login() function
            return redirect('resources')
        else:
            error_message = "Invalid username or password."

    return render(request, 'login.html', {'error_message': error_message})

def logout(request):
    user_id = request.session.get('user_id')
    request.session.flush()
    logger.info("User %s logged out", user_id)
    return redirect('login')

@csrf_exempt
def chatbot_message(request):
    API_KEY = os.getenv('API_KEY')
    PROJECT_ID = os.getenv('PROJECT_ID')

    logger.info(API_KEY)
    logger.info(API_KEY)
    logger.info(API_KEY)

    logger.info(PROJECT_ID)
    logger.info(PROJECT_ID)
    logger.info(PROJECT_ID)

    if request.method == 'POST':
        try:
            # Initialize Watson ModelInference inside the function
            credentials = ibm_watsonx_ai.Credentials(
                url="https://us-south.ml.cloud.ibm.com",
                api_key=API_KEY,
            )
            client = APIClient(credentials)

            model = ModelInference(
                model_id="ibm/granite-13b-chat-v2",
                api_client=client,
                project_id=PROJECT_ID,
                params={"max_new_tokens": 8000},
            )

            # Extract user message from the request
            user_message = json.loads(request.body).get('message', '')

            # Create the prompt for Watson
            prompt = f"""
            You are a crisis assistant designed to provide direct and practical support during emergencies. Respond to the user's inquiries with relevant and actionable advice.

            Instructions:
            - If the user expresses urgency or asks for immediate help, respond with concise and relevant information without initiating self-dialogue.
            - If the user cannot get matched with assistance, offer clear and practical steps they can take to prepare for the storm, including:
            - Gathering emergency supplies
            - Securing their home
            - Creating an emergency plan
            - If the user's request is ambiguous, ask gently for clarification to better assist them.
            - Maintain a calm and supportive tone throughout the interaction.

            For this message:
            "{user_message}"

            Provide a direct, helpful response to address the user's need.
            """

            # Generate Watson's response
            response = model.generate_text(prompt)

            # Ensure response is correctly formatted
            if isinstance(response, str):
                watson_reply = response
            else:
                watson_reply = response.get('generated_text', "I'm not sure how to respond.")

            return JsonResponse({'response': watson_reply})
        except Exception as e:
            logger.error(f"Error in chatbot_message: {e}")
            return JsonResponse({'error': 'An error occurred while communicating with Watson.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def update_user_state(request):
    """Update the user's state."""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Return a friendly response or handle anonymous users gracefully
            return JsonResponse({'error': 'You need to log in to change your state.'}, status=401)

        state = request.POST.get('state')
        if state in ['neither', 'help', 'helper']:
            request.user.state = state  # Only modify if the user is authenticated
            request.user.save()
            logger.info("User %s changed state to %s", request.user.username, state)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid state provided.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def add_inventory(request):
    """Allows helpers to add inventory items."""
    if request.method == 'POST':
        if request.user.state == 'helper':
            item_name = request.POST.get('item_name')
            quantity = int(request.POST.get('quantity', 0))
            
            if item_name and quantity > 0:
                InventoryItem.objects.create(name=item_name, quantity=quantity)
                logger.info("User %s added %s (x%s) to inventory", request.user.username, item_name, quantity)
            else:
                logger.warning("Invalid inventory data provided by %s", request.user.username)
        else:
            logger.warning("Unauthorized attempt to add inventory by %s", request.user.username)
    return redirect('home')

@csrf_exempt
def request_item(request, item_id):
    """Allows users in need to request items from the inventory."""
    if request.method == 'POST':
        if request.user.state == 'help':
            item = get_object_or_404(InventoryItem, id=item_id)
            if item.quantity > 0:
                item.quantity -= 1
                item.save()
                logger.info("User %s requested %s", request.user.username, item.name)
            else:
                logger.warning("User %s tried to request %s but it's out of stock", request.user.username, item.name)
        else:
            logger.warning("Unauthorized request attempt by %s", request.user.username)
    return redirect('home')

@csrf_exempt
def update_user_state(request):
    """Update the user's state."""
    if request.method == 'POST':
        state = request.POST.get('state')
        if state in ['neither', 'help', 'helper']:
            request.user.state = state
            request.user.save()
            logger.info("User %s changed state to %s", request.user.username, state)
            return redirect('home')
    return JsonResponse({'error': 'Invalid state'}, status=400)

def resources(request):
    # Mock data for shelters, hospitals, and gas stations
    shelters = [
        {'name': 'Gainesville Shelter A', 'address': '1234 Shelter Rd', 'distance': 1.2, 'contact': '352-123-4567'},
        {'name': 'Gainesville Shelter B', 'address': '5678 Safe Haven St', 'distance': 2.1, 'contact': '352-987-6543'},
        {'name': 'Gainesville Shelter C', 'address': '4321 Shelter Ct', 'distance': 2.5, 'contact': '352-555-1212'},
        {'name': 'Gainesville Shelter D', 'address': '9101 Refuge Ln', 'distance': 3.0, 'contact': '352-444-3333'},
        {'name': 'Gainesville Shelter E', 'address': '2020 Safety Ave', 'distance': 3.8, 'contact': '352-111-2222'},
    ]

    hospitals = [
        {'name': 'UF Health Shands Hospital', 'address': '1600 SW Archer Rd', 'distance': 1.1, 'contact': '352-265-0111'},
        {'name': 'North Florida Regional Medical', 'address': '6500 W Newberry Rd', 'distance': 3.5, 'contact': '352-333-4000'},
        {'name': 'VA Medical Center', 'address': '1601 SW Archer Rd', 'distance': 1.2, 'contact': '352-376-1611'},
        {'name': 'Gainesville Urgent Care', 'address': '9200 NW 39th Ave', 'distance': 4.5, 'contact': '352-332-1890'},
        {'name': 'Alachua General Hospital', 'address': '701 NW 1st St', 'distance': 2.8, 'contact': '352-338-0022'},
    ]

    gas_stations = [
        {'name': 'Shell Gas Station', 'address': '1001 NW 13th St', 'distance': 1.5, 'contact': '352-378-0222'},
        {'name': 'Chevron', 'address': '2002 SW Archer Rd', 'distance': 1.8, 'contact': '352-123-4567'},
        {'name': 'BP Gas', 'address': '3003 NW 6th St', 'distance': 2.2, 'contact': '352-444-5555'},
        {'name': 'Circle K', 'address': '4004 SW 20th Ave', 'distance': 3.1, 'contact': '352-555-6666'},
        {'name': 'Wawa', 'address': '5005 University Ave', 'distance': 2.7, 'contact': '352-777-8888'},
    ]

    context = {
        'shelters': shelters,
        'hospitals': hospitals,
        'gas_stations': gas_stations,
    }

    return render(request, 'resources.html', context)

def prevention(request):
    return render(request, 'prevention.html')
