from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer
from accounts.serializers import UserSerializer, FreelanceProfileSerializer, StudentProfileSerializer, UserUpdateSerializer
from accounts.models import User,FreelanceProfile, StudentProfile
from accounts.views.permissions.is_freelance import IsFreelance
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    


class FreelanceStudent(GenericAPIView):
    permission_classes = [IsFreelance]
    queryset = User.objects.all()
    pagination_class = CustomPagination
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'is_IELTS_student', 'gender', 'english_level']
    search_fields = ['user__first_name', 'user__last_name', 'user__national_code', 'user__phone_number', 'gender']
    ordering_fields = ['user', 'is_IELTS_student', 'gender', 'english_level']

    def get(self, *args, **kwargs):
        data = []
        freelance = FreelanceProfile.objects.get(user=self.request.user)
        students = self.filter_queryset(StudentProfile.objects.filter(freelance=freelance))
        for obj in students:
            student_serializer = StudentProfileSerializer(obj)
            student_sub = Subscription.objects.filter(user=obj,paid=True)
            sub_serializer = SubscriptionSerializer(student_sub,many=True)
            student_data = {"student":student_serializer.data, "subscription":sub_serializer.data}
            data.append(student_data)
        page = self.paginate_queryset(data)
        if page is not None:
            return self.get_paginated_response(page)
        serializer = self.filter_queryset(StudentProfile.objects.filter(freelance=freelance))
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, *args, **kwargs):
        data = self.request.data
        data["password"] = "12345678"
        data["user_type"] = "student"
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            student_user = User.objects.get(id=serializer.data["id"])
            student_user.set_password(data["password"])
            student_user.save()
            student_profile = StudentProfile.objects.get(user=student_user)
            student_profile.freelance = FreelanceProfile.objects.get(user=self.request.user)
            student_profile.gender = data["gender"]
            student_profile.english_level = data["english_level"]
            student_profile.education = data["education"]
            student_profile.majors_name = data["majors_name"]
            student_profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class FreelanceStudentMultiple(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsFreelance]

    def post(self, *args, **kwargs):
        data = self.request.data
        data["password"] = "12345678"
        data["user_type"] = "student"
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            student_user = User.objects.get(id=serializer.data["id"])
            student_user.set_password(data["password"])
            student_user.save()
            student_profile = StudentProfile.objects.get(user=student_user)
            student_profile.freelance = FreelanceProfile.objects.get(user=self.request.user)
            student_profile.gender = data["gender"]
            student_profile.english_level = data["english_level"]
            student_profile.education = data["education"]
            student_profile.majors_name = data["majors_name"]
            student_profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class FreelanceStudentItem(APIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsFreelance]
    def get(self, *args, **kwargs):
        try:
            freelance = FreelanceProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],freelance=freelance)
            student_serializer = self.serializer_class(student)
            active_subs = Subscription.objects.filter(user=student, status="Active")
            audio_video_scripter = active_subs.filter(type="Audio-Video-Scripter").last()
            if audio_video_scripter:
                audio_video_scripter_remaining_days = audio_video_scripter.remaining_days()
            else:
                audio_video_scripter_remaining_days = 0
            
            memory_mirror = active_subs.filter(type="Memory-Mirror").last()
            if memory_mirror:
                memory_mirror_remaining_days = memory_mirror.remaining_days()
            else:
                memory_mirror_remaining_days = 0
            membership = {"Audio-Video-Scripter": audio_video_scripter_remaining_days,
                        "Memory-Mirror": memory_mirror_remaining_days}          
            combined_data = {
                **student_serializer.data,
                "membership": membership,
            }
            return Response(combined_data, status=status.HTTP_200_OK)
        except:
            return Response("Student not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def patch(self, *args, **kwargs):
        try:
            freelance = FreelanceProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],freelance=freelance)

            user_serializer = UserUpdateSerializer(student.user, data=self.request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

            serializer = self.serializer_class(student, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("Student not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            freelance = FreelanceProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],freelance=freelance)
            base_user = student.user
            student.delete()
            base_user.delete()
            return Response("Student deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Student not found or something went wrong, try again.", status=status.HTTP_400_BAD_REQUEST)
