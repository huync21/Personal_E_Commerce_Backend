from django.contrib import admin

# Register your models here.
from carts.models import CartItems

admin.site.register(CartItems)