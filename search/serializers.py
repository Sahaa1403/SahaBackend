from search.models import SearchData,KnowledgeBase,Label,Source,SocialMedia,KnowledgeBaseLabelUser
from rest_framework import serializers
from accounts.serializers import UserShortSerializer
from django.db.models import Count


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
    class Meta:
        model = SocialMedia
        fields = '__all__'

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
    label = serializers.SerializerMethodField()
    source = SourceSerializer(read_only=True)
    social_media = SocialMediaShortSerializer(read_only=True)
    class Meta:
        model = KnowledgeBase
        fields = '__all__'

    def get_label(self, obj):
        # Aggregate labels and count them
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base=obj)
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
            }
            for label in labels
        ]
    """ 
    def get_label(self, obj):
        label = KnowledgeBaseLabelUser.objects.filter(knowledge_base=obj)
        return KnowledgeBaseLabelUserSerializer(label, many=True).data
    """


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
        return KnowledgeBaseSerializer(kb_items, many=True).data

    def get_common_labels(self, obj):
        request = self.context.get('request', None)
        user = request.user if request and hasattr(request, 'user') else None
        labels = KnowledgeBaseLabelUser.objects.filter(knowledge_base__source=obj).exclude(
            label__name__in=["خبر حقیقت", "خبر نادرست", "خبر مخرب", "خبر دروغین"]).distinct()
        common_l = []
        for item in labels:
            label_data = LabelSerializer(item.label).data
            common_l.append({
                "label": label_data,
                "is_user": item.user == user if user else False
            })
        return common_l

    def get_labels(self, obj):
        # Aggregate labels and count them
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj)
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
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
        return KnowledgeBaseSerializer(kb_items, many=True).data

    def get_common_labels(self, obj):
        request = self.context.get('request', None)
        user = request.user if request and hasattr(request, 'user') else None
        labels = KnowledgeBaseLabelUser.objects.filter(knowledge_base__source=obj).exclude(
            label__name__in=["خبر حقیقت", "خبر نادرست", "خبر مخرب", "خبر دروغین"]).distinct()
        common_l = []
        for item in labels:
            label_data = LabelSerializer(item.label).data
            common_l.append({
                "label": label_data,
                "is_user": item.user == user if user else False
            })
        return common_l

    def get_labels(self, obj):
        # Aggregate labels and count them
        labels = (
            KnowledgeBaseLabelUser.objects
            .filter(knowledge_base__source=obj)
            .values('label__id', 'label__name')
            .annotate(count=Count('id'))
        )
        return [
            {
                "label_id": label["label__id"],
                "label_name": label["label__name"],
                "count": label["count"],
            }
            for label in labels
        ]





class AddKnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = '__all__'



class SocialMediaSerializer(serializers.ModelSerializer):
    knowledge_base_items = serializers.SerializerMethodField()
    class Meta:
        model = SocialMedia
        fields = ['id', 'title', 'description', 'photo', 'file', 'updated_at', 'created_at', 'knowledge_base_items']
    def get_knowledge_base_items(self, obj):
        kb_items = KnowledgeBase.objects.filter(social_media=obj)
        return KnowledgeBaseSerializer(kb_items, many=True).data




