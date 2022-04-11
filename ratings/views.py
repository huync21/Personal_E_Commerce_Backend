from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from ratings.models import Rating
from ratings.permissions import RatingApiPermission
from ratings.serializers import RatingSerializer


class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    pagination_class = None
    permission_classes = (RatingApiPermission,)

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        list_rating_of_product = Rating.objects.filter(product_id=product_id).order_by('-created_at')
        return list_rating_of_product

    def create(self, request, *args, **kwargs):
        pass


