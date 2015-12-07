from django.conf.urls import url

from .views import account_info, delete_account

urlpatterns = [
    url(r'^$', account_info, name='account_info'),
    url(r'^delete$', delete_account, name='delete_account'),
]
