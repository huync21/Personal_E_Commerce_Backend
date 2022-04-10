from django.db import models

# Create your models here.


class Banner(models.Model):
    banner_name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='photos/banners')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.banner_name