from decimal import Decimal
from django import template


register = template.Library()
TWOPLACES = Decimal(10) ** -2


@register.filter
def cents_to_dollars(value):
    d = Decimal(value) / 100
    return '${}'.format(d.quantize(TWOPLACES))
