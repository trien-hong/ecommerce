from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Product(models.Model):
    # i'll add in more categories and possible more fields later
    CHOICES_CATEGORY = [
        ("kitchen", "kitchen"),
        ("living room", "living room"),
        ("garage", "garage"),
        ("bathroom", "bathroom"),
        ("bedroom", "bedroom"),
        ("office", "office"),
        ("outdoor", "outdoor"),
        ("toys", "toys"),
        ("games", "games"),
        ("clothing", "clothing"),
        ("electronics", "electronics"),
        ("mechanical parts", "mechanical parts")
    ]

    title = models.CharField(max_length=50)
    picture = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=100, upload_to="product_picture", null=False, blank=False)
    description = models.CharField(max_length=500)
    category = models.CharField(choices=CHOICES_CATEGORY)
    list_date = models.DateTimeField(auto_now=True)
    lister = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    bought = models.BooleanField()

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)

class Sold(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    buy_date = models.DateTimeField(auto_now=True)
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)