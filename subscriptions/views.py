from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from itertools import groupby

from .models import LineUp, Subscription


@login_required
def dashboard(request):
    lineups_by_date = []
    two_weeks_ago = timezone.now() - timedelta(days=14)

    # Products a user is subscribed to.
    products = request.user.product_set.all()

    # ordered lineups based on the above products.
    lineups = LineUp.objects.filter(
        products__in=products,
        date_uploaded__gte=two_weeks_ago).order_by('-date_uploaded')

    # and her we group the lineups returned by the date they were uploaded,
    # so that we can format the output easily
    for date, group in groupby(lineups, key=lambda x: x.date_uploaded):
        lineups_by_date.append({
            'date': date,
            'lineups': list(group)
        })

    return TemplateResponse(request, 'subscriptions/dashboard.html', {
        'lineups_by_date': lineups_by_date
    })
