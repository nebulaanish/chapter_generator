from django.db import models


# Base model to include created_at and updated_at fields
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Reference Type Model
class StyleReference(BaseModel):
    REFERENCE_TYPES = [
        ("professional", "Professional"),
        ("personal", "Personal"),
        ("technical", "Technical"),
        ("philosophical", "Philosophical"),
        ("fun", "Fun"),
    ]
    type = models.CharField(max_length=20, choices=REFERENCE_TYPES, unique=True)

    def __str__(self):
        return self.get_type_display()  # Returns the display name of the selected type


# Chapter Model
class Chapter(BaseModel):

    CHAPTER_STATUS = [
        ("draft", "Draft"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=100)
    outlines = models.JSONField()  # Stores chapter outlines in JSON format
    status = models.CharField(max_length=10, choices=CHAPTER_STATUS, default="draft")
    reference_type = models.ForeignKey(StyleReference, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Resources(BaseModel):

    RESOURCE_TYPES = [
        ("blog", "Blog"),
        ("pdf", "Pdf"),
        ("research_paper", "Research Paper"),
    ]
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    upload = models.FileField(upload_to="uploads/")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    content_extracted = models.TextField(null=True)
