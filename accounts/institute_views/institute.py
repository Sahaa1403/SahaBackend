from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, InstituteSerializer, UserUpdateSerializer, InstituteWalletSerializer
from accounts.models import User,InstituteProfile, InstituteWallet
from accounts.views.permissions.is_institute import IsInstitute
from accounts.models.institute_profile import InstituteProfile
from django.http import JsonResponse



class Institute(APIView):
    serializer_class = InstituteSerializer
    permission_classes = [IsInstitute]

    def get(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(institute)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        serializer = InstituteSerializer(institute, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


    def post(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(institute, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class InstituteFull(APIView):
    serializer_class = InstituteSerializer
    permission_classes = [IsInstitute]
    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        user_serializer = UserUpdateSerializer(user,data=data,partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        institute = InstituteProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(institute,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(institute, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class ZarinpalMerchantID(APIView):
    serializer_class = InstituteSerializer
    permission_classes = [IsInstitute]

    def post(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        #institute.ZP_MERCHANT_ID = self.request.data['ZP_MERCHANT_ID']
        #institute.save()
        serializer = self.serializer_class(institute, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class InstitutePricing(APIView):
    serializer_class = InstituteSerializer
    permission_classes = [IsInstitute]

    def post(self, *args, **kwargs):
        try:
            institute = InstituteProfile.objects.get(user=self.request.user)
            institute.audio_scripter_price_each_day = self.request.data['audio_scripter_price_each_day']
            institute.memory_mirror_price_each_day = self.request.data['memory_mirror_price_each_day']
            institute.save()
            return Response("Institute pricing updated.", status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstituteWalletView(APIView):
    serializer_class = InstituteWalletSerializer
    permission_classes = [IsInstitute]

    def get(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        wallet,created = InstituteWallet.objects.get_or_create(user=institute)
        serializer = self.serializer_class(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
