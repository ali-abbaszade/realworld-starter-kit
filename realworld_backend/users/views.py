from rest_framework.response import Response
from rest_framework import status
from djoser.views import TokenCreateView
from djoser import utils

from .serializers import UserSerializer


class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        utils.login_user(self.request, serializer.user)
        user_serializer = UserSerializer(serializer.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
