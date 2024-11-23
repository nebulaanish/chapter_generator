from chapter_generator.models import Chapter
from rest_framework import serializers


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"
