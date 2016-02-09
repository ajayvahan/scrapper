from django.conf.urls import include, url
from django.contrib import admin

# from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^templates$', TemplateView.as_view(template_name="hello.html"), name='whatever'),
    url(r'^$', 'apps.home.views.home', name='home'),
    url(r'^admin/', admin.site.urls),
]
