from wagtailmodeladmin.options import ModelAdmin, wagtailmodeladmin_register
from .models import LineUp, Subscription, Product


class LineUpModelAdmin(ModelAdmin):
    model = LineUp
    menu_label = 'Line Ups'
    menu_icon = 'date'
    menu_order = 100
    add_to_settings_menu = False

    list_display = (
        '__str__',
        'uploaded_pdf',
        'date_uploaded',
        'date_email_sent',
        'products_list',
    )

    list_filter = (
        'date_uploaded',
        'date_email_sent',
    )

    search_fields = (
        'uploaded_pdf__title',
        'date_uploaded',
    )


class ProductModelAdmin(ModelAdmin):
    model = Product
    menu_label = 'Products'
    menu_icon = 'date'
    menu_order = 200
    add_to_settings_menu = False

    list_display = (
        'name',
        'sport',
        'recurly_plan_code',
        'price',
        'duration',
    )

    list_filter = (
        'sport',
        'duration',
    )

    search_fields = (
        'name',
    )


class SubscriptionModelAdmin(ModelAdmin):
    model = Subscription
    menu_label = 'Subscriptions'
    menu_icon = 'date'
    menu_order = 300
    add_to_settings_menu = False

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
        'state',
        'product',
        'activated_at',
        'canceled_at',
        'expired_at',
    )

    search_fields = (
        'user__email',
    )


wagtailmodeladmin_register(LineUpModelAdmin)
wagtailmodeladmin_register(ProductModelAdmin)
wagtailmodeladmin_register(SubscriptionModelAdmin)
