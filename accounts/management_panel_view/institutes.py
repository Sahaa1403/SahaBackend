from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import InstituteSerializer, StudentProfileSerializer
from accounts.views.permissions.is_institute import IsInstitute
from accounts.models.institute_profile import InstituteProfile
from accounts.models.student_profile import StudentProfile
from rest_framework.permissions import AllowAny, IsAuthenticated




class InstituteLists(APIView):
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        institute = InstituteProfile.objects.all()
        serializer = self.serializer_class(institute,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class StudentLists(APIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        institute = StudentProfile.objects.all()
        serializer = self.serializer_class(institute,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
