from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import LineUp, Subscription


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Subscription)
