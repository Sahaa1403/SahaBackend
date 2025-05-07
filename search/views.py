from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from search.models import SearchData,KnowledgeBase, Label, Source, SocialMedia, KnowledgeBaseLabelUser
from search.serializers import SearchSerializer,SearchDataSerializer,AddKnowledgeBaseSerializer, \
    KnowledgeBaseSerializer, LabelSerializer, CreateSourceSerializer, SourceSerializer, \
    SourceFullSerializer, SourceWithKBSerializer, EditSourceSerializer,SocialMediaSerializer,\
    KnowledgeBaseLabelUserSerializer, CreateKnowledgeBaseLabelUserSerializer
import requests
import logging
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework_mongoengine.viewsets import ModelViewSet
import json
import urllib.parse
import math

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.get_page_size(self.request))
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'last_page': total_pages,
            'results': data
        })





class ObjectsNumbersAPIViewSet(APIView):
    serializer_class = SocialMediaSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            filter = self.request.GET.get('filter', '')

            if filter == "source":
                kb = KnowledgeBase.objects.filter(source__isnull=False)
                kbl = KnowledgeBaseLabelUser.objects.filter(knowledge_base__source__isnull=False)
            elif filter == "social_media":
                kb = KnowledgeBase.objects.filter(social_media__isnull=False)
                kbl = KnowledgeBaseLabelUser.objects.filter(knowledge_base__social_media__isnull=False)
            else:
                kb = KnowledgeBase.objects.all()
                kbl = KnowledgeBaseLabelUser.objects.all()

            all_count = kb.count()
            real = kb.filter(category="real").count()
            dis = kbl.filter(label__name="فریب دهی").count()
            mis = kbl.filter(label__name="نادرست").count()
            mal = kbl.filter(label__name="آسیب رسان").count()
            other = all_count-(dis+real+mis+mal)

            def percent(count):
                return round((count / all_count) * 100, 2) if all_count > 0 else 0

            data = {
                "all": all_count,
                "real": real,
                "real_percent": percent(real),
                "dis": dis,
                "dis_percent": percent(dis),
                "mis": mis,
                "mis_percent": percent(mis),
                "mal": mal,
                "mal_percent": percent(mal),
                "other": other,
                "other_percent": percent(other),
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Something went wrong, try again - {}".format(e)}, status=status.HTTP_400_BAD_REQUEST)


class SocialmediaFullAPIViewSet(GenericAPIView):
    queryset = SocialMedia.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = SocialMediaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'created_at']
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'created_at']
    def get(self, *args, **kwargs):
        sm = self.filter_queryset(SocialMedia.objects.all())
        page = self.paginate_queryset(sm)
        if page is not None:
            serializer = self.serializer_class(page, many=True ,context={'request': self.request})
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(SocialMedia.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class SocialmediaItemViewSet(APIView):
    serializer_class = SocialMediaSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            sm = SocialMedia.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(sm,context={'request': self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("SocialMedia not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def put(self, *args, **kwargs):
        try:
            sm = SocialMedia.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(sm, data=self.request.data, partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("SocialMedia not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            sm = SocialMedia.objects.get(id=self.kwargs["id"])
            sm.delete()
            return Response("SocialMedia deleted.", status=status.HTTP_200_OK)
        except:
            return Response("SocialMedia not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)




class SourceFullAPIViewSet(GenericAPIView):
    queryset = Source.objects.all()
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = SourceFullSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'created_at']
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'created_at']

    def get(self, *args, **kwargs):
        source = self.filter_queryset(Source.objects.all())
        page = self.paginate_queryset(source)
        if page is not None:
            serializer = self.serializer_class(page, many=True ,context={'request': self.request})
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Source.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)



class SourceViewSet(APIView):
    serializer_class = SourceSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        source = Source.objects.all()
        serializer = SourceFullSerializer(source, many=True ,context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, *args, **kwargs):
        serializer = CreateSourceSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class SourceItemViewSet(APIView):
    serializer_class = SourceSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            source = Source.objects.get(id=self.kwargs["id"])
            serializer = SourceWithKBSerializer(source,context={'request': self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Error - {}".format(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, *args, **kwargs):
        try:
            source = Source.objects.get(id=self.kwargs["id"])
            serializer = EditSourceSerializer(source, data=self.request.data, partial=True)
            if serializer.is_valid():
                obj = serializer.save()
                return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("Source not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            source = Source.objects.get(id=self.kwargs["id"])
            source.delete()
            return Response("Source deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Source not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)




class LabelViewSet(APIView):
    serializer_class = LabelSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        labels = Label.objects.all()
        serializer = self.serializer_class(labels,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class LabelItemViewSet(APIView):
    serializer_class = LabelSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            label = Label.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(label)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Label not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def put(self, *args, **kwargs):
        try:
            label = Label.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(label, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("label not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            label = Label.objects.get(id=self.kwargs["id"])
            label.delete()
            return Response("Label deleted.", status=status.HTTP_200_OK)
        except:
            return Response("Label not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)



class AddLabelViewSet(APIView):
    serializer_class = KnowledgeBaseLabelUserSerializer
    permission_classes = [IsAuthenticated]
    def delete(self, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        label_id = data["label"]
        knowledge_base_id = data["knowledge_base"]
        try:
            instance = KnowledgeBaseLabelUser.objects.get(
                label_id=label_id,
                knowledge_base_id=knowledge_base_id,
                user=user
            )
            instance.delete()
            return Response({'message': 'Association removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except KnowledgeBaseLabelUser.DoesNotExist:
            return Response({'error': 'Association not found.'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, *args, **kwargs):
        data=self.request.data
        data["user"]=self.request.user.id
        user_type_names = self.request.user.user_type.values_list('name', flat=True)
        if not any(name in ['researcher', 'manager'] for name in user_type_names):
            return Response("You do not have permission to edit the element", status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            # Check if an object already exists for this knowledge_base and user
            kb_label_user = KnowledgeBaseLabelUser.objects.get(
                knowledge_base_id=data["knowledge_base"],
                user_id=data["user"]
            )
            # If exists, update the label
            kb_label_user.label_id = data["label"]
            kb_label_user.save()
            serializer = CreateKnowledgeBaseLabelUserSerializer(kb_label_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KnowledgeBaseLabelUser.DoesNotExist:
            # If it does not exist, create a new one
            serializer = CreateKnowledgeBaseLabelUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class AddSourceLabelViewSet(APIView):
    serializer_class = KnowledgeBaseLabelUserSerializer
    permission_classes = [IsAuthenticated]
    def delete(self, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        label_id = data["label"]
        knowledge_base_id = data["knowledge_base"]
        try:
            instance = KnowledgeBaseLabelUser.objects.get(
                label_id=label_id,
                knowledge_base_id=knowledge_base_id,
                user=user
            )
            instance.delete()
            return Response({'message': 'Association removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except KnowledgeBaseLabelUser.DoesNotExist:
            return Response({'error': 'Association not found.'}, status=status.HTTP_404_NOT_FOUND)


    def post(self, *args, **kwargs):
        data=self.request.data
        data["user"]=self.request.user.id
        serializer = CreateKnowledgeBaseLabelUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




class KnowledgeBaseViewSet(APIView):
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        kb = KnowledgeBase.objects.all()
        serializer = self.serializer_class(kb,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, *args, **kwargs):
        serializer = AddKnowledgeBaseSerializer(data=self.request.data)
        if serializer.is_valid():
            item = serializer.save()
            url = 'http://62.60.198.225:5682/text/kb/add_news'
            headers = {
                'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
                'Content-Type': 'application/json',
            }
            payload = {
                'category': item.category,
                'id': str(item.id),
                'body': item.body,
            }
            response = requests.post(url, params=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                print(data)
                return Response(KnowledgeBaseSerializer(item).data, status=status.HTTP_201_CREATED)
            else:
                print("Status Code:", response.status_code)
                print("Response Text:", response.text)
                print("Request Payload:", payload)
                print("Request Headers:", headers)
                return Response("Failed to submit data!", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



class KnowledgeBaseItemViewSet(APIView):
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            kb = KnowledgeBase.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(kb,context={'request': self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("KnowledgeBase not found or something went wrong, try again - {}".format(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, *args, **kwargs):
        try:
            kb = KnowledgeBase.objects.get(id=self.kwargs["id"])
            serializer = AddKnowledgeBaseSerializer(kb, data=self.request.data, partial=True)
            if serializer.is_valid():
                item = serializer.save()

                url = 'http://62.60.198.225:5682/text/kb/update_news'
                headers = {
                    'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
                    'Content-Type': 'application/json',
                }
                payload = {
                    'old_category': item.old_category,
                    'id': str(item.id),
                    'body': item.body,
                    'new_category': item.category,
                }

                response = requests.put(url, params=payload, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    print(data)
                    return Response(KnowledgeBaseSerializer(item).data)
                else:
                    print("Status Code:", response.status_code)
                    print("Response Text:", response.text)
                    print("Request Payload:", payload)
                    print("Request Headers:", headers)
                    return Response("Failed to submit data!", status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response("KnowledgeBase not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            item = KnowledgeBase.objects.get(id=self.kwargs["id"])
            if item:
                url = 'http://62.60.198.225:5682/text/kb/remove_news'
                headers = {
                    'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
                    'Content-Type': 'application/json',
                }
                payload = {
                    'category': item.category,
                    'id': str(item.id),
                }
                response = requests.delete(url, params=payload, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    print(data)
                    item.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    print("Status Code:", response.status_code)
                    print("Response Text:", response.text)
                    print("Request Payload:", payload)
                    print("Request Headers:", headers)
                    return Response("Failed to submit data!", status=status.HTTP_400_BAD_REQUEST)
            return Response("KnowledgeBase deleted.", status=status.HTTP_200_OK)
        except:
            return Response("KnowledgeBase not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)




class SearchByID(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        search = SearchData.objects.get(id=self.kwargs["id"])
        if search:
            return Response(SearchSerializer(search).data, status=status.HTTP_200_OK)
        return Response({'error': 'Search data not found'}, status=status.HTTP_404_NOT_FOUND)





class Search(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            search_text = request.data.get('search')
            if not search_text:
                return Response({'error': 'Search field is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare search data
            search_data = {'user': self.request.user.id if self.request.user.is_authenticated else None, 'text': search_text}
            serializer = SearchSerializer(data=search_data)
            if serializer.is_valid():
                search_item = serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # External AI API request
            url = 'http://62.60.198.225:5682/text/check_news'
            headers = {
                'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
                'Content-Type': 'application/json',
            }
            payload = {'input_news': search_text}

            response = requests.post(url, params=payload, headers=headers)

            if response.status_code == 200:
                ai_result = response.json()

                try:
                    fact = KnowledgeBase.objects.get(id=ai_result['fact_id'])
                    fact_data = KnowledgeBaseSerializer(fact).data
                except:
                    fact_data = None
                combined_result = {
                    'id': str(search_item.id),
                    'ai_result': ai_result,
                    'fact_data': fact_data
                }
                if ai_result['result'] == "real":
                    search_item.result = "real"
                else:
                    search_item.result = "fake"
                search_item.processed = True
                search_item.ai_answer = combined_result
                search_item.save()
                return Response(combined_result, status=status.HTTP_200_OK)
            else:
                logger.warning(f"AI service failed | Status: {response.status_code} | Response: {response.text}")
                return Response({'error': 'Failed to fetch AI response.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Unexpected error occurred during search")
            return Response({'error': 'Something went wrong, please try again.{}'.format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, *args, **kwargs):
        try:
            search = SearchData.objects.all()
            serializer = SearchSerializer(search,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Error - {}".format(e), status=status.HTTP_400_BAD_REQUEST)




#----------------------




class MediaSearch(APIView):
    permission_classes = [AllowAny]
    def post(self, *args, **kwargs):
        try:
            data = self.request.data
            search = data['search']
            # todo - save search
            # todo - connect to AI and get data
            # todo - response data

            response_data = {
                "id": 243,
                "keywords": {"اعتراض", "نظام ـ سلامت"},
                "locations": {"ایران", "تهران", "خوزستان"},
                "possibilities": [
                    {"probability": "حقیقت", "percentage": 17.2},
                    {"probability": "دروغ", "percentage": 16.5},
                    {"probability": "فریب", "percentage": 36.6},
                    {"probability": "سوءقصد", "percentage": 28.9}
                ],
                "websites": [
                    {"website": "وبسایت‌های داخلی", "percentage": 60.4},
                    {"website": "شبکه‌های اجتماعی خارجی", "percentage": 92.2},
                    {"website": "وبسایت‌های خارجی", "percentage": 100},
                    {"website": "شبکه‌های اجتماعی داخلی", "percentage": 34.1}
                ],
                "posts": [
                    {
                        "title": "تجمع اعتراضی پرستاران مقابل استانداری خوزستان",
                        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoBujouyZLFZC5nyf7TIUPqqEkNqLyXeabew&s",
                        "text": "امروز (30 آبان)، جمعی از پرستاران خوزستان با تجمع مقابل استانداری خواستار رسیدگی به مطالبات قانونی خود شدند. این پرستاران اصلی‌ترین خواسته‌های خود را برقراری فوق العاده خاص با ضریب 3 و گنجاندن آن در حکم، اجرای دقیق تعرفه‌گذاری عادلانه، اجرای قانون مشاغل سخت و زیان‌آور، ممنوعیت اضافه‌کار اجباری و برقراری امنیت شغلی عنوان کردند.",
                        "date": "June 7, 2021"
                    },
                    {
                        "title": "تجمع اعتراضی پرستاران مقابل استانداری خوزستان",
                        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoBujouyZLFZC5nyf7TIUPqqEkNqLyXeabew&s",
                        "text": "امروز (30 آبان)، جمعی از پرستاران خوزستان با تجمع مقابل استانداری خواستار رسیدگی به مطالبات قانونی خود شدند. این پرستاران اصلی‌ترین خواسته‌های خود را برقراری فوق العاده خاص با ضریب 3 و گنجاندن آن در حکم، اجرای دقیق تعرفه‌گذاری عادلانه، اجرای قانون مشاغل سخت و زیان‌آور، ممنوعیت اضافه‌کار اجباری و برقراری امنیت شغلی عنوان کردند.",
                        "date": "June 7, 2021"
                    }
                ],
                "created_data": "Feb 25, 2025"
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong please try again.", status=status.HTTP_400_BAD_REQUEST)






class Answer(APIView):
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            #search = Search.objects.get(id=self.kwargs["id"])
            # todo - connect to AI and get search object
            # todo - response data

            data = {
                "id": 243,
                "keywords": {"اعتراض","نظام ـ سلامت"},
                "locations": {"ایران","تهران","خوزستان"},
                "possibilities": [
                    {"probability": "حقیقت", "percentage": 17.2},
                    {"probability": "دروغ", "percentage": 16.5},
                    {"probability": "فریب", "percentage": 36.6},
                    {"probability": "سوءقصد", "percentage": 28.9}
                ],
                "websites": [
                    {"website": "وبسایت‌های داخلی", "percentage": 60.4},
                    {"website": "شبکه‌های اجتماعی خارجی", "percentage": 92.2},
                    {"website": "وبسایت‌های خارجی", "percentage": 100},
                    {"website": "شبکه‌های اجتماعی داخلی", "percentage": 34.1}
                ],
                "posts": [
                    {
                        "title": "تجمع اعتراضی پرستاران مقابل استانداری خوزستان",
                        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoBujouyZLFZC5nyf7TIUPqqEkNqLyXeabew&s",
                        "text": "امروز (30 آبان)، جمعی از پرستاران خوزستان با تجمع مقابل استانداری خواستار رسیدگی به مطالبات قانونی خود شدند. این پرستاران اصلی‌ترین خواسته‌های خود را برقراری فوق العاده خاص با ضریب 3 و گنجاندن آن در حکم، اجرای دقیق تعرفه‌گذاری عادلانه، اجرای قانون مشاغل سخت و زیان‌آور، ممنوعیت اضافه‌کار اجباری و برقراری امنیت شغلی عنوان کردند.",
                        "date": "June 7, 2021"
                    },
                    {
                        "title": "تجمع اعتراضی پرستاران مقابل استانداری خوزستان",
                        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoBujouyZLFZC5nyf7TIUPqqEkNqLyXeabew&s",
                        "text": "امروز (30 آبان)، جمعی از پرستاران خوزستان با تجمع مقابل استانداری خواستار رسیدگی به مطالبات قانونی خود شدند. این پرستاران اصلی‌ترین خواسته‌های خود را برقراری فوق العاده خاص با ضریب 3 و گنجاندن آن در حکم، اجرای دقیق تعرفه‌گذاری عادلانه، اجرای قانون مشاغل سخت و زیان‌آور، ممنوعیت اضافه‌کار اجباری و برقراری امنیت شغلی عنوان کردند.",
                        "date": "June 7, 2021"
                    }
                ],
                "created_data": "Feb 25, 2025"
            }

            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong please try again.", status=status.HTTP_400_BAD_REQUEST)





"""
    # Get all data
    data = SearchData.objects()
    # Create a data
    data = SearchData(text="nima", email="nima@example.com")
    data.save()
    
    
    get method example:
    
    def get(self, *args, **kwargs):
       data = SearchData.objects()  # Get all MongoDB documents
       serializer = SearchDataSerializer(data, many=True)
       return Response(serializer.data)
"""





""" 
response_data = {
    "id": 243,
    "keywords": {"اعتراض", "نظام ـ سلامت"},
    "locations": {"ایران", "تهران", "خوزستان"},
    "possibilities": [
        {"probability": "حقیقت", "percentage": 17.2},
        {"probability": "دروغ", "percentage": 16.5},
        {"probability": "فریب", "percentage": 36.6},
        {"probability": "سوءقصد", "percentage": 28.9}
    ],
    "websites": [
        {"website": "وبسایت‌های داخلی", "percentage": 60.4},
        {"website": "شبکه‌های اجتماعی خارجی", "percentage": 92.2},
        {"website": "وبسایت‌های خارجی", "percentage": 100},
        {"website": "شبکه‌های اجتماعی داخلی", "percentage": 34.1}
    ],
    "posts": [
        {
            "title": "تجمع اعتراضی پرستاران مقابل استانداری خوزستان",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoBujouyZLFZC5nyf7TIUPqqEkNqLyXeabew&s",
            "text": "امروز (30 آبان)، جمعی از پرستاران خوزستان با تجمع مقابل استانداری خواستار رسیدگی به مطالبات قانونی خود شدند. این پرستاران اصلی‌ترین خواسته‌های خود را برقراری فوق العاده خاص با ضریب 3 و گنجاندن آن در حکم، اجرای دقیق تعرفه‌گذاری عادلانه، اجرای قانون مشاغل سخت و زیان‌آور، ممنوعیت اضافه‌کار اجباری و برقراری امنیت شغلی عنوان کردند.",
            "date": "June 7, 2021"
        },
        {
            "title": "تجمع اعتراضی پرستاران مقابل استانداری خوزستان",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoBujouyZLFZC5nyf7TIUPqqEkNqLyXeabew&s",
            "text": "امروز (30 آبان)، جمعی از پرستاران خوزستان با تجمع مقابل استانداری خواستار رسیدگی به مطالبات قانونی خود شدند. این پرستاران اصلی‌ترین خواسته‌های خود را برقراری فوق العاده خاص با ضریب 3 و گنجاندن آن در حکم، اجرای دقیق تعرفه‌گذاری عادلانه، اجرای قانون مشاغل سخت و زیان‌آور، ممنوعیت اضافه‌کار اجباری و برقراری امنیت شغلی عنوان کردند.",
            "date": "June 7, 2021"
        }
    ],
    "created_data": "Feb 25, 2025"
}
"""