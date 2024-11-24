from chapter_generator.serializers.resource import ResourceSerializer
from chapter_generator.serializers.stylereference import StyleReferenceSerializer
from chapter_generator.models import Chapter, StyleReference, Resources
from rest_framework import serializers


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


class ChapterInputSerializer(serializers.Serializer):
    source = serializers.CharField()
    source_type = serializers.CharField()
    course_outline = serializers.ListField(child=serializers.JSONField())

    def create(self, validated_data):
        return validated_data
