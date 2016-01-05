from django.conf import settings


def global_settings(request):
    return {
        'RECURLY_PUBLIC_KEY': settings.RECURLY_PUBLIC_KEY
    }
