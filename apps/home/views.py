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
from apps.home.forms import ScrapSearchForm
from apps.home.forms import DashboardSearchForm, DashboardFilterForm
from apps.home.models import Product
from django.db.models import Q
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
import logging
from django.core.cache import cache

# Get an instance of a logger
logger = logging.getLogger(settings.LOGGER)


def home(request):
    """View for Home page."""
    # Contexts to send in html.
    ctx = {'title': 'Home page', 'home': 'active'}
    return render(request, "home/home.html", ctx)


@login_required
def dashboard(request):
    """View for Dashboard page."""
    # Creating form object.
    form = DashboardSearchForm()
    form2 = DashboardFilterForm()

    # Contexts to send in html.
    ctx = {'title': 'Dashboard page', 'dashboard': 'active',
           'form': form, 'form2': form2}
    return render(request, "dashboard/dashboard.html", ctx)


@login_required
def dashboard_search(request):
    """View for Dashboard search page.

    It validates form and filter the product table based on search item
    and store the list in the result and send it in the html context.
    """
    # Initial  context values.
    result = None
    feedback = None

    # Creating form object.
    form = DashboardSearchForm()
    form2 = DashboardFilterForm()

    # If method is ajax
    if request.is_ajax():
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

        # Storing the result in the cache.
        cache.set('result_product', result, None)

        # Context to send in html.
        ctx = {'result': result, 'dashboard_feedback': feedback}

        # Passing the context to html and rendering to string.
        # Store it in result variable.
        result_html = render_to_string(
            'dashboard/result.html', ctx,
            context_instance=RequestContext(request))

        # dictionary to pass in json.dumps.
        json_data = {'result': result_html}

        # Send HttpResponse using json.dumps.
        return HttpResponse(
            json.dumps(json_data), content_type='application/json')

    # Contexts to send in html.
    ctx = {'title': 'Dashboard page', 'dashboard': 'active',
           'form': form, 'form2': form2}
    return render(request, "dashboard/dashboard.html", ctx)

    # If method POST.
    if request.method == 'POST':
        # Creating form object.
        form = DashboardSearchForm()

        # Contexts to send in html.
        ctx = {'title': 'Dashboard page', 'dashboard': 'active', 'form': form}
        return render(request, "dashboard/dashboard.html", ctx)


def product_display(request, name):
    """View for product_display page."""
    try:
        # Filter the product table where the slug_name.
        product = Product.objects.filter(slug_name=name)

        # Get pk from the product and store in pk variable.
        pk = product[0].pk

        # Store the product_id and price in the cache.
        cache.set('product_id', pk, None)
        cache.set('price', product[0].price, None)

        ctx = ({'title': 'Product display page', 'product': product[0]})
        return render(request, "dashboard/product_display.html", ctx)

    except Exception as e:
        logger.exception("EXCEPTION :" + str(e))

        # Redirect to the dashboard page.
        return HttpResponseRedirect(reverse('dashboard'))


@login_required
def dashboard_filter(request):
    """View for dashboard filter."""
    # Creating form object.
    form = DashboardSearchForm()
    form2 = DashboardFilterForm()

    # If method is ajax
    if request.is_ajax():
        # Getting the searched results from cache.
        result = cache.get('result_product')

        # Creating form object.
        form2 = DashboardFilterForm(request.GET)

        feedback = None

        if form2.is_valid():

            filter_data = form2.cleaned_data

            if result:
                # Filtering with respect to price.
                if filter_data['price_sort'] == 'LH':
                    result = result.order_by('price')
                elif filter_data['price_sort'] == 'HL':
                    result = result.order_by('-price')

                # Filtering with respect to site preferrence.
                if filter_data['amazon'] and filter_data['flipkart']:
                    pass
                elif filter_data['amazon']:
                    result = result.filter(
                        Q(site_reference__icontains='amazon'))
                elif filter_data['flipkart']:
                    result = result.filter(
                        Q(site_reference__icontains='flipkart'))

            else:
                # Make result to none.
                result = None

                # Send feedback.
                feedback = "Search in Scrap page "

        # Context to send in html.
        ctx = {'result': result, 'dashboard_feedback': feedback}

        # Passing the context to html and rendering to string.
        # Store it in result variable.
        result_html = render_to_string(
            'dashboard/result.html', ctx,
            context_instance=RequestContext(request))

        # dictionary to pass in json.dumps.
        json_data = {'result': result_html}

        # Send HttpResponse using json.dumps.
        return HttpResponse(
            json.dumps(json_data), content_type='application/json')

    # Contexts to send in html.
    ctx = {'title': 'Dashboard page', 'dashboard': 'active',
           'form': form, 'form2': form2}
    return render(request, "dashboard/dashboard.html", ctx)


@login_required
def profile(request):
    """View for Profile page."""
    # Context to send in html.
    ctx = ({'title': 'profile page', 'profile': 'active'})
    return render(request, "dashboard/profile.html", ctx)


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
                # Store form cleaned_data in data variable.
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

                # Feedback message to send in the context.
                feedback = "successfully updated"

                # Context to send in the html.
                ctx = {'form': form, 'title': 'Edit profile page',
                       'feedback': feedback, 'edit_profile': 'active'}
                return render(request, "dashboard/edit_profile.html", ctx)

            except Exception as e:
                logger.exception("EXCEPTION :" + str(e))
        else:
            logger.error('FORM ERRORS: ' + str(form.errors))

    # If method is GET.
    elif request.method == 'GET':
        # Creating form object.
        form = forms.EditProfileForm(request)

    # Context to send in html.
    ctx = {'form': form, 'title': 'Edit profile page',
           'edit_profile': 'active'}
    return render(request, "dashboard/edit_profile.html", ctx)


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

            # Context to send in html.
            ctx = {'result': result, 'scrap_feedback': feedback}

            # Passing the context to html and rendering to string.
            # Store it in result variable.
            result = render_to_string(
                'dashboard/result.html', ctx,
                context_instance=RequestContext(request))

            # dictionary to pass in json.dumps.
            json_data = {'result': result}

            # Send HttpResponse using json.dumps.
            return HttpResponse(
                json.dumps(json_data), content_type='application/json')

    # If method is GET.
    elif request.method == 'GET':
        # Creating form object.
        form = ScrapSearchForm()
        result = None
        feedback = None

    # Context to send in html.
    ctx = {'title': 'Scrap page', 'scrap': 'active', 'form': form,
           'result': result, 'feedback': feedback}
    return render(request, "dashboard/scrap.html", ctx)
