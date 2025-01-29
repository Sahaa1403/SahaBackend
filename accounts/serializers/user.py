from django.contrib.auth import get_user_model
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id","username","phone_number", "email", "first_name", "last_name","birth_date","national_code","user_type","education","majors_name","confirmed","is_profile_fill")



class UserAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name","last_name","birth_date","national_code","user_type","education","majors_name","invite_code")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name")
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": True},
        }
