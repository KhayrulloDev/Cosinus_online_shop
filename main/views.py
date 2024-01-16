import json
from sqlite3 import IntegrityError
from .models import BankCard
from .utils import step_3
import stripe
from random import sample

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import View

from models import Product, Basket, Order
from .forms import OrderForm
from .utils import increment_count, decrement_count, save_order_to_database


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        all_products = Product.objects.all()
        if len(all_products) >= 8:
            products = sample(list(all_products), 8)
        else:
            products = all_products
        return render(request, template_name=self.template_name, context={'products': products})

    def post(self, request):
        id = request.POST.get('id')
        user_id = request.user.id
        try:
            check_card = Basket.objects.get(user=request.user, product=id)
            check_card.count += 1
            check_card.save()
            messages.info(request, 'Added successfully!')
            return redirect('/cart')
        except Basket.DoesNotExist:
            card = Basket.objects.create(
                product_id=id,
                user_id=user_id
            )
            card.save()
            messages.info(request, 'Added successfully!')
            return redirect('/cart')


class ShopView(View):
    template_name = 'shop.html'
    max_products_to_display = 16

    ####   Bu kod postgres seachdan foydalanish uchun
    # def get(self, request):
    #     query = request.GET.get('query')
    #     products = self.get_products(query)
    #     return render(request, self.template_name, context={'products': products, 'query': query})
    #
    # def get_products(self, query=None):
    #     if query:
    #         results = Product.search(query)
    #     else:
    #         all_products = list(Product.objects.all())
    #         if all_products and len(all_products) > self.max_products_to_display:
    #             results = sample(all_products, self.max_products_to_display)
    #         else:
    #             results = all_products[::-1]
    #     return results

    def get(self, request):
        query = request.GET.get('query', None)
        if query is not None:
            products = Product.objects.filter(name__icontains=query)
        else:
            products = Product.objects.all()
        context = {'products': products}
        print(context)
        return render(request, self.template_name, context)

    def post(self, request):
        id = request.POST.get('id')
        user_id = request.user.id
        try:
            check_card = Basket.objects.get(user=request.user, product=id)
            check_card.count += 1
            check_card.save()
            messages.info(request, 'Added successfully!')
            return redirect('/cart')
        except Basket.DoesNotExist:
            card = Basket.objects.create(
                product_id=id,
                user_id=user_id
            )
            card.save()
            messages.info(request, 'Added successfully!')
            return redirect('/cart')


class ShoppingCartView(View):
    tempalate_name = 'cart.html'
    context = {}

    def get(self, request):
        shopping_cart = Basket.objects.filter(user=request.user).values('product_id')
        products = Product.objects.filter(pk__in=shopping_cart)
        data = []
        for product in products:
            shop = Basket.objects.get(Q(user=request.user, product=product))
            product.count = shop.count
            data.append(product)
        self.context.update({'products': data})
        return render(request, 'cart.html', self.context)

    def post(self, request):
        id = request.POST.get('id')
        user = request.user
        shopping_cart = Basket.objects.get(Q(product_id=id) & Q(user=user))
        shopping_cart.delete()
        return redirect('/cart')


class CreateOrderView(View):
    template_name = 'create_order.html'

    def get(self, request, *args, **kwargs):
        form = OrderForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_details', order_id=order.id)
        else:
            return render(request, self.template_name, {'form': form, 'error': 'Invalid data'})


class OrderDetailsView(View):
    template_name = 'order_details.html'

    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        return render(request, self.template_name, {'order': order})


class ListOrdersView(View):
    template_name = 'list_orders.html'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        return render(request, self.template_name, {'orders': orders})


class ChargeView(View):
    template_name = 'paymant.html'

    def post(self, request, *args, **kwargs):
        token = request.POST.get('stripeToken')
        amount = float(request.POST.get('amount_pay', 0))
        amount = amount * 100
        if amount:
            try:
                customer = stripe.Customer.create(
                    email=request.user.email,
                    source=token,
                )
                order = save_order_to_database(
                    user=request.user,
                    amount=amount,
                    product_id=request.POST.get('product_id'),
                    quantity=request.POST.get('quantity'),
                    to_whom=request.POST.get('to_whom'),
                    delivery_time=request.POST.get('delivery_time'),
                    place_of_delivery=request.POST.get('place_of_delivery')
                )

                # Pul yechib olish
                charge = stripe.Charge.create(
                    amount=amount,
                    currency='uzs',
                    description=f'Buyurtma #{order.id}',
                    customer=customer.id,
                )

                return render(request, self.template_name, {'success': charge})
            except stripe.error.CardError as e:
                return render(request, 'paymant.html', {'error': e})
        else:
            return render(request, 'paymant.html', {'error': "Noto'g'ri formatdagi summa"})



class AddCardView(View):

    def get(self, request):
        return render(request, 'add-card.html')
    def post(self, request, *args, **kwargs):
        cart_number1 = request.POST.get('cart_nuber')
        expiration_date = request.POST.get('expiration_date')
        cvc = request.POST.get('cvc')

        card_number = step_3(cart_number1)

        try:
            card_data = BankCard.objects.get(card_number=card_number)
        except BankCard.DoesNotExist:
            card_data = None

        if card_data:
            return JsonResponse({'success': False, 'message': 'Card already exists!'}, status=400)
        else:
            try:
                BankCard.objects.create(
                    card_number=card_number,
                    card_expiration=expiration_date,
                    card_cvc=cvc,
                    user_id=request.POST.get('user_id')
                )
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'IntegrityError occurred'}, status=500)

        return JsonResponse({'success': True, 'message': 'Successfully added'})


class IncrementCountView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            id = json_data.get('id')
        except json.JSONDecodeError:
            id = None
        result = increment_count(id, request.user)
        return JsonResponse({'result': result})


class DecrementCountView(View):

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            id = json_data.get('id')
        except json.JSONDecodeError:
            id = None
        result = decrement_count(id, request.user)
        return JsonResponse({'result': result})
