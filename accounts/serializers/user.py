from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id","username","user_type","name","email","image","created_at","updated_at","is_active")
        #fields = "__all__"
