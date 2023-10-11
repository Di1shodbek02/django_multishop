from django import template

register = template.Library()


@register.simple_tag
def total_price(price, count):
    return int(price) * int(count)
