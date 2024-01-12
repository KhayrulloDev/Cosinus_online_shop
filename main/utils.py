
from django.db.models import Q

from .models.basket import Basket


def increment_count(id, user):
    try:
        shopping_cart = Basket.objects.get(Q(product_id=id) & Q(user=user))
        shopping_cart.count += 1
        shopping_cart.save()
    except:
        return False
    return True


def decrement_count(id, user):
    try:
        shopping_cart = Basket.objects.get(Q(product_id=id) & Q(user=user))
        shopping_cart.count -= 1
        shopping_cart.save()
    except:
        return False
    return True