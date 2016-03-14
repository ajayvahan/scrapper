"""URLs for scrapper project."""

from django.conf.urls import include, url
from django.contrib import admin

# from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', 'apps.home.views.home', name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', 'apps.usermanager.views.signup', name='signup'),
    url(r'^login/$', 'apps.usermanager.views.login_user', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {"next_page": "/"}, name='logout'),
    url(r'^dashboard/$', 'apps.home.views.dashboard', name='dashboard'),
    url(r'^dashboard/search/$', 'apps.home.views.dashboard_search',
        name='dashboard_search'),
    url(r'^dashboard/search/filter$', 'apps.home.views.dashboard_filter',
        name='dashboard_filter'),
    url(r'^profile/$', 'apps.home.views.profile', name='profile'),
    url(r'^profile/edit/$', 'apps.home.views.edit_profile',
        name='edit_profile'),
    url(r'^dashboard/scrap/$', 'apps.home.views.scrap', name='scrap'),
    url(r'^activate/$', 'apps.usermanager.views.activate', name='activate'),
    url(r'^checkout/address$', 'apps.checkout.views.checkout_address',
        name='checkout_address'),
    url(r'^checkout/payment$', 'apps.checkout.views.checkout_payment',
        name='checkout_payment'),
    url(r'^product/(?P<name>[-\w\d]+)/$', 'apps.home.views.product_display',
        name="product_display"),
    url(r'^checkout/address/summary$', 'apps.checkout.views.checkout_summary',
        name='checkout_summary'),


]
