from rest_framework import serializers
from accounts.models.freelance_profile import FreelanceProfile, FreelanceWallet

class FreelanceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelanceProfile
        fields = "__all__"



class FreelanceWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelanceWallet
        #fields = "__all__"
        fields = ("balance", "updated_at")
