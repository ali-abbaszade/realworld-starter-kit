from rest_framework import serializers
from rest_framework.authtoken.models import Token
from dj_rest_auth.serializers import LoginSerializer, TokenSerializer
from .models import CustomUser


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, user):
        token = Token.objects.get(user=user)
        return token.key

    class Meta:
        model = CustomUser
        fields = ("email", "token", "username", "bio", "image")
