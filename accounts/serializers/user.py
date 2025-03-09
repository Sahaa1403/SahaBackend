from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.functions import login
from django.utils.text import slugify
from accounts.models import UserType


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer(many=True, read_only=True)
    user_type_ids = serializers.PrimaryKeyRelatedField(queryset=UserType.objects.all(), source="user_type", many=True, write_only=True)
    active_type = UserTypeSerializer(read_only=True)
    active_type_id = serializers.PrimaryKeyRelatedField(queryset=UserType.objects.all(), source="active_type", write_only=True)
    class Meta:
        model = get_user_model()
        fields = ("active_status","id","username","user_type","user_type_ids","active_type","active_type_id","permissions","name","email","image","organization_unit","cooperation_type","created_at","updated_at","is_active")
        #fields = "__all__"



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        access, refresh = login(user)

        return {
            "refresh_token": refresh,
            "access_token": access,
            "user_data": UserSerializer(user).data,
        }




User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    username = serializers.CharField(required=False, allow_blank=True)  # Make username optional

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        username = validated_data.get('username')

        # Generate a unique username from email if not provided
        if not username:
            base_username = slugify(email.split('@')[0])  # Example: "test@example.com" -> "test"
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

        user = User.objects.create_user(email=email, username=username, password=password)
        return user
