from django.db import transaction
from rest_framework import viewsets, status

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from E_Commerce_Backend.paginations import MyPagination
from carts.models import CartItems
from orders.models import Order, OrderProduct, Payment, Shipment
from orders.permissions import OrderAPIPermission, ShipmentAPIPermission
from orders.serializers import OrderSerializer, PaymentSerializer, ShipmentSerializer, OrderProductSerializer
from store.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (OrderAPIPermission,)
    pagination_class = None

    def get_queryset(self):
        current_user = self.request.user
        list_order = Order.objects.filter(account_id=current_user.id).order_by("-modified_at")
        return list_order

    @action(methods=['get'], detail=False, url_path='all', url_name='all-order-pagination',
            name='order-pagination', permission_classes=(OrderAPIPermission,))
    def orders(self, request):
        paginator = MyPagination()
        current_user = self.request.user
        list_order = Order.objects.filter(account_id=current_user.id).order_by("-modified_at")
        page = paginator.paginate_queryset(list_order, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        current_user = self.request.user
        # input
        phone = self.request.data["phone"]
        shipping_address = self.request.data["shipping_address"]
        list_cart_item_id = list(self.request.data["list_cart_item_ids"])
        shipment_id = int(self.request.data["shipment_id"])
        payment_id = int(self.request.data["payment_id"])
        total_price = int(self.request.data["total_price"])

        # process
        shipment = Shipment.objects.get(id=shipment_id)
        payment = Payment.objects.get(id=payment_id)
        order_total = total_price+shipment.price

        with transaction.atomic():
            order = Order.objects.create(payment_id=payment_id, shipment_id=shipment_id, phone=phone,
                                         shipping_address=shipping_address, account_id=current_user.id,
                                         total_price=total_price, order_total=order_total, shipping_price=shipment.price)
            for cart_item_id in list_cart_item_id:
                cart_item = CartItems.objects.get(id=int(cart_item_id))
                product = Product.objects.get(id=cart_item.product_id)
                if product is not None:
                    if product.stock >= cart_item.quantity:
                        order_product = OrderProduct(product_id=cart_item.product_id, price=cart_item.product.price,
                                                     quantity=cart_item.quantity, order_id=order.id)
                        product.stock = product.stock - order_product.quantity
                        product.save()
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

    # @action(methods=['get'], detail=False, url_path='payment-method', url_name='payment-method', name='payment-method', permission_classes=(ShipmentAPIPermission,) )
    # def get_payment_method(self, request):
    #     order_id = self.request.query_params.get('order_id')
    #     order = Order.objects.get(id=order_id)
    #     payment = order.payment
    #     return Response(data=PaymentSerializer(payment, many=False, context={"request": request}).data, status= status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='shipment-methods', url_name='shipment-methods',
            name='shipment-methods', permission_classes=(ShipmentAPIPermission,))
    def shipment_methods(self, request):
        shipments = Shipment.objects.all()
        return Response(data=ShipmentSerializer(list(shipments), many=True, context={"request": request}).data, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False, url_path='shipment-method', url_name='shipment-method', name='shipment-method',
    #         permission_classes=(ShipmentAPIPermission,))
    # def get_shipment_method(self, request):
    #     order_id = self.request.query_params.get('order_id')
    #     order = Order.objects.get(id=order_id)
    #     shipment = order.shipment
    #     return Response(data=PaymentSerializer(shipment, many=False, context={"request": request}).data,
    #                     status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='detail', url_name='detail',
            name='order-detail')
    def order_details(self, request):
        order_id = self.request.query_params.get('order_id')
        order_products = OrderProduct.objects.filter(order_id=order_id)

        return Response(data=OrderProductSerializer(list(order_products), many=True, context={"request": request}).data, status=status.HTTP_200_OK)