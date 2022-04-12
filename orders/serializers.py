from rest_framework import serializers

from orders.models import Payment, Shipment, Order, OrderProduct


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','payment', 'shipment', 'total_price', 'phone', 'shipping_address', 'created_at', 'status']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'quantity', 'price']