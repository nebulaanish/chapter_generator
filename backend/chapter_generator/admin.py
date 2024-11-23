from django.contrib import admin

from .models import StyleReference, Chapter, Resources


@admin.register(StyleReference)
class StyleReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "created_at",
        "updated_at",
    )
    search_fields = ("type",)


class ResourcesInline(admin.TabularInline):
    model = Resources
    extra = 1


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "reference_type",
        "created_at",
        "updated_at",
    )


@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = (
        "resource_type",
        "chapter",
        "upload",
        "created_at",
    )
