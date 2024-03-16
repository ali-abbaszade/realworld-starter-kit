from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from .serializers import UserSerializer, LoginSerializer


class CustomLoginView(LoginView):

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)
