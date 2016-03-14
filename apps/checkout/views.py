"""Checkout app views."""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from apps.checkout.forms import DeliveryDetailForm, DeliveryQuantityForm
from .models import DeliveryDetail
from django.http import HttpResponse
import json
from django.core.cache import cache
import random
import logging

# Get an instance of a logger.
logger = logging.getLogger(settings.LOGGER)

# Stripe API secret key.
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_payment(request):
    """View for checkout payment page."""
    # Get publishable key from settings and store in a variable.
    publish_key = settings.STRIPE_PUBLISHABLE_KEY

    # Get total from cache
    total = cache.get('total')

    # If total is none, redirect to dashboard page.
    if not total:
        return HttpResponseRedirect(reverse('dashboard'))

    # If request method POST.
    if request.method == 'POST':

        # Stored stripeToken in the post request to a variable.
        token = request.POST['stripeToken']

        # Create the charge on Stripe's servers
        # this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=int(total * 100),  # amount in cents, again
                currency="inr",
                source=token,
                description="Example charge"
            )

            # Clear the cache when whole payment is done.
            cache.clear()

            # Contexts to send in html.
            ctx = {'title': 'checkout feedback'}
            return render(request, "checkout/checkout_feedback.html", ctx)

        except stripe.error.CardError as e:
            # The card has been declined
            # Feedback message to send in html
            feedback = str(e)

            # Contexts to send in html.
            ctx = {'title': 'checkout feedback', 'feedback': feedback}
            return render(request, "checkout/checkout_feedback.html", ctx)

    # Contexts to send in html.
    ctx = {'title': 'checkout payment', 'publish_key': publish_key}
    return render(request, "checkout/checkout_payment.html", ctx)


@login_required
def checkout_address(request):
    """View for checkout_address page."""
    # Get product_id and price from cache
    product_id = cache.get('product_id')
    price = cache.get('price')

    # If total is none, redirect to dashboard page.
    if not product_id:
        return HttpResponseRedirect(reverse('dashboard'))

    # Creating form object.
    form = DeliveryDetailForm()

    # If request method POST.
    if request.method == 'POST':

        # Creating form object with request.POST
        form = DeliveryDetailForm(request.POST)

        if form.is_valid():
            # Store form cleaned_data in data variable.
            data = form.cleaned_data

            # Generating order id with 10 digit random number.
            order_id = 'OD' + str(random.randint(1000000000, 9999999999))

            try:
                data = {'name': data['name'], 'address': data['address'],
                        'phone': data['phone'], 'zip_code': data['zip_code'],
                        'order_id': order_id, 'user_id': request.user.pk,
                        'product_id': product_id, 'price': price}

                # Create new order row.
                order = DeliveryDetail.objects.create(**data)

                # Store order in the cache.
                cache.set('order', order, None)

                # Redirect to checkout_summary
                return HttpResponseRedirect(reverse('checkout_summary'))

            except Exception as e:
                logger.exception("EXCEPTION :" + str(e))
                order = None

    # Contexts to send in html.
    ctx = {'title': 'Checkout address', 'form': form}
    return render(request, "checkout/checkout_address.html", ctx)


@login_required
def checkout_summary(request):
    """View for checkout_summary page."""
    # Get order from cahe
    order = cache.get('order')

    # If order is none , redirect to dashboard.
    if not order:
        return HttpResponseRedirect(reverse('dashboard'))

    # Get total from order.
    total = order.total

    # store total in the cache.
    cache.set('total', total, None)

    # Create form object.
    form = DeliveryQuantityForm()

    # If the request method is post.
    if request.method == 'POST':
        # Create form object with request.POST
        form = DeliveryQuantityForm(request.POST)

        # Create an empty response dict.
        response = {}

        # If form is valid.
        if form.is_valid():

            try:
                # Store the form cleaned data in the data variable,
                data = form.cleaned_data

                # Filter deliverydetail table where order_id.
                quantity = DeliveryDetail.objects.filter(
                    order_id=order.order_id)

                # Update the quantity column.
                quantity.update(**data)

                # Call the save function inorder to update total column.
                quantity[0].save()

                # Get updated total from the quantity,
                total = quantity[0].total

                # Set new updated total in the cache.
                cache.set('total', total, None)

                # In response dict store success, message and total_price.
                response['success'] = True
                response['message'] = 'successfully updated'
                response['total_price'] = total

            except Exception as e:
                logger.exception("EXCEPTION :" + str(e))

                # In response dict store success and message.
                response['success'] = False
                response['message'] = "Exception as occured"
        else:
            response['success'] = False
            response['message'] = 'Please enter valid quantity'
        # Sending the json response
        return HttpResponse(
            json.dumps(response), content_type='application/json')

    # Contexts to send in html.
    ctx = {'title': 'Checkout summary', 'order': order, 'form': form}
    return render(request, "checkout/checkout_summary.html", ctx)
