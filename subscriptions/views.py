import recurly

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib import messages
from datetime import timedelta
from itertools import groupby, chain
from .models import LineUp, Sport, Product, Subscription
from . import signals


@login_required
def dashboard(request):
    if request.GET.get('success') == 'true':
        product = Product.objects.get(recurly_plan_code=request.GET['plan'])
        messages.success(
            request,
            ('Thanks for subscribing to the {} plan. Your lineups will appear '
             'automatically on this page, and you\'ll also receive email '
             'notifications.').format(product.name)
        )
        return redirect(reverse('dashboard'))

    lineups_by_date = []
    two_weeks_ago = timezone.now() - timedelta(days=14)

    # Subscriptions a user has.
    subscriptions = request.user.subscription_set.all().select_related(
        'product'
    )

    lineups = []

    # ordered lineups based on the subscriptions.
    for subscription in subscriptions:
        lineups.append(LineUp.objects.filter(
            Q(date_uploaded__gte=two_weeks_ago) &
            Q(date_uploaded__gte=subscription.activated_at),
            products__in=[subscription.product]
        ).order_by('-date_uploaded'))

    all_lineups = list(chain(*lineups))

    # and her we group the lineups returned by the date they were uploaded,
    # so that we can format the output easily
    for date, group in groupby(
        all_lineups,
        key=lambda x: x.date_uploaded.date()
    ):
        lineups_by_date.append({
            'date': date,
            'lineups': list(group)
        })

    return TemplateResponse(request, 'subscriptions/dashboard.html', {
        'lineups_by_date': lineups_by_date
    })


@login_required
def user_subscriptions(request):
    subscriptions_by_sport = []
    sports = Sport.objects.all().prefetch_related('product_set')

    for sport in sports:
        sport_dict = {
            'name': sport.name,
            'products': []
        }

        for product in sport.product_set.all().order_by('price'):
            subscribed = bool(product.subscribed.filter(
                email=request.user.email,
                subscription__state=Subscription.ACTIVE
            ).count())
            sport_dict['products'].append({
                'product': product,
                'is_subscribed': subscribed
            })

        subscriptions_by_sport.append(sport_dict)

    return TemplateResponse(request, 'subscriptions/user_subscriptions.html', {
        'RECURLY_SUBDOMAIN': settings.RECURLY_SUBDOMAIN,
        'subscriptions_by_sport': subscriptions_by_sport
    })


@csrf_exempt
@require_POST
def push_notifications(request):
    raw_data = request.body
    data = recurly.objects_for_push_notification(raw_data)

    try:
        signal = getattr(signals, data['type'])
    except AttributeError:
        return HttpResponseBadRequest("Invalid notification name.")

    signal.send(sender=request, data=data)

    return HttpResponse()
