from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from users.utils.check_password import check_repeat_password
from django.contrib.auth import  get_user_model
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        logger.debug(f"Attempting login with email: {email}")
        try:
            user = User.objects.get(email=email)
            print(user)
        except ObjectDoesNotExist:
            print(1)
            logger.error(f"Authentication failed for email: {email}")
            raise ValidationError("No active account found with the given credentials")

        if not user.check_password(password):
            logger.error(f"Invalid credentials for email: {email}")
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            logger.error(f"User account is inactive for email: {email}")
            raise AuthenticationFailed("This account is inactive")

        data = super().validate(attrs)

        logger.debug(f"Token successfully generated for email: {email}")

        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']

    def validate(self, data):
        check_repeat_password(data['password'], data['password_confirm'])
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(email=validated_data['email'])
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

class ActivateSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    code = serializers.CharField(required=True, max_length=6)


class RESENDACTIVATIONSERIALIZER(serializers.Serializer):
    email = serializers.EmailField(required=True)


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'firstname', 'lastname']


class ResetPasswordCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    def validate(self, data):
        check_repeat_password(data['new_password'], data['new_password_confirm'])
        return data
