from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.models.user_manager import UserManager


class UserType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name


class User(AbstractUser):
    cooperation_type_choices = (
        ("official", "official"),
        ("contractual", "contractual"),)

    active_status = models.BooleanField(default=True)
    user_type = models.ManyToManyField(UserType, blank=True)
    username = models.CharField(max_length=250,unique=True)
    email = models.EmailField(max_length=250,unique=True)
    name = models.CharField(max_length=200, null=True,blank=True)
    image = models.ImageField(upload_to="user_image", blank=True, null=True)
    organization_unit = models.CharField(max_length=200, null=True,blank=True)
    cooperation_type = models.CharField(max_length=60, blank=True, null=True, choices=cooperation_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.email) +' | '+ str(self.name)

    def is_profile_fill(self):
        if self.email is not None and self.username is not None and self.name is not None:
            return True
        else:
            return False
