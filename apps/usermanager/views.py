"""Views for usermanager app.

It contains signup view method for signup page, login_user view
method for login page, activate view method for activate page,
generate_activation_key method for generating activation key,
send_activation_mail method for sending email.

"""


from apps.usermanager import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.models import make_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from apps.usermanager.models import UserDetail
from apps.usermanager.models import UserActivation
from django.conf import settings
from django.core.mail import send_mail
import hashlib
import random
from apps import constants as con
import logging

# Get an instance of a logger
logger = logging.getLogger(settings.LOGGER)


def signup(request):
    """Register new user.

    It validate the form and save data in the auth_user and
    userdetail table.If user is already loged in redirect
    to dashboard page.
    """
    # If the user is loged in redirect to dashboard
    if request.user.pk:
        # Redirecting to dashboard.
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        # Create obj for SignUpFrom
        form = forms.SignUpForm(request.POST)

        # Check form is valid
        if form.is_valid():
            # Storing cleaned data to variable
            data = form.cleaned_data

            # Check password is equal to confirm password
            if data['confirm_password'] == data['password']:

                # Pop the confirm_password key from data
                data.pop('confirm_password')

                # Encrypting the password
                data['password'] = make_password(
                    data['password'], salt="scrapper")

                # Setting is_active to False
                data['is_active'] = False

                # Save the data in auth_user table
                user = User.objects.create(**data)

                # Save the user_id in UserDetail table
                data1 = {'user_id': user.pk}
                UserDetail.objects.create(**data1)

                # Save the user_id in UserDetail table
                activation_key = generate_activation_key(data['email'])
                data2 = {'user_id': user.pk, 'activation_key': activation_key}
                UserActivation.objects.create(**data2)

            else:
                user = None

                # Context to send in html.
                ctx = (
                    {'form': form, 'title': 'Signup page', 'signup': 'active'}
                )

                # Sending error message in html.
                messages.error(request, 'Password didnt match')

                return render_to_response(
                    'signup.html', ctx,
                    context_instance=RequestContext(request)
                )
            if user:

                    try:
                        # Calling send-activation-mail method.
                        send_activation_mail(
                            user.username, data['email'], activation_key)

                        # Feedback message to send in html context.
                        feedback = "successfully register and account\
                         activation link is sent to your mail"

                        # Context to send in html.
                        ctx = (
                            {'form': form, 'title': 'Signup page',
                             'signup': 'active', 'feedback': feedback}
                        )
                        return render_to_response(
                            'signup.html', ctx,
                            context_instance=RequestContext(request)
                        )

                    except Exception as e:
                        logger.exception("EXCEPTION :" + str(e))

    # If the method is GET.
    elif request.method == 'GET':
        # Creating form object.
        form = forms.SignUpForm()

    # Sending context to html.
    ctx = (
        {'form': form, 'title': 'Signup page', 'signup': 'active'}
    )

    return render_to_response(
        'signup.html', ctx, context_instance=RequestContext(request)
    )


def generate_activation_key(email):
    """Generating an unique acitivation key."""
    # Create salt
    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:40]

    # Create activation key combining both email and salt
    activation_key = hashlib.sha1(
        str(salt + email).encode('utf-8')).hexdigest()
    return activation_key


def send_activation_mail(username, receiver_email, activation_key):
    """Sending an activation mail to the registered user."""
    subject = "Acitvation Email - Mysite.com"
    message = "Acitvation mail"

    # link to send in the html content
    html_message = "<h4>Click <a href='{0}?id={1}'>here</a>\
     to activate</h4>".format(con.ACTIVATION_URL, activation_key)

    # Sender email.
    from_email = settings.EMAIL_HOST_USER

    # receiver email.
    to_email = [receiver_email]

    # calling send_mail function by passing required parameters.
    send_mail(
        subject, message, from_email, to_email,
        fail_silently=False, html_message=html_message)


def activate(request):
    """To active user.

    Get activation key from GET request and using that get user_id.
    use this user_id as pk id for auth_user and update is_active status
    to True.
    """
    if request.method == 'GET':

        try:
            data = request.GET.copy()

            if data:
                # Getting user_activation object where activation key
                activate = UserActivation.objects.get(
                    activation_key=data['id'])
                data1 = {'is_active': True}

                # Update auth_user table is_active status to True.
                User.objects.filter(pk=activate.user_id).update(**data1)
                ctx = {'title': 'Activate page'}
                return render_to_response(
                    'activate.html', ctx,
                    context_instance=RequestContext(request))

            else:
                feedback = "Page Not Found"

                # Context to send in html.
                ctx = {'title': 'Activate page', 'feedback': feedback}
                return render_to_response(
                    'activate.html', ctx,
                    context_instance=RequestContext(request))

        except Exception as e:
            logger.exception("EXCEPTION :" + str(e))

            # Store exception in feedback.
            feedback = str(e)

            # Context to send in html.
            ctx = {'title': 'Activate page', 'feedback': feedback}
            return render_to_response('activate.html', ctx,
                                      context_instance=RequestContext(request))


def login_user(request):
    """To login user.

    It validates the form and authenticate user.If user then check
    is_active status,if true then login the user and redirect to
    dashboard page.
    """
    # If user already exist.
    if request.user.pk:

        # Redirecting to dashboard.
        return HttpResponseRedirect(reverse('dashboard'))

    # If the method is POST.
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            # Store the data form cleaned_data to data
            data = form.cleaned_data

            # Authenticating user.
            auth_user = authenticate(
                username=data['username'], password=data['password']
            )

            # If user exist the login user.
            if auth_user:

                if auth_user.is_active:

                    # Login user
                    login(request, auth_user)

                    # Redirect to dashboard.
                    return HttpResponseRedirect(reverse('dashboard'))

                else:
                    # Context to send in html.
                    ctx = ({
                        'form': form, 'title': 'Login page', 'login': 'active'
                    })

                    # Send error message in html.
                    messages.error(request, 'Please activate your account.')

                    return render_to_response(
                        'login.html', ctx,
                        context_instance=RequestContext(request)
                    )

            else:

                # Context to send in html.
                ctx = (
                    {'form': form, 'title': 'Login page', 'login': 'active'}
                )

                # Send error message in html.
                messages.error(request, 'Wrong username or password')

                return render_to_response(
                    'login.html', ctx, context_instance=RequestContext(request)
                )

    # If the method is GET.
    elif request.method == 'GET':
        # Create form object.
        form = forms.LoginForm()

    # Context to send in html.
    ctx = ({'form': form, 'title': 'Login page', 'login': 'active'})

    return render_to_response(
        'login.html', ctx, context_instance=RequestContext(request)
    )
