from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
from djoser.views import TokenCreateView, UserViewSet
from djoser import utils

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, ProfileSerializer
from .models import Follow

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


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "username"

    def get_serializer_context(self):
        return {"user": self.request.user}

    @action(
        methods=["get"],
        detail=False,
        url_path="(?P<username>\\w+)",
    )
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        data = ProfileSerializer(user, context={"user": self.request.user}).data
        return Response(data, status=status.HTTP_200_OK)

    @action(
        methods=["delete", "post"],
        detail=True,
        url_path="follow",
    )
    def follow_unfollow_user(self, request, username=None):
        target_user = self.get_object()
        if self.request.method == "POST":
            if target_user.id == self.request.user.id:
                return Response(
                    "Invalid follow request", status=status.HTTP_400_BAD_REQUEST
                )
            try:
                Follow.objects.create(
                    follower_id=self.request.user.id,
                    following_id=target_user.id,
                )
                serializer = ProfileSerializer(
                    target_user, context={"user": self.request.user}
                )
                return Response(serializer.data)
            except:
                return Response(f"You already followed {target_user.username}.")

        elif self.request.method == "DELETE":
            follow = get_object_or_404(
                Follow, follower_id=self.request.user.id, following_id=target_user.id
            )
            follow.delete()
            serializer = ProfileSerializer(
                target_user, context={"user": self.request.user}
            )
            return Response(serializer.data)
