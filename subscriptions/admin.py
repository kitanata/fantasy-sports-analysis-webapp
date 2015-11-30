from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import LineUp, Subscription, Product


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'date_uploaded',
        'date_email_sent',
        'products_list'
    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'product',
        'date_subscribed'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
