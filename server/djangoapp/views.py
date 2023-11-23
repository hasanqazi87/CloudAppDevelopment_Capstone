from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from operator import itemgetter
import logging
import json
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)

DEALERSHIP_URL = 'https://hasanqazi87-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership'
REVIEW_URL = 'https://hasanqazi87-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review'


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')


# Create a `login_request` view to handle sign in request
def login_request(request):
    username, password = itemgetter('username', 'passwd')(request.POST)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('djangoapp:index'))
    return redirect(reverse('djangoapp:signup'))


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect(reverse('djangoapp:index'))


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        username, firstname, lastname, password = itemgetter('username', 'firstname', 'lastname', 'passwd')(request.POST)
        User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
        return redirect(reverse('djangoapp:index'))
    return render(request, 'djangoapp/registration.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        dealerships = get_dealers_from_cf(DEALERSHIP_URL, **request.GET)
        return HttpResponse(dealerships)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    reviews = get_dealer_reviews_from_cf(REVIEW_URL, dealer_id=dealer_id)
    return HttpResponse(reviews)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        return redirect(reverse('djangoapp:index'))
    if request.method == 'GET':
        # post_data = request.POST
        # Frontend form not built yet, using hardcoded example data to test the view
        json_payload = {
                "time": datetime.utcnow().isoformat(),
                "id": 4270,
                "name": "Hasan",
                "dealership": dealer_id,
                "review": "Excellent service",
                "purchase": False,
                "purchase_date": "2022-10-31",
                "car_make": "Acura",
                "car_model": "TLX",
                "car_year": "2023"
        }
        # json_payload = {
        #     'review': {
        #         'time': datetime.utcnow().isoformat(),
        #         'id': post_data['id'],
        #         'name': post_data['name'],
        #         'dealership': dealer_id,
        #         'review': post_data['review'],
        #         'purchase': post_data['purchase'],
        #         'purchase_date': post_data['purchase_date'],
        #         'car_make': post_data['car_make'],
        #         'car_model': post_data['car_model'],
        #         'car_year': post_data['car_year'],
        #     }
        # }
        response = post_request(REVIEW_URL, json_payload=json_payload)
        return HttpResponse(response)
