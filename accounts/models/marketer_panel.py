from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import InstituteProfile, User


class MarketerPanel(models.Model):
    address_type_choices = (
        ("Parents' Home", "Parents' Home"),
        ("Dormitory", "Dormitory"),
        ("Personal Residence", "Personal Residence"), )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    occupancy_type = models.CharField(max_length=100, default="Personal Residence", choices=address_type_choices)
    description = models.TextField(max_length=4000, blank=True, null=True)
    cart_number = models.BigIntegerField(null=True, blank=True)
    shaba = models.CharField(max_length=100, null=True, blank=True)
    #revenue = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.user)

'''
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "marketer":
        MarketerPanel.objects.create(user=instance)
'''



class MarketerWallet(models.Model):
    user = models.OneToOneField(MarketerPanel, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=1, default=0)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return str(self.user) + ' | '+ str(self.balance)
