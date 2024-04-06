from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="users/", null=True)
    followers = models.ManyToManyField("self", symmetrical=False)

    def count_followers(self):
        return self.followers.count()

    def count_following(self):
        return CustomUser.objects.filter(followers=self).count()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
