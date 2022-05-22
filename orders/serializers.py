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
    modified_at = serializers.DateTimeField(format="%d %b %Y")
    payment = PaymentSerializer()
    shipment = ShipmentSerializer()
    class Meta:
        model = Order
        fields = ['id', 'payment', 'shipment', 'order_total', 'total_price', 'shipping_price', 'phone', 'shipping_address', 'modified_at',
                  'status']


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'quantity', 'price']
