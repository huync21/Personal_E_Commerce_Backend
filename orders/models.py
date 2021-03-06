from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from accounts.models import Account
from store.models import Product


class Payment(models.Model):
    payment_method = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/payments', null=True)

    def __str__(self):
        return self.payment_method


class Shipment(models.Model):
    service_provider = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/shipments', null=True)

    def __str__(self):
        return self.service_provider


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        DELIVERING = 'Delivering', _('Delivering')
        CANCELED = "Canceled", _('Canceled')
        COMPLETED = 'Completed', _('Completed')

    total_price = models.IntegerField()
    order_total = models.IntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=True)
    shipping_address = models.CharField(max_length=1000)
    status = models.CharField(max_length=20,
                              choices=OrderStatus.choices,
                              default=OrderStatus.DELIVERING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    shipping_price = models.IntegerField()

    def __str__(self):
        return str(self.id)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
