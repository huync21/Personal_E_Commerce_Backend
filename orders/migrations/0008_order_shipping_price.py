# Generated by Django 4.0.3 on 2022-04-29 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_payment_image_shipment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_price',
            field=models.IntegerField(null=True),
        ),
    ]
