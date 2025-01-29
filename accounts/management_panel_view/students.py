from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import InstituteSerializer, StudentProfileSerializer
from accounts.models.student_profile import StudentProfile
from rest_framework.permissions import AllowAny



class StudentLists(APIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        student = StudentProfile.objects.all()
        serializer = self.serializer_class(student,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
