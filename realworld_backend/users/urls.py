from django.urls import path

from dj_rest_auth.views import LoginView
from . import views

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="rest_login"),
]
