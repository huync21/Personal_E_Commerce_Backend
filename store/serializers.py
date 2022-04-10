from rest_framework import serializers
from categories.serializers import CategorySerializer
from store.models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'slug', 'description', 'price', 'images', 'stock', 'category')
