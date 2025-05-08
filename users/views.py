from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import (
    RegisterSerializer,
    ActivateSerializer,
    RESENDACTIVATIONSERIALIZER,
    MeSerializer,
    ResetPasswordCodeSerializer,
    ResetPasswordSerializer
)
from users.utils.generate_code import validate_code
from users.utils.send_activation import send_code_email_activation

User = get_user_model()

# users/views.py
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.GenericViewSet):
    lookup_field = 'email'

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'activate':
            return ActivateSerializer
        elif self.action == 'reset_password_code':
            return ResetPasswordCodeSerializer
        elif self.action == 'reset_password':
            return ResetPasswordSerializer
        elif self.action == 'register':
            return RegisterSerializer
        elif self.action == 'resend_activation':
            return RESENDACTIVATIONSERIALIZER
        elif self.action == 'me':
            return MeSerializer
        return ActivateSerializer

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

    @action(detail=False, methods=["get",'put','patch'])
    def me(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def reset_password_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if validate_code(serializer.validated_data["email"], "reset", serializer.validated_data["code"]):
            return Response({"message": "Code validated."}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"message": "Password changed."}, status=status.HTTP_200_OK)
