from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Products(models.Model):
    CATEGORY = [
        ("kitchen", "kitchen"),
        ("living room", "living room"),
        ("garage", "garage"),
        ("bathroom", "bathroom"),
        ("bedroom", "bedroom")
    ]

    title = models.CharField(max_length=25)
    picture = ResizedImageField(size=[325, 325], crop=['middle', 'center'], quality=100, upload_to="product_picture", null=False, blank=False)
    category = models.CharField(choices=CATEGORY)
    description = models.CharField(max_length=500)
    list_date = models.DateTimeField(auto_now=True)
    lister = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    # there's no price yet. i'll add that in later.