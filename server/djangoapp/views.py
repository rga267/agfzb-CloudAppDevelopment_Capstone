from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .models import CarModel
from django.contrib.auth import login, logout, authenticate
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def loginPage(request):
    context = {}

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)

        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

def logoutPage(request):
    logout(request)
    return redirect('djangoapp:index')


def renderStatic(request):
    context = {}
    if request.method == "GET":
        return render(request, 'static.html', context)

def registration(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


def aboutPage(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contactPage(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)





# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://ed95a2d2.eu-gb.apigw.appdomain.cloud/api/dealerships"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://ed95a2d2.eu-gb.apigw.appdomain.cloud/api/review"
        dealer_details = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        context["review_list"] = dealer_details
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        print("GET add_review")
        context["dealer_id"] = dealer_id
        context["cars"] = CarModel.objects.all()
        print(CarModel.objects.all())
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        print("POST add_review")

        form = request.POST
        review = {
            "name": request.user.first_name + ' ' + request.user.last_name,
            "dealership": int(dealer_id),
            "review": form["content"],
            "purchase": bool(form.get("purchasecheck")),
        }

        if form.get("purchasecheck"):
            review["purchase_date"] = datetime.strptime(form.get("purchase_date"), "%m/%d/%Y").isoformat()
            car = CarModel.objects.get(pk=form['car'])
            review["car_make"] = car.maker.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime('%Y')

        print('review', review)

        url="https://ed95a2d2.eu-gb.apigw.appdomain.cloud/api/review"

        json_result = post_request(url, {"review": review})
        print(json_result)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

