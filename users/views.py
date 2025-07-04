from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers
from users.serializers import (
    RegisterSerializer,
    ActivateSerializer,
    ResendActivationSerializer,
    MeSerializer,
    SendResetPasswordCodeSerializer,
    ResetPasswordWithCodeSerializer
)
from users.utils.check_password import check_repeat_password
from users.utils.generate_code import validate_code
from users.utils.send_activation import send_code_email_activation, send_code_email_reset_password

User = get_user_model()

# users/views.py
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.GenericViewSet):
    lookup_field = 'email'

    def get_permissions(self):
        if self.action in ['me']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'activate':
            return ActivateSerializer
        elif self.action == 'send_reset_password_code':
            return SendResetPasswordCodeSerializer
        elif self.action == 'reset_password_code':
            return ResetPasswordWithCodeSerializer
        elif self.action == 'register':
            return RegisterSerializer
        elif self.action == 'resend_activation':
            return ResendActivationSerializer
        elif self.action == 'me':
            return MeSerializer
        return serializers.Serializer

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User created successfully. Please check your email to activate your account.",
                         'email': user.email}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def activate(self, request, email=None):
        code = request.data.get("code")

        if validate_code(email, "activate", code):
            try:
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                return Response({"message": "User activated."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def resend_activation(self, request):
        email = request.data["email"]

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({"message": "User already activated."}, status=status.HTTP_400_BAD_REQUEST)
            send_code_email_activation(user)
            return Response({"message": "User created successfully. Please check your email to activate your account.",
                             'email': user.email}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User does not found."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = MeSerializer(user, data=request.data, partial=(request.method == "PATCH"))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def send_reset_password_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        send_code_email_reset_password(user)
        return Response({"message": "Reset code sent to your email."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def reset_password_code(self, request, email=None):
        serializer = self.get_serializer(data=request.data, context={"email": email})
        serializer.is_valid(raise_exception=True)
        user = serializer.context["user"]
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"message": "Password changed."}, status=status.HTTP_200_OK)


