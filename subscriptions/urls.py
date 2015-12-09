from django.conf.urls import url

from . import views

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
    )
]
