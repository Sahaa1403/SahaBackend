from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import InstituteSerializer
from accounts.models.institute_profile import InstituteProfile
from rest_framework.permissions import AllowAny



class InstituteLists(APIView):
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        institute = InstituteProfile.objects.all()
        serializer = self.serializer_class(institute,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
