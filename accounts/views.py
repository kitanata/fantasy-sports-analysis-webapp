from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import (
    EmailUserCreationForm,
    EmailUserAccountInfoForm,
    DeleteAccountForm
)


def signup(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                ('Thanks for creating an account! You can access your account '
                 'details through the dropdown in the upper right of the page'
                 '.')
            )
            return redirect(reverse('dashboard'))

    form = EmailUserCreationForm()

    return TemplateResponse(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def account_info(request):
    if request.method == 'POST':
        form = EmailUserAccountInfoForm(request.POST, instance=request.user)
        if form.is_valid:
            messages.success(
                request,
                'You have successfully updated your profile information.'
            )
            form.save()

    form = EmailUserAccountInfoForm(instance=request.user)

    return TemplateResponse(request, 'accounts/account_info.html', {
        'form': form
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid:
            request.user.delete()
            logout(request)
            messages.success(
                request,
                'You have successfully deleted your account.'
            )
            return redirect(reverse('home'))

    form = DeleteAccountForm()

    return TemplateResponse(request, 'accounts/delete_account.html', {
        'form': form
    })
