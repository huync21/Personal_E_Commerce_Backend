from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
from store.models import Product


class Payment(models.Model):
    payment_method = models.CharField(max_length=100)


class Shipment(models.Model):
    service_provider = models.CharField(max_length=100)
    price = models.IntegerField()


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        DELIVERING = 'Delivering', _('Delivering')
        CANCELED = "Canceled", _('Canceled')
        COMPLETED = 'Completed', _('Completed')

    total_price = models.IntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=1000)
    status = models.CharField(max_length=20,
                              choices=OrderStatus.choices,
                              default=OrderStatus.DELIVERING)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



