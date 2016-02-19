from django.conf.urls import include, url
from django.contrib import admin

# from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^templates$', TemplateView.as_view(template_name="hello.html"), name='whatever'),
    url(r'^$', 'apps.home.views.home', name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', 'apps.usermanager.views.signup', name='signup'),
    url(r'^login/$', 'apps.usermanager.views.login_user', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {"next_page": "/"}, name='logout'),
    url(r'^dashboard/$', 'apps.home.views.dashboard', name='dashboard'),
    url(r'^profile/$', 'apps.home.views.profile', name='profile'),
    url(r'^profile/edit/$', 'apps.home.views.edit_profile', name='edit_profile'),
    url(r'^dashboard/scrap$', 'apps.home.views.scrap', name='scrap'),


]
