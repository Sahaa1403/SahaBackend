from rest_framework import serializers
from accounts.models.institute_profile import InstituteProfile, InstituteWallet


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteProfile
        fields = "__all__"
        
        
class InstituteWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteWallet
        fields = ("balance", "updated_at")

