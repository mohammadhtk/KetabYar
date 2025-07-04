from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser

from users.serializers import (
    RegisterSerializer,
    ActivateSerializer,
    ResendActivationSerializer,
    MeSerializer,
    SendResetPasswordCodeSerializer,
    ResetPasswordWithCodeSerializer,
    UserAvatarSerializer
)
from users.utils.check_password import check_repeat_password
from users.utils.generate_code import validate_code
from users.utils.send_activation import send_code_email_activation, send_code_email_reset_password

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


User = get_user_model()

# users/views.py
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.GenericViewSet):
    lookup_field = 'email'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ['me', 'update_avatar', 'delete_avatar']:
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
        elif self.action == 'update_avatar':
            return UserAvatarSerializer
        elif self.action == 'delete_avatar':
            return UserAvatarSerializer
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
            serializer = MeSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = MeSerializer(user, data=request.data, partial=(request.method == "PATCH"))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
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

    @swagger_auto_schema(
        request_body=UserAvatarSerializer,
        responses={200: "Avatar updated successfully."}
    )
    @action(
        detail=False,
        methods=["post"],
        url_path='avatar',
        permission_classes=[IsAuthenticated],
    )
    def update_avatar(self, request):
        serializer = UserAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.avatar = serializer.validated_data["avatar"]
        user.save()

        avatar_url = request.build_absolute_uri(user.avatar.url)
        return Response({
            "message": "Avatar updated successfully.",
            "avatar_url": avatar_url
        }, status=status.HTTP_200_OK)
    
    
    

    @action(detail=False, methods=["delete"])
    def delete_avatar(self, request):
        user = request.user
        if not user.avatar:
            return Response({"message": "No avatar to delete."}, status=status.HTTP_400_BAD_REQUEST)

        user.avatar.delete(save=True)
        user.avatar = None
        user.save()
        return Response({"message": "Avatar deleted successfully."}, status=status.HTTP_200_OK)