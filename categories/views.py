# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = None
    queryset = Category.objects.all()
