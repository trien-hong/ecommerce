import uuid
from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth import get_user_model

class Product(models.Model):
    # i'll add in more categories and possible more fields later
    
    PLEASE_CHOOSE_CATEGORY = ""
    KITCHEN = "kitchen"
    LIVING_ROOM = "living room"
    GARAGE = "garage"
    BATHROOM = "bathroom"
    BEDROOM = "bedroom"
    OFFICE = "office"
    OUTDOOR = "outdoor"
    TOYS = "toys"
    GAMES = "games"
    CLOTHING = "clothing"
    ELECTRONICS = "electronics"

    CHOICES_CATEGORY = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_CATEGORY, "Choose a category"),
        (KITCHEN, "kitchen"),
        (LIVING_ROOM, "living room"),
        (GARAGE, "garage"),
        (BATHROOM, "bathroom"),
        (BEDROOM, "bedroom"),
        (OFFICE, "office"),
        (OUTDOOR, "outdoor"),
        (TOYS, "toys"),
        (GAMES, "games"),
        (CLOTHING, "clothing"),
        (ELECTRONICS, "electronics")
    ]

    PLEASE_CHOOSE_CONDITION = ""
    NEW = "new"
    OPEN_BOX = "open box"
    PREOWNED = "preowned"
    USED_LIKE_NEW = "use (like new)"
    USED_MODERATELY = "used (moderately)"
    USED_HEAVILY = "used (heavily)"
    BROKEN_UNUSABLE = "broken (unusable)"

    CHOICES_CONDITION = [
        # actual values are what's stores in the database
        # (actual values, human readable values)
        # for this case, both are the same
        (PLEASE_CHOOSE_CONDITION, "Choose a condition"),
        (NEW, "new"),
        (OPEN_BOX, "open box"),
        (PREOWNED, "preowned"),
        (USED_LIKE_NEW, "used (like new)"),
        (USED_MODERATELY, "used (moderately)"),
        (USED_HEAVILY, "used (heavily)"),
        (BROKEN_UNUSABLE, "broken (unusable)")
    ]

    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=50)
    picture = ResizedImageField(size=[500, 500], crop=["middle", "center"], quality=100, upload_to="product_picture", null=False, blank=False)
    description = models.CharField(max_length=500)
    category = models.CharField(choices=CHOICES_CATEGORY)
    condition = models.CharField(choices=CHOICES_CONDITION)
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