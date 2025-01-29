from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, FreelanceProfileSerializer, UserUpdateSerializer, FreelanceWalletSerializer
from accounts.models import User,FreelanceProfile,FreelanceWallet
from accounts.views.permissions.is_freelance import IsFreelance


class Freelance(APIView):
    serializer_class = FreelanceProfileSerializer
    permission_classes = [IsFreelance]

    def get(self, *args, **kwargs):
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(freelance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        serializer = FreelanceProfileSerializer(freelance, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


    def post(self, *args, **kwargs):
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(freelance, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class FreelanceFull(APIView):
    serializer_class = FreelanceProfileSerializer
    permission_classes = [IsFreelance]
    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        user_serializer = UserUpdateSerializer(user,data=data,partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        freelance = FreelanceProfile.objects.get(user=user)
        serializer = self.serializer_class(freelance,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, *args, **kwargs):
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(freelance, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class FreelanceWalletView(APIView):
    serializer_class = FreelanceWalletSerializer
    permission_classes = [IsFreelance]

    def get(self, *args, **kwargs):
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        wallet,created = FreelanceWallet.objects.get_or_create(user=freelance)
        serializer = self.serializer_class(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
