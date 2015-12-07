from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import signup

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^account/', include('accounts.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('subscriptions.urls')),
    url(r'^signup/', signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,
                                       document_root=settings.MEDIA_ROOT)
