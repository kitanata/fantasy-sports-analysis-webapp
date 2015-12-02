from django.conf.urls import url

from .views import account_info

urlpatterns = [
    url(r'^$', account_info, name='account_info'),
]
