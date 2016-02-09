# http://docs.recurly.com/integration/push-notifications

from django.dispatch import Signal, receiver
from django.db.models.signals import m2m_changed
from django.utils import timezone
from datetime import timedelta, datetime
from activecampaign import ActiveCampaign
from .models import LineUp

ac = ActiveCampaign()

# For convienience, I'm defining all the notifications recurly can send.
# Not all of these will be used, but the routing is tested.

# Accounts
new_account_notification = Signal(providing_args=('data',))
canceled_account_notification = Signal(providing_args=('data',))
billing_info_updated_notification = Signal(providing_args=('data',))

# Subscriptions
new_subscription_notification = Signal(providing_args=('data',))
updated_subscription_notification = Signal(providing_args=('data',))
expired_subscription_notification = Signal(providing_args=('data',))
canceled_subscription_notification = Signal(providing_args=('data',))
renewed_subscription_notification = Signal(providing_args=('data',))
reactivated_account_notification = Signal(providing_args=('data',))

# Payments
successful_payment_notification = Signal(providing_args=('data',))
failed_payment_notification = Signal(providing_args=('data',))
successful_refund_notification = Signal(providing_args=('data',))
void_payment_notification = Signal(providing_args=('data',))

# Invoices
new_invoice_notification = Signal(providing_args=('data',))
closed_invoice_notification = Signal(providing_args=('data',))
past_due_invoice_notification = Signal(providing_args=('data',))


@receiver(m2m_changed, sender=LineUp.products.through)
def send_email_campaign(sender, instance, action, **kwargs):
    if action == 'post_add':
        lineup = instance

        if lineup.template_id:
            data_dict = {
                'type': 'single',
                'name': 'campaign: {}'.format(timezone.now()),
                # this is dumb and bad, fix.
                'sdate': datetime.utcnow() - timedelta(hours=5),
                'status': 1,
                'public': 1,
                'tracklinks': 'all',
                'trackreads': 1,
                'trackreplies': 0,
                'htmlunsub': 0,
                'textunsub': 0
            }

            data_dict['m[{}]'.format(lineup.template_id)] = 100

            for product in lineup.products.all():
                data_dict['p[{}]'.format(product.list_id)] = product.list_id

            response = ac.api(
                'campaign_create',
                method='post',
                data=data_dict
            )

            print(response)

            if response['result_code'] != 0:
                lineup.date_email_sent = timezone.now()
                lineup.save()
