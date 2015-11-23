from django.contrib import admin
from .models import LineUp, Subscription


@admin.register(LineUp)
class LineUpAdmin(admin.ModelAdmin):
    raw_id_fields = ('subscriptions',)
    autocomplete_lookup_fields = {
        'm2m': ['subscriptions']
    }


admin.site.register(Subscription)
