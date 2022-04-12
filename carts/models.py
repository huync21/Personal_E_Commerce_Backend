from django.db import models

# Create your models here.
from accounts.models import Account
from store.models import Product


class CartItems(models.Model):
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return 'product: ' + self.product.product_name + ' || quantity:' + str(self.quantity)
