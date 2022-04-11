from django.contrib import admin

# Register your models here.
from orders.models import Payment, Shipment, Order, OrderProduct

admin.site.register(Payment)
admin.site.register(Shipment)
admin.site.register(Order)
admin.site.register(OrderProduct)