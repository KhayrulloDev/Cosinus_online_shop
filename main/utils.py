
from django.db.models import Q

from .models import Product, Order
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

def save_order_to_database(user, amount, product_id, quantity, to_whom, delivery_time, place_of_delivery):
    product = Product.objects.get(id=product_id)

    order = Order(
        user=user,
        amount=amount,
        product=product,
        quantity=quantity,
        to_whom=to_whom,
        delivery_time=delivery_time,
        place_of_delivery=place_of_delivery
    )
    order.save()
    return order