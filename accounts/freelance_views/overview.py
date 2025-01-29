from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, FreelanceProfileSerializer
from accounts.models import User,FreelanceProfile
from accounts.views.permissions.is_freelance import IsFreelance


class FreelanceOverview(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsFreelance]

    def get(self, *args, **kwargs):
        user=self.request.user
        freelance = FreelanceProfile.objects.get(user=user)
        data = {
            "user": self.serializer_class(user).data,
            "freelance": FreelanceProfileSerializer(freelance).data,
            "students": None,
            "payments": None,
        }
        return Response(data, status=status.HTTP_200_OK)