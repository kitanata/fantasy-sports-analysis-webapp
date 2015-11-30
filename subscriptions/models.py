from django.db import models
from django.conf import settings
from django.utils import timezone


class Product(models.Model):
    DAILY = 'daily'
    MONTHLY = 'monthly'
    DURATION_CHOICES = (
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
    )

    name = models.CharField(max_length=128)
    duration = models.CharField(max_length=24, choices=DURATION_CHOICES)

    def __str__(self):
        return '%s' % self.name


class LineUp(models.Model):
    pdf = models.FileField()
    date_uploaded = models.DateField(default=timezone.now)
    products = models.ManyToManyField(Product)

    class Meta:
        verbose_name = 'Line Up'
        get_latest_by = 'date_uploaded'


class Subscription(models.Model):
    product = models.ForeignKey(Product)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '%s subscribed to %s' % (self.user.email, self.product.name,)
