from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting(icon='mail')
class ActiveCampaignSettings(BaseSetting):
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=10)
