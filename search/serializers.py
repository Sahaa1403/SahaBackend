from search.models import SearchData,KnowledgeBase,Label,Source,SocialMedia,KnowledgeBaseLabelUser
from rest_framework import serializers
from accounts.serializers import UserShortSerializer
from django.db.models import Count
from collections import defaultdict


class SearchDataSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    text = serializers.CharField()

    def create(self, validated_data):
        """Create a new MongoEngine document."""
        return SearchData(**validated_data).save()

    def update(self, instance, validated_data):
        """Update an existing document."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchData
        fields = '__all__'




class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'



class SourceSerializer(serializers.ModelSerializer):
    default_label = LabelSerializer()

    class Meta:
        model = Source
        fields = '__all__'


class SocialMediaShortSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    class Meta:
        model = SocialMedia
        fields = '__all__'

    def get_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        # Step 1: Get all labels grouped (correct counting, without 'user')
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__social_media=obj)
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )

        # Step 2: Build a mapping label_id -> list of user IDs
        label_users = {}
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__social_media=obj)
            .values('label__id', 'user')
        )
        for entry in user_qs:
            label_id = entry['label__id']
            user_id = entry['user']
            label_users.setdefault(label_id, []).append(user_id)

        # Step 3: Combine the count and user list
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": current_user_id in label_users.get(label["label__id"], []),
            }
            for label in labels
        ]


class EditSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class CreateSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'



class KnowledgeBaseLabelUserSerializer(serializers.ModelSerializer):
    label = LabelSerializer(read_only=True)
    user = UserShortSerializer(read_only=True)
    class Meta:
        model = KnowledgeBaseLabelUser
        fields = '__all__'

class CreateKnowledgeBaseLabelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBaseLabelUser
        fields = '__all__'


class ShortKnowledgeBaseLabelUserSerializer(serializers.ModelSerializer):
    label = LabelSerializer(read_only=True)
    class Meta:
        model = KnowledgeBaseLabelUser
        fields = '__all__'

class KnowledgeBaseSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    common_labels = serializers.SerializerMethodField()
    source = SourceSerializer(read_only=True)
    social_media = SocialMediaShortSerializer(read_only=True)
    class Meta:
        model = KnowledgeBase
        fields = '__all__'

    def get_common_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        labels = KnowledgeBaseLabelUser.objects.filter(
            knowledge_base=obj
        ).exclude(
            label__name__in=["واقعیت", "نادرست", "فریب دهی", "آسیب رسان"]
        ).values(
            'label__id', 'label__name'
        ).annotate(
            count=Count('id')
        )

        # Step 2: Build a mapping label_id -> list of user IDs
        label_users = {}
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base=obj)
            .values('label__id', 'user')
        )
        for entry in user_qs:
            label_id = entry['label__id']
            user_id = entry['user']
            label_users.setdefault(label_id, []).append(user_id)

        # Step 3: Combine the count and user list
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": current_user_id in label_users.get(label["label__id"], []),
            }
            for label in labels
        ]

    def get_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        # Step 1: Get all labels grouped (correct counting, without 'user')
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base=obj, label__name__in=["واقعیت", "نادرست", "فریب دهی", "آسیب رسان"])
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )

        # Step 2: Build a set of label_ids the current user has used
        user_labeled_label_ids = set(
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base=obj, user_id=current_user_id)
            .values_list('label_id', flat=True)
        ) if current_user_id else set()

        # Step 3: Build a mapping label_id -> list of user IDs
        label_users = defaultdict(list)
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base=obj)
            .values('label_id', 'user_id')
        )
        for entry in user_qs:
            label_users[entry['label_id']].append(entry['user_id'])

        # Step 4: Combine result
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": label["label__id"] in user_labeled_label_ids,
            }
            for label in labels
        ]


class SourceFullSerializer(serializers.ModelSerializer):
    knowledge_base_items = serializers.SerializerMethodField()
    common_labels = serializers.SerializerMethodField()
    default_label = LabelSerializer()
    labels = serializers.SerializerMethodField()
    class Meta:
        model = Source
        fields = ['id', 'title', 'description', 'category', 'default_label','common_labels', 'labels', 'photo', 'file', 'updated_at', 'created_at', 'knowledge_base_items']
    def get_knowledge_base_items(self, obj):
        kb_items = KnowledgeBase.objects.filter(source=obj)
        return KnowledgeBaseSerializer(kb_items, many=True, context=self.context).data
        #return KnowledgeBaseSerializer(kb_items, many=True).data

    def get_common_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        labels = KnowledgeBaseLabelUser.objects.filter(
            knowledge_base__source=obj
        ).exclude(
            label__name__in=["واقعیت", "نادرست", "فریب دهی", "آسیب رسان"]
        ).values(
            'label__id', 'label__name'
        ).annotate(
            count=Count('id')
        )

        # Step 2: Build a mapping label_id -> list of user IDs
        label_users = {}
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj)
            .values('label__id', 'user')
        )
        for entry in user_qs:
            label_id = entry['label__id']
            user_id = entry['user']
            label_users.setdefault(label_id, []).append(user_id)

        # Step 3: Combine the count and user list
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": current_user_id in label_users.get(label["label__id"], []),
            }
            for label in labels
        ]

    def get_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        # Step 1: Get all labels grouped (correct counting, without 'user')
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj)
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )

        # Step 2: Build a set of label_ids the current user has used
        user_labeled_label_ids = set(
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj, user_id=current_user_id)
            .values_list('label_id', flat=True)
        ) if current_user_id else set()

        # Step 3: Build a mapping label_id -> list of user IDs
        label_users = defaultdict(list)
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj)
            .values('label_id', 'user_id')
        )
        for entry in user_qs:
            label_users[entry['label_id']].append(entry['user_id'])

        # Step 4: Combine result
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": label["label__id"] in user_labeled_label_ids,
            }
            for label in labels
        ]


class SourceWithKBSerializer(serializers.ModelSerializer):
    knowledge_base_items = serializers.SerializerMethodField()
    default_label = LabelSerializer()
    common_labels = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()
    class Meta:
        model = Source
        fields = ['id', 'title', 'description', 'category', 'default_label','common_labels', 'labels', 'photo', 'file', 'updated_at', 'created_at', 'knowledge_base_items']
    def get_knowledge_base_items(self, obj):
        kb_items = KnowledgeBase.objects.filter(source=obj)
        return KnowledgeBaseSerializer(kb_items, many=True, context=self.context).data
        #return KnowledgeBaseSerializer(kb_items, many=True).data

    def get_common_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        labels = KnowledgeBaseLabelUser.objects.filter(
            knowledge_base__source=obj
        ).exclude(
            label__name__in=["واقعیت", "نادرست", "فریب دهی", "آسیب رسان"]
        ).values(
            'label__id', 'label__name'
        ).annotate(
            count=Count('id')
        )

        # Step 2: Build a mapping label_id -> list of user IDs
        label_users = {}
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj)
            .values('label__id', 'user')
        )
        for entry in user_qs:
            label_id = entry['label__id']
            user_id = entry['user']
            label_users.setdefault(label_id, []).append(user_id)

        # Step 3: Combine the count and user list
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": current_user_id in label_users.get(label["label__id"], []),
            }
            for label in labels
        ]


    def get_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        # Step 1: Get all labels grouped (correct counting, without 'user')
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj,label__name__in=["واقعیت", "نادرست", "فریب دهی", "آسیب رسان"])
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )

        # Step 2: Build a set of label_ids the current user has used
        user_labeled_label_ids = set(
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj, user_id=current_user_id)
            .values_list('label_id', flat=True)
        ) if current_user_id else set()

        # Step 3: Build a mapping label_id -> list of user IDs
        label_users = defaultdict(list)
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj)
            .values('label_id', 'user_id')
        )
        for entry in user_qs:
            label_users[entry['label_id']].append(entry['user_id'])

        # Step 4: Combine result
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": label["label__id"] in user_labeled_label_ids,
            }
            for label in labels
        ]





class AddKnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = '__all__'



class SocialMediaSerializer(serializers.ModelSerializer):
    knowledge_base_items = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()
    class Meta:
        model = SocialMedia
        fields = ['id', 'title', 'description', 'photo', 'file', 'updated_at', 'created_at', 'labels', 'knowledge_base_items']
    def get_knowledge_base_items(self, obj):
        kb_items = KnowledgeBase.objects.filter(social_media=obj)
        return KnowledgeBaseSerializer(kb_items, many=True, context=self.context).data
        #return KnowledgeBaseSerializer(kb_items, many=True).data

    def get_labels(self, obj):
        request = self.context.get('request', None)
        current_user_id = request.user.id if request and hasattr(request, 'user') else None

        # Step 1: Get all labels grouped (correct counting, without 'user')
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__social_media=obj)
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )

        # Step 2: Build a mapping label_id -> list of user IDs
        label_users = {}
        user_qs = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__social_media=obj)
            .values('label__id', 'user')
        )
        for entry in user_qs:
            label_id = entry['label__id']
            user_id = entry['user']
            label_users.setdefault(label_id, []).append(user_id)

        # Step 3: Combine the count and user list
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
                "users": label_users.get(label["label__id"], []),
                "is_labeled_by_user": current_user_id in label_users.get(label["label__id"], []),
            }
            for label in labels
        ]

