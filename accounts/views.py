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

            request.user.email = form.cleaned_data['email']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

    form = EmailUserAccountInfoForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email
    })

    return TemplateResponse(request, 'accounts/account_info.html', {
        'form': form
    })
