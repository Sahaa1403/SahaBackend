from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, UserUpdateSerializer, MarketerPanelSerializer, MarketerWalletSerializer
from accounts.models import User,MarketerPanel,MarketerWallet
from accounts.views.permissions.is_marketer import IsMarketer



class MarketerFull(APIView):
    serializer_class = MarketerPanelSerializer
    permission_classes = [IsMarketer]
    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        user_serializer = UserUpdateSerializer(user,data=data,partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        marketer = MarketerPanel.objects.get(user=user)
        serializer = self.serializer_class(marketer,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, *args, **kwargs):
        marketer = MarketerPanel.objects.get(user=self.request.user)
        serializer = self.serializer_class(marketer, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class MarketerWalletView(APIView):
    serializer_class = MarketerWalletSerializer
    permission_classes = [IsMarketer]

    def get(self, *args, **kwargs):
        marketer = MarketerPanel.objects.get(user=self.request.user)
        wallet,created = MarketerWallet.objects.get_or_create(user=marketer)
        serializer = self.serializer_class(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
