from rest_framework import serializers
from users.utils.check_password import check_repeat_password
from django.contrib.auth import  get_user_model
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


class RESENDACTIVATIONSERIALIZER(serializers.Serializer):
    email = serializers.EmailField(required=True)

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
