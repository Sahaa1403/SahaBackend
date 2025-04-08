from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from search.models import SearchData,KnowledgeBase, Label
from search.serializers import SearchSerializer,SearchDataSerializer,AddKnowledgeBaseSerializer, KnowledgeBaseSerializer, LabelSerializer
from rest_framework_mongoengine.viewsets import ModelViewSet
import requests
import json
import urllib.parse
import logging


logger = logging.getLogger(__name__)


class LabelViewSet(viewsets.ViewSet):
    def list(self, request):
        labels = Label.objects.all()
        serializer = LabelSerializer(labels, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            label = serializer.save()
            return Response(LabelSerializer(label).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        label = Label.objects(id=pk).first()
        if label:
            return Response(LabelSerializer(label).data)
        return Response({'error': 'Label not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        label = Label.objects(id=pk).first()
        if not label:
            return Response({'error': 'Label not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            label = serializer.save()
            return Response(LabelSerializer(label).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        label = Label.objects(id=pk).first()
        if label:
            label.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Label not found'}, status=status.HTTP_404_NOT_FOUND)


class KnowledgeBaseViewSet(viewsets.ViewSet):
    def list(self, request):
        items = KnowledgeBase.objects.all()
        serializer = KnowledgeBaseSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AddKnowledgeBaseSerializer(data=request.data)
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        item = KnowledgeBase.objects(id=pk).first()
        if item:
            return Response(KnowledgeBaseSerializer(item).data)
        return Response({'error': 'KnowledgeBase item not found'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        item = KnowledgeBase.objects(id=pk).first()
        if not item:
            return Response({'error': 'KnowledgeBase item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddKnowledgeBaseSerializer(item, data=request.data)
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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        item = KnowledgeBase.objects(id=pk).first()
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

        return Response({'error': 'KnowledgeBase item not found'}, status=status.HTTP_404_NOT_FOUND)




class Search(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            search_text = request.data.get('search')
            if not search_text:
                return Response({'error': 'Search field is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare search data
            search_data = {'user_id': request.user.id if request.user.is_authenticated else None, 'text': search_text}
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

                fact = KnowledgeBase(id=ai_result['fact_id'])
                combined_result = {
                    'ai_result': ai_result,
                    'fact_data': KnowledgeBaseSerializer(fact).data
                }
                search_item.ai_answer = combined_result
                search_item.save()
                return Response(combined_result, status=status.HTTP_200_OK)
            else:
                logger.warning(f"AI service failed | Status: {response.status_code} | Response: {response.text}")
                return Response({'error': 'Failed to fetch AI response.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Unexpected error occurred during search")
            return Response({'error': 'Something went wrong, please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




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