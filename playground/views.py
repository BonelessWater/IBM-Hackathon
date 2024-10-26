from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
from pathlib import Path
from datetime import datetime, timedelta, date
import json
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'home.html')