from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import LineUp, Subscription, Product, Sport
from .forms import ProductAdminForm


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'pdf',
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

    list_filter = (
        'user',
        'state',
        'product',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    prepopulated_fields = {
        'recurly_plan_code': ('sport', 'name',)
    }

    readonly_fields = ('list_id',)

    list_display = (
        'name',
        'sport',
        'recurly_plan_code',
        'price',
        'duration',
    )


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    pass
