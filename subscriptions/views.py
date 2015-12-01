from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from itertools import groupby, chain

from .models import LineUp, Subscription


@login_required
def dashboard(request):
    lineups_by_date = []
    two_weeks_ago = timezone.now() - timedelta(days=14)

    # Subscriptions a user has.
    subscriptions = request.user.subscription_set.all().select_related(
        'product')

    lineups = []

    # ordered lineups based on the subscriptions.
    for subscription in subscriptions:
        lineups.append(LineUp.objects.filter(
            Q(date_uploaded__gte=two_weeks_ago) &
            Q(date_uploaded__gte=subscription.date_subscribed),
            products__in=[subscription.product]
        ).order_by('-date_uploaded'))

    all_lineups = list(chain(*lineups))

    # and her we group the lineups returned by the date they were uploaded,
    # so that we can format the output easily
    for date, group in groupby(all_lineups, key=lambda x: x.date_uploaded):
        lineups_by_date.append({
            'date': date,
            'lineups': list(group)
        })

    return TemplateResponse(request, 'subscriptions/dashboard.html', {
        'lineups_by_date': lineups_by_date
    })


@login_required
def user_subscriptions(request):
    pass
