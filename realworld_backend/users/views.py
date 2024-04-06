from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from djoser.views import TokenCreateView, UserViewSet
from djoser import utils

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, ProfileSerializer


User = get_user_model()


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


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="(?P<username>\\w+)",
    )
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        data = ProfileSerializer(user, context={"request": request}).data
        return Response(data, status=status.HTTP_200_OK)
