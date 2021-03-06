import recurly
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.forms import CheckboxSelectMultiple
from decimal import Decimal
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel, MultiFieldPanel
)
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


recurly.SUBDOMAIN = settings.RECURLY_SUBDOMAIN
recurly.API_KEY = settings.RECURLY_API_KEY


@register_snippet
class Sport(models.Model):
    name = models.CharField(
        max_length=128,
        help_text=('Will be used to group subscriptions together, should be '
                   'a display friendly name')
    )

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return '%s' % self.name


class Product(models.Model):
    DAILY = 'days'
    MONTHLY = 'months'
    DURATION_CHOICES = (
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
    )

    DOLLAR_TO_CENTS = 100

    name = models.CharField(max_length=128)

    # Store the Recurly plan code in our db for lookups.
    # From recurly docs: https://dev.recurly.com/docs/create-plan
    # Max length, 50 chars, must be unique, and can only contain
    # the following: [a-z 0-9 @ - _ .]
    recurly_plan_code = models.CharField(
        max_length=50,
        unique=True,
        blank=False,  # We're using pre-populated fields here.
        validators=[
            RegexValidator(
                # ignore case, a-z, 0-9, @, literal -, _, and literal .
                regex=r'(?i)[a-z0-9@\-_\.]',
                message=('Code entered must only contain alphanumeric '
                         'characters, as well as @, -, _, and .')
            )
        ],
        verbose_name='Recurly Plan Code',
        help_text='Used to uniquely identify the product in recurly.'
    )

    # Billing cycle for the product plan. Valid values for recurly are
    # daily and monthly, so I use choices here.
    duration = models.CharField(
        max_length=24,
        choices=DURATION_CHOICES,
        help_text=('Choose whether this product is a monthly subscription '
                   'or a one day purchase.')
    )

    # Sport is used on several pages to group products for display.
    sport = models.ForeignKey(
        Sport,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Used to group together products.'
    )

    # The price of the subscription, stored as a decimal field, but
    # converted to an integer in cents for storage on recurly.
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Price of the product'
    )

    # We use a through model here because we want to store additional
    # info about the subscription.
    subscribed = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Subscription'
    )

    # Upload an image for display on marketing screens.
    marketing_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=('Displayed on a user\'s dashboard page, and in any'
                   'marketing messaging related to this product.')
    )

    panels = [
        FieldPanel('name'),
        SnippetChooserPanel('sport'),
        ImageChooserPanel('marketing_image'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('duration', classname='col6'),
                FieldPanel('price', classname='col6'),
            ]),
        ], 'Price and Duration'),
    ]

    def is_daily(self):
        if self.duration == self.DAILY:
            return True

        return False

    def is_monthly(self):
        return not self.is_daily()

    def get_recurly_plan(self):
        return recurly.Plan.get(self.recurly_plan_code)

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        # Get plan if already existant. If not, create a new plan.
        try:
            plan = self.get_recurly_plan()
            plan.name = self.name
        except recurly.NotFoundError:
            plan = recurly.Plan(
                plan_code=self.recurly_plan_code,
                name=self.name
            )

        # Convert USD price into cents.
        amount_in_cents = recurly.Money(int(self.price * self.DOLLAR_TO_CENTS))
        plan.unit_amount_in_cents = amount_in_cents

        # Apply the selected duration (interval length defaults to 1)
        plan.interval_unit = self.duration
        plan.success_url = settings.RECURLY_SUCCESS_URL
        plan.cancel_url = settings.RECURLY_CANCEL_URL

        # Save the model and plan in recurly.
        plan.save()
        super(Product, self).save(*args, **kwargs)


class LineUp(models.Model):
    pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    date_uploaded = models.DateTimeField(
        verbose_name='Date Uploaded',
        default=timezone.now
    )

    date_email_sent = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Last Email Sent',
        help_text=('Auto-filled. Records the last time an update email was'
                   ' sent to subscribers for this specific line up')
    )

    products = models.ManyToManyField(Product)

    def products_list(self):
        return ', '.join([product.name for product in self.products.all()])

    products_list.verbose_name = 'List of Products'

    panels = [
        DocumentChooserPanel('pdf'),
        FieldPanel('date_uploaded'),
        FieldPanel('date_email_sent'),
        FieldPanel('products', widget=CheckboxSelectMultiple)
    ]

    def __str__(self):
        return '#{}'.format(self.pk)

    class Meta:
        verbose_name = 'Line Up'
        get_latest_by = 'date_uploaded'


class Subscription(models.Model):
    ACTIVE = 'active'
    CANCELED = 'canceled'
    FUTURE = 'future'
    EXPIRED = 'expired'

    STATE_CHOICES = (
        (ACTIVE, 'active',),
        (CANCELED, 'canceled',),
        (FUTURE, 'future',),
        (EXPIRED, 'expired',),
    )

    # Relations we use locally.
    product = models.ForeignKey(
        Product,
        related_name='product',
        help_text='The product this subscription is for.'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text='The user that owns this subscription.'
    )

    # Recurly Mirrored Fields:
    state = models.CharField(
        blank=False,
        null=False,
        max_length=64,
        choices=STATE_CHOICES
    )

    # We're not using UUIDField here because we're populating directly
    # from Recurly.
    uuid = models.CharField(
        max_length=128,
        db_index=True,
        help_text='Recurly uuid.',
        editable=False
    )

    activated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Date Subscribed',
        help_text='Records the date this subscription became active.'
    )

    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date Cancelled',
        help_text='Records the date this subscription was cancelled.'
    )

    expired_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date Expired',
        help_text='Records the date this subscription expired, or will expire.'
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('product', classname='col6'),
                FieldPanel('user', classname='col6'),
            ]),
        ], 'User and Product'),
        FieldPanel('state'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('activated_at', classname='col4'),
                FieldPanel('expired_at', classname='col4'),
                FieldPanel('canceled_at', classname='col4'),
            ]),
        ], 'Dates'),
    ]

    def __str__(self):
        return '#{}'.format(self.pk)
