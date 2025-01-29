from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models.user_manager import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts import models as user_models


class User(AbstractUser):

    phone_regex = RegexValidator(
        regex=r"^09\d{9}",
        message="{}\n{}".format(
            _("Phone number must be entered in the format: '09999999999'."),
            _("Up to 11 digits allowed."),
        ),
    )

    user_type_choices = (
        ("student", "student"),
        ("institute", "institute"),
        ("freelance", "freelance"),
        ("marketer", "marketer"),
        ("admin", "admin"),
        ("unknown", "unknown"),)

    education_type_choices = (
        ("BA/BSc", "BA/BSc"),
        ("MA/MSc", "MA/MSc"),
        ("Ph.D", "Ph.D"),
        ("High school Diploma", "High school Diploma"),
        ("Associate Degree", "Associate Degree"),)

    username = models.CharField(max_length=128,unique=True,blank=True,null=True)
    user_type = models.CharField(max_length=10, default="unknown",choices=user_type_choices)
    national_code = models.CharField(max_length=50,null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex],max_length=11,unique=True)
    email = models.EmailField(max_length=90,null=True,blank=True,unique=True)
    birth_date = models.DateField(null=True,blank=True)
    education = models.CharField(max_length=100, default="BA/BSc",choices=education_type_choices)
    majors_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    invite_code = models.IntegerField(blank=True, null=True)
    confirmed = models.BooleanField(default=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.phone_number) +' | '+ str(self.first_name) +' | '+ str(self.last_name)

    def is_profile_fill(self):
        if self.first_name is not None and self.last_name is not None and self.phone_number is not None and self.national_code is not None and self.birth_date is not None and self.user_type is not None and self.education is not None:
            return True
        else:
            return False