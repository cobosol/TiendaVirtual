from django import template
from cart import cart
register = template.Library()
@register.inclusion_tag("tags/cart_box.html")

def cart_box(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count }