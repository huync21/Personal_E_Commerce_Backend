from django.db import transaction, IntegrityError
from django.shortcuts import render
from rest_framework import viewsets, status

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import CartItems
from orders.models import Order, OrderProduct, Payment, Shipment
from orders.permissions import OrderAPIPermission, ShipmentAPIPermission
from orders.serializers import OrderSerializer, PaymentSerializer, ShipmentSerializer
from store.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (OrderAPIPermission,)
    pagination_class = None

    def get_queryset(self):
        current_user = self.request.user
        list_order = Order.objects.filter(account_id=current_user.id)
        return list_order

    def create(self, request, *args, **kwargs):
        current_user = self.request.user
        # input
        phone = self.request.data["phone"]
        shipping_address = self.request.data["shipping_address"]
        list_cart_item_id = list(self.request.data["list_cart_item_id"])
        shipment_id = int(self.request.data["shipment_id"])
        payment_id = int(self.request.data["payment_id"])
        total_price = int(self.request.data["total_price"])

        # process

        with transaction.atomic():
            order = Order.objects.create(payment_id=payment_id, shipment_id=shipment_id, phone=phone,
                                         shipping_address=shipping_address, account_id=current_user.id,
                                         total_price=total_price)
            for cart_item_id in list_cart_item_id:
                cart_item = CartItems.objects.get(id=cart_item_id)
                product = Product.objects.get(id=cart_item.product_id)
                if product is not None:
                    if product.stock >= cart_item.quantity:
                        order_product = OrderProduct(product_id=cart_item.product_id, price=cart_item.product.price,
                                                     quantity=cart_item.quantity, order_id=order.id)
                        order_product.save()
                        cart_item.delete()
                    else:
                        return Response(data={"message": "San pham " + product + " chi con lai" + product.stock +
                                                         " san pham trong khi ban dat " + cart_item.quantity + " san pham"}
                                        , status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"message": "San pham " + product.product_name + " khong ton tai"},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response(data={"message": "Thanh toan don hang thanh cong"}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='payment-methods', url_name='payment-methods', name='payment-methods', permission_classes=(ShipmentAPIPermission,))
    def payment_methods(self, request):
        payments = Payment.objects.all()
        return Response(data=PaymentSerializer(list(payments), many=True, context={"request": request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='shipment-methods', url_name='shipment-methods',
            name='shipment-methods', permission_classes=(ShipmentAPIPermission,))
    def shipment_methods(self, request):
        shipments = Shipment.objects.all()
        return Response(data=ShipmentSerializer(list(shipments), many=True, context={"request": request}).data, status=status.HTTP_200_OK)
