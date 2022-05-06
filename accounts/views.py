import re

import jwt
import phonenumbers
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
# Create your views here.
from django.urls import reverse
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from rest_framework import status, generics, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
# from api.permissions import ProductPermission
from accounts.models import Account
from E_Commerce_Backend import settings
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
from accounts.permissions import AccountAPIPermission
from accounts.serializers import RegisterSerializer, LoginSerializer, AccountSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        # validate các trường và lưu xuống db
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = Account.objects.get(email=user_data['email'])

        # gen ra token chứa thông tin về user đấy để tí đính vào link xác thực để biết là xác thực cho user nào
        token = RefreshToken.for_user(user).access_token

        # gửi mail cho người dùng
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absolute_url = "http://" + current_site + relative_link + "?token=" + str(token)
        email_subject = "Xác nhận tài khoản của bạn: "
        email_body = "Xin chào " + user.first_name + ", hãy xác nhận tài khoản E-Commerce của bạn bằng link dưới:\n" + absolute_url
        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()

        return Response(user_data, status=status.HTTP_201_CREATED)



class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = Account.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
            else:
                return Response({'email': 'You have already activated this email!'}, status=status.HTTP_200_OK)
            return Response({'email': 'Active email successfully!'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation token has expired!'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountAPIView(generics.GenericAPIView):
    permission_classes = (AccountAPIPermission,)

    def get(self, request):
        serializer = AccountSerializer(self.request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user_data = request.data

        if not user_data['username'].isalnum():
            raise serializers.ValidationError({"message": "The user name should only contain alphanumeric characters."}
            )
        try:
            if not carrier._is_mobile(number_type(phonenumbers.parse(user_data['phone_number'], 'VN'))):
                raise serializers.ValidationError(
                    {"message": "Please type in valid phone number"}
                )
        except:
            raise serializers.ValidationError(
                {"message": "Please type in valid phone number"}
            )

        user = self.request.user
        if Account.objects.filter(username=user_data['username']).exists() and user.username != user_data['username']:
            raise serializers.ValidationError({"message": "This user name has already existed!"})
        user.username = user_data['username']
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        if user_data.get('image') is not None:
            user.image = user_data['image']
        user.phone_number = user_data['phone_number']
        user.save()

        return Response({"message": "Change user info successfully!"}, status=status.HTTP_200_OK)
