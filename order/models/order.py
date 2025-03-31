from django.contrib.auth.models import User
from django.db import models
from product.models import Product

class Order(models.Model):
    product = models.ManyToManyField(Product, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)