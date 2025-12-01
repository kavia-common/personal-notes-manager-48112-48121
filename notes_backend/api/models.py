from django.db import models


class NoteQuerySet(models.QuerySet):
    """Custom queryset to help filtering by archived flag and searching."""

    def active(self):
        return self.filter(is_archived=False)

    def archived(self):
        return self.filter(is_archived=True)

    def search_title(self, q: str | None):
        if q:
            return self.filter(title__icontains=q.strip())
        return self


class Note(models.Model):
    """
    A personal note with optional archive state.

    Fields:
      - title: required, max 200
      - content: optional text
      - tags: optional comma separated string for quick labeling
      - is_archived: boolean flag, default false
      - created_at/updated_at: auto timestamps
    """

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, default="")
    tags = models.CharField(max_length=255, blank=True, default="")
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = NoteQuerySet.as_manager()

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(fields=["is_archived"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - convenience
        return f"Note<{self.id}> {self.title[:30]}"
