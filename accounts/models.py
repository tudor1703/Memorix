from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    class UserType(models.TextChoices):
        CLIENT = "client", "Client"
        PHOTOGRAPHER = "photographer", "Photographer"

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENT
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email