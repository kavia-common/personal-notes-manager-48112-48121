from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Note
from .serializers import NoteSerializer


@api_view(["GET"])
def health(request: Request) -> Response:
    """Simple health check endpoint to verify server status."""
    return Response({"message": "Server is up!"})


class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing personal notes.

    Supports:
      - list with pagination
      - retrieve
      - create
      - update (PUT/PATCH)
      - destroy (DELETE)
      - archive/unarchive via custom actions

    Query params for list:
      - search: substring match on title
      - is_archived: 'true'/'false' to filter by archive status
    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search") or None
        is_archived_param = self.request.query_params.get("is_archived")
        if is_archived_param is not None:
            val = str(is_archived_param).lower()
            if val in ("true", "1", "yes"):
                qs = qs.filter(is_archived=True)
            elif val in ("false", "0", "no"):
                qs = qs.filter(is_archived=False)
        qs = qs.search_title(search)
        return qs

    @action(detail=True, methods=["post"])
    def archive(self, request: Request, pk: str | int = None) -> Response:
        """Archive a note."""
        note = self.get_object()
        if note.is_archived:
            return Response({"detail": "Already archived."}, status=status.HTTP_200_OK)
        note.is_archived = True
        note.save(update_fields=["is_archived", "updated_at"])
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unarchive(self, request: Request, pk: str | int = None) -> Response:
        """Unarchive a note."""
        note = self.get_object()
        if not note.is_archived:
            return Response({"detail": "Already active."}, status=status.HTTP_200_OK)
        note.is_archived = False
        note.save(update_fields=["is_archived", "updated_at"])
        return Response(NoteSerializer(note).data, status=status.HTTP_200_OK)
