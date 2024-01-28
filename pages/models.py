import uuid
from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth import get_user_model
from .choices import ChoicesCategory, ChoicesCondition # to change the choices edit choices.py

class Product(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=50)
    picture = ResizedImageField(size=[500, 500], crop=["middle", "center"], quality=100, upload_to="product_picture", null=False, blank=False)
    description = models.CharField(max_length=500)
    category = models.CharField(choices=ChoicesCategory.CHOICES_CATEGORY) # to change the choices edit choices.py
    condition = models.CharField(choices=ChoicesCondition.CHOICES_CONDITION) # to change the choices edit choices.py
    upc = models.CharField(max_length=12, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    list_date = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bought = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

class Cart(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Sold(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buy_date = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)