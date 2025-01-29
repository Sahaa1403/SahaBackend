from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import InstituteProfile, User, FreelanceProfile


class StudentProfile(models.Model):
    gender_type_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Rather-not-say", "Rather-not-say"))

    english_level_choices = (
        ("A1", "A1"),
        ("A2", "A2"),
        ("B1", "B1"),
        ("B2", "B2"),
        ("C1", "C1"),
        ("C2", "C2"),
        ("IELTS", "IELTS"),)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_IELTS_student = models.BooleanField(default=False)
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, blank=True, null=True)
    freelance = models.ForeignKey(FreelanceProfile, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=20, default="Male", choices=gender_type_choices)
    english_level = models.CharField(max_length=10, default="A1", choices=english_level_choices)
    description = models.TextField(max_length=4000, blank=True, null=True)
    image = models.ImageField(upload_to="student_photo", blank=True, null=True)
    cart_number = models.BigIntegerField(null=True, blank=True, default=0)
    shaba = models.CharField(max_length=100, null=True, blank=True, default=0)

    def parent_type(self):
        if self.institute:
            return "Institute"
        else:
            return "Freelance"

    def __str__(self):
        return self.user.phone_number

'''
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "student":
        StudentProfile.objects.create(user=instance)
'''




class StudentWallet(models.Model):
    user = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=1, default=0)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return str(self.user) + ' | '+ str(self.balance)
