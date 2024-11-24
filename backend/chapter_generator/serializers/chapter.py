from chapter_generator.models import Chapter, StyleReference, Resources
from rest_framework import serializers


class StyleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleReference
        fields = ["id", "type"]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = ["id", "resource_type", "upload", "content_extracted"]


class ChapterSerializer(serializers.ModelSerializer):

    reference_type = StyleReferenceSerializer()
    resources = ResourceSerializer(many=True)

    class Meta:
        model = Chapter
        fields = ["id", "title", "outlines", "status", "reference_type", "resources"]

    def create(self, validated_data):
        reference_type_data = validated_data.pop("reference_type")
        reference_type, _ = StyleReference.objects.get_or_create(**reference_type_data)

        resources_data = validated_data.pop("resources")
        chapter = Chapter.objects.create(
            reference_type=reference_type, **validated_data
        )

        for resource_data in resources_data:
            Resources.objects.create(chapter=chapter, **resource_data)

        return chapter
