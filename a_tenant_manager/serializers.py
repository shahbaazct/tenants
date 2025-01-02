from django.contrib.auth import get_user_model
from rest_framework import serializers


class TenantUserSerializer(serializers.ModelSerializer):
    """Serializer for user data in the tenant context."""

    class Meta:
        model = get_user_model()  # Get the user model specified in settings
        fields = ("id", "username", "email", "first_name", "last_name", "is_active")