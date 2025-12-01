from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_archived", "updated_at", "created_at")
    search_fields = ("title", "tags")
    list_filter = ("is_archived",)
    ordering = ("-updated_at",)
