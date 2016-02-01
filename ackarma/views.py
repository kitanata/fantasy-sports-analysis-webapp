from django.template.response import TemplateResponse
from subscriptions.models import Sport, Subscription


def homepage(request):
    subscriptions_by_sport = []
    sports = Sport.objects.all().prefetch_related('product_set')

    for sport in sports:
        sport_dict = {
            'name': sport.name,
            'products': []
        }

        for product in sport.product_set.all().order_by('price'):
            if request.user.is_authenticated():
                subscribed = bool(product.subscribed.filter(
                    email=request.user.email,
                    subscription__state=Subscription.ACTIVE
                ).count())
            else:
                subscribed = False

            sport_dict['products'].append({
                'product': product,
                'is_subscribed': subscribed
            })

        subscriptions_by_sport.append(sport_dict)

    return TemplateResponse(request, 'home.html', {
        'subscriptions_by_sport': subscriptions_by_sport
    })
