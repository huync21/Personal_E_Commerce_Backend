from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from accounts.models import Account
from store.models import Product


class Rating(models.Model):
    star_num = models.IntegerField(default=5,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    comment = models.CharField(max_length=555)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
