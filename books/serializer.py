from rest_framework import serializers
from .models import BookStatus

class BookStatusSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BookStatus
        fields = ['openlibrary_id', 'user', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
