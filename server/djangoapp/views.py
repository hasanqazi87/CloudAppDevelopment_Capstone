from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from operator import itemgetter
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


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
        #url = "https://d65e5e43-83be-4e04-bf34-e149095716c3-bluemix.cloudantnosqldb.appdomain.cloud/api/dealership"
        url = 'https://hasanqazi87-3000.theiadocker-2-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership'
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url, **request.GET)
        # Concat all dealer's short name
        dealer_names = ', '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

