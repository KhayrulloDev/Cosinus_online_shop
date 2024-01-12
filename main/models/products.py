from django.contrib.postgres.search import TrigramSimilarity
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='pics/')
    status = models.BooleanField(default=True)


    # Bu postgres searchdan foydalanish uchun
    # @classmethod
    # def search(cls, query):
    #     return cls.objects.annotate(
    #         similarity=TrigramSimilarity('name', query)
    #     ).filter(similarity__gt=0.3).order_by('-similarity')

    def __str__(self):
        return f"{self.name}"

