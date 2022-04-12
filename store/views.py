from django.db.models import Q
# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from E_Commerce_Backend.paginations import MyPagination
from store.models import Product
from store.serializers import ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = MyPagination
    # permission_classes = (ProductPermission,)
    queryset = Product.objects.filter(is_available=True).order_by('-created_date')

    @action(methods=['get'], detail=False, url_path='search', url_name='search')
    def search(self, request):
        search_key_word = request.query_params['keyword']
        list_products = Product.objects.order_by('-created_date').filter(
            Q(product_name__icontains=search_key_word)
            | Q(description__icontains=search_key_word)
            | Q(category__category_name__icontains=search_key_word)
        )
        page = self.paginate_queryset(list_products)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=False, url_path='by-category', url_name='by-category')
    def get_products_by_category(self, request):
        category_slug = request.query_params['category']
        list_products = Product.objects.order_by('-created_date').filter(category__slug=category_slug)
        page = self.paginate_queryset(list_products)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
