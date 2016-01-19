from django.conf.urls import url
from django.contrib.auth import views as auth
from .forms import CrispyAuthenticationForm
from . import views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(
        r'^login/$',
        auth.login,
        {'authentication_form': CrispyAuthenticationForm},
        name='login'
        ),
    url(r'^logout/$', auth.logout, name='logout'),
    url(r'^change-password/$', auth.password_change, name='password_change'),
    url(
        r'^change-password/done/$',
        auth.password_change_done,
        name='password_change_done'
    ),
    url(r'^reset-password/$', auth.password_reset, name='password_reset'),
    url(
        r'^reset-password/done/$',
        auth.password_reset_done,
        name='password_reset_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(
        r'^reset/done/$',
        auth.password_reset_complete,
        name='password_reset_complete'
    ),
    url(r'^info/$', views.account_info, name='account_info'),
    url(r'^delete/$', views.delete_account, name='delete_account'),
]
