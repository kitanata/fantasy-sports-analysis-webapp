from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from itertools import groupby

from .models import LineUp, Subscription


@login_required
def dashboard(request):
    lineups_by_date = []

    # Products a user is subscribed to.
    products = request.user.product_set.all()

    lineups = LineUp.objects.filter(
        products__in=products).order_by('-date_uploaded')

    for date, group in groupby(lineups, key=lambda x: x.date_uploaded):
        lineups_by_date.append({
            'date': date,
            'lineups': list(group)
        })

    return TemplateResponse(request, 'subscriptions/dashboard.html', {
        'lineups_by_date': lineups_by_date
    })
