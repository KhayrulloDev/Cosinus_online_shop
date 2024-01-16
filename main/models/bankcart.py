from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BankCart(models.Model):
    card_number = models.CharField()
    card_expiration = models.IntegerField()
    card_cvc = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
