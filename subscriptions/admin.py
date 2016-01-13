from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import LineUp, Subscription, Product, Sport


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'date_uploaded',
        'date_email_sent',
        'products_list',
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
        'state',
        'activated_at',
        'canceled_at',
        'expired_at',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'recurly_plan_code': ('sport', 'name',)
    }

    readonly_fields = ('list_id',)

    list_display = (
        'name',
        'sport',
        'price',
        'duration',
    )


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    pass
