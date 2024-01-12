from django.db import models
from .products import Product


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    to_whom = models.CharField(max_length=255)
    delivery_time = models.DateTimeField()
    place_of_delivery = models.CharField(max_length=255)

    def total_price(self):
        return self.quantity * self.product.price
