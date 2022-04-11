from django.contrib import admin

# Register your models here.
from ratings.models import Rating

admin.site.register(Rating)