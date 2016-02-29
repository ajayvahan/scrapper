"""home app views.

It contains home view method for home page, dashboard view method
for dashboard page, dashboard_search view method for dashboard search
page, scrap view method for scrap page, profile view method for profile
page, edit_profile view method for edit_profile page and save function
for saving image.
"""


import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.usermanager import forms
from django.contrib.auth.models import User
from apps.usermanager.models import UserDetail
from django.conf import settings
from apps.home.scrap import Scrap
from apps.home.forms import ScrapSearchForm, DashboardSearchForm
from apps.home.models import Product
from django.db.models import Q
import logging

# Get an instance of a logger
logger = logging.getLogger(settings.LOGGER)


def home(request):
    """View for Home page."""
    # Contexts to send in html.
    ctx = {'title': 'Home page', 'home': 'active'}
    return render(request, "home.html", ctx)


@login_required
def dashboard(request):
    """View for Dashboard page."""
    # Creating form object.
    form = DashboardSearchForm()

    # Contexts to send in html.
    ctx = {'title': 'Dashboard page', 'dashboard': 'active', 'form': form}
    return render(request, "dashboard.html", ctx)


@login_required
def dashboard_search(request):
    """View for Dashboard search page.

    It validates form and filter the product table based on search item
    and store the list in the result and send it in the html context.
    """
    # Initial  context values.
    result = None
    feedback = None

    # If method is GET.
    if request.method == 'GET':

        # Creating form object.
        form = DashboardSearchForm(request.GET)

        if form.is_valid():

            # Reading search_item value from cleaned_data.
            search_item = form.cleaned_data.get('search_item')

            # Filtering fields in Product table based on search item.
            # Storing the list in variable.
            product = Product.objects.filter(
                Q(name__icontains=search_item) |
                Q(price__icontains=search_item) |
                Q(product_type__icontains=search_item) |
                Q(site_reference__icontains=search_item) |
                Q(description__icontains=search_item))

            if product:

                # Storing the product list in result.
                result = product

            # If product does not exist.
            else:

                # Make result to none.
                result = None

                # Send feedback.
                feedback = "Search in Scrap page "

    # If method POST.
    if request.method == 'POST':

        # Creating form object.
        form = DashboardSearchForm()

    # Context to send in html.
    ctx = {'title': 'Dashboard page', 'dashboard': 'active',
           'form': form, 'result': result, 'feedback': feedback}
    return render(request, "dashboard.html", ctx)


@login_required
def profile(request):
    """View for Profile page."""
    # Context to send in html.
    ctx = ({'title': 'profile page', 'profile': 'active'})
    return render(request, "profile.html", ctx)


@login_required
def edit_profile(request):
    """View for Edit profile page.

    It validates the form and update auth_user and user_detail tables.
    """
    # If method POST.
    if request.method == 'POST':
        # Creating form object.
        form = forms.EditProfileForm(request, request.POST, request.FILES)

        if form.is_valid():

            try:
                data = form.cleaned_data

                # Store only first_name and last_name fields in data1.
                # For updating auth_user table.
                data1 = {'first_name': data['first_name'],
                         'last_name': data['last_name']}

                # Storind data in data2 for updating UserDetail table.
                data2 = {'phone': data['phone'], 'marital': data['marital'],
                         'street': data['street'],
                         'city': data['city'], 'state': data['state'],
                         'extra_note': data['extra_note'],
                         'zip_code': data['zip_code'],
                         'date_of_birth': data['date_of_birth'],
                         'address': data['address'], 'gender': data['gender'],
                         'mail': data['mail'], 'message': data['message'],
                         'phonecall': data['phonecall'],
                         'other': data['other'], 'user_id': request.user.pk}

                # Handling exceptions in saving the file.
                try:
                    upload_to = 'uploads/{0}/'.format(request.user.pk)
                    image = '{0}{1}'.format(upload_to, request.FILES['image'])

                    # calling save file method.
                    save_file(request.FILES['image'], upload_to)

                    # adding the image in the data2 dict.
                    data2['image'] = image

                except Exception as e:
                    logger.exception("NO IMAGE :" + str(e))

                # Updating auth_user table with data1.
                User.objects.filter(pk=request.user.pk).update(**data1)

                # Updating UserDetail table with data2.
                UserDetail.objects.filter(user=request.user.pk).update(**data2)

                logger.info('EDIT PROFILE: ' + 'SUCCESS')
                feedback = "successfully updated"
                ctx = {'form': form, 'title': 'Edit profile page',
                       'feedback': feedback, 'edit_profile': 'active'}
                return render(request, "edit_profile.html", ctx)

            except Exception as e:
                logger.exception("EXCEPTION :" + str(e))
        else:
            logger.error('FORM ERRORS: ' + str(form.errors))

    # If method is GET.
    elif request.method == 'GET':
        # Creating form object.
        form = forms.EditProfileForm(request)

    # Context to send in html.
    ctx = {'form': form, 'title': 'profile page', 'edit_profile': 'active'}
    return render(request, "edit_profile.html", ctx)


def save_file(file, upload_to):
    """To save the file in a new directory."""
    file_name = file.name

    # Set path
    path = settings.MEDIA_ROOT + upload_to

    logger.info('PATH: ' + str(path))

    # Create the directory if it doesnt exits.
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(path + file_name, 'wb+')

    # Write the file.
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()


@login_required
def scrap(request):
    """View for Scrap page.

    It validates the form and based on site choice it call the respective
    method from Scrap class and store the returned values in result to
    send in html context.
    """
    # If the method is POST.
    if request.method == 'POST':
        # Creating form object.
        form = ScrapSearchForm(request.POST)

        # Initial context value.
        result = None

        if form.is_valid():
            # Reading values from cleaned_data.
            search_item = form.cleaned_data.get("search_item")
            site_choice = form.cleaned_data.get("site_choice")

            # Instantiating Scrap class.
            scrap = Scrap()

            # Setting intial value.
            feedback = None

            # If site choice is 'F'.
            if site_choice == 'F':
                # Calling flipkart method in Scrap.
                # Store the return value in result.
                result = scrap.flipkart(search_item)
                if not result:
                    feedback = "Search item not found"

            else:
                # Calling amazon method in Scrap.
                # Store the return value in result.
                result = scrap.amazon(search_item)
                if not result:
                    feedback = "Search item not found"

    # If method is GET.
    elif request.method == 'GET':
        # Creating form object.
        form = ScrapSearchForm()
        result = None
        feedback = None

    # Context to send in html.
    ctx = {'title': 'Scrap page', 'scrap': 'active', 'form': form,
           'result': result, 'feedback': feedback}
    return render(request, "scrap.html", ctx)
