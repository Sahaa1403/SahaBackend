from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config import responses
from accounts.functions import get_user_data, login
from config.settings import ACCESS_TTL
from accounts.serializers import UserSerializer,StudentProfileSerializer, InstituteSerializer, \
    UserUpdateSerializer, FreelanceProfileSerializer, StudentWalletSerializer
from django.contrib.auth import authenticate
from accounts.views.permissions import IsStudent
from rest_framework.permissions import AllowAny
from accounts.models.student_profile import StudentProfile, InstituteProfile, StudentWallet
from subscription.models import Subscription, DefaultPrice, FreeTrial
from django.utils.timezone import now


class StudentLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, *args, **kwargs):
        phone_number = self.request.data.get("phone_number")
        password = self.request.data.get("password")
        user = authenticate(phone_number=phone_number, password=password)

        if user is not None:
            access, refresh = login(user)
        else:
            return Response("phone_number or password is incorrect", status=status.HTTP_406_NOT_ACCEPTABLE)

        data = {
            "refresh_token": refresh,
            "access_token": access,
            "user_data": UserSerializer(user).data,
        }
        response = Response(
            {
                "success": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            max_age=ACCESS_TTL * 24 * 3600,
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response





class StudentOverview(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsStudent]

    def get(self, *args, **kwargs):
        user=self.request.user
        student = StudentProfile.objects.get(user=user)
        subs = Subscription.objects.filter(user=student)
        for sub in subs:
            if sub.paid:
                if sub.expired():
                    sub.status = "Expired"
                else:
                    sub.status = "Active"
            else:
                sub.status = "Canceled"
            sub.save()

        active_subs = Subscription.objects.filter(user=student, status="Active")

        audio_video_scripter = active_subs.filter(type="Audio-Video-Scripter").last()
        if audio_video_scripter:
            audio_video_scripter_remaining_days = audio_video_scripter.remaining_days()
        else:
            audio_video_scripter_remaining_days = 0

        memory_mirror = active_subs.filter(type="Memory-Mirror").last()        #.order_by('-remaining_days')[:1]
        if memory_mirror:
            memory_mirror_remaining_days = memory_mirror.remaining_days()
        else:
            memory_mirror_remaining_days = 0
            
        free_trial = FreeTrial.objects.filter(user=student).first()
        if free_trial:
            free_trial.check_expired()
            free_trial_status = free_trial.is_active
            if free_trial_status == "Active":
                remaining_free_trial_days = free_trial.remaining_days()
                if remaining_free_trial_days < 0:
                    remaining_free_trial_days = 0
            else:
                free_trial_status = "Expired"
                remaining_free_trial_days = 0
        else:
            free_trial_status = "Ready-To-Use"
            remaining_free_trial_days = 0

        membership = {
            "Audio-Video-Scripter": audio_video_scripter_remaining_days,
            "Memory-Mirror": memory_mirror_remaining_days,
            "Free-Trial": remaining_free_trial_days,
            "Free-Trial-Status" : free_trial_status,
        }

        if student.parent_type() == "Institute":
            memory_mirror_price = student.institute.memory_mirror_price_each_day
            audio_scripter_price = student.institute.audio_scripter_price_each_day
        else:
            default_price = DefaultPrice.objects.all().last()
            memory_mirror_price = default_price.memory_mirror
            audio_scripter_price = default_price.audio_video_scripter

        data = {
            "user": self.serializer_class(user).data,
            "student": StudentProfileSerializer(student).data,
            "membership": membership,
            "institute": InstituteSerializer(student.institute).data,
            "freelance": FreelanceProfileSerializer(student.freelance).data,
            "parent_type": student.parent_type(),
            "memory_mirror_price": memory_mirror_price,
            "audio_scripter_price": audio_scripter_price,
            "payments": None,
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        user = self.request.user
        student = StudentProfile.objects.get(user=user)
        serializer = StudentProfileSerializer(student, data=self.request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class StudentInstituteData(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsStudent]

    def get(self, *args, **kwargs):
        user=self.request.user
        student = StudentProfile.objects.get(user=user)
        data = InstituteSerializer(student.institute).data
        return Response(data, status=status.HTTP_200_OK)






class StudentFull(APIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsStudent]

    def get(self, *args, **kwargs):
        student = StudentProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        user_serializer = UserUpdateSerializer(user,data=data,partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        student = StudentProfile.objects.get(user=user)
        serializer = self.serializer_class(student,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, *args, **kwargs):
        student = StudentProfile.objects.get(user=self.request.user)
        serializer = self.serializer_class(student, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)







class StudentWalletView(APIView):
    serializer_class = StudentWalletSerializer
    permission_classes = [IsStudent]

    def get(self, *args, **kwargs):
        student = StudentProfile.objects.get(user=self.request.user)
        wallet,created = StudentWallet.objects.get_or_create(user=student)
        serializer = self.serializer_class(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
