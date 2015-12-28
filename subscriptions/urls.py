from django.conf.urls import url

from . import views
from . import receivers

urlpatterns = [
    url(
        r'^dashboard/',
        views.dashboard,
        name='dashboard'
    ),
    url(
        r'^subscriptions/',
        views.user_subscriptions,
        name='user_subscriptions'
    ),
    url(
        r'^push_notifications/',
        views.push_notifications,
        name='push_notifications'
    ),
    url(
        r'^billing_info/',
        views.billing_information,
        name='billing_information'
    )
]
