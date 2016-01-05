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

from .models import LineUp, Sport, Subscription, Product
from .forms import BillingInfoForm
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


def upgrade_subscription(request, plan_code):
    if not request.user:
        messages.info(
            request,
            'To process your order you will need to create an account'
        )
        url = reverse('signup')
        url = url + '?next=upgrade_subscription'
        return redirect(reverse('signup'))
    else:
        email = request.user.email

        try:
            account = recurly.Account.get(email)
            # Previously un-nested, unnecessary to try and call .billing_info
            # on what is obviously None
            try:
                billing_info = account.billing_info
            except AttributeError:
                billing_info = None

        except recurly.errors.NotFoundError:
            account = None
            billing_info = None

        if billing_info is not None:
            product = Product.objects.find_or_fail(recurly_plan_code=plan_code)
            sport = product.sport
            subscription = Subscription.objects.filter(
                sport=sport,
                user=request.user
            ).first()

            if subscription is None:
                recurly_subscription = recurly.Subscription()
                recurly_subscription.plan_code = plan_code
                recurly_subscription.currency = 'USD'
                recurly_subscription.account = account
                recurly_subscription.save()

                messages.success(
                    request,
                    'Thank you for subscribing to {}!'.format(product.name)
                )
            else:
                recurly_subscription = recurly.Subscription.get(
                    subscription.uuid
                )
                recurly_subscription.plan_code = plan_code
                recurly_subscription.currency = 'USD'
                recurly_subscription.timeframe = 'now'
                recurly_subscription.save()

                messages.success(
                    request,
                    'Thank you for upgrading your subscription to {}!'.format(
                        product.name
                    )
                )

            return redirect(reverse('dashboard'))

        else:
            # Temporary, obviously
            messages.info(
                request,
                ('Please fill out billing information before trying to ',
                 'subscribe to a product.')
            )
            return redirect(reverse('billing_information'))


@login_required
def billing_information(request):
    email = request.user.email

    try:
        account = recurly.Account.get(email)
        # Previously un-nested, unnecessary to try and call .billing_info
        # on what is obviously None
        try:
            billing_info = account.billing_info
        except AttributeError:
            billing_info = None

    except recurly.errors.NotFoundError:
        account = None
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
        billing = billing_info.__dict__

        form = BillingInfoForm(initial={
            'first_name': billing.get('first_name', ''),
            'last_name': billing.get('last_name', ''),
            'number': 'xxxx xxxx xxxx {}'.format(
                billing.get('last_four', 'xxxx')
            ),
            'month': billing.get('month', ''),
            'year': billing.get('year', ''),
            'address1': billing.get('address1', ''),
            'address2': billing.get('address2', ''),
            'city': billing.get('city', ''),
            'state': billing.get('state', ''),
            'country': billing.get('country', '')
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
