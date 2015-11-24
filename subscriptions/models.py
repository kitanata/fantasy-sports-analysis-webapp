from django.db import models


class Subscription(models.Model):
    DAILY = 'daily'
    MONTHLY = 'monthly'
    DURATION_CHOICES = (
        (DAILY, 'Daily'),
        (MONTHLY, 'Monthly'),
    )

    name = models.CharField(max_length=128)
    duration = models.CharField(max_length=24, choices=DURATION_CHOICES)
    sport = models.CharField(max_length=24)

    def __str__(self):
        return '%s' % self.name


class LineUp(models.Model):
    pdf = models.FileField()
    date_uploaded = models.DateField(auto_now_add=True)
    subscriptions = models.ManyToManyField(Subscription, blank=True)

    class Meta:
        verbose_name = 'Line Up'
