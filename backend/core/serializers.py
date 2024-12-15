from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import File, ShareLink

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "role", "mfa_secret"]

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id", "filename", "owner", "created_at"]

class ShareLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareLink
        fields = ["id", "token", "expires_at", "permission", "file"]
