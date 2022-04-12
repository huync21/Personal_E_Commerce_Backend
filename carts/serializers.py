from rest_framework.serializers import ModelSerializer

from carts.models import CartItems
from store.serializers import ProductSerializer


class CartSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItems
        fields = ["id", "quantity", "product"]