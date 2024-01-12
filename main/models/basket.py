from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Basket(models.Model):
    count = models.PositiveBigIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"


