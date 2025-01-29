from rest_framework import serializers
from accounts.models.student_profile import StudentProfile, StudentWallet
from accounts.serializers.user import UserSerializer

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"



class MultipleStudentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProfile
        fields = "__all__"
        


class StudentWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentWallet
        #fields = "__all__"
        fields = ("balance", "updated_at")
