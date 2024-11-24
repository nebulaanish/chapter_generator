from chapter_generator.models import Resources
from rest_framework import serializers


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = ["id", "resource_type", "upload", "content_extracted"]
