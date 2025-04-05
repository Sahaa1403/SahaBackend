from search.models import SearchData,KnowledgeBase, Label
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer


class SearchDataSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    text = serializers.CharField()
    #email = serializers.EmailField()
    #age = serializers.IntegerField()
    #created_at = serializers.DateTimeField()

    def create(self, validated_data):
        """Create a new MongoEngine document."""
        return SearchData(**validated_data).save()

    def update(self, instance, validated_data):
        """Update an existing document."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class LabelSerializer(DocumentSerializer):
    class Meta:
        model = Label
        fields = '__all__'

class KnowledgeBaseSerializer(DocumentSerializer):
    label = LabelSerializer(read_only=True)
    class Meta:
        model = KnowledgeBase
        fields = '__all__'

class AddKnowledgeBaseSerializer(DocumentSerializer):
    class Meta:
        model = KnowledgeBase
        fields = '__all__'
