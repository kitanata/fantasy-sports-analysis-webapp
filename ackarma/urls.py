from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from .views import homepage


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('accounts.urls')),
    url(r'^', include('subscriptions.urls')),
    url(r'^$', homepage, name='home'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
