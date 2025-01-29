from rest_framework import serializers
from accounts.models.marketer_panel import MarketerPanel, MarketerWallet
from accounts.serializers.user import UserAllFieldsSerializer

class MarketerPanelSerializer(serializers.ModelSerializer):
    user=UserAllFieldsSerializer(read_only=True)
    class Meta:
        model = MarketerPanel
        fields = "__all__"



class MarketerWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketerWallet
        fields = ("balance", "updated_at")
