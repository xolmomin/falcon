from django import template

from apps.models import Wishlist

register = template.Library()


@register.filter
def check_wishlist(user, product):
    if user.is_anonymous:
        return False
    return Wishlist.objects.filter(user=user, product=product).exists()
