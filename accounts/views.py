from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .forms import EmailUserCreationForm, EmailUserAccountInfoForm


def signup(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')

    form = EmailUserCreationForm()

    return TemplateResponse(request, 'registration/signup.html', {
        'form': form
    })


@login_required
def account_info(request):
    if request.method == 'POST':
        form = EmailUserAccountInfoForm(request.POST, instance=request.user)
        if form.is_valid:
            form.save()

    form = EmailUserAccountInfoForm(instance=request.user)

    return TemplateResponse(request, 'accounts/account_info.html', {
        'form': form
    })
