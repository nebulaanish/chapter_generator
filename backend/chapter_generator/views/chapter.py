from chapter_generator.services.rag_services import RAGSystem
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from chapter_generator.models import Chapter
from chapter_generator.serializers.chapter import (
    ChapterSerializer,
    ChapterInputSerializer,
)


class ChapterViewSet(ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    @action(detail=False, methods=["post"])
    def generate(self, request):
        serializer = ChapterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        rag_system = RAGSystem()

        rag_system.load_document(
            data.get("source"), source_type=data.get("source_type", "url")
        )
        rag_system.save_index("faiss_index_folder")
        rag_system.load_index("faiss_index_folder")

        chapter = []
        for paragraph in data.get("course_outline"):
            query_content = " ".join(paragraph.get("content"))
            all_title = [
                paragraph.get("title") for paragraph in data.get("course_outline")
            ]
            query_text = f"""Create a paragraph which is a part of chapter. The paragraph will serve as {paragraph.get("title")}, 
            the overall chapter includes following topics {all_title}. 
            The content should include {query_content}. 
            Make sure the paragraph is concise and is coherent with other topics of the chapter.
            If the context, doesn't have any information about the query contents. Please provide "No Relevant Information Found".
            """

            output = rag_system.get_response(query_text)
            chapter.append(output)

        response = "\n\n".join(chapter)
        title = rag_system.get_response_to_prompt(
            f"Create a suitable title for the given chapter. Here's the content: {response}"
        )

        if "No Relevant Information Found" in response:
            return Response(
                {"title": "No Relevant Information Found", "text": ""}, status=200
            )
        return Response({"title": title, "text": response}, status=200)
