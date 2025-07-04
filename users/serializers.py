from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from users.utils.check_password import check_repeat_password
from users.utils.generate_code import validate_code
from django.contrib.auth import  get_user_model
import logging
logger = logging.getLogger(__name__)

User = get_user_model()


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


class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        read_only_fields = ['email']


class SendResetPasswordCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
class ResetPasswordWithCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    def validate(self, data):
        check_repeat_password(data['new_password'], data['new_password_confirm'])

        email = self.context.get("email")
        if not email:
            raise serializers.ValidationError("Email is required.")

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        
        if not validate_code(email=email,action_type="reset",  input_code=data['code']):
            raise serializers.ValidationError("Invalid or expired code.")
        
        self.context["user"] = user
        return data



class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        check_repeat_password(data['new_password'], data['new_password_confirm'])
        user = self.context['request'].user
        if not user.check_password(data['current_password']):
            raise AuthenticationFailed("Current password is incorrect.")
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()