from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note with simple validation.

    Validations:
      - title: required, trimmed, cannot be empty after trimming
      - tags: stored as comma-separated string but accepts string
    """

    # PUBLIC_INTERFACE
    def validate_title(self, value: str) -> str:
        """Validate and normalize the note title: trimmed and non-empty."""
        if value is None:
            raise serializers.ValidationError("Title is required.")
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "tags",
            "is_archived",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
