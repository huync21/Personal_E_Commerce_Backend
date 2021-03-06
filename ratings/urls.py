from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ratings import views

router = DefaultRouter()
router.register('', views.RatingViewSet, basename='Rating')

urlpatterns = [
    path('', include(router.urls)),
]