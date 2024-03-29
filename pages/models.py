import uuid
from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from .choices import Choices # to see or edit the choices go to choices.py

class User(AbstractUser):
    member_id = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid.uuid4)
    state_territory = models.CharField(choices=Choices.CHOICES_STATE_TERRITORY, default="") # to see or edit the choices go to choices.py
    profile_picture = ResizedImageField(size=[125, 125], crop=["middle", "center"], quality=100, upload_to="profile_picture", null=True, blank=True) # size is [x, y] in pixels
    banner_picture = ResizedImageField(size=[1250, 300], crop=["middle", "center"], quality=100, upload_to="banner_picture", null=True, blank=True) # size is [x, y] in pixels
    items_sold = models.PositiveIntegerField(default=0)
    credits = models.DecimalField(max_digits=11, decimal_places=2, default=5.00) # number > 999,999,999.99 will result in an error

class Product(models.Model):
    uuid = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=50)
    product_picture = ResizedImageField(size=[500, 500], crop=["middle", "center"], quality=100, upload_to="product_picture", null=False, blank=False) # size is [x, y] in pixels
    description = models.CharField(max_length=500)
    category = models.CharField(choices=Choices.CHOICES_CATEGORY) # to see or edit the choices go to choices.py
    condition = models.CharField(choices=Choices.CHOICES_CONDITION) # to see or edit the choices go to choices.py
    price = models.DecimalField(max_digits=6, decimal_places=2) # number > 9,999.99 will result in an error
    upc = models.CharField(max_length=12, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    list_date = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(choices=Choices.CHOICES_PRODUCT_STATUS, default=Choices.CHOICES_PRODUCT_STATUS[1][0]) # to see or edit the choices go to choices.py
    views = models.PositiveIntegerField(default=0)

class WishList(models.Model):
    uuid = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Cart(models.Model):
    uuid = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Sold(models.Model):
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buy_date = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    uuid = models.UUIDField(primary_key=False, editable=False, unique=True, default=uuid.uuid4)
    buyer = models.ForeignKey(get_user_model(), related_name="buyer", on_delete=models.CASCADE)
    seller = models.ForeignKey(get_user_model(), related_name="seller", on_delete=models.CASCADE)
    overall_rating = models.CharField(choices=Choices.CHOICES_OVERALL_RATING) # to see or edit the choices go to choices.py
    accurate_description = models.PositiveIntegerField(choices=Choices.CHOICES_FEEDBACK_RATING) # to see or edit the choices go to choices.py
    shipping_speed = models.PositiveIntegerField(choices=Choices.CHOICES_FEEDBACK_RATING) # to see or edit the choices go to choices.py
    shipping_cost = models.PositiveIntegerField(choices=Choices.CHOICES_FEEDBACK_RATING) # to see or edit the choices go to choices.py
    communication = models.PositiveIntegerField(choices=Choices.CHOICES_FEEDBACK_RATING) # to see or edit the choices go to choices.py
    comment = models.CharField(max_length=250)
    feedback_date = models.DateTimeField(auto_now_add=True)
