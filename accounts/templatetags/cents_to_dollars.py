from django import template


register = template.Library()


@register.filter
def cents_to_dollars(value):
    value = str(value)
    dollars_part = value[:-2]
    cents_part = value[-2:]
    return '${}.{}'.format(dollars_part, cents_part)
