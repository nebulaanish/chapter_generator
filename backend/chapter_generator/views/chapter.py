from rest_framework.viewsets import ModelViewSet
from chapter_generator.models import Chapter
from chapter_generator.serializers.chapter import ChapterSerializer


class ChapterViewSet(ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
