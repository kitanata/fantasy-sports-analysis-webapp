from django.db import models
from django.conf import settings
from django.utils import timezone


class Sport(models.Model):
    name = models.CharField(
        max_length=128,
        help_text=('Will be used to group subscriptions together, should be'
                   'a display friendly name')
    )


class Product(models.Model):
    DAILY = 'daily'
    MONTHLY = 'monthly'
    DURATION_CHOICES = (
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
    )

    name = models.CharField(max_length=128)
    duration = models.CharField(max_length=24, choices=DURATION_CHOICES)

    sport = models.ForeignKey(Sport, null=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    subscribed = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Subscription'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        help_text=('Displayed on a user\'s dashboard page, and in any'
                   'marketing messaging related to this product.')
    )

    def __str__(self):
        return '%s' % self.name


class LineUp(models.Model):
    pdf = models.FileField()
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

    def __str__(self):
        return '%s' % self.pdf

    class Meta:
        verbose_name = 'Line Up'
        get_latest_by = 'date_uploaded'


class Subscription(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_subscribed = models.DateField(
        default=timezone.now,
        verbose_name='Date Subscribed',
        help_text='Records the date this subscription became active.'
    )

    def __str__(self):
        return '%s subscribed to %s' % (self.user.email, self.product.name,)
