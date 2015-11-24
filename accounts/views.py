from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from .forms import EmailUserCreationForm


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
