from search.models import SearchData,KnowledgeBase,Label,Source,SocialMedia
from rest_framework import serializers

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



class KnowledgeBaseSerializer(serializers.ModelSerializer):
    label = LabelSerializer(read_only=True)
    source = SourceSerializer(read_only=True)
    social_media = SocialMediaShortSerializer(read_only=True)
    class Meta:
        model = KnowledgeBase
        fields = '__all__'


class SourceFullSerializer(serializers.ModelSerializer):
    knowledge_base_items = serializers.SerializerMethodField()
    common_labels = serializers.SerializerMethodField()
    default_label = LabelSerializer()
    class Meta:
        model = Source
        fields = ['id', 'title', 'description', 'category', 'default_label', 'common_labels', 'photo', 'file', 'updated_at', 'created_at', 'knowledge_base_items']
    def get_knowledge_base_items(self, obj):
        kb_items = KnowledgeBase.objects.filter(source=obj)
        return KnowledgeBaseSerializer(kb_items, many=True).data
    def get_common_labels(self, obj):
        labels = Label.objects.filter(knowledgebase__source=obj).distinct()
        return LabelSerializer(labels, many=True).data



class SourceWithKBSerializer(serializers.ModelSerializer):
    knowledge_base_items = serializers.SerializerMethodField()
    default_label = LabelSerializer()
    common_labels = serializers.SerializerMethodField()
    class Meta:
        model = Source
        fields = ['id', 'title', 'description', 'category', 'default_label', 'common_labels', 'photo', 'file', 'updated_at', 'created_at', 'knowledge_base_items']
    def get_knowledge_base_items(self, obj):
        kb_items = KnowledgeBase.objects.filter(source=obj)
        return KnowledgeBaseSerializer(kb_items, many=True).data
    def get_common_labels(self, obj):
        labels = Label.objects.filter(knowledgebase__source=obj).distinct()
        return LabelSerializer(labels, many=True).data


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
