from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from accounts.views import signup

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^account/', TemplateView.as_view(
        template_name='accounts/basic_information.html'),
        name='account_info'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('subscriptions.urls')),
    url(r'^signup/', signup, name='signup'),
]
