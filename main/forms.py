from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user','customer_name', 'product', 'quantity', 'to_whom', 'delivery_time', 'place_of_delivery']