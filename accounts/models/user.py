from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.models.user_manager import UserManager

class User(AbstractUser):
    user_type_choices = (
        ("author", "author"),
        ("researcher", "researcher"),
        ("manager", "manager"),
        ("unknown", "unknown"),)

    user_type = models.CharField(max_length=30, default="unknown", choices=user_type_choices)
    username = models.CharField(max_length=250,unique=True)
    email = models.EmailField(max_length=250,unique=True)
    name = models.CharField(max_length=200, null=True,blank=True)
    image = models.ImageField(upload_to="user_image", blank=True, null=True)
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