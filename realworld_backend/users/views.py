from rest_framework.response import Response
from rest_framework import status
from djoser.views import TokenCreateView, UserViewSet
from djoser import utils

from .serializers import UserSerializer


class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        utils.login_user(self.request, serializer.user)
        user_serializer = UserSerializer(serializer.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class CustomUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
