from rest_framework.routers import DefaultRouter
from django.urls import path, include


from . import views

router = DefaultRouter()
router.register("users", views.CustomUserViewSet)

urlpatterns = [
    path("users/login/", views.CustomTokenCreateView.as_view(), name="login"),
    path("user/", views.current_user, name="current_user"),
    path("", include(router.urls)),
]
