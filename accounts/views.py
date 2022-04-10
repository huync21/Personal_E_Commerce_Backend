import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
# Create your views here.
from django.urls import reverse
from rest_framework import status, generics
from rest_framework.response import Response
# from api.permissions import ProductPermission
from accounts.models import Account
from E_Commerce_Backend import settings
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
from accounts.serializers import RegisterSerializer, LoginSerializer


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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)