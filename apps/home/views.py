from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.usermanager import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from apps.usermanager.models import UserDetail
from django.conf import settings
from apps.home.scrap import Scrap
import os
from apps.home.forms import ScrapSearchForm, DashboardSearchForm
from apps.home.models import Product
from django.db.models import Q


# Create your views here.
def home(request):
    ctx = {'title': 'Home page', 'home': 'active'}
    return render(request, "home.html", ctx)


@login_required
def dashboard(request):
    result= None
    if request.method == 'GET':
        form = DashboardSearchForm(request.GET)

        if form.is_valid():
            search_item = form.cleaned_data.get('search_item')
            product = Product.objects.filter(
                Q(name__icontains=search_item) |
                Q(price__icontains=search_item) |
                Q(product_type__icontains=search_item) |
                Q(site_reference__icontains=search_item) |
                Q(description__icontains=search_item))
            if product:
                print(product)
                result = product
            else:
                result = None
                print('search in SCRAp')


    ctx = {'title': 'Dashboard page', 'dashboard': 'active', 'form': form, 'result': result}
    return render(request, "dashboard.html", ctx)

@login_required
def profile(request):


    # ud = UserDetail.objects.get(user=request.user)


    ctx = ({'title': 'profile page', 'profile': 'active',})

    return render(request, "profile.html", ctx)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # import pdb
        # pdb.set_trace()
        form = forms.EditProfileForm(request, request.POST, request.FILES)
        if form.is_valid():
            try:
                data = request.POST.copy()
                print(request.user.pk)
                try:
                    mail = data['mail']
                except:
                    mail = None
                try:
                    message = data['message']
                except:
                    message = None
                try:
                    phonecall = data['phonecall']
                except:
                    phonecall = None
                try:
                    other = data['other']
                except:
                    other = None
                try:
                    gender = data['gender']
                except:
                    gender = None
                try:
                    image = data['image']
                except:
                    image = None

                if data['date_of_birth'] in ['', ' ', None]:
                    data['date_of_birth'] = None
                if data['phone'] in ['', ' ', None]:
                    data['phone'] = None

                try:
                    upload_to = '/uploads/{0}/'.format(request.user.pk)
                    image = '{0}{1}'.format(upload_to, request.FILES['image'])
                except:
                    image = None

                data1 = {'first_name': data['first_name'],
                         'last_name': data['last_name']}
                data2 = {'phone': data['phone'], 'marital': data['marital'],
                         'image': image, 'street': data['street'],
                         'city': data['city'], 'state': data['state'],
                         'extra_note': data['extra_note'],
                         'zip_code': data['zip_code'],
                         'date_of_birth': data['date_of_birth'],
                         'address': data['address'], 'gender': gender,
                         'mail': mail, 'message': message,
                         'phonecall': phonecall, 'other': other,
                         'user_id': request.user.pk}

                try:
                    save_file(request.FILES['image'], upload_to)
                except:
                    pass

                if data2['mail'] == 'on':
                    data2['mail'] = True
                else:
                    data2['mail'] = False

                if data2['message'] == 'on':
                    data2['message'] = True
                else:
                    data2['message'] = False

                if data2['phonecall'] == 'on':
                    data2['phonecall'] = True
                else:
                    data2['phonecall'] = False

                if data2['other'] == 'on':
                    data2['other'] = True
                else:
                    data2['other'] = False

                print(data1)
                print(data2)

                # Updating auth_user table with data1
                User.objects.filter(pk=request.user.pk).update(**data1)

                # Updating UserDetail table with data2
                UserDetail.objects.filter(user=request.user.pk).update(**data2)

                print('success')
            except Exception as e:
                print(e)
        else:
            print(form.errors)
    elif request.method == 'GET':
        form = forms.EditProfileForm(request)
    ctx = {'form': form, 'title': 'profile page'}
    return render(request, "edit_profile.html", ctx)

def save_file(f, upload_to):

    file_name = f.name
    path = settings.MEDIA_ROOT + upload_to
    # create the directory if it doesnt exits
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(path + file_name, 'wb+')
    # write the file
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


@login_required
def scrap(request):
    if request.method == 'POST':
        form = ScrapSearchForm(request.POST)
        if form.is_valid():
            search_item = form.cleaned_data.get("search_item")
            site_choice = form.cleaned_data.get("site_choice")
            scrap = Scrap()
            if site_choice == 'F':
                result = scrap.flipkart(search_item)
            else:
                result = scrap.amazon(search_item)

    elif request.method == 'GET':
        form = ScrapSearchForm()
        result = None

    ctx = {'title': 'Scrap page', 'scrap': 'active', 'form': form, 'result': result}
    return render(request, "scrap.html", ctx)