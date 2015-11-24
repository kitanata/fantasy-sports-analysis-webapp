from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import LineUp, Subscription, Product


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Subscription)
admin.site.register(Product)
