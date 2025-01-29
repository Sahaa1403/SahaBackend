from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, InstituteSerializer
from accounts.models import User
from accounts.views.permissions.is_institute import IsInstitute
from accounts.models.institute_profile import InstituteProfile



class InstituteOverview(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsInstitute]

    def get(self, *args, **kwargs):
        user=self.request.user
        institute = InstituteProfile.objects.get(user=user)
        data = {
            "user": self.serializer_class(user).data,
            "institute": InstituteSerializer(institute).data,
            "students": None,
            "payments": None,
        }
        return Response(data, status=status.HTTP_200_OK)