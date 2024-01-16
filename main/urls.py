from django.urls import path

from main.views import HomeView, ShopView, ShoppingCartView, ListOrdersView, CreateOrderView, OrderDetailsView, \
    AddCardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('cart', ShoppingCartView.as_view(), name='cart'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('order_details/<int:order_id>/', OrderDetailsView.as_view(), name='order_details'),
    path('list_orders/', ListOrdersView.as_view(), name='list_orders'),
    path('add-cart/', AddCardView.as_view(), name='card-add'),
]
