from django.urls import path
from users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [

    path("register/", UserViewSet.as_view({'post': 'register'}), name="user-register"),
    path("users/me/", UserViewSet.as_view({"get": "me", "put": "me", "patch": "me"}), name="user-me"),
    path("resend_activation/", UserViewSet.as_view({"post": "resend_activation"}), name="resend-activation"),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),

    path("activate/<str:email>/", UserViewSet.as_view({"post": "activate"}), name="user-activate"),
    path("reset-password/", UserViewSet.as_view({"post": "send_reset_password_code"}), name="reset-password-code"),
    path("reset-password/code/", UserViewSet.as_view({"post": "reset_password"}), name="reset-password"),
]

