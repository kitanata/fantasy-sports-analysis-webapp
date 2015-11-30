from django.template.response import TemplateResponse

from .models import LineUp, Subscription


def dashboard(request):
    return TemplateResponse(request, 'subscriptions/dashboard.html', {
        'lineups_by_date': []
    })
