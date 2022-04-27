from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import LoginAPIView, RegisterView, VerifyEmail, AccountAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('login/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('register', RegisterView.as_view(), name='register'),
    path('email-verify', VerifyEmail.as_view(), name='email-verify'),
    path('', AccountAPIView.as_view(), name='account')
]
