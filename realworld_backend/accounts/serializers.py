from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from rest_framework import serializers


class LoginSerializer(BaseLoginSerializer):
    email = serializers.EmailField()
