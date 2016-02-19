from django.shortcuts import render
from apps.usermanager import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.models import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from apps.usermanager.models import UserDetail
# Create your views here.


def signup(request):
    """Register new user."""
    # if the user is loged in redirect to dashboard
    if request.user.pk:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':

        # Create obj for SignUpFrom
        form = forms.SignUpForm(request.POST)

        # Check form is valid
        if form.is_valid():

            # Storing cleaned data to variable
            data = form.cleaned_data
            print (data)

            # Check password is equal to confirm password
            if data['confirm_password'] == data['password']:

                # Pop the confirm_password key from data
                data.pop('confirm_password')

                password = data['password']

                data['password'] = make_password(
                    data['password'], salt="scrapper")

                # save the data in auth_user table
                user = User.objects.create(**data)
                print(user.pk)
                # save the user_id in UserDetail table
                data1 = {'user_id': user.pk}
                UserDetail.objects.create(**data1)
            else:
                user = None
                ctx = ({'form': form, 'title': 'Signup page', 'signup': 'active'})
                messages.error(request, 'Password didnt match')
                return render_to_response(
                    'signup.html', ctx, context_instance=RequestContext(request))
            if user:

                auth_user = authenticate(
                    username=data['username'], password=password
                )
                if auth_user:
                    login(request, auth_user)

                    return HttpResponseRedirect(reverse('dashboard'))
            print (data)
    elif request.method == 'GET':
        form = forms.SignUpForm()
    ctx = ({'form': form, 'title': 'Signup page', 'signup': 'active'})
    return render_to_response(
        'signup.html', ctx, context_instance=RequestContext(request)
    )


def login_user(request):
    if request.user.pk:
        return HttpResponseRedirect(reverse('dashboard'))
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print (data["username"])
            auth_user = authenticate(
                username=data['username'], password=data['password']
            )
            print (auth_user)
            if auth_user:
                login(request, auth_user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                ctx = ({'form': form, 'title': 'Login page', 'login': 'active'})
                messages.error(request, 'Wrong username or password')
                return render_to_response(
                    'login.html', ctx, context_instance=RequestContext(request))

            print (data)
    elif request.method == 'GET':
        form = forms.LoginForm()
    ctx = ({'form': form, 'title': 'Login page', 'login': 'active'})
    return render_to_response(
        'login.html', ctx, context_instance=RequestContext(request)
    )
