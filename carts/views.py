from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from carts.models import CartItems
from carts.permissions import CartAPIPermission
from carts.serializers import CartSerializer
from store.models import Product


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    pagination_class = None
    permission_classes = (CartAPIPermission,)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.is_active = False
        cart_item.save()
        return Response(data={"message": "Delete Cart Item Successfully!"}, status=status.HTTP_200_OK)

    def get_queryset(self):
        account = self.request.user
        cart_item_of_user = CartItems.objects.filter(account_id=account.id, is_active=True).order_by('-created_at')
        return cart_item_of_user

    def create(self, request, *args, **kwargs):
        cart_item_from_request = self.request.data
        quantity = int(cart_item_from_request["quantity"])
        product_id = int(cart_item_from_request["product_id"])

        # Check xem trong list cart item cua nguoi dung da co product nay chua
        existed_cart_item = None
        list_cart_item_of_user = self.get_queryset()
        for cart_item in list_cart_item_of_user:
            pid = cart_item.product_id
            if product_id == pid:
                existed_cart_item = cart_item
                break

        # Neu co product y trong list cart item roi thi update lai quantity
        message = ""
        if existed_cart_item is not None:
            quantity = existed_cart_item.quantity + quantity

        # Check xem quantiy co vuot qua quantity cua product khong, neu vuot qua thi them khong thanh cong
        product = Product.objects.get(id=product_id)
        if quantity > product.stock:
            return Response(data={"message": "The quantity you want to add to cart is beyond the quantity in stock of "
                                             "product."}, status=status.HTTP_400_BAD_REQUEST)

        # Neu co product y trong list cart item roi thi update quantity cua cart item do
        # Neu khong thi them moi cart item
        if existed_cart_item is not None:
            existed_cart_item.quantity = quantity
            existed_cart_item.save()
            message = "Update cart item successfully!"
        else:
            CartItems.objects.create(quantity=quantity, product_id=product_id, account_id=self.request.user.id)
            message = "Add product to cart successfully!"

        return Response({"message": message}, status=status.HTTP_200_OK)


