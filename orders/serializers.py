from rest_framework import serializers

from orders.models import Payment, Shipment, Order, OrderProduct
from store.serializers import ProductSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y")
    class Meta:
        model = Order
        fields = ['id', 'payment', 'shipment','order_total', 'total_price', 'phone', 'shipping_address', 'created_at', 'status']


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'quantity', 'price']
