from django.dispatch import receiver

from . import signals
from .models import Subscription, Product


@receiver(signals.new_subscription_notification)
def new_subscription_handler(sender, **kwargs):
    """
    Handle the new subscription event from Recurly by creating a new
    subscription for the given user and product.
    """

    sub = kwargs['data']['subscription']
    plan_code = sub.plan.plan_code
    product = Product.objects.get(recurly_plan_code=plan_code)

    Subscription.objects.create(
        user=sender.user,
        product=product,
        state=sub.state,
        uuid=sub.uuid,
        activated_at=sub.activated_at,
        canceled_at=sub.canceled_at,
        expired_at=sub.expires_at
    )


@receiver(signals.updated_subscription_notification)
def update_subscription_handler(sender, **kwargs):
    pass
