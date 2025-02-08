from search.models import SearchData
from rest_framework import serializers


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
