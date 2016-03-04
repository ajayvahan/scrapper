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
    url(r'^profile/$', 'apps.home.views.profile', name='profile'),
    url(r'^profile/edit/$', 'apps.home.views.edit_profile',
        name='edit_profile'),
    url(r'^dashboard/scrap/$', 'apps.home.views.scrap', name='scrap'),
    url(r'^activate/$', 'apps.usermanager.views.activate', name='activate'),

]
