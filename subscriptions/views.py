import recurly

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
from datetime import timedelta
from itertools import groupby, chain
from .models import LineUp, Sport
from .forms import BillingInfoForm
from . import signals


@login_required
def dashboard(request):
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
                email=request.user.email).count())
            sport_dict['products'].append({
                'product': product,
                'is_subscribed': subscribed
            })

        subscriptions_by_sport.append(sport_dict)

    return TemplateResponse(request, 'subscriptions/user_subscriptions.html', {
        'RECURLY_SUBDOMAIN': settings.RECURLY_SUBDOMAIN,
        'subscriptions_by_sport': subscriptions_by_sport
    })


@login_required
def billing_information(request):
    email = request.user.email

    try:
        account = recurly.Account.get(email)
    except recurly.errors.NotFoundError:
        account = None

    try:
        billing_info = account.billing_info
    except AttributeError:
        billing_info = None

    if request.method == 'POST':
        form = BillingInfoForm(request.POST)
        if form.is_valid():
            form.clean()
            token = form.cleaned_data['token']

            if account is None:
                account = recurly.Account(account_code=email)
                account.first_name = request.user.first_name
                account.last_name = request.user.last_name
                account.email = email
                account.save()

            if billing_info is None:
                account.billing_info = recurly.BillingInfo()
                billing_info = account.billing_info

            billing_info.token_id = token
            account.update_billing_info(billing_info)

            messages.success(
                request,
                'Successfully updated your billing information.'
            )

    if billing_info is not None:
        form = BillingInfoForm(initial={
            'first_name': billing_info.first_name,
            'last_name': billing_info.last_name,
            'number': 'xxxx xxxx xxxx {}'.format(billing_info.last_four),
            'month': billing_info.month,
            'year': billing_info.year,
            'address1': billing_info.address1,
            'address2': billing_info.address2,
            'city': billing_info.city,
            'state': billing_info.state,
            'country': billing_info.country
        })
    else:
        form = BillingInfoForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })

    return TemplateResponse(
        request,
        'subscriptions/billing_information.html',
        {
            'form': form
        }
    )


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
