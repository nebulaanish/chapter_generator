from chapter_generator.models import StyleReference
from rest_framework import serializers


class StyleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleReference
        fields = ["id", "type"]
