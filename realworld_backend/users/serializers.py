from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from djoser.serializers import UserCreateSerializer

from .models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ("username", "email", "password")


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        token = Token.objects.get(user=user)
        return token.key

    class Meta:
        model = User
        fields = ("email", "token", "username", "bio", "image")


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    def get_following(self, target_user):
        user = self.context.get("user")
        return Follow.objects.filter(
            follower_id=user.id, following_id=target_user.id
        ).exists()

    class Meta:
        model = User
        fields = ("username", "bio", "image", "following")
