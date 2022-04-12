
from django.urls.conf import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.CartViewSet, basename='CartItems')

urlpatterns = [
    path('', include(router.urls)),
]