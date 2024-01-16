
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


import os
from dotenv import load_dotenv

load_dotenv()
STEP = int(os.environ.get('STEP'))


def step_1(card_number: str):
    card_number = ''.join(str((int(x) + STEP) % 10) for x in card_number)
    return card_number


def step_2(card_number: str):
    letters = 'JABCDEFGHI'
    card_number = step_1(card_number)
    hashed_card = []
    for i in range(len(card_number)):
        hashed_card.append(letters[int(card_number[i])])
    return ''.join(hashed_card)


def step_3(card_number: str):
    card_number = step_2(card_number)
    three_hashed = ''
    for i in card_number:
        three_hashed += str(ord(i))
    return three_hashed[::-1]


def decode_card_number(card_number: str):
    card_number = card_number[::-1]
    card_partitions = [card_number[i]+card_number[i+1] for i in range(0, len(card_number)-1, 2)]
    number = ''
    for x in card_partitions:
        m = int(x) - 64 - STEP
        if m < 0:
            m += 10
        number += str(m)
    return number


def collect_to_list(card_data):
    cards_data = []
    for element in card_data:
        id = element.id
        card_number = decode_card_number(element.card_number)
        card_expiration = element.card_expiration
        data = {
            'id': id,
            'card_number': card_number[:4] + '*'*8 + card_number[-4:],
            'card_expiration': card_expiration
        }
        cards_data.append(data)
    return cards_data