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
        ("electronics", "electronics")
    ]

    CHOICES_CONDITION = [
        ("new", "new"),
        ("open box", "open box"),
        ("preowned", "preowned"),
        ("used (like new)", "used (like new)"),
        ("used (moderately)", "used (moderately)"),
        ("used (heavily)", "used (heavily)"),
        ("broken (unusable)", "broken (unusable)")
    ]

    title = models.CharField(max_length=50)
    picture = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=100, upload_to="product_picture", null=False, blank=False)
    description = models.CharField(max_length=500)
    category = models.CharField(choices=CHOICES_CATEGORY)
    condition = models.CharField(choices=CHOICES_CONDITION)
    list_date = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bought = models.BooleanField()

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Sold(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buy_date = models.DateTimeField(auto_now=True)
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)