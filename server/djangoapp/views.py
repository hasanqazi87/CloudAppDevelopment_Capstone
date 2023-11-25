from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from operator import itemgetter
from math import floor
import logging
import json
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)

DEALERSHIP_URL = 'https://hasanqazi87-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership'
REVIEW_URL = 'https://hasanqazi87-5000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/review'


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
    context = {
        'dealerships': get_dealers_from_cf(DEALERSHIP_URL, **request.GET)
    }
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    dealer = get_dealers_from_cf(DEALERSHIP_URL, id=dealer_id)
    context = {
        'dealer': dealer.pop() if dealer else [],
        'reviews': get_dealer_reviews_from_cf(REVIEW_URL, dealer_id=dealer_id)
    }
    return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    dealer = get_dealers_from_cf(DEALERSHIP_URL, id=dealer_id)
    cars = CarModel.objects.filter(dealer_id=dealer_id)
    context = {
        'dealer': dealer.pop() if dealer else [],
        'cars': cars,
    }
    if not request.user.is_authenticated:
        return redirect(reverse('djangoapp:index'))
    if request.method == 'POST':
        post_data = request.POST
        car_selected = cars.get(pk=post_data['car'])
        json_payload = {
            'id': floor(datetime.now().timestamp()),
            'name': post_data['person'],
            'dealership': dealer_id,
            'review': post_data['content'],
            'purchase': 'on' in post_data['purchase'],
            'purchase_date': post_data['purchase_date'],
            'car_make': car_selected.car_make.name,
            'car_model': car_selected.name,
            'car_year': car_selected.year.strftime('%Y'),
        }
        post_request(REVIEW_URL, json_payload=json_payload)
        return redirect(reverse('djangoapp:dealer_details', kwargs={'dealer_id': dealer_id}))
    return render(request, 'djangoapp/add_review.html', context)
