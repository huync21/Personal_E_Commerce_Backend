from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet

from banners.models import Banner
from banners.serializers import BannerSerializer


class BannerViewSet(ReadOnlyModelViewSet):
    serializer_class = BannerSerializer
    pagination_class = None
    queryset = Banner.objects.all()