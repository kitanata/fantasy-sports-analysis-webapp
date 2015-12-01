from django.conf.urls import url

from .views import dashboard, user_subscriptions

urlpatterns = [
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^subscriptions/', user_subscriptions, name='user_subscriptions')
]
