import uuid
from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from .choices import Choices # to change the choices edit choices.py

class User(AbstractUser):
    credits = models.DecimalField(max_digits=9, decimal_places=2, default=5.00)

class Product(models.Model):
    uuid = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=50)
    picture = ResizedImageField(size=[500, 500], crop=["middle", "center"], quality=100, upload_to="product_picture", null=False, blank=False)
    description = models.CharField(max_length=500)
    category = models.CharField(choices=Choices.CHOICES_CATEGORY) # to change the choices edit choices.py
    condition = models.CharField(choices=Choices.CHOICES_CONDITION) # to change the choices edit choices.py
    price = models.DecimalField(max_digits=6, decimal_places=2)
    upc = models.CharField(max_length=12, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    list_date = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bought = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

class Cart(models.Model):
    uuid = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Sold(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buy_date = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)