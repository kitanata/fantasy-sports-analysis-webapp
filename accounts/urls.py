from django.conf.urls import url

from .views import account_info, delete_account, payment_history

urlpatterns = [
    url(r'^$', account_info, name='account_info'),
    url(r'^delete$', delete_account, name='delete_account'),
    url(r'^payment-history/$', payment_history, name='payment_history'),
]
