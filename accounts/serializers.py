from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import Account


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "The user name should only contain alphanumeric characters."
            )

        return attrs

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=10)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    first_name = serializers.CharField(max_length=255, min_length=1, read_only=True)
    last_name = serializers.CharField(max_length=255, min_length=1, read_only=True)
    phone_number = serializers.CharField(max_length=10, read_only=True)
    refresh_token = serializers.CharField(max_length=255, min_length=1, read_only=True)
    access_token = serializers.CharField(max_length=255, min_length=1, read_only=True)

    class Meta:
        model = Account
        fields = ['email', 'password', 'username', 'first_name', 'last_name', 'phone_number', 'refresh_token',
                  'access_token']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        account = Account.objects.get(email=email)
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid email or password, try again!')
        if not account.is_verified:
            raise AuthenticationFailed('Please verify your email to login!')
        if not account.is_active:
            raise AuthenticationFailed('Account has not been activated, contact admin!')

        tokens = user.tokens()

        return {
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'refresh_token': tokens['refresh'],
            'access_token': tokens['access']
        }


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'username']
