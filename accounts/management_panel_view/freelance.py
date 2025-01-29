from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import FreelanceProfileSerializer
from accounts.models.freelance_profile import FreelanceProfile
from rest_framework.permissions import AllowAny



class FreelanceLists(APIView):
    serializer_class = FreelanceProfileSerializer
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        freelance = FreelanceProfile.objects.all()
        serializer = self.serializer_class(freelance,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
