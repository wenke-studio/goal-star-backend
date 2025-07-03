from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as AbstractUserManager


class UserManager(AbstractUserManager):
    pass


class User(AbstractUser):
    objects = UserManager()
