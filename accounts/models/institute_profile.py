from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models.user import User



class InstituteProfile(models.Model):
    address_type_choices = (
        ("Landlord", "Landlord"),
        ("Tenant", "Tenant"),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    provinces = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    supervisor_phone1 = models.CharField(max_length=100, blank=True, null=True)
    supervisor_phone2 = models.CharField(max_length=100, blank=True, null=True)
    administrative_officer_phone1 = models.CharField(max_length=100, blank=True, null=True)
    administrative_officer_phone2 = models.CharField(max_length=100, blank=True, null=True)
    occupancy_type = models.CharField(max_length=100, default="Landlord", choices=address_type_choices)
    school_address = models.CharField(max_length=256, blank=True, null=True)
    logo = models.ImageField(upload_to="institute_logo",blank=True,null=True)
    cover = models.ImageField(upload_to="institute_cover",blank=True, null=True)
    slogan = models.CharField(max_length=500, blank=True, null=True)
    tax_case_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=6000, blank=True, null=True)
    ZP_MERCHANT_ID = models.CharField(max_length=256,default="00000000-0000-0000-0000-000000000000",blank=True,null=True)
    primary_color = models.CharField(max_length=100, blank=True, null=True)
    secondary_color = models.CharField(max_length=100, blank=True, null=True)
    memory_mirror_price_each_day = models.IntegerField(blank=True, null=True)
    audio_scripter_price_each_day = models.IntegerField(blank=True, null=True)
    teaching_positions = models.JSONField(null=True, blank=True)
    teaching_qualifications  = models.JSONField(null=True, blank=True)
    #wallet = models.IntegerField(default=0)

    def __str__(self):
        return self.user.phone_number

'''
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "institute":
        InstituteProfile.objects.create(user=instance)
'''

class InstituteWallet(models.Model):
    user = models.OneToOneField(InstituteProfile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=1, default=0)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return str(self.user) + ' | '+ str(self.balance)