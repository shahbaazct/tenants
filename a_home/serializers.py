from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Item


class TenantItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item  # Get the user model specified in settings
        fields = ("id", "name")
