from django.urls import path, include
from rest_framework.routers import DefaultRouter

from banners import views

router = DefaultRouter()
router.register('', views.BannerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]