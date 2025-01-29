from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, InstituteSerializer, StudentProfileSerializer, UserUpdateSerializer
from accounts.serializers.student import MultipleStudentProfileSerializer
from accounts.models import User,InstituteProfile,StudentProfile
from accounts.views.permissions.is_institute import IsInstitute
from accounts.models.institute_profile import InstituteProfile
from rest_framework.permissions import AllowAny, IsAuthenticated
from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer
from datetime import datetime
import pandas as pd
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    

class InstituteStudent(GenericAPIView):
    permission_classes = [IsInstitute]
    queryset = User.objects.all()
    pagination_class = CustomPagination
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'is_IELTS_student', 'gender', 'english_level']
    search_fields = ['user__first_name', 'user__last_name', 'user__national_code', 'user__phone_number', 'gender']
    ordering_fields = ['user', 'is_IELTS_student', 'gender', 'english_level']

    def get(self, *args, **kwargs):
        data = []
        institute = InstituteProfile.objects.get(user=self.request.user)
        students = self.filter_queryset(StudentProfile.objects.filter(institute=institute))
        for obj in students:
            student_serializer = StudentProfileSerializer(obj)
            student_sub = Subscription.objects.filter(user=obj,paid=True)
            sub_serializer = SubscriptionSerializer(student_sub,many=True)
            student_data = {"student":student_serializer.data, "subscription":sub_serializer.data}
            data.append(student_data)
        page = self.paginate_queryset(data)
        if page is not None:
            return self.get_paginated_response(page)
        serializer = self.filter_queryset(StudentProfile.objects.filter(institute=institute))
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
            student_profile.institute = InstituteProfile.objects.get(user=self.request.user)
            student_profile.gender = data["gender"]
            student_profile.english_level = data["english_level"]
            student_profile.education = data["education"]
            student_profile.majors_name = data["majors_name"]
            student_profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class InstituteStudentMultiple(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsInstitute]  
    
    def post(self, request, *args, **kwargs):

        excel_file = self.request.FILES.get('file')
        users_data = []
        students = []  
        errors = []  
        df = pd.read_excel(excel_file, dtype={'Phone Number': str})
        
        required_fields = ['Phone Number', 'First Name', 'Last Name', 'Birth Date', 'Gender', 'English Level']
            
        for index, row in df.iterrows():
            date_value = row['Birth Date']  # Birth date
            if isinstance(date_value, datetime):
                date_value = date_value.date()
                
            missing_fields = []
            for field in required_fields:
                if pd.isna(row.get(field)) or row.get(field) == "":
                    missing_fields.append(field)
            
            if missing_fields:
                errors.append({
                    "row": index + 1,
                    "missing_fields": missing_fields,
                    "error": "These fields are required and cannot be empty."
                })
                continue
                
            if User.objects.filter(phone_number=row['Phone Number']).exists():
                errors.append({
                    "row": index + 1, 
                    "phone_number": row['Phone Number'],
                    "error": "This phone number already exits!"
                })
                continue
            
            user_data = {
                'phone_number': row['Phone Number'],
                'first_name': row['First Name'],
                'last_name': row['Last Name'],
                'birth_date': date_value,
            }
            users_data.append(user_data)
        if errors:
            return Response({"message": "Validation errors found","errors": errors}, status=400)                
        user_serializer = UserSerializer(data=users_data, many=True)
        if user_serializer.is_valid():
            users = user_serializer.save()       
            for i, row in enumerate(df.iterrows()):
                if i < len(users):
                    student_data = {
                        'user': users[i].id,
                        'gender': row[1]['Gender'],
                        'english_level': row[1]['English Level'],
                    }
                    
                    students.append(student_data)
            student_serializer = MultipleStudentProfileSerializer(data=students, many=True)
            if student_serializer.is_valid():
                student_ser = student_serializer.save()
                institute = InstituteProfile.objects.get(user=self.request.user)
                
                for student in student_ser:
                    student.institute = institute
                    student.save()
                              
                for user in users:
                    user.user_type = 'student'
                    user.set_password('12345678')
                    user.save() 
                                       
                return Response({"message": "Success"}, status=200)
            else:
                print("Student serializer errors:", student_serializer.errors)
                return Response({"message": "Error", "errors": student_serializer.errors}, status=400)
        else:
            return Response({"message": "Error", "errors": user_serializer.errors}, status=400)





class InstituteStudentItem(APIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsInstitute]
    def get(self, *args, **kwargs):
        try:
            institute = InstituteProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],institute=institute)
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
            institute = InstituteProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],institute=institute)

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
            institute = InstituteProfile.objects.get(user=self.request.user)
            student = StudentProfile.objects.get(id=self.kwargs["id"],institute=institute)
            base_user = student.user
            student.delete()
            base_user.delete()
            return Response("Student deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Student not found or something went wrong, try again.", status=status.HTTP_400_BAD_REQUEST)

